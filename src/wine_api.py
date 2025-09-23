# src/wine_api.py
import requests
import streamlit as st
from typing import List, Dict, Optional

class WineDatabase:
    """Interface to wine database APIs for specific bottle recommendations"""
    
    def __init__(self):
        # We'll use multiple free APIs as fallbacks
        self.apis = {
            'spoonacular': self._search_spoonacular,
            'open_wine': self._search_open_wine
        }
        
    def search_wines(self, wine_type: str, food_pairing: str = None, max_price: int = 100) -> List[Dict]:
        """
        Search for specific wine bottles based on criteria
        Returns list of wine recommendations with details
        """
        wines = []
        
        # Try Spoonacular API first (free tier available)
        try:
            wines = self._search_spoonacular(wine_type, food_pairing, max_price)
        except:
            pass
        
        # If no results, try backup method
        if not wines:
            wines = self._get_fallback_recommendations(wine_type, food_pairing)
        
        return wines
    
    def _search_spoonacular(self, wine_type: str, food: str, max_price: int) -> List[Dict]:
        """Search using Spoonacular API (requires free API key)"""
        # Note: User needs to get free key from https://spoonacular.com/food-api
        api_key = st.secrets.get("SPOONACULAR_API_KEY", None)
        
        if not api_key:
            return []
        
        url = "https://api.spoonacular.com/food/wine/recommendation"
        params = {
            "wine": wine_type,
            "maxPrice": max_price,
            "apiKey": api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [
                    {
                        "name": wine.get("title", "Unknown"),
                        "description": wine.get("description", ""),
                        "price": wine.get("price", "N/A"),
                        "rating": wine.get("averageRating", 0),
                        "image": wine.get("imageUrl", ""),
                        "link": wine.get("link", "")
                    }
                    for wine in data.get("recommendedWines", [])[:3]
                ]
        except:
            pass
        
        return []
    
    def _search_open_wine(self, wine_type: str, food: str, max_price: int) -> List[Dict]:
        """Search using Open Wine Database (no key required)"""
        # This is a simplified example - you'd need to implement based on actual API
        return []
    
    def _get_fallback_recommendations(self, wine_type: str, food: str) -> List[Dict]:
        """Provide curated recommendations when APIs are unavailable"""
        
        # Curated recommendations based on wine type
        recommendations = {
            "Pinot Noir": [
                {"name": "Meiomi Pinot Noir", "price": "$18-22", "description": "Smooth, versatile California Pinot with notes of berry and vanilla", "rating": 4.2},
                {"name": "La Crema Pinot Noir", "price": "$15-20", "description": "Elegant Sonoma Coast Pinot with cherry and spice notes", "rating": 4.1},
                {"name": "Böen Pinot Noir", "price": "$25-30", "description": "Rich, complex California Pinot with dark fruit flavors", "rating": 4.3}
            ],
            "Cabernet Sauvignon": [
                {"name": "Josh Cellars Cabernet", "price": "$12-15", "description": "Bold, approachable Cab with blackberry and vanilla", "rating": 4.0},
                {"name": "Decoy Cabernet Sauvignon", "price": "$20-25", "description": "Napa Valley Cab with rich fruit and soft tannins", "rating": 4.3},
                {"name": "The Prisoner Cabernet", "price": "$45-50", "description": "Premium Napa blend with complex dark fruit", "rating": 4.5}
            ],
            "Chardonnay": [
                {"name": "Kendall-Jackson Chardonnay", "price": "$12-15", "description": "Classic California Chard with tropical fruit and oak", "rating": 4.0},
                {"name": "Sonoma-Cutrer Chardonnay", "price": "$20-25", "description": "Elegant Russian River Valley Chard", "rating": 4.2},
                {"name": "Rombauer Chardonnay", "price": "$30-35", "description": "Rich, buttery Carneros Chardonnay", "rating": 4.4}
            ],
            "Sauvignon Blanc": [
                {"name": "Oyster Bay Sauvignon Blanc", "price": "$8-10", "description": "Crisp New Zealand Sauv Blanc with citrus notes", "rating": 3.9},
                {"name": "Whitehaven Sauvignon Blanc", "price": "$12-15", "description": "Vibrant Marlborough wine with tropical flavors", "rating": 4.2},
                {"name": "Cloudy Bay Sauvignon Blanc", "price": "$25-30", "description": "Premium New Zealand icon with complex aromatics", "rating": 4.4}
            ]
        }
        
        # Extract wine type from the recommendation text
        wine_key = None
        for key in recommendations.keys():
            if key.lower() in wine_type.lower():
                wine_key = key
                break
        
        if wine_key:
            return recommendations[wine_key]
        
        # Default recommendations if no match
        return [
            {"name": "Please consult your local wine shop", "price": "Varies", "description": f"Ask for a {wine_type} that pairs with your dish", "rating": 0}
        ]

    def format_bottle_recommendations(self, wines: List[Dict]) -> str:
        """Format wine bottles for display"""
        if not wines:
            return "No specific bottles found. Please consult your local wine shop."
        
        formatted = "🍾 **Specific Bottle Recommendations:**\n\n"
        for i, wine in enumerate(wines, 1):
            formatted += f"**{i}. {wine['name']}**\n"
            formatted += f"   💰 {wine['price']}\n"
            if wine.get('rating', 0) > 0:
                formatted += f"   ⭐ Rating: {wine['rating']}/5\n"
            formatted += f"   📝 {wine['description']}\n\n"
        
        return formatted