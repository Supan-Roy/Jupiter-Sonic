import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile

from app.core.config import settings
from app.core.dependencies import get_enhancement_module
from app.modules.base import EnhancementModuleInterface, EnhancementResult
from app.utils.files import save_upload_file

router = APIRouter()


@router.post("/enhance", response_model=EnhancementResult)
async def enhance_audio(
    file: UploadFile = File(..., description="Audio file to clean/enhance"),
    enhancement_module: EnhancementModuleInterface = Depends(get_enhancement_module),
):
    """Clean uploaded audio by removing noise and restoring spectral levels."""
    temp_path = save_upload_file(file)
    filename = f"enhanced_{uuid.uuid4().hex}.wav"

    output_dir = Path(settings.OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    target_path = output_dir / filename

    try:
        result = await enhancement_module.enhance_audio(
            str(temp_path), str(target_path)
        )
        result.enhanced_audio_path = f"/static/outputs/{filename}"
        return result
    finally:
        if temp_path.exists():
            temp_path.unlink()
