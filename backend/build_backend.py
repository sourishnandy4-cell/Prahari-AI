import os
import subprocess
import sys

def compile_fastapi_backend():
    print("=== Aegis AI: Compiling FastAPI Backend with PyInstaller ===")
    
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name=aegis_backend",
        "--onefile",
        "--noconfirm",
        "--clean",
        "--add-data=backend;backend",
        "backend/app/main.py"
    ]
    
    print("Executing command:", " ".join(cmd))
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("✅ FastAPI backend successfully compiled to dist/aegis_backend.exe!")
    else:
        print("❌ PyInstaller compilation failed.")

if __name__ == "__main__":
    compile_fastapi_backend()
