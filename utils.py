# utils.py
import os
import json
import pandas as pd
from pathlib import Path
from typing import Dict, Any

def ensure_directories():
    """Create necessary directories"""
    directories = ['./documents', './chroma_db']
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

def save_query_history(query: str, answer: str, sources: list):
    """Save query history to JSON file"""
    history_file = Path("./query_history.json")
    
    entry = {
        "timestamp": str(pd.Timestamp.now()),
        "query": query,
        "answer": answer,
        "sources": sources
    }
    
    if history_file.exists():
        with open(history_file, 'r') as f:
            history = json.load(f)
    else:
        history = []
    
    history.append(entry)
    
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)

def get_file_stats(folder_path: str) -> Dict[str, Any]:
    """Get statistics about files in folder"""
    folder = Path(folder_path)
    if not folder.exists():
        return {"total_files": 0, "file_types": {}}
    
    files = list(folder.rglob("*"))
    file_types = {}
    total_size = 0
    
    for file in files:
        if file.is_file():
            ext = file.suffix.lower()
            file_types[ext] = file_types.get(ext, 0) + 1
            total_size += file.stat().st_size
    
    return {
        "total_files": len([f for f in files if f.is_file()]),
        "file_types": file_types,
        "total_size_mb": round(total_size / (1024 * 1024), 2)
    }
