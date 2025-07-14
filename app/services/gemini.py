
import google.generativeai as genai
from app.core.config import settings
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

def call_gemini_api(message: str) -> str:
    """
    Call Gemini API using the official Google library with proper error handling.
    
    Args:
        message: The text message to send to Gemini
        
    Returns:
        Generated text response from Gemini
        
    Raises:
        HTTPException: For various API errors with appropriate status codes
    """
    if not message or not message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )
    
    if not settings.GOOGLE_API_KEY:
        logger.error("Google API key not configured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API configuration error"
        )
    
    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate content
        response = model.generate_content(message)
        
        # Check if response was blocked
        if response.candidates[0].finish_reason.name == "SAFETY":
            logger.warning("Content blocked by safety filters")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Content blocked by safety filters"
            )
        
        # Check if response has text
        if not response.text:
            logger.error("No text content in AI response")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No text content generated"
            )
        
        return response.text
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        error_message = str(e).lower()
        
        # Handle specific API errors
        if "api_key" in error_message or "authentication" in error_message:
            logger.error("Authentication error with Gemini API")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI service authentication failed"
            )
        elif "quota" in error_message or "rate" in error_message:
            logger.error("Rate limit or quota exceeded")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="AI service rate limit exceeded. Please try again later."
            )
        elif "timeout" in error_message:
            logger.error("Timeout calling Gemini API")
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="AI service request timeout"
            )
        elif "connection" in error_message:
            logger.error("Connection error calling Gemini API")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI service connection failed"
            )
        else:
            logger.error(f"Unexpected error calling Gemini API: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI service error"
            )