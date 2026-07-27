from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.core.dependencies import get_translation_module
from app.modules.base import TranslationModuleInterface, TranslationResult

router = APIRouter()


class TranslationRequest(BaseModel):
    text: str = Field(..., description="Text content to translate")
    source_lang: str = Field(
        ..., description="ISO 639-1 source language code (e.g. 'en')"
    )
    target_lang: str = Field(
        ..., description="ISO 639-1 target language code (e.g. 'es')"
    )


@router.post("/translate", response_model=TranslationResult)
async def translate_text(
    payload: TranslationRequest,
    translation_module: TranslationModuleInterface = Depends(get_translation_module),
):
    """Translate text content from one language to another using local models."""
    return await translation_module.translate(
        text=payload.text,
        source_lang=payload.source_lang,
        target_lang=payload.target_lang,
    )
