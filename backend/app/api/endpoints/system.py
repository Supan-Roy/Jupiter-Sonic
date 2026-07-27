from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/status")
def get_system_status():
    """Return enabled status of local AI modules and general metadata."""
    return {
        "project_name": settings.PROJECT_NAME,
        "environment": settings.ENV,
        "debug": settings.DEBUG,
        "modules": {
            "asr": {
                "enabled": settings.ENABLE_ASR,
                "model_id": settings.ASR_MODEL_ID
            },
            "diarization": {
                "enabled": settings.ENABLE_DIARIZATION,
                "model_id": settings.DIARIZATION_MODEL_ID
            },
            "cloning": {
                "enabled": settings.ENABLE_CLONING,
                "model_id": "EmbeddingsExtractor"
            },
            "tts": {
                "enabled": settings.ENABLE_TTS,
                "model_id": settings.TTS_MODEL_ID
            },
            "translation": {
                "enabled": settings.ENABLE_TRANSLATION,
                "model_id": settings.TRANSLATION_MODEL_ID
            },
            "enhancement": {
                "enabled": settings.ENABLE_ENHANCEMENT,
                "model_id": settings.ENHANCEMENT_MODEL_ID
            },
            "alignment": {
                "enabled": settings.ENABLE_ALIGNMENT,
                "model_id": settings.ALIGNMENT_MODEL_ID
            },
            "dubbing": {
                "enabled": settings.ENABLE_DUBBING,
                "model_id": "MultiModulePipeline"
            }
        }
    }
