import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    gemini_api_key: str
    max_concurrent_requests: int = 5
    max_retries: int = 5
    output_dir: str = "./output"
    enable_prompt_optimization: bool = False
    archive_format: str = "none"  # "zip", "tar", or "none"
    dry_run: bool = False
    
    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
            max_concurrent_requests=int(os.getenv("MAX_CONCURRENT_REQUESTS", "5")),
            max_retries=int(os.getenv("MAX_RETRIES", "5")),
            output_dir=os.getenv("OUTPUT_DIR", "./output"),
            enable_prompt_optimization=os.getenv("ENABLE_PROMPT_OPTIMIZATION", "false").lower() == "true",
            archive_format=os.getenv("ARCHIVE_FORMAT", "none"),
            dry_run=os.getenv("DRY_RUN", "false").lower() == "true"
        )