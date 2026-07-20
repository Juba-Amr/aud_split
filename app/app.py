import streamlit as st
import requests
import base64

st.title("Speech to Text")

audio = st.file_uploader(
    "Upload audio",
    type=["wav", "mp3", "m4a", "flac"]
)

if audio and st.button("Transcribe"):

    audio_b64 = base64.b64encode(audio.read()).decode()

    payload = {
        "input": {
            "audio": audio_b64
        }
    }

    response = requests.post(
        RUNPOD_ENDPOINT,
        headers={
            "Authorization": f"Bearer {RUNPOD_API_KEY}"
        },
        json=payload
    )

    st.write(response.json()["output"]["text"])