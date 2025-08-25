"""
FastAPI application for Multilingual AI Tutor.

This module sets up the main FastAPI application with CORS middleware,
API routing, and application configuration for the multilingual tutoring platform.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Sets up the main FastAPI app with middleware and metadata.
    Includes CORS middleware for cross-origin requests.

    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    app = FastAPI(
        title="Multilingual AI Tutor",
        description="AI-powered language coach with real-time conversational practice",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
