import tempfile
from faster_whisper import WhisperModel

model = WhisperModel(
    "large-v3",
    device="cuda",
    compute_type="float16"
)

def handler(event):
    audio_bytes = event["input"]["audio"]

    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        f.write(bytes(audio_bytes))
        f.flush()

        segments, info = model.transcribe(
            f.name,
            beam_size=5,
            vad_filter=True
        )

        text = " ".join(segment.text for segment in segments)

    return {
        "text": text,
        "language": info.language
    }