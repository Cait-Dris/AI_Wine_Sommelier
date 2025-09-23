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
    """AI Wine Sommelier system with multiple personas."""
    
    def __init__(self, model: str = "llama3.2"):
        self.llm = LLMClient(model)
        self.prompt_builder = PromptBuilder()
        self.conversation_history: List[Dict[str, Any]] = []
        self.wine_db = WineDatabase()
    
    def recommend(self, customer_name, dish_description, persona, save_response=True, include_bottles=True):
        """Generate wine recommendation for a given dish and persona"""
        
        # Get the AI recommendation (existing code)
        prompt = self.prompt_builder.build(
            persona=persona,
            customer_name=customer_name,
            user_input=dish_description
        )
        
        response = self.llm.chat(prompt)
        
        # Extract wine type from response for bottle search
        if include_bottles:
            wine_type = self._extract_wine_type(response)
            if wine_type:
                bottles = self.wine_db.search_wines(wine_type, dish_description)
                if bottles:
                    bottle_text = self.wine_db.format_bottle_recommendations(bottles)
                    response += "\n\n---\n\n" + bottle_text
        
        if save_response:
            self._save_interaction(customer_name, dish_description, persona, response)
        
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
