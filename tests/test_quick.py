#!/usr/bin/env python
"""Quick test of the sommelier system."""

from src.simple_client import SimpleLLMClient
from src.personas import PERSONAS
from src.prompt_builder import PromptBuilder

# Test the components
print("Testing components...")

# Test client
client = SimpleLLMClient()
print("✓ Client created")

# Test personas
print(f"✓ Found {len(PERSONAS)} personas")

# Test prompt builder
builder = PromptBuilder()
prompt = builder.build(
    PERSONAS["professional"],
    "Test User",
    "Grilled salmon"
)
print("✓ Prompt builder works")

# Now test full system
from src.sommelier import WineSommelier

sommelier = WineSommelier()
print("✓ Sommelier created")

response = sommelier.recommend(
    customer_name="Caitlin",
    dish_description="Grilled salmon with asparagus",
    persona="professional"
)

print("\n" + "="*50)
print("Wine Recommendation:")
print("="*50)
print(response)
