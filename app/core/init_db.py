"""
Database initialization utility
Ensures data directory exists for SQLite
"""
import os
from pathlib import Path


def ensure_data_directory():
    """Create data directory if it doesn't exist."""
    # Get the directory where the database will be stored
    db_path = Path("./data")
    
    # Create directory if it doesn't exist
    db_path.mkdir(exist_ok=True)
    
    # Also ensure chroma_db directory exists
    chroma_path = Path("./chroma_db")
    chroma_path.mkdir(exist_ok=True)
    
    return str(db_path)


if __name__ == "__main__":
    ensure_data_directory()
    print("✓ Data directories created")
