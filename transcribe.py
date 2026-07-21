from faster_whisper import WhisperModel
from tqdm import tqdm


model = WhisperModel(
    "large-v3",
    device="cuda",
    compute_type="float16"
)


audio_file = "audio.mp3"


segments, info = model.transcribe(
    audio_file,
    beam_size=5
)


duration = info.duration


with open(
    "transcription.txt",
    "w",
    encoding="utf-8"
) as f:

    with tqdm(
        total=duration,
        desc="Transcribing",
        unit="sec"
    ) as bar:

        last_time = 0

        for segment in segments:

            f.write(
                segment.text.strip() + "\n"
            )

            current_time = segment.end

            bar.update(
                current_time - last_time
            )

            last_time = current_time


print("Done. Saved to transcription.txt")