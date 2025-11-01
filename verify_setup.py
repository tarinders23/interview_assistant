#!/usr/bin/env python3
"""Verification script to check if the Interview Assistant is properly set up."""

import sys
import os
from pathlib import Path


def check_mark():
    return "✅"


def cross_mark():
    return "❌"


def warning_mark():
    return "⚠️ "


def main():
    print("=" * 70)
    print("Interview Assistant - System Verification")
    print("=" * 70)
    print()
    
    all_checks_passed = True
    
    # Check 1: Python version
    print("1. Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"   {check_mark()} Python {version.major}.{version.minor}.{version.micro}")
    else:
        print(f"   {cross_mark()} Python version should be 3.10 or higher")
        print(f"      Current: {version.major}.{version.minor}.{version.micro}")
        all_checks_passed = False
    
    # Check 2: Required files
    print("\n2. Checking required files...")
    required_files = [
        "requirements.txt",
        "README.md",
        ".env.example",
        ".gitignore",
        "src/config.py",
        "src/agent/interview_agent.py",
        "src/parsers/resume_parser.py",
        "src/models/__init__.py",
        "src/prompts/templates.py",
        "src/api/main.py",
        "cli.py",
        "run_api.py",
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   {check_mark()} {file_path}")
        else:
            print(f"   {cross_mark()} {file_path} - MISSING")
            all_checks_passed = False
    
    # Check 3: .env file
    print("\n3. Checking configuration...")
    if Path(".env").exists():
        print(f"   {check_mark()} .env file exists")
        
        # Check if API key is set
        try:
            with open(".env", "r") as f:
                content = f.read()
                if "OPENAI_API_KEY=your_openai_api_key_here" in content:
                    print(f"   {warning_mark()} OpenAI API key not configured")
                    print("      Edit .env and add your API key")
                elif "OPENAI_API_KEY=" in content and len(content.split("OPENAI_API_KEY=")[1].split()[0]) > 20:
                    print(f"   {check_mark()} OpenAI API key appears to be set")
                else:
                    print(f"   {warning_mark()} OpenAI API key may not be properly configured")
        except Exception as e:
            print(f"   {warning_mark()} Could not verify API key: {e}")
    else:
        print(f"   {warning_mark()} .env file not found")
        print("      Run: cp .env.example .env")
        print("      Then add your OpenAI API key")
    
    # Check 4: Try importing core modules
    print("\n4. Checking module imports...")
    modules_to_check = [
        ("src.config", "Configuration"),
        ("src.models", "Data Models"),
        ("src.parsers", "Resume Parser"),
        ("src.prompts", "Prompt Templates"),
        ("src.agent", "Question Agent"),
        ("src.api", "API"),
    ]
    
    sys.path.insert(0, os.path.abspath("."))
    
    for module_name, display_name in modules_to_check:
        try:
            __import__(module_name)
            print(f"   {check_mark()} {display_name}")
        except ImportError as e:
            print(f"   {cross_mark()} {display_name} - Import failed")
            print(f"      Error: {e}")
            all_checks_passed = False
        except Exception as e:
            print(f"   {warning_mark()} {display_name} - {type(e).__name__}: {e}")
    
    # Check 5: Dependencies
    print("\n5. Checking dependencies...")
    required_packages = [
        "langchain",
        "langchain_openai",
        "openai",
        "pdfplumber",
        "fastapi",
        "uvicorn",
        "pydantic",
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"   {check_mark()} {package}")
        except ImportError:
            print(f"   {cross_mark()} {package} - Not installed")
            missing_packages.append(package)
            all_checks_passed = False
    
    if missing_packages:
        print(f"\n   Install missing packages:")
        print(f"   pip install -r requirements.txt")
    
    # Check 6: Directory structure
    print("\n6. Checking directory structure...")
    required_dirs = [
        "src",
        "src/agent",
        "src/api",
        "src/models",
        "src/parsers",
        "src/prompts",
        "examples",
        "tests",
        "docs",
    ]
    
    for dir_path in required_dirs:
        if Path(dir_path).is_dir():
            print(f"   {check_mark()} {dir_path}/")
        else:
            print(f"   {cross_mark()} {dir_path}/ - MISSING")
            all_checks_passed = False
    
    # Summary
    print("\n" + "=" * 70)
    if all_checks_passed and not missing_packages:
        print("✅ All checks passed! The system is ready to use.")
        print("\nNext steps:")
        print("1. Make sure your OpenAI API key is set in .env")
        print("2. Try: python examples/usage_example.py")
        print("3. Or start the API: python run_api.py")
        print("4. Or use the CLI: python cli.py --help")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        if missing_packages:
            print("\nInstall dependencies:")
            print("  pip install -r requirements.txt")
        if not Path(".env").exists():
            print("\nSetup configuration:")
            print("  cp .env.example .env")
            print("  # Then edit .env and add your OpenAI API key")
    print("=" * 70)
    
    return 0 if all_checks_passed else 1


if __name__ == "__main__":
    sys.exit(main())
