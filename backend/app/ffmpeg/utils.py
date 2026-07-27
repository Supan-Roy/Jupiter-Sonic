import asyncio
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


async def run_ffmpeg_cmd(args: list[str]) -> bool:
    """Helper to execute an FFmpeg command asynchronously."""
    cmd = [settings.FFMPEG_PATH] + args
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            return True
        else:
            logger.error(
                f"FFmpeg failed with exit code {process.returncode}. error: {stderr.decode()}"
            )
            return False
    except FileNotFoundError:
        logger.error(
            f"FFmpeg executable not found at path: {settings.FFMPEG_PATH}. Please install FFmpeg."
        )
        return False
    except Exception as e:
        logger.error(f"Failed to execute FFmpeg command: {e}")
        return False


async def convert_to_speech_wav(
    input_path: str, output_path: str, sample_rate: int = 16000
) -> bool:
    """Convert any audio/video input to 16kHz mono PCM 16-bit WAV (required by most ASR models)."""
    # -y: overwrite output
    # -i: input
    # -ar: sample rate
    # -ac: audio channels (1 = mono)
    # -acodec pcm_s16le: 16-bit PCM codec
    args = [
        "-y",
        "-i",
        input_path,
        "-ar",
        str(sample_rate),
        "-ac",
        "1",
        "-acodec",
        "pcm_s16le",
        output_path,
    ]
    return await run_ffmpeg_cmd(args)


async def extract_audio(video_path: str, output_audio_path: str) -> bool:
    """Extract audio track from video file and save to target path."""
    args = [
        "-y",
        "-i",
        video_path,
        "-vn",  # Disable video recording
        "-acodec",
        "copy",  # Copy audio codec (no re-encoding, extremely fast)
        output_audio_path,
    ]
    # If the direct audio copy fails due to incompatible formats, fallback to wav conversion
    success = await run_ffmpeg_cmd(args)
    if not success:
        logger.warning("Fast audio copy failed, attempting full wav conversion...")
        return await convert_to_speech_wav(video_path, output_audio_path)
    return True


async def merge_audio_video(
    video_path: str, audio_path: str, output_video_path: str
) -> bool:
    """Merge a new audio track with an existing video track, replacing original audio."""
    # -y: overwrite
    # -i: video input
    # -i: audio input
    # -c:v copy: copy video stream directly (fast, lossless)
    # -c:a aac: encode audio to standard AAC for mp4 compatibility
    # -map 0:v:0: take video from first input
    # -map 1:a:0: take audio from second input
    # -shortest: end compilation when shortest track finishes
    args = [
        "-y",
        "-i",
        video_path,
        "-i",
        audio_path,
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-shortest",
        output_video_path,
    ]
    return await run_ffmpeg_cmd(args)


async def get_media_duration(file_path: str) -> float:
    """Query duration of audio/video using ffprobe."""
    cmd = [
        settings.FFPROBE_PATH,
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        file_path,
    ]
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode == 0:
            return float(stdout.decode().strip())
    except Exception as e:
        logger.error(f"Failed to query media duration with ffprobe: {e}")
    return 0.0
