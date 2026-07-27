from typing import Optional
from fastapi import APIRouter, Depends, File, Form, UploadFile
from app.core.dependencies import get_diarization_module
from app.modules.base import DiarizationModuleInterface, DiarizationResult
from app.utils.files import save_upload_file

router = APIRouter()

@router.post("/diarize", response_model=DiarizationResult)
async def diarize_audio(
    file: UploadFile = File(..., description="Audio file to separate speakers"),
    num_speakers: Optional[int] = Form(None, description="Expected speaker count"),
    diarization_module: DiarizationModuleInterface = Depends(get_diarization_module)
):
    """Run speaker diarization to find who spoke when in the audio file."""
    temp_path = save_upload_file(file)
    try:
        result = await diarization_module.diarize(str(temp_path), num_speakers=num_speakers)
        return result
    finally:
        if temp_path.exists():
            temp_path.unlink()
