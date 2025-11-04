"""
FastAPI Application - Web API Service
Main application file with API endpoints
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
from typing import List, Optional
import os
from dotenv import load_dotenv

from app.database import get_db_connection, close_db_connection
from app.models import Item

# Load environment variables
load_dotenv()

# Create FastAPI app instance
app = FastAPI(
    title="Item Management API",
    description="Simple REST API for managing items with PostgreSQL",
    version="1.0.0"
)

# API Key Authentication
async def verify_api_key(x_api_key: str = Header(...)):
    """
    Verify API Key from request header
    
    Args:
        x_api_key: API key from X-API-Key header
        
    Raises:
        HTTPException: If API key is invalid
    """
    expected_key = os.getenv('API_KEY')
    if x_api_key != expected_key:
        raise HTTPException(
            status_code=403,
            detail="Invalid API Key"
        )
    return x_api_key


@app.get("/")
async def root():
    """
    Root endpoint - API information
    
    Returns:
        dict: API information and available endpoints
    """
    return {
        "message": "Welcome to Item Management API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "API information",
            "GET /items": "Get all items (requires API key)",
            "GET /items/{id}": "Get item by ID (requires API key)",
            "GET /docs": "API documentation (Swagger UI)"
        }
    }


@app.get("/items", response_model=List[Item])
async def get_items(api_key: str = Depends(verify_api_key)):
    """
    Get all items from database
    
    Args:
        api_key: Verified API key from dependency
        
    Returns:
        List[Item]: List of all items
        
    Raises:
        HTTPException: If database error occurs
    """
    connection = None
    try:
        # Connect to database
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Execute query
        cursor.execute("""
            SELECT id, name, description, price, quantity, created_at
            FROM items
            ORDER BY id
        """)
        
        # Fetch all results
        items = cursor.fetchall()
        
        # Close cursor
        cursor.close()
        
        return items
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
    finally:
        if connection:
            close_db_connection(connection)


@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int, api_key: str = Depends(verify_api_key)):
    """
    Get a specific item by ID
    
    Args:
        item_id: Item ID to retrieve
        api_key: Verified API key from dependency
        
    Returns:
        Item: Item details
        
    Raises:
        HTTPException: If item not found or database error
    """
    connection = None
    try:
        # Connect to database
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Execute query
        cursor.execute("""
            SELECT id, name, description, price, quantity, created_at
            FROM items
            WHERE id = %s
        """, (item_id,))
        
        # Fetch result
        item = cursor.fetchone()
        
        # Close cursor
        cursor.close()
        
        # Check if item exists
        if not item:
            raise HTTPException(
                status_code=404,
                detail=f"Item with ID {item_id} not found"
            )
        
        return item
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
    finally:
        if connection:
            close_db_connection(connection)


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    
    Returns:
        dict: Health status
    """
    connection = None
    try:
        # Test database connection
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        
        db_status = "healthy"
    except:
        db_status = "unhealthy"
    finally:
        if connection:
            close_db_connection(connection)
    
    return {
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "database": db_status
    }


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors"""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
