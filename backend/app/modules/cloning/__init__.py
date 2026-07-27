import asyncio

from app.modules.base import VoiceCloningModuleInterface, VoiceCloningResult


class MockVoiceCloningModule(VoiceCloningModuleInterface):
    async def extract_voice_print(
        self, reference_audio_path: str, speaker_name: str
    ) -> VoiceCloningResult:
        # Simulate local embedding calculation
        await asyncio.sleep(0.6)

        # In a real model, this would be a .pth, .bin or .json embedding file
        mock_embedding_path = (
            f"/models/embeddings/{speaker_name.lower().replace(' ', '_')}_embedding.bin"
        )

        return VoiceCloningResult(
            embedding_path=mock_embedding_path, speaker_name=speaker_name, success=True
        )
