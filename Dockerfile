FROM python:3.10-slim

# Cài đặt espeak-ng (Bộ xử lý phiên âm Tiếng Việt chuẩn 100%)
RUN apt-get update && apt-get install -y \
    espeak-ng \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt Piper TTS và FastAPI
RUN pip install --no-cache-dir fastapi uvicorn piper-tts

WORKDIR /app

# Copy toàn bộ mã nguồn và thư mục model vào Docker container
COPY . .

EXPOSE 10000

# Lệnh khởi chạy server API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
