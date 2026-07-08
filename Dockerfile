FROM python:3.10-slim
RUN apt-get update && apt-get install -y ffmpeg
WORKDIR /code
COPY . .
RUN pip install python-telegram-bot yt-dlp
CMD ["python", "bot.py"]
