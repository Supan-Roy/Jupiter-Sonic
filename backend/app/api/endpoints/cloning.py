from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.core.dependencies import get_voice_cloning_module
from app.modules.base import VoiceCloningModuleInterface, VoiceCloningResult
from app.utils.files import save_upload_file

router = APIRouter()


@router.post("/clone", response_model=VoiceCloningResult)
async def clone_voice(
    file: UploadFile = File(..., description="Reference audio of target voice"),
    speaker_name: str = Form(
        ..., description="Label or name for the cloned voice print"
    ),
    cloning_module: VoiceCloningModuleInterface = Depends(get_voice_cloning_module),
):
    """Generate and save local speaker voice embeddings for synthesis."""
    temp_path = save_upload_file(file)
    try:
        result = await cloning_module.extract_voice_print(
            str(temp_path), speaker_name=speaker_name
        )
        return result
    finally:
        if temp_path.exists():
            temp_path.unlink()
