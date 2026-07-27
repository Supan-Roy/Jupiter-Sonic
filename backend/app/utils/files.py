import shutil
from pathlib import Path
from fastapi import UploadFile
from app.core.config import settings

def save_upload_file(upload_file: UploadFile) -> Path:
    """Save an uploaded file to the temporary directory and return its path."""
    temp_dir = Path(settings.TEMP_DIR)
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = temp_dir / upload_file.filename
    # Avoid collisions if file exists
    counter = 1
    while file_path.exists():
        file_path = temp_dir / f"{file_path.stem}_{counter}{file_path.suffix}"
        counter += 1
        
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
        
    return file_path
