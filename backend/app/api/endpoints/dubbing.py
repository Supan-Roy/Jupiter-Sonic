import shutil
import uuid
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, Depends, File, Form, UploadFile
from app.core.config import settings
from app.core.dependencies import get_dubbing_pipeline
from app.modules.base import DubbingPipelineInterface, DubbingResult
from app.utils.files import save_upload_file

router = APIRouter()

@router.post("/dub", response_model=DubbingResult)
async def run_dubbing_pipeline(
    file: UploadFile = File(..., description="Video (or Audio) file to dub"),
    target_lang: str = Form(..., description="Target ISO language code (e.g. 'es', 'fr')"),
    source_lang: Optional[str] = Form(None, description="Optional source language code"),
    num_speakers: Optional[int] = Form(None, description="Optional speaker count"),
    dubbing_pipeline: DubbingPipelineInterface = Depends(get_dubbing_pipeline)
):
    """Run full automated local AI dubbing: transcribes, translates, synthesizes, and merges tracks."""
    temp_path = save_upload_file(file)
    try:
        # Run the pipeline
        result = await dubbing_pipeline.run_dubbing(
            video_path=str(temp_path),
            target_lang=target_lang,
            source_lang=source_lang,
            num_speakers=num_speakers
        )
        
        output_dir = Path(settings.OUTPUT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save output assets in static directory
        video_filename = f"dubbed_{uuid.uuid4().hex}{Path(result.dubbed_video_path).suffix or '.mp4'}"
        audio_filename = f"dubbed_{uuid.uuid4().hex}{Path(result.output_audio_path).suffix or '.wav'}"
        
        target_video_path = output_dir / video_filename
        target_audio_path = output_dir / audio_filename
        
        if Path(result.dubbed_video_path).exists():
            shutil.move(result.dubbed_video_path, str(target_video_path))
            result.dubbed_video_path = f"/static/outputs/{video_filename}"
            
        if Path(result.output_audio_path).exists():
            shutil.move(result.output_audio_path, str(target_audio_path))
            result.output_audio_path = f"/static/outputs/{audio_filename}"
            
        return result
    finally:
        # Cleanup uploaded file
        if temp_path.exists():
            temp_path.unlink()
