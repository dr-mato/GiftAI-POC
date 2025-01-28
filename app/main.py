# app/main.py
from fastapi import FastAPI, HTTPException, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from .schemas import GiftRequest, GiftResponse
from .services import generate_gift_categories_ai, fetch_gift_suggestions

# Initialize the rate limiter with the key function (client's IP address)
limiter = Limiter(key_func=get_remote_address)

# Initialize the FastAPI app
app = FastAPI(
    title="GiftAI POC",
    description="An API to suggest gifts based on user preferences.",
    version="1.0.0"
)

# Attach the rate limiter to the app's state
app.state.limiter = limiter

# Add the rate limit exception handler
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/suggest-gifts", response_model=GiftResponse)
@limiter.limit("5/minute")  # Limit to 5 requests per minute per IP
def suggest_gifts(request: Request, gift_request: GiftRequest):

    try:
        # Generate gift categories using AI
        categories = generate_gift_categories_ai(gift_request)

        # Fetch gift suggestions based on categories and budget
        recommendations = fetch_gift_suggestions(categories, gift_request.budget)

        if not recommendations:
            raise HTTPException(status_code=404, detail="No gift recommendations found for the given criteria.")

        return GiftResponse(recommendations=recommendations)

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
