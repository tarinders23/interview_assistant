#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "google-genai",
#     "python-dotenv",
# ]
# ///
"""
Example UV Script with Inline Dependencies

This demonstrates uv's ability to run standalone scripts with their own dependencies.
Run this script with: uv run examples/uv_script_example.py

More info: https://docs.astral.sh/uv/#scripts
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


def main():
    """Simple example showing script with inline dependencies."""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env file")
        print("This is just a demonstration of uv script with inline dependencies.")
        return
    
    print("✅ UV Script Example")
    print("=" * 50)
    print(f"Python version: {__import__('sys').version}")
    print(f"google-genai version: {genai.__version__}")
    print(f"Script location: {__file__}")
    print("\nThis script has its own dependencies defined inline!")
    print("No need to install them separately - uv handles it automatically.")
    print("\nTo run: uv run examples/uv_script_example.py")


if __name__ == "__main__":
    main()
