from pathlib import Path
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from app.core.config import settings
from app.core.dependencies import get_tts_module
from app.modules.base import TTSModuleInterface, TTSResult

router = APIRouter()

from typing import Optional

class TTSRequest(BaseModel):
    text: str = Field(..., description="Text content to synthesize into speech")
    voice_print_path: str = Field(..., description="Local file path of the cloned voice print")
    output_filename: Optional[str] = Field(None, description="Optional custom filename (must end in .wav)")

@router.post("/synthesize", response_model=TTSResult)
async def synthesize_speech(
    payload: TTSRequest,
    tts_module: TTSModuleInterface = Depends(get_tts_module)
):
    """Synthesize text into speech using a voice print, saving to the static outputs folder."""
    filename = payload.output_filename or f"tts_{uuid.uuid4().hex}.wav"
    if not filename.endswith(".wav"):
        filename += ".wav"
        
    output_dir = Path(settings.OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    target_path = output_dir / filename
    
    result = await tts_module.synthesize(
        text=payload.text,
        voice_print_path=payload.voice_print_path,
        output_path=str(target_path)
    )
    
    # Update absolute path to reflect web server path relative to root
    # E.g. static/outputs/tts_xyz.wav so frontend can easily hit http://localhost:8000/static/outputs/tts_xyz.wav
    result.audio_path = f"/static/outputs/{filename}"
    return result
