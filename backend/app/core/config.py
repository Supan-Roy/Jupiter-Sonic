import json
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    PROJECT_NAME: str = "Jupiter Sonic"
    API_V1_STR: str = "/api/v1"

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    CORS_ORIGINS: list[str] | str = []

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, str) and v.startswith("["):
            try:
                return json.loads(v)
            except Exception:
                return [v]
        return v

    # Database
    DATABASE_URL: str = "sqlite:///./jupiter_sonic.db"

    # Audio/Video Directories and Utilities
    FFMPEG_PATH: str = "ffmpeg"
    FFPROBE_PATH: str = "ffprobe"
    MODEL_DIR: str = "./models"
    OUTPUT_DIR: str = "./static/outputs"
    TEMP_DIR: str = "./temp"

    # Module Switches
    ENABLE_ASR: bool = True
    ENABLE_DIARIZATION: bool = True
    ENABLE_CLONING: bool = True
    ENABLE_TTS: bool = True
    ENABLE_TRANSLATION: bool = True
    ENABLE_ENHANCEMENT: bool = True
    ENABLE_ALIGNMENT: bool = True
    ENABLE_DUBBING: bool = True

    # Model Identifiers (HuggingFace Hub / Local Path)
    ASR_MODEL_ID: str = "openai/whisper-base"
    DIARIZATION_MODEL_ID: str = "pyannote/speaker-diarization-3.1"
    TTS_MODEL_ID: str = "coqui/XTTS-v2"
    TRANSLATION_MODEL_ID: str = "facebook/nllb-200-distilled-600M"
    ENHANCEMENT_MODEL_ID: str = "speechbrain/metricgan-plus-voicebank"
    ALIGNMENT_MODEL_ID: str = "reach-out/wav2vec2-forced-aligner"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def model_path(self) -> Path:
        p = Path(self.MODEL_DIR)
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def output_path(self) -> Path:
        p = Path(self.OUTPUT_DIR)
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def temp_path(self) -> Path:
        p = Path(self.TEMP_DIR)
        p.mkdir(parents=True, exist_ok=True)
        return p


settings = Settings()
