#!/usr/bin/env python
"""Script to start the Interview Assistant API server."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import uvicorn
from src.config import settings


def main():
    """Start the API server."""
    print("=" * 80)
    print("Starting Interview Assistant API Server")
    print("=" * 80)
    print(f"Host: {settings.api_host}")
    print(f"Port: {settings.api_port}")
    print(f"Model: {settings.model_name}")
    print(f"Debug: {settings.debug}")
    print("=" * 80)
    print(f"\nAPI Documentation: http://localhost:{settings.api_port}/docs")
    print(f"Health Check: http://localhost:{settings.api_port}/health")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 80 + "\n")
    
    uvicorn.run(
        "src.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError starting server: {str(e)}")
        print("\nMake sure you have:")
        print("1. Set OPENAI_API_KEY in your .env file")
        print("2. Installed all dependencies: pip install -r requirements.txt")
        sys.exit(1)
