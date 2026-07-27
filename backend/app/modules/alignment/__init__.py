import asyncio

from app.modules.base import AlignedWord, AlignmentModuleInterface, AlignmentResult


class MockAlignmentModule(AlignmentModuleInterface):
    async def align_words(self, audio_path: str, text: str) -> AlignmentResult:
        # Simulate local forced alignment model latency
        await asyncio.sleep(0.3)

        words = text.split()
        aligned_words = []

        current_time = 0.0
        word_duration = 0.35
        gap = 0.05

        for w in words:
            # Clean punctuation for the score mapping
            cleaned_word = w.strip(".,!?;:()\"'")
            aligned_words.append(
                AlignedWord(
                    word=cleaned_word,
                    start=round(current_time, 2),
                    end=round(current_time + word_duration, 2),
                    score=0.97,
                )
            )
            current_time += word_duration + gap

        return AlignmentResult(words=aligned_words)
