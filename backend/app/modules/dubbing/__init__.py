import asyncio
import shutil
from pathlib import Path

from app.modules.alignment import MockAlignmentModule
from app.modules.asr import MockASRModule
from app.modules.base import DubbingPipelineInterface, DubbingResult
from app.modules.diarization import MockDiarizationModule
from app.modules.enhancement import MockEnhancementModule
from app.modules.translation import MockTranslationModule
from app.modules.tts import MockTTSModule


class MockDubbingPipeline(DubbingPipelineInterface):
    def __init__(self):
        self.asr = MockASRModule()
        self.diarization = MockDiarizationModule()
        self.translation = MockTranslationModule()
        self.alignment = MockAlignmentModule()
        self.tts = MockTTSModule()
        self.enhancement = MockEnhancementModule()

    async def run_dubbing(
        self,
        video_path: str,
        target_lang: str,
        source_lang: str | None = None,
        num_speakers: int | None = None,
    ) -> DubbingResult:
        # Simulate video demuxing and audio extraction
        await asyncio.sleep(0.3)

        # 1. Transcribe the extracted audio
        asr_res = await self.asr.transcribe(video_path, language=source_lang)

        # 2. Separate speakers
        await self.diarization.diarize(video_path, num_speakers=num_speakers)

        # 3. Translate transcription to target language
        trans_res = await self.translation.translate(
            asr_res.text, source_lang=asr_res.language, target_lang=target_lang
        )

        # Determine temporary/output paths
        input_p = Path(video_path)
        parent_dir = input_p.parent

        temp_audio = parent_dir / f"{input_p.stem}_dubbed_temp.wav"
        enhanced_audio = parent_dir / f"{input_p.stem}_dubbed_{target_lang}.wav"
        output_video = parent_dir / f"{input_p.stem}_dubbed_{target_lang}.mp4"

        # 4. Synthesize translated text via TTS (simulates using voice profiles from cloning)
        await self.tts.synthesize(
            text=trans_res.translated_text,
            voice_print_path="mock_speaker_embedding.bin",
            output_path=str(temp_audio),
        )

        # 5. Perform forced word alignment and sync (simulated)
        await self.alignment.align_words(str(temp_audio), trans_res.translated_text)

        # 6. Enhance/clean the synthesized speech track
        await self.enhancement.enhance_audio(str(temp_audio), str(enhanced_audio))

        # Remove intermediate raw tts file
        if temp_audio.exists():
            temp_audio.unlink()

        # 7. Remux final audio track back into video container (mock copies file or writes log)
        if input_p.exists() and input_p.suffix.lower() == ".mp4":
            shutil.copy(str(input_p), str(output_video))
        else:
            with open(str(output_video), "w") as f:
                f.write("Mock dubbed video file content")

        return DubbingResult(
            dubbed_video_path=str(output_video),
            output_audio_path=str(enhanced_audio),
            success=True,
        )
