from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os

app = FastAPI(title="Piper TTS Vietnamese API")

# Bật CORS để Web GitHub Pages có thể gọi API không bị trình duyệt chặn
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "online", "message": "Piper TTS API đang hoạt động!"}

@app.get("/tts")
def text_to_speech(
    text: str = Query(..., description="Văn bản tiếng Việt cần đọc"),
    model: str = Query("tranthanh", description="Tên mô hình giọng đọc")
):
    if not text.strip():
        raise HTTPException(status_code=400, detail="Văn bản không được để trống")

    output_wav = "/tmp/output.wav"
    
    # Đường dẫn file model .onnx
    model_path = f"model/{model}.onnx"
    
    # Nếu model không tồn tại -> Lấy file .onnx đầu tiên tìm thấy trong thư mục model/
    if not os.path.exists(model_path):
        available_models = [f for f in os.listdir("model") if f.endswith(".onnx")]
        if available_models:
            model_path = os.path.join("model", available_models[0])
        else:
            raise HTTPException(status_code=404, detail="Không tìm thấy file .onnx trong thư mục model/")

    try:
        # Chạy Piper CLI chính thức (xử lý unicode Tiếng Việt an toàn)
        cmd = ["piper", "--model", model_path, "--output_file", output_wav]
        subprocess.run(cmd, input=text.encode('utf-8'), check=True)

        return FileResponse(output_wav, media_type="audio/wav", filename="speech.wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi tạo giọng đọc: {str(e)}")
