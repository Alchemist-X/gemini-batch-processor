import os
import json
import zipfile
import tarfile
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class Archiver:
    def __init__(self, output_dir: str, archive_format: str = "none"):
        self.output_dir = Path(output_dir)
        self.archive_format = archive_format
        self.success_dir = self.output_dir / "successful"
        self.failed_dir = self.output_dir / "failed"
        self.metadata_dir = self.output_dir / "metadata"
        
        # Create directories
        self.success_dir.mkdir(parents=True, exist_ok=True)
        self.failed_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)
    
    def save_successful_result(self, image_name: str, result: str, metadata: Dict[str, Any] = None):
        """Save successful processing result."""
        result_file = self.success_dir / f"{image_name}_result.txt"
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(result)
        
        if metadata:
            metadata_file = self.success_dir / f"{image_name}_metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
    
    def save_failed_result(self, image_name: str, error_message: str, metadata: Dict[str, Any] = None):
        """Save failed processing result."""
        error_file = self.failed_dir / f"{image_name}_error.log"
        with open(error_file, 'w', encoding='utf-8') as f:
            f.write(error_message)
        
        if metadata:
            metadata_file = self.failed_dir / f"{image_name}_metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
    
    def save_processing_stats(self, stats: Dict[str, Any]):
        """Save overall processing statistics."""
        stats_file = self.metadata_dir / "processing_stats.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)
    
    def save_prompt_evolution(self, evolution_data: Dict[str, Any]):
        """Save prompt evolution history."""
        evolution_file = self.metadata_dir / "prompt_evolution.json"
        with open(evolution_file, 'w', encoding='utf-8') as f:
            json.dump(evolution_data, f, indent=2)
    
    def create_archive(self):
        """Create compressed archive of results."""
        if self.archive_format == "none":
            return
        
        archive_name = f"results.{self.archive_format}"
        archive_path = self.output_dir / archive_name
        
        if self.archive_format == "zip":
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(self.output_dir):
                    for file in files:
                        if file != archive_name:  # Don't include the archive itself
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, self.output_dir)
                            zipf.write(file_path, arcname)
        elif self.archive_format == "tar":
            with tarfile.open(archive_path, 'w:gz') as tar:
                for root, dirs, files in os.walk(self.output_dir):
                    for file in files:
                        if file != archive_name:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, self.output_dir)
                            tar.add(file_path, arcname)
        
        logger.info(f"Archive created: {archive_path}")