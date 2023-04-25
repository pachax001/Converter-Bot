#FROM python:3.9-slim-buster
FROM anasty17/mltb:latest
WORKDIR /app
RUN chmod 777 /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN apt install ffmpeg

COPY . .

CMD ["python3", "bot.py"]
