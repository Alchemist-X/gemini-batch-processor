import asyncio
import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from PIL import Image
import google.generativeai as genai
from google.generativeai.types import GenerationConfig

from config import Config
from retry_handler import RetryHandler
from prompt_optimizer import PromptOptimizer
from archiver import Archiver

logger = logging.getLogger(__name__)

class GeminiBatchProcessor:
    def __init__(self, config: Config):
        self.config = config
        self.retry_handler = RetryHandler(config.max_retries)
        self.prompt_optimizer = PromptOptimizer()
        self.archiver = Archiver(config.output_dir, config.archive_format)
        
        # Configure Gemini API
        genai.configure(api_key=config.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    async def process_image_batch(self, image_paths: List[str], base_prompt: str) -> Dict[str, Any]:
        """Process a batch of images concurrently."""
        semaphore = asyncio.Semaphore(self.config.max_concurrent_requests)
        tasks = []
        
        for image_path in image_paths:
            task = self._process_single_image_with_semaphore(
                image_path, base_prompt, semaphore
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        successful_count = 0
        failed_count = 0
        total_processed = len(results)
        
        for i, result in enumerate(results):
            image_name = Path(image_paths[i]).stem
            if isinstance(result, Exception):
                logger.error(f"Failed to process {image_name}: {str(result)}")
                self.archiver.save_failed_result(image_name, str(result))
                failed_count += 1
            elif result is None:
                logger.warning(f"Processing returned None for {image_name}")
                self.archiver.save_failed_result(image_name, "Processing returned None")
                failed_count += 1
            else:
                self.archiver.save_successful_result(image_name, result)
                successful_count += 1
        
        # Save statistics
        stats = {
            "total_images": total_processed,
            "successful": successful_count,
            "failed": failed_count,
            "success_rate": successful_count / total_processed if total_processed > 0 else 0,
            "max_concurrent_requests": self.config.max_concurrent_requests,
            "max_retries": self.config.max_retries
        }
        self.archiver.save_processing_stats(stats)
        
        # Save prompt evolution data
        evolution_stats = self.prompt_optimizer.get_evolution_stats()
        self.archiver.save_prompt_evolution(evolution_stats)
        
        # Create archive if requested
        if self.config.archive_format != "none":
            self.archiver.create_archive()
        
        return stats
    
    async def _process_single_image_with_semaphore(
        self, 
        image_path: str, 
        base_prompt: str, 
        semaphore: asyncio.Semaphore
    ) -> Optional[str]:
        """Process single image with semaphore control."""
        async with semaphore:
            return await self._process_single_image(image_path, base_prompt)
    
    async def _process_single_image(self, image_path: str, base_prompt: str) -> Optional[str]:
        """Process a single image with retry and prompt optimization."""
        current_prompt = base_prompt
        original_prompt = base_prompt
        
        for attempt in range(self.config.max_retries + 1):
            try:
                if self.config.dry_run:
                    logger.info(f"[DRY RUN] Would process {image_path} with prompt: {current_prompt}")
                    return f"[DRY RUN] Result for {Path(image_path).name}"
                
                # Validate image
                if not self._validate_image(image_path):
                    raise ValueError(f"Invalid or unsupported image format: {image_path}")
                
                # Check file size (Gemini has 20MB limit)
                if os.path.getsize(image_path) > 20 * 1024 * 1024:
                    raise ValueError(f"Image too large (>20MB): {image_path}")
                
                # Process with Gemini
                image = Image.open(image_path)
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: self.model.generate_content([current_prompt, image])
                )
                
                if response.text:
                    logger.info(f"Successfully processed {Path(image_path).name}")
                    return response.text
                else:
                    raise ValueError("Empty response from Gemini API")
                    
            except Exception as e:
                error_msg = str(e)
                logger.warning(f"Attempt {attempt + 1} failed for {Path(image_path).name}: {error_msg}")
                
                if attempt < self.config.max_retries:
                    # Optimize prompt for next attempt
                    if self.config.enable_prompt_optimization:
                        failure_analysis = self.prompt_optimizer.analyze_failure(current_prompt, error_msg)
                        optimized_prompt = self.prompt_optimizer.optimize_prompt(current_prompt, failure_analysis)
                        self.prompt_optimizer.record_prompt_evolution(
                            Path(image_path).name, current_prompt, optimized_prompt
                        )
                        current_prompt = optimized_prompt
                    
                    # Wait before retry (exponential backoff handled by retry_handler)
                    await asyncio.sleep(min(1.0 * (2 ** attempt), 30.0))
                else:
                    logger.error(f"Max retries exceeded for {Path(image_path).name}")
                    return None
        
        return None
    
    def _validate_image(self, image_path: str) -> bool:
        """Validate if the file is a supported image format."""
        try:
            with Image.open(image_path) as img:
                img.verify()
            return True
        except Exception:
            return False
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported image formats."""
        return ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif']