import asyncio
import wave
from pathlib import Path
from app.modules.base import TTSModuleInterface, TTSResult

class MockTTSModule(TTSModuleInterface):
    async def synthesize(self, text: str, voice_print_path: str, output_path: str) -> TTSResult:
        # Simulate neural model synthesis latency
        await asyncio.sleep(0.8)
        
        # Ensure target directory exists
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create a valid 16kHz, mono, 16-bit PCM WAV file containing 2 seconds of silence
        # (16000 samples/sec * 2 bytes/sample * 2 seconds = 64000 bytes)
        with wave.open(str(out_path), 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(16000)
            wav_file.writeframes(b'\x00' * 64000)
            
        return TTSResult(
            audio_path=str(out_path),
            duration=2.0
        )
