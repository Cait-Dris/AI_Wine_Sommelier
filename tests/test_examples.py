"""Test examples to verify the system works."""
import sys
from pathlib import Path
# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.sommelier import WineSommelier

def test_basic_recommendation():
    """Test that basic recommendation works."""
    sommelier = WineSommelier()
    
    response = sommelier.recommend(
        customer_name="Test User",
        dish_description="Pasta with tomato sauce",
        persona="professional"
    )
    
    assert response is not None
    assert len(response) > 50
    print("✓ Basic recommendation test passed")
    print(f"Response preview: {response[:200]}...")

def test_all_personas():
    """Test that all personas generate responses."""
    sommelier = WineSommelier()
    
    results = sommelier.compare_personas(
        "Test User",
        "Grilled chicken"
    )
    
    assert len(results) == 3  # professional, valley_girl, rick_sanchez
    for persona, response in results.items():
        assert response is not None
        print(f"✓ {persona} persona works")

if __name__ == "__main__":
    print("Running Wine Sommelier Tests\n")
    print("=" * 50)
    test_basic_recommendation()
    print("\n" + "=" * 50)
    test_all_personas()
    print("\n✅ All tests passed!")
