# app/services.py
import openai
from typing import List
from .schemas import GiftRecommendation
from .config import settings

# Initialize OpenAI API
openai.api_key = settings.OPENAI_API_KEY

# Define category to products mapping
category_product_map = {
    "Tech Gadgets": [
        GiftRecommendation(
            product_name="Wireless Earbuds",
            price=99.99,
            product_link="https://amazon.com/dp/B08XYZ1234",
            image_url="https://amazon.com/images/B08XYZ1234.jpg",
            description="High-quality wireless earbuds with noise cancellation."
        )
    ],
    "Books": [
        GiftRecommendation(
            product_name="Bestselling Novel",
            price=15.99,
            product_link="https://amazon.com/dp/B08XYZ9101",
            image_url="https://amazon.com/images/B08XYZ9101.jpg",
            description="An engaging novel that captivates readers from start to finish."
        )
    ],
    "Eco-Friendly Products": [
        GiftRecommendation(
            product_name="Reusable Water Bottle",
            price=25.00,
            product_link="https://amazon.com/dp/B08XYZ1122",
            image_url="https://amazon.com/images/B08XYZ1122.jpg",
            description="Eco-friendly reusable water bottle made from sustainable materials."
        )
    ],
    "Fashion Accessories": [
        GiftRecommendation(
            product_name="Stylish Sunglasses",
            price=49.99,
            product_link="https://amazon.com/dp/B08XYZ3344",
            image_url="https://amazon.com/images/B08XYZ3344.jpg",
            description="Trendy sunglasses with UV protection."
        )
    ],
    "Camera Accessories": [
        GiftRecommendation(
            product_name="Camera Lens Kit",
            price=85.00,
            product_link="https://amazon.com/dp/B08XYZ5566",
            image_url="https://amazon.com/images/B08XYZ5566.jpg",
            description="Versatile lens kit for photography enthusiasts."
        )
    ],
    "Travel Gear": [
        GiftRecommendation(
            product_name="Portable Charger",
            price=30.00,
            product_link="https://amazon.com/dp/B08XYZ7788",
            image_url="https://amazon.com/images/B08XYZ7788.jpg",
            description="High-capacity portable charger for all your devices."
        )
    ],
    "Home Decor": [
        GiftRecommendation(
            product_name="Decorative Plant",
            price=20.00,
            product_link="https://amazon.com/dp/B08XYZ9900",
            image_url="https://amazon.com/images/B08XYZ9900.jpg",
            description="A beautiful decorative plant to enhance any living space."
        )
    ],
    # Add more categories and products as needed
}

VALID_CATEGORIES = set(category_product_map.keys())

def generate_gift_categories_ai(gift_request) -> List[str]:
    """
    Generates gift categories using OpenAI's GPT model based on user input.
    """
    prompt = (
        f"Given the following user preferences, suggest relevant gift categories. "
        f"The categories should be among the following options: Tech Gadgets, Books, Fashion Accessories, Camera Accessories, Travel Gear, Home Decor, Eco-Friendly Products.\n\n"
        f"Age: {gift_request.age}\n"
        f"Hobbies: {', '.join(gift_request.hobbies)}\n"
        f"Favorite TV Shows: {', '.join(gift_request.favorite_tv_shows)}\n"
        f"Budget: ${gift_request.budget}\n"
        f"Relationship: {gift_request.relationship}\n"
        f"Additional Preferences: {gift_request.additional_preferences}\n\n"
        f"Categories:"
    )

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=60,
            n=1,
            stop=None,
            temperature=0.7,
        )
        categories_text = response.choices[0].text.strip()
        categories = [category.strip() for category in categories_text.split(",") if category.strip()]
        
        return categories
    except openai.error.OpenAIError as e:
        return []
    except Exception as e:
        return []

def fetch_gift_suggestions(categories: List[str], budget: float) -> List[GiftRecommendation]:
    """
    Fetches gift suggestions based on categories and budget.
    """
    
    # Validate and sanitize categories
    valid_categories = [cat for cat in categories if cat in VALID_CATEGORIES]
    
    if not valid_categories:
        # Return all products within budget
        recommendations = [product for products in category_product_map.values() for product in products if product.price <= budget]
        return recommendations if recommendations else []
    
    recommendations = []
    for category in valid_categories:
        products = category_product_map.get(category, [])
        for product in products:
            if product.price <= budget:
                recommendations.append(product)
    
    return recommendations if recommendations else []
