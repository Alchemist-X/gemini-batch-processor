import json
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class PromptOptimizer:
    def __init__(self):
        self.failure_patterns = {}
        self.prompt_evolution_history = {}
    
    def analyze_failure(self, original_prompt: str, error_message: str) -> Dict[str, any]:
        """
        Analyze failure patterns and suggest prompt modifications.
        """
        analysis = {
            "original_prompt": original_prompt,
            "error_type": self._categorize_error(error_message),
            "suggested_modifications": []
        }
        
        # Common failure patterns and solutions
        if "content safety" in error_message.lower():
            analysis["suggested_modifications"].extend([
                "Add 'safe for work' to the prompt",
                "Make the description more specific and less ambiguous",
                "Avoid potentially sensitive topics"
            ])
        elif "prompt too long" in error_message.lower():
            analysis["suggested_modifications"].append(
                "Shorten the prompt to be more concise"
            )
        elif "invalid image" in error_message.lower():
            analysis["suggested_modifications"].extend([
                "Specify image format requirements",
                "Add 'clear, high-quality image' to prompt"
            ])
        else:
            # Generic optimizations
            analysis["suggested_modifications"].extend([
                "Make the prompt more specific",
                "Add style descriptors (e.g., 'anime style', 'cartoon')",
                "Include technical terms (e.g., 'high resolution', 'detailed')"
            ])
        
        return analysis
    
    def optimize_prompt(self, original_prompt: str, failure_analysis: Dict[str, any]) -> str:
        """
        Generate an optimized prompt based on failure analysis.
        """
        if not failure_analysis["suggested_modifications"]:
            return original_prompt
        
        # Apply the first suggested modification
        modification = failure_analysis["suggested_modifications"][0]
        
        if "safe for work" in modification:
            optimized = f"{original_prompt}, safe for work"
        elif "more specific" in modification:
            optimized = f"detailed {original_prompt}"
        elif "anime style" in modification:
            optimized = f"{original_prompt}, anime style illustration"
        elif "shorten" in modification:
            # Simple truncation for now
            words = original_prompt.split()
            optimized = " ".join(words[:20]) if len(words) > 20 else original_prompt
        else:
            optimized = f"{original_prompt}, high quality, detailed"
        
        logger.info(f"Prompt optimized: '{original_prompt}' -> '{optimized}'")
        return optimized
    
    def _categorize_error(self, error_message: str) -> str:
        """Categorize error types for better handling."""
        error_lower = error_message.lower()
        if "safety" in error_lower or "blocked" in error_lower:
            return "content_safety"
        elif "rate" in error_lower or "429" in error_lower:
            return "rate_limit"
        elif "400" in error_lower or "invalid" in error_lower:
            return "invalid_request"
        elif "timeout" in error_lower:
            return "timeout"
        else:
            return "other"
    
    def record_prompt_evolution(self, image_name: str, original_prompt: str, optimized_prompt: str):
        """Record prompt evolution for tracking."""
        if image_name not in self.prompt_evolution_history:
            self.prompt_evolution_history[image_name] = []
        self.prompt_evolution_history[image_name].append({
            "original": original_prompt,
            "optimized": optimized_prompt
        })
    
    def get_evolution_stats(self) -> Dict[str, any]:
        """Get statistics about prompt optimization."""
        return {
            "total_optimizations": len(self.prompt_evolution_history),
            "evolution_history": self.prompt_evolution_history
        }