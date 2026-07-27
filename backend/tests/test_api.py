import io
from fastapi.testclient import TestClient

def test_asr_transcribe(client: TestClient):
    file_data = b"fake audio wav file data"
    response = client.post(
        "/api/v1/asr/transcribe",
        files={"file": ("test.wav", io.BytesIO(file_data), "audio/wav")},
        data={"language": "en"}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "text" in json_data
    assert "segments" in json_data
    assert len(json_data["segments"]) > 0

def test_diarization_diarize(client: TestClient):
    file_data = b"fake audio data"
    response = client.post(
        "/api/v1/diarization/diarize",
        files={"file": ("test.wav", io.BytesIO(file_data), "audio/wav")},
        data={"num_speakers": 2}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "segments" in json_data
    assert "num_speakers" in json_data
    assert json_data["num_speakers"] == 2

def test_voice_cloning(client: TestClient):
    file_data = b"reference audio data"
    response = client.post(
        "/api/v1/cloning/clone",
        files={"file": ("ref.wav", io.BytesIO(file_data), "audio/wav")},
        data={"speaker_name": "Test Speaker"}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert json_data["speaker_name"] == "Test Speaker"
    assert "embedding_path" in json_data

def test_tts_synthesize(client: TestClient):
    response = client.post(
        "/api/v1/tts/synthesize",
        json={
            "text": "Hello world from Jupiter Sonic test",
            "voice_print_path": "mock_voice.bin"
        }
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "audio_path" in json_data
    assert json_data["duration"] == 2.0

def test_translation_translate(client: TestClient):
    response = client.post(
        "/api/v1/translation/translate",
        json={
            "text": "Hello",
            "source_lang": "en",
            "target_lang": "es"
        }
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "translated_text" in json_data
    assert json_data["source_language"] == "en"
    assert json_data["target_language"] == "es"

def test_audio_enhancement(client: TestClient):
    file_data = b"noisy audio wav data"
    response = client.post(
        "/api/v1/enhancement/enhance",
        files={"file": ("noisy.wav", io.BytesIO(file_data), "audio/wav")}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "enhanced_audio_path" in json_data
    assert "snr_db" in json_data

def test_forced_alignment(client: TestClient):
    file_data = b"audio waveforms"
    response = client.post(
        "/api/v1/alignment/align",
        files={"file": ("audio.wav", io.BytesIO(file_data), "audio/wav")},
        data={"text": "hello jupiter sonic"}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "words" in json_data
    assert len(json_data["words"]) == 3
    assert json_data["words"][0]["word"] == "hello"

def test_dubbing_pipeline(client: TestClient):
    file_data = b"mock mp4 container data"
    response = client.post(
        "/api/v1/dubbing/dub",
        files={"file": ("video.mp4", io.BytesIO(file_data), "video/mp4")},
        data={"target_lang": "es", "source_lang": "en"}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert "dubbed_video_path" in json_data
    assert "output_audio_path" in json_data
