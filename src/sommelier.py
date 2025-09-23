"""Main sommelier system."""
import json
from src.wine_api import WineDatabase
from datetime import datetime
from typing import Dict, Any, List

# Use absolute imports instead of relative
from src.simple_client import SimpleLLMClient as LLMClient
from src.personas import PERSONAS
from src.prompt_builder import PromptBuilder

class WineSommelier:
    def __init__(self, llm_client=None):
        if llm_client is None:
            from src.simple_client import SimpleLLMClient
            llm_client = SimpleLLMClient()
        self.llm = llm_client
        self.prompt_builder = PromptBuilder()
        self.wine_db = WineDatabase()
        self.conversation_history = []
    
    def recommend(self, customer_name, dish_description, persona, save_response=True, include_bottles=False):
        """Generate wine recommendation for a given dish and persona"""
        
        # Store the original persona string for saving
        persona_key = persona if isinstance(persona, str) else persona
        
        # Get the persona object if a string key was passed
        if isinstance(persona, str):
            persona_obj = PERSONAS[persona]
        else:
            persona_obj = persona
        
        # Pass the persona object to prompt_builder
        prompt = self.prompt_builder.build(
            persona_obj,
            customer_name,
            dish_description
        )
        
        response = self.llm.chat(prompt)
        
        # Only add bottle recommendations if requested
        if include_bottles and hasattr(self, 'wine_db'):
            wine_type = self._extract_wine_type(response)
            if wine_type:
                bottles = self.wine_db.search_wines(wine_type, dish_description)
                if bottles:
                    bottle_text = self.wine_db.format_bottle_recommendations(bottles)
                    response += "\n\n---\n\n" + bottle_text
        
        if save_response:
            # Use the string key for saving, not the object
            self._save_interaction(customer_name, dish_description, persona_key, response)
        
        return response

    def _extract_wine_type(self, text: str) -> str:
        """Extract the wine type from the recommendation text"""
        wine_types = [
            "Cabernet Sauvignon", "Merlot", "Pinot Noir", "Syrah", "Malbec",
            "Chardonnay", "Sauvignon Blanc", "Pinot Grigio", "Riesling",
            "Rosé", "Prosecco", "Champagne", "Chianti", "Bordeaux"
        ]
        
        text_lower = text.lower()
        for wine in wine_types:
            if wine.lower() in text_lower:
                return wine
        
        return None
    
    def _save_interaction(self, name: str, dish: str, persona: str, response: str):
        """Save interaction to history."""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "customer": name,
            "dish": dish,
            "persona": persona,  # This should be a string
            "response": response
        }
        self.conversation_history.append(interaction)
    
    def compare_personas(self, customer_name: str, dish: str) -> Dict[str, str]:
        """Get recommendations from all personas for comparison."""
        results = {}
        for persona_name in PERSONAS.keys():
            results[persona_name] = self.recommend(
                customer_name, 
                dish, 
                persona_name,  # Pass the string key
                save_response=False, 
                include_bottles=False
            )
        return results