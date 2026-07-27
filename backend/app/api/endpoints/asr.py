
from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.core.dependencies import get_asr_module
from app.modules.base import ASRModuleInterface, ASRResult
from app.utils.files import save_upload_file

router = APIRouter()


@router.post("/transcribe", response_model=ASRResult)
async def transcribe_audio(
    file: UploadFile = File(..., description="Audio file to transcribe"),
    language: str | None = Form(
        None, description="Optional ISO language code override"
    ),
    asr_module: ASRModuleInterface = Depends(get_asr_module),
):
    """Upload an audio file and transcribe its speech using local models."""
    temp_path = save_upload_file(file)
    try:
        result = await asr_module.transcribe(str(temp_path), language=language)
        return result
    finally:
        if temp_path.exists():
            temp_path.unlink()
