"""Main sommelier system."""
import json
from datetime import datetime
from typing import Dict, Any, List

# Use absolute imports instead of relative
from src.simple_client import SimpleLLMClient as LLMClient
from src.personas import PERSONAS
from src.prompt_builder import PromptBuilder

class WineSommelier:
    """AI Wine Sommelier system with multiple personas."""
    
    def __init__(self, model: str = "llama3.2"):
        self.llm = LLMClient(model)
        self.prompt_builder = PromptBuilder()
        self.conversation_history: List[Dict[str, Any]] = []
    
    def recommend(
        self,
        customer_name: str,
        dish_description: str,
        persona: str = "professional",
        save_response: bool = True
    ) -> str:
        """Get wine recommendation for a dish."""
        if persona not in PERSONAS:
            available = list(PERSONAS.keys())
            return f"Unknown persona: {persona}. Available: {available}"
        
        persona_config = PERSONAS[persona]
        prompt = self.prompt_builder.build(
            persona=persona_config,
            user_name=customer_name,
            user_input=dish_description
        )
        
        response = self.llm.chat(prompt)
        
        if save_response:
            self._save_interaction(customer_name, dish_description, persona, response)
        
        return response
    
    def _save_interaction(self, name: str, dish: str, persona: str, response: str):
        """Save interaction to history."""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "customer": name,
            "dish": dish,
            "persona": persona,
            "response": response
        }
        self.conversation_history.append(interaction)
    
    def compare_personas(self, customer_name: str, dish: str) -> Dict[str, str]:
        """Get recommendations from all personas for comparison."""
        results = {}
        for persona_name in PERSONAS.keys():
            results[persona_name] = self.recommend(
                customer_name, dish, persona_name, save_response=False
            )
        return results
