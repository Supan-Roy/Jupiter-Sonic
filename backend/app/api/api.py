from fastapi import APIRouter
from app.api.endpoints import (
    asr,
    diarization,
    cloning,
    tts,
    translation,
    enhancement,
    alignment,
    dubbing,
    system,
)

api_router = APIRouter()

# Mount all endpoint routers
api_router.include_router(system.router, tags=["System Status"])
api_router.include_router(asr.router, prefix="/asr", tags=["Speech Recognition (ASR)"])
api_router.include_router(diarization.router, prefix="/diarization", tags=["Speaker Diarization"])
api_router.include_router(cloning.router, prefix="/cloning", tags=["Voice Cloning"])
api_router.include_router(tts.router, prefix="/tts", tags=["Text to Speech (TTS)"])
api_router.include_router(translation.router, prefix="/translation", tags=["Translation"])
api_router.include_router(enhancement.router, prefix="/enhancement", tags=["Audio Enhancement"])
api_router.include_router(alignment.router, prefix="/alignment", tags=["Forced Alignment"])
api_router.include_router(dubbing.router, prefix="/dubbing", tags=["Dubbing Pipeline"])
