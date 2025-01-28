# app/services.py
import random
import openai
from typing import List
from .schemas import GiftRecommendation
from .config import settings

# Initialize OpenAI API
openai.api_key = settings.OPENAI_API_KEY

def generate_gift_categories(age: int, hobbies: List[str], favorite_tv_shows: List[str], budget: float, relationship: str, additional_preferences: str) -> List[str]:
    """
    Mock function to generate gift categories based on user input.
    """
    categories = []
    
    if age < 18:
        categories.append("Toys")
    elif 18 <= age < 30:
        categories.extend(["Tech Gadgets", "Books", "Fashion Accessories"])
    else:
        categories.extend(["Home Decor", "Kitchen Appliances", "Books"])
    
    if "photography" in hobbies:
        categories.append("Camera Accessories")
    if "traveling" in hobbies:
        categories.append("Travel Gear")
    
    if "eco-friendly" in additional_preferences.lower():
        categories.append("Sustainable Products")
    
    # Remove duplicates
    categories = list(set(categories))
    
    return categories

def generate_gift_categories_ai(gift_request) -> List[str]:
    """
    Generates gift categories using OpenAI's GPT model based on user input.
    """
    prompt = (
        f"Given the following user preferences, suggest relevant gift categories:\n"
        f"Age: {gift_request.age}\n"
        f"Hobbies: {', '.join(gift_request.hobbies)}\n"
        f"Favorite TV Shows: {', '.join(gift_request.favorite_tv_shows)}\n"
        f"Budget: ${gift_request.budget}\n"
        f"Relationship: {gift_request.relationship}\n"
        f"Additional Preferences: {gift_request.additional_preferences}\n"
        f"Provide the categories as a comma-separated list."
    )

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.7,
        )
        categories_text = response.choices[0].text.strip()
        categories = [category.strip() for category in categories_text.split(",")]
        return categories
    except Exception as e:
        # Handle exceptions (e.g., API errors, rate limits)
        print(f"Error generating categories with AI: {e}")
        return []


def fetch_gift_suggestions(categories: List[str], budget: float) -> List[GiftRecommendation]:
    """
    Mock function to fetch gift suggestions based on categories and budget.
    """
    mock_products = {
        "Tech Gadgets": [
            {
                "product_name": "Wireless Earbuds",
                "price": 99.99,
                "product_link": "https://amazon.com/dp/B08XYZ1234",
                "image_url": "https://amazon.com/images/B08XYZ1234.jpg",
                "description": "High-quality wireless earbuds with noise cancellation."
            },
            {
                "product_name": "Smartwatch",
                "price": 199.99,
                "product_link": "https://amazon.com/dp/B07XYZ5678",
                "image_url": "https://amazon.com/images/B07XYZ5678.jpg",
                "description": "Stylish smartwatch with multiple health tracking features."
            }
        ],
        "Books": [
            {
                "product_name": "Bestselling Novel",
                "price": 15.99,
                "product_link": "https://amazon.com/dp/B08XYZ9101",
                "image_url": "https://amazon.com/images/B08XYZ9101.jpg",
                "description": "An engaging novel that captivates readers from start to finish."
            }
        ],
        "Sustainable Products": [
            {
                "product_name": "Reusable Water Bottle",
                "price": 25.00,
                "product_link": "https://amazon.com/dp/B08XYZ1122",
                "image_url": "https://amazon.com/images/B08XYZ1122.jpg",
                "description": "Eco-friendly reusable water bottle made from sustainable materials."
            }
        ],
        # Add more categories and products as needed
    }
    
    recommendations = []
    
    for category in categories:
        products = mock_products.get(category, [])
        for product in products:
            if product["price"] <= budget:
                recommendations.append(GiftRecommendation(**product))
    
    # Randomly select up to 5 recommendations
    recommendations = random.sample(recommendations, min(len(recommendations), 5))
    
    return recommendations
