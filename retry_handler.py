import asyncio
import random
import logging
from typing import Callable, Any, Optional
from google.generativeai.types import GenerationConfig

logger = logging.getLogger(__name__)

class RetryHandler:
    def __init__(self, max_retries: int = 5):
        self.max_retries = max_retries
    
    async def execute_with_retry(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> Optional[Any]:
        """
        Execute a function with exponential backoff retry logic.
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                return result
                
            except Exception as e:
                last_exception = e
                logger.warning(f"Attempt {attempt + 1}/{self.max_retries} failed: {str(e)}")
                
                # Determine delay based on error type
                if "429" in str(e) or "rate limit" in str(e).lower():
                    # Rate limit - use longer delay
                    base_delay = 2.0
                elif "400" in str(e) or "invalid" in str(e).lower():
                    # Invalid request - don't retry
                    logger.error(f"Invalid request, skipping retry: {str(e)}")
                    return None
                else:
                    # Other errors - standard exponential backoff
                    base_delay = 1.0
                
                if attempt < self.max_retries - 1:
                    delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), 60.0)
                    logger.info(f"Waiting {delay:.2f} seconds before retry...")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"Max retries exceeded: {str(e)}")
        
        return None