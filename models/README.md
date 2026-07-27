# Local Model Storage 🪐🤖

This directory is used to store and cache neural network weights and configuration parameters for Jupiter Sonic. 

By default, all models run in **fully offline mode**. When model download scripts are executed, weights will be cached here rather than in default user home directories (`~/.cache`), ensuring that the project remains self-contained.

## Expected Subdirectories

* `whisper/` - Speech recognition checkpoints (e.g. `base.pt`, `large-v3.pt`).
* `pyannote/` - Speaker diarization configs and weights.
* `xtts/` - Text-to-Speech voices and XTTS engine configuration.
* `nllb/` - Multilingual translation network structures.
* `embeddings/` - Voiceprint cloning `.bin` or `.pth` vector outputs.

## Setup offline environment

When executing model pipelines, set your environment paths to look here:
```bash
# E.g. setting Hugging Face Cache directory
export HF_HOME=./models
```
