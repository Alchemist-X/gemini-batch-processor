#!/usr/bin/env python3
"""
Gemini Batch Processor - Main Entry Point

Usage:
    python main.py --input-dir /path/to/images --prompt "your prompt here"
"""

import argparse
import asyncio
import logging
import os
from pathlib import Path

from config import Config
from processor import GeminiBatchProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Gemini Batch Processor')
    parser.add_argument('--input-dir', required=True, help='Input directory containing images')
    parser.add_argument('--prompt', required=True, help='Base prompt for all images')
    parser.add_argument('--output-dir', default='./output', help='Output directory for results')
    parser.add_argument('--max-concurrent', type=int, default=5, help='Maximum concurrent requests')
    parser.add_argument('--max-retries', type=int, default=5, help='Maximum retry attempts per image')
    parser.add_argument('--enable-prompt-optimization', action='store_true', help='Enable automatic prompt refinement')
    parser.add_argument('--archive-format', choices=['zip', 'tar', 'none'], default='none', help='Archive format')
    parser.add_argument('--dry-run', action='store_true', help='Test without making actual API calls')
    return parser.parse_args()

def load_config_from_args(args):
    """Load configuration from command line arguments."""
    # Load from environment first
    config = Config.from_env()
    
    # Override with command line arguments
    config.max_concurrent_requests = args.max_concurrent
    config.max_retries = args.max_retries
    config.output_dir = args.output_dir
    config.enable_prompt_optimization = args.enable_prompt_optimization
    config.archive_format = args.archive_format
    config.dry_run = args.dry_run
    
    # Validate API key
    if not config.gemini_api_key and not args.dry_run:
        raise ValueError("GEMINI_API_KEY environment variable is required")
    
    return config

def get_image_files(input_dir: str, supported_formats=None) -> list:
    """Get list of supported image files from input directory."""
    if supported_formats is None:
        supported_formats = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif']
    
    input_path = Path(input_dir)
    if not input_path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")
    
    image_files = []
    for file_path in input_path.rglob("*"):
        if file_path.suffix.lower() in supported_formats:
            image_files.append(str(file_path))
    
    if not image_files:
        logger.warning(f"No supported image files found in {input_dir}")
    
    return image_files

async def main():
    """Main entry point."""
    args = parse_arguments()
    
    try:
        # Load configuration
        config = load_config_from_args(args)
        
        # Get image files
        image_files = get_image_files(args.input_dir)
        logger.info(f"Found {len(image_files)} images to process")
        
        if not image_files:
            logger.info("No images to process, exiting.")
            return
        
        # Initialize processor
        processor = GeminiBatchProcessor(config)
        
        # Process images
        logger.info(f"Starting batch processing with prompt: '{args.prompt}'")
        stats = await processor.process_image_batch(image_files, args.prompt)
        
        # Print summary
        logger.info("Batch processing completed!")
        logger.info(f"Total images: {stats['total_images']}")
        logger.info(f"Successful: {stats['successful']}")
        logger.info(f"Failed: {stats['failed']}")
        logger.info(f"Success rate: {stats['success_rate']:.2%}")
        logger.info(f"Results saved to: {config.output_dir}")
        
    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())