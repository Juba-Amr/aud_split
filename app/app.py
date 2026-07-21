import streamlit as st
import tempfile
import os
import gdown

from whisper_engine import transcribe_audio


st.set_page_config(
    page_title="Speech To Text"
)


st.title("Speech To Text")


# -------------------------
# Session state
# -------------------------

if "queue" not in st.session_state:
    st.session_state.queue = []

if "results" not in st.session_state:
    st.session_state.results = {}



# -------------------------
# Add files
# -------------------------

source = st.radio(
    "Add audio source",
    [
        "Upload files",
        "Google Drive link"
    ]
)


if source == "Upload files":

    files = st.file_uploader(
        "Select audio files",
        type=[
            "mp3",
            "wav",
            "m4a",
            "flac",
            "ogg",
            "webm",
            "mp4"
        ],
        accept_multiple_files=True
    )


    if files:

        if st.button("Add files to queue"):

            for file in files:

                suffix = os.path.splitext(
                    file.name
                )[1]

                temp = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix
                )

                temp.write(
                    file.read()
                )

                temp.close()

                st.session_state.queue.append(
                    {
                        "name": file.name,
                        "path": temp.name
                    }
                )

            st.success(
                "Files added"
            )



else:

    drive_url = st.text_input(
        "Google Drive file link"
    )


    if st.button("Add Drive file"):

        if drive_url:

            temp = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".mp3"
            )


            with st.spinner(
                "Downloading..."
            ):

                gdown.download(
                    drive_url,
                    temp.name,
                    quiet=False
                )


            st.session_state.queue.append(
                {
                    "name": os.path.basename(temp.name),
                    "path": temp.name
                }
            )


            st.success(
                "Added to queue"
            )



# -------------------------
# Queue display
# -------------------------

st.divider()

st.subheader("Queue")


if not st.session_state.queue:

    st.write(
        "No files waiting."
    )


else:

    for i, item in enumerate(
        st.session_state.queue
    ):

        col1, col2 = st.columns(
            [4,1]
        )

        col1.write(
            item["name"]
        )

        if col2.button(
            "Remove",
            key=f"remove_{i}"
        ):

            os.remove(
                item["path"]
            )

            st.session_state.queue.pop(i)

            st.rerun()



# -------------------------
# Process queue
# -------------------------

if st.session_state.queue:

    if st.button(
        "Start transcription"
    ):

        progress = st.progress(0)

        status = st.empty()


        total = len(
            st.session_state.queue
        )


        for index, item in enumerate(
            st.session_state.queue
        ):

            status.write(
                f"Processing {item['name']}"
            )


            text = transcribe_audio(
                item["path"],
                progress,
                status
            )


            st.session_state.results[
                item["name"]
            ] = text


            progress.progress(
                (index + 1) / total
            )


        st.success(
            "All files processed"
        )


        st.session_state.queue = []



# -------------------------
# Results
# -------------------------

if st.session_state.results:

    st.divider()

    st.subheader(
        "Results"
    )


    for filename, text in st.session_state.results.items():

        st.write(
            filename
        )


        st.text_area(
            "Transcript",
            text,
            height=200,
            key=filename
        )


        st.download_button(
            "Download TXT",
            text,
            file_name=f"{filename}.txt",
            mime="text/plain",
            key=f"download_{filename}"
        )