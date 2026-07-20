FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

RUN apt update && apt install -y ffmpeg python3-pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "runpod.serverless.start"]