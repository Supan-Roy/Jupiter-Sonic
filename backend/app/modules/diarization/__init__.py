import asyncio

from app.modules.base import (
    DiarizationModuleInterface,
    DiarizationResult,
    SpeakerSegment,
)


class MockDiarizationModule(DiarizationModuleInterface):
    async def diarize(
        self, audio_path: str, num_speakers: int | None = None
    ) -> DiarizationResult:
        # Simulate processing time
        await asyncio.sleep(0.4)

        return DiarizationResult(
            segments=[
                SpeakerSegment(start=0.0, end=3.0, speaker_label="SPEAKER_01"),
                SpeakerSegment(start=3.0, end=6.5, speaker_label="SPEAKER_02"),
                SpeakerSegment(start=6.5, end=7.0, speaker_label="SPEAKER_01"),
            ],
            num_speakers=2,
        )
