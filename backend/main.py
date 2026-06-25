"""
Main FastAPI application entry point for FinBudPlanner backend.

This module initializes the FastAPI application, configures CORS,
includes all API routers, and creates database tables on startup.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, income, expense, budget, dashboard

# Create database tables on startup
# This will create all tables defined in models.py if they don't exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(title="FinBudPlanner API")

# Configure CORS (Cross-Origin Resource Sharing)
# This allows the Angular frontend to make requests to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],  # Angular frontend URLs
    allow_credentials=True,  # Allow cookies and authentication headers
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include API routers with prefixes and tags for documentation
# All endpoints are prefixed with /api
app.include_router(auth.router, prefix="/api", tags=["authentication"])
app.include_router(income.router, prefix="/api", tags=["income"])
app.include_router(expense.router, prefix="/api", tags=["expense"])
app.include_router(budget.router, prefix="/api", tags=["budget"])
app.include_router(dashboard.router, prefix="/api", tags=["dashboard"])

@app.get("/")
def root():
    """
    Root endpoint - basic API information.
    
    Returns:
        dict: Welcome message
    """
    return {"message": "FinBudPlanner API is running"}

@app.get("/health")
def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        dict: Health status
    """
    return {"status": "healthy"}

# Run the application if executed directly
if __name__ == "__main__":
    import uvicorn
    # Start the FastAPI server on all interfaces, port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
