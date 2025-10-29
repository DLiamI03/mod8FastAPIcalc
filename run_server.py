#!/usr/bin/env python3
"""
Startup script for FastAPI Calculator
"""
import subprocess
import sys
from pathlib import Path


def main():
    """Start the FastAPI calculator application."""
    project_dir = Path(__file__).parent
    
    # Change to project directory
    import os
    os.chdir(project_dir)
    
    # Start the server
    try:
        print("🚀 Starting FastAPI Calculator server...")
        print("📱 Web interface: http://localhost:8000")
        print("📖 API docs: http://localhost:8000/docs")
        print("🔍 Alternative docs: http://localhost:8000/redoc")
        print("💡 Press CTRL+C to stop the server\n")
        
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("\n💡 Make sure you're in the project directory and have activated the virtual environment.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())