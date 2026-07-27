import asyncio

from app.modules.base import ASRModuleInterface, ASRResult, ASRSegment, WordTimestamp


class MockASRModule(ASRModuleInterface):
    async def transcribe(
        self, audio_path: str, language: str | None = None
    ) -> ASRResult:
        # Simulate local speech processing latency
        await asyncio.sleep(0.5)

        return ASRResult(
            text="Hello and welcome to Jupiter Sonic. This is a fully local AI speech platform.",
            segments=[
                ASRSegment(
                    start=0.0,
                    end=3.0,
                    text="Hello and welcome to Jupiter Sonic.",
                    words=[
                        WordTimestamp(
                            word="Hello", start=0.0, end=0.5, probability=0.99
                        ),
                        WordTimestamp(word="and", start=0.5, end=0.7, probability=0.98),
                        WordTimestamp(
                            word="welcome", start=0.7, end=1.2, probability=0.99
                        ),
                        WordTimestamp(word="to", start=1.2, end=1.4, probability=0.95),
                        WordTimestamp(
                            word="Jupiter", start=1.4, end=2.0, probability=0.99
                        ),
                        WordTimestamp(
                            word="Sonic.", start=2.0, end=3.0, probability=0.99
                        ),
                    ],
                ),
                ASRSegment(
                    start=3.0,
                    end=7.0,
                    text="This is a fully local AI speech platform.",
                    words=[
                        WordTimestamp(
                            word="This", start=3.0, end=3.3, probability=0.99
                        ),
                        WordTimestamp(word="is", start=3.3, end=3.5, probability=0.99),
                        WordTimestamp(word="a", start=3.5, end=3.6, probability=0.99),
                        WordTimestamp(
                            word="fully", start=3.6, end=4.1, probability=0.99
                        ),
                        WordTimestamp(
                            word="local", start=4.1, end=4.6, probability=0.99
                        ),
                        WordTimestamp(word="AI", start=4.6, end=5.0, probability=0.98),
                        WordTimestamp(
                            word="speech", start=5.0, end=5.5, probability=0.99
                        ),
                        WordTimestamp(
                            word="platform.", start=5.5, end=6.5, probability=0.99
                        ),
                    ],
                ),
            ],
            language=language or "en",
        )
