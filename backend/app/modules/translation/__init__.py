import asyncio
from app.modules.base import TranslationModuleInterface, TranslationResult

class MockTranslationModule(TranslationModuleInterface):
    async def translate(self, text: str, source_lang: str, target_lang: str) -> TranslationResult:
        # Simulate local translation model processing latency
        await asyncio.sleep(0.3)
        
        # Simple mock translation responses
        translations = {
            "es": "Hola y bienvenidos a Jupiter Sonic. Esta es una plataforma de voz de IA totalmente local.",
            "fr": "Bonjour et bienvenue sur Jupiter Sonic. Il s'agit d'une plateforme vocale IA entièrement locale.",
            "de": "Hallo und willkommen bei Jupiter Sonic. Dies ist eine vollständig lokale KI-Sprachplattform.",
            "zh": "您好，欢迎来到 Jupiter Sonic。这是一个完全本地化的人工智能语音平台。"
        }
        
        translated = translations.get(
            target_lang.lower(), 
            f"[Mock Translation to {target_lang}]: {text}"
        )
        
        return TranslationResult(
            translated_text=translated,
            source_language=source_lang,
            target_language=target_lang
        )
