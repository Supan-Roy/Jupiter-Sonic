import asyncio
import shutil
import wave
from pathlib import Path

from app.modules.base import EnhancementModuleInterface, EnhancementResult


class MockEnhancementModule(EnhancementModuleInterface):
    async def enhance_audio(
        self, audio_path: str, output_path: str
    ) -> EnhancementResult:
        # Simulate enhancement processing latency
        await asyncio.sleep(0.4)

        in_path = Path(audio_path)
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if in_path.exists():
            shutil.copy(str(in_path), str(out_path))
        else:
            # Create a mock valid wav of 1 second if source doesn't exist
            with wave.open(str(out_path), "wb") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(16000)
                wav_file.writeframes(b"\x00" * 32000)

        return EnhancementResult(enhanced_audio_path=str(out_path), snr_db=24.5)
