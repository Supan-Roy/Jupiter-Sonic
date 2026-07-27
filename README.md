# Jupiter Sonic 🪐🎙️

An open-source, fully local **Speech Intelligence Platform**.

Jupiter Sonic is an advanced audio intelligence toolkit and server engine designed for voice cloning, AI dubbing, speech recognition (ASR), speaker diarization, multilingual translation, and audio processing. The platform is designed from the ground up to run **100% locally** on your own hardware, ensuring complete privacy, zero external API costs, and full offline capability.

---

## 🌌 Long-Term Vision

Jupiter Sonic aims to democratize production-ready speech intelligence by providing a robust, extensible pipeline for:

* **Voice Cloning**: High-fidelity few-shot and zero-shot voice cloning.
* **AI Dubbing**: Fully automated video/audio translation pipeline with speaker voice preservation and lip sync (forced-alignment).
* **Speech Recognition (ASR)**: Multi-language speech-to-text with word-level timestamps.
* **Speaker Diarization**: Multi-speaker identification and segmentation (who spoke when).
* **Multilingual Translation**: Seamless text-to-text and speech-to-speech translation preserving source voice characteristics.
* **Emotion Preservation**: Retaining pitch, tone, and prosody across speech synthesis and translations.
* **Audio Restoration**: Locally powered audio enhancement, background noise suppression, and volume leveling.
* **Local AI Inference**: Optimized execution across CPUs and GPUs (CUDA/MPS) without cloud API dependency.
* **Modular AI Pipelines**: Easily swappable model backends (e.g. swapping Whisper, Faster-Whisper, or Whisper-large-v3 without modifying core workflows).

---

## 🛠️ Technology Stack

### Backend
* **Python 3.12**
* **FastAPI**: Modern, asynchronous, high-performance web framework.
* **Pydantic v2**: Data validation and configuration management.
* **Uvicorn**: Asynchronous ASGI server.
* **SoundFile & librosa**: Precision audio read/write and processing.
* **FFmpeg**: Subprocess wrapper pipelines for high-performance audio/video manipulation.

### Frontend
* **React 18** + **Vite** + **TypeScript**
* **Tailwind CSS**: Modern utility-first CSS styling.
* **shadcn/ui**: Accessible and beautiful component base.

### Database & Storage
* **SQLite** (Development database)
* **PostgreSQL** (Production database support coming soon)

### Development & DevOps
* **Docker & Docker Compose**: Unified local orchestrations.
* **Ruff & Black**: Python linting and code formatting.
* **Pytest**: Backend unit and integration testing.
* **ESLint & Prettier**: Frontend linting and formatting.
* **GitHub Actions**: Continuous integration and unit test runners.

---

## 📁 Repository Architecture

The codebase emphasizes clean architecture and separation of concerns:

```
Jupiter Sonic/
├── .github/workflows/   # CI/CD pipelines
├── backend/
│   ├── app/
│   │   ├── api/         # FastAPI REST controllers
│   │   ├── core/        # App configuration, SQLite sessions, security
│   │   ├── ffmpeg/      # FFmpeg command-line wrappers
│   │   ├── modules/     # Swappable AI Engine Modules (Interfaces & Mock classes)
│   │   ├── pipelines/   # Multi-module orchestrations (e.g., ASR + Translation + TTS)
│   │   ├── schemas/     # Pydantic verification models
│   │   ├── services/    # Business rules and orchestration layer
│   │   └── main.py      # Application entry point
│   ├── tests/           # API and module pytest scripts
│   └── Dockerfile       # Production-ready Python environment with FFmpeg
├── frontend/
│   ├── src/             # TypeScript React source
│   │   ├── components/  # Dashboard widgets, custom sliders, charts
│   │   ├── services/    # REST clients for backend modules
│   │   └── App.tsx      # Main application view
│   └── Dockerfile       # Multi-stage frontend development and static serve Dockerfile
├── docs/                # Comprehensive architecture guides
├── models/              # Local cache directory for model checkpoints
└── scripts/             # Utility automation (e.g., model weights downloader)
```

---

## 🚀 Getting Started

### Prerequisites
* **Docker** & **Docker Compose**
* **Python 3.12+** (if running locally without Docker)
* **Node.js 18+** & **npm** (if running frontend locally)
* **FFmpeg** (installed and added to system path if running outside Docker)

### Quickstart with Docker Compose

To spin up the entire platform (FastAPI Backend + React Frontend + SQLite database):

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/jupiter-sonic.git
   cd jupiter-sonic
   ```

2. **Prepare Environment File**:
   Copy `.env.example` to `.env` (it contains standard development defaults):
   ```bash
   cp .env.example .env
   ```

3. **Build and Run the Services**:
   ```bash
   docker-compose up -d --build
   ```

4. **Verify Application Ports**:
   * **React Dashboard**: http://localhost:5173
   * **FastAPI Docs (Swagger)**: http://localhost:8000/docs

---

## 📖 Module Swap Guide

Each capability in the `backend/app/modules` directory implements a standard interface defined in `backend/app/modules/base.py`. For example, the `ASRModuleInterface` specifies a `transcribe(audio_path: str) -> ASRResult` signature. 

To swap an AI model:
1. Implement the protocol in a new class (e.g., `FasterWhisperASRModule`).
2. Register/inject your implementation in `backend/app/core/dependencies.py`.
3. The rest of the pipelines and endpoints will transition automatically.

---

## 📄 License

Jupiter Sonic is open-source software licensed under the [MIT License](LICENSE).

---

Developed by - **Supan Roy** ([contact@supanroy.com](mailto:contact@supanroy.com))
