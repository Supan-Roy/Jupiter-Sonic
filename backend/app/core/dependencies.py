from fastapi import HTTPException, status
from app.core.config import settings
from app.modules.base import (
    ASRModuleInterface,
    DiarizationModuleInterface,
    VoiceCloningModuleInterface,
    TTSModuleInterface,
    TranslationModuleInterface,
    EnhancementModuleInterface,
    AlignmentModuleInterface,
    DubbingPipelineInterface,
)
from app.modules.asr import MockASRModule
from app.modules.diarization import MockDiarizationModule
from app.modules.cloning import MockVoiceCloningModule
from app.modules.tts import MockTTSModule
from app.modules.translation import MockTranslationModule
from app.modules.enhancement import MockEnhancementModule
from app.modules.alignment import MockAlignmentModule
from app.modules.dubbing import MockDubbingPipeline

def get_asr_module() -> ASRModuleInterface:
    if not settings.ENABLE_ASR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ASR module is disabled"
        )
    return MockASRModule()

def get_diarization_module() -> DiarizationModuleInterface:
    if not settings.ENABLE_DIARIZATION:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Diarization module is disabled"
        )
    return MockDiarizationModule()

def get_voice_cloning_module() -> VoiceCloningModuleInterface:
    if not settings.ENABLE_CLONING:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Voice cloning module is disabled"
        )
    return MockVoiceCloningModule()

def get_tts_module() -> TTSModuleInterface:
    if not settings.ENABLE_TTS:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Text-to-Speech module is disabled"
        )
    return MockTTSModule()

def get_translation_module() -> TranslationModuleInterface:
    if not settings.ENABLE_TRANSLATION:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Translation module is disabled"
        )
    return MockTranslationModule()

def get_enhancement_module() -> EnhancementModuleInterface:
    if not settings.ENABLE_ENHANCEMENT:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Audio enhancement module is disabled"
        )
    return MockEnhancementModule()

def get_alignment_module() -> AlignmentModuleInterface:
    if not settings.ENABLE_ALIGNMENT:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Forced alignment module is disabled"
        )
    return MockAlignmentModule()

def get_dubbing_pipeline() -> DubbingPipelineInterface:
    if not settings.ENABLE_DUBBING:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Dubbing pipeline orchestrator is disabled"
        )
    return MockDubbingPipeline()

