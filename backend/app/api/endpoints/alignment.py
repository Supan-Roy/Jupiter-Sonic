from fastapi import APIRouter, Depends, File, Form, UploadFile
from app.core.dependencies import get_alignment_module
from app.modules.base import AlignmentModuleInterface, AlignmentResult
from app.utils.files import save_upload_file

router = APIRouter()

@router.post("/align", response_model=AlignmentResult)
async def align_audio_text(
    file: UploadFile = File(..., description="Audio file containing speech"),
    text: str = Form(..., description="Transcription text corresponding to the audio speech"),
    alignment_module: AlignmentModuleInterface = Depends(get_alignment_module)
):
    """Perform forced-alignment to sync words in the text with matching audio timestamps."""
    temp_path = save_upload_file(file)
    try:
        result = await alignment_module.align_words(str(temp_path), text=text)
        return result
    finally:
        if temp_path.exists():
            temp_path.unlink()
