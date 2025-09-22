"""Prompt construction utilities."""
from typing import Optional

class PromptBuilder:
    """Build structured prompts from components."""
    
    @staticmethod
    def build(
        persona,  # We'll pass the persona object directly
        user_name: str,
        user_input: str,
        include_examples: bool = True
    ) -> str:
        """Construct a complete prompt from components."""
        user_request = f"Customer {user_name} asks: {user_input}"
        
        examples_section = persona.examples if include_examples and hasattr(persona, 'examples') and persona.examples else ""
        tone_section = f"\nTone: {persona.tone_markers}" if hasattr(persona, 'tone_markers') and persona.tone_markers else ""
        
        return f"""
{persona.role}
{persona.instruction}
{tone_section}

Output Format:
{persona.output_format}

Context:
{persona.context}

{examples_section}

Current Request:
{user_request}
"""
