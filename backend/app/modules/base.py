from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel, Field

# --- Core Data Schemas ---

class WordTimestamp(BaseModel):
    word: str = Field(..., description="The word spoken")
    start: float = Field(..., description="Start time in seconds")
    end: float = Field(..., description="End time in seconds")
    probability: Optional[float] = Field(None, description="Confidence score")

class ASRSegment(BaseModel):
    start: float
    end: float
    text: str
    words: Optional[List[WordTimestamp]] = None

class ASRResult(BaseModel):
    text: str = Field(..., description="Full transcribed text")
    segments: List[ASRSegment] = Field(default_factory=list, description="Text segments with timestamps")
    language: str = Field(..., description="Detected language code")

class SpeakerSegment(BaseModel):
    start: float = Field(..., description="Start time of segment")
    end: float = Field(..., description="End time of segment")
    speaker_label: str = Field(..., description="Speaker identifier (e.g. SPEAKER_01)")

class DiarizationResult(BaseModel):
    segments: List[SpeakerSegment] = Field(default_factory=list)
    num_speakers: int = Field(..., description="Total speakers detected")

class VoiceCloningResult(BaseModel):
    embedding_path: str = Field(..., description="Path to saved voice print/embedding")
    speaker_name: str = Field(..., description="Target speaker label")
    success: bool = True

class TTSResult(BaseModel):
    audio_path: str = Field(..., description="Path to synthesized WAV file")
    duration: float = Field(..., description="Duration in seconds")

class TranslationResult(BaseModel):
    translated_text: str
    source_language: str
    target_language: str

class EnhancementResult(BaseModel):
    enhanced_audio_path: str = Field(..., description="Path to noise-reduced clean audio")
    snr_db: Optional[float] = Field(None, description="Signal-to-noise ratio estimate in dB")

class AlignedWord(BaseModel):
    word: str
    start: float
    end: float
    score: float

class AlignmentResult(BaseModel):
    words: List[AlignedWord] = Field(default_factory=list)

class DubbingResult(BaseModel):
    dubbed_video_path: str = Field(..., description="Path to output video with aligned dubbed audio")
    output_audio_path: str = Field(..., description="Path to isolated dubbed audio track")
    success: bool = True

# --- AI Module Interfaces (ABCs) ---

class ASRModuleInterface(ABC):
    @abstractmethod
    async def transcribe(self, audio_path: str, language: Optional[str] = None) -> ASRResult:
        """Transcribe an audio file to text."""
        pass

class DiarizationModuleInterface(ABC):
    @abstractmethod
    async def diarize(self, audio_path: str, num_speakers: Optional[int] = None) -> DiarizationResult:
        """Analyze speaker separation in an audio file."""
        pass

class VoiceCloningModuleInterface(ABC):
    @abstractmethod
    async def extract_voice_print(self, reference_audio_path: str, speaker_name: str) -> VoiceCloningResult:
        """Generate and save speaker voice embeddings from a clean audio sample."""
        pass

class TTSModuleInterface(ABC):
    @abstractmethod
    async def synthesize(self, text: str, voice_print_path: str, output_path: str) -> TTSResult:
        """Synthesize text into speech using a saved voice embedding."""
        pass

class TranslationModuleInterface(ABC):
    @abstractmethod
    async def translate(self, text: str, source_lang: str, target_lang: str) -> TranslationResult:
        """Translate text content from source to target language."""
        pass

class EnhancementModuleInterface(ABC):
    @abstractmethod
    async def enhance_audio(self, audio_path: str, output_path: str) -> EnhancementResult:
        """Reduce background noise, restore spectral shape and output clean audio."""
        pass

class AlignmentModuleInterface(ABC):
    @abstractmethod
    async def align_words(self, audio_path: str, text: str) -> AlignmentResult:
        """Compute forced time-alignment between audio file and text transcription."""
        pass

class DubbingPipelineInterface(ABC):
    @abstractmethod
    async def run_dubbing(
        self,
        video_path: str,
        target_lang: str,
        source_lang: Optional[str] = None,
        num_speakers: Optional[int] = None
    ) -> DubbingResult:
        """Orchestrate entire pipeline to transcribe, translate, synthesize, and merge back dubbed audio."""
        pass
