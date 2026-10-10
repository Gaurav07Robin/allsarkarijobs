import sys
import os

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import uvicorn

def main():
    print("=" * 60)
    print(">> AllSarkariJobs Server & Crawler Hub Starting...")
    print("=" * 60)
    print(">> Public Portal:      http://127.0.0.1:8000")
    print(">> Admin Review Hub:   http://127.0.0.1:8000/admin")
    print(">> API Documentation:  http://127.0.0.1:8000/docs")
    print("=" * 60)

    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
