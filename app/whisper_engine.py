import streamlit as st
from faster_whisper import WhisperModel


@st.cache_resource
def load_model():

    return WhisperModel(
        "large-v3-turbo",
        device="cuda",
        compute_type="float16"
    )


model = load_model()


def transcribe_audio(audio_path, progress_bar=None, status_text=None):

    segments, info = model.transcribe(
        audio_path,
        beam_size=5
    )

    duration = info.duration
    text = []

    for segment in segments:

        text.append(segment.text.strip())

        if progress_bar:

            progress = segment.end / duration

            progress_bar.progress(
                min(progress, 1.0)
            )

            if status_text:
                status_text.write(
                    f"Processing: {int(progress * 100)}%"
                )


    return "\n".join(text)