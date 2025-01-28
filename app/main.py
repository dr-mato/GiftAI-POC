# app/main.py
from fastapi import FastAPI, HTTPException, Request
from .schemas import GiftRequest, GiftResponse
from .services import generate_gift_categories_ai, fetch_gift_suggestions
from .logger import logger
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="GiftAI POC",
    description="An API to suggest gifts based on user preferences.",
    version="1.0.0"
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/suggest-gifts", response_model=GiftResponse)
@limiter.limit("5/minute")  # Limit to 5 requests per minute per IP
def suggest_gifts(gift_request: GiftRequest):
    logger.info(f"Received gift request: {gift_request}")

    try:
        # Generate gift categories using AI
        categories = generate_gift_categories_ai(gift_request)
        logger.info(f"Generated categories: {categories}")

        # Fetch gift suggestions based on categories and budget
        recommendations = fetch_gift_suggestions(categories, gift_request.budget)
        logger.info(f"Fetched {len(recommendations)} recommendations.")

        if not recommendations:
            raise HTTPException(status_code=404, detail="No gift recommendations found for the given criteria.")

        return GiftResponse(recommendations=recommendations)

    except HTTPException as http_exc:
        logger.error(f"HTTPException occurred: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Error processing gift request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
