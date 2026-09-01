"""
PRAHARI AI — Backend Bundler (PyInstaller)
==========================================
Compiles the FastAPI backend into a standalone Windows executable
that can be embedded in the Electron desktop app.

Usage:
    cd "c:/Users/Win11/OneDrive/Desktop/Projects/Aegis AI"
    .\\venv\\Scripts\\python.exe backend/build_backend.py

Output:
    dist/aegis_backend/aegis_backend.exe   (folder mode — recommended)
    dist/aegis_backend.exe                 (onefile mode — slower startup)
"""

import os
import sys
import shutil
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def compile_fastapi_backend():
    print("=" * 60)
    print("  PRAHARI AI — PyInstaller Backend Bundler")
    print("=" * 60)

    # Ensure PyInstaller is installed
    try:
        import PyInstaller
        print(f"[OK] PyInstaller {PyInstaller.__version__} found.")
    except ImportError:
        print("[!] PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

    # Paths
    entry_point = os.path.join(PROJECT_ROOT, "backend", "app", "main.py")
    data_dir     = os.path.join(PROJECT_ROOT, "data")
    backend_pkg  = os.path.join(PROJECT_ROOT, "backend")
    dist_dir     = os.path.join(PROJECT_ROOT, "dist")

    # Clean previous build
    for d in [os.path.join(PROJECT_ROOT, "build"), os.path.join(dist_dir, "aegis_backend")]:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"[Cleaned] {d}")

    # PyInstaller command — folder mode for fastest cold startup
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=aegis_backend",
        "--distpath", dist_dir,
        "--workpath", os.path.join(PROJECT_ROOT, "build"),
        "--specpath", os.path.join(PROJECT_ROOT, "build"),
        "--noconfirm",
        "--clean",
        # Bundle the entire backend package
        f"--add-data={backend_pkg}{os.pathsep}backend",
        # Bundle the data directory (SOP PDF, vectorstore, uploads)
        f"--add-data={data_dir}{os.pathsep}data",
        # Include uvicorn CLI runner
        "--hidden-import=uvicorn.main",
        "--hidden-import=uvicorn.config",
        "--hidden-import=uvicorn.logging",
        "--hidden-import=uvicorn.lifespan.on",
        "--hidden-import=uvicorn.protocols.http.h11_impl",
        "--hidden-import=uvicorn.protocols.http.httptools_impl",
        "--hidden-import=uvicorn.protocols.websockets.websockets_impl",
        # FastAPI / Starlette
        "--hidden-import=fastapi",
        "--hidden-import=starlette",
        "--hidden-import=starlette.middleware.cors",
        "--hidden-import=pydantic",
        "--hidden-import=pydantic_settings",
        # LangChain
        "--hidden-import=langchain",
        "--hidden-import=langchain_community",
        "--hidden-import=langchain_chroma",
        "--hidden-import=langchain_ollama",
        "--hidden-import=langchain_text_splitters",
        # ChromaDB
        "--hidden-import=chromadb",
        "--hidden-import=chromadb.db.impl.sqlite",
        "--hidden-import=chromadb.api.local",
        # BM25
        "--hidden-import=rank_bm25",
        # PDF / multipart
        "--hidden-import=pypdf",
        "--hidden-import=multipart",
        "--hidden-import=python_multipart",
        "--hidden-import=aiofiles",
        # Collect all packages to ensure nothing is missed
        "--collect-all=chromadb",
        "--collect-all=langchain_chroma",
        entry_point,
    ]

    print(f"\n[Running] PyInstaller with {len(cmd)} arguments...")
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)

    if result.returncode == 0:
        exe_path = os.path.join(dist_dir, "aegis_backend", "aegis_backend.exe")
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"\n[OK] Backend compiled successfully!")
            print(f"   Output: {exe_path}")
            print(f"   Size: {size_mb:.1f} MB")
            print(f"\nNext: Copy {os.path.join(dist_dir, 'aegis_backend')} folder")
            print("      into the Electron 'resources/backend/' directory.")
        else:
            print(f"\n[OK] Build succeeded. Check: {dist_dir}")
    else:
        print(f"\n[ERROR] PyInstaller compilation failed (exit code {result.returncode}).")
        print("   Ensure all dependencies are installed: pip install -r requirements.txt")
        print("   Also install: pip install pyinstaller")
        sys.exit(1)


if __name__ == "__main__":
    compile_fastapi_backend()
