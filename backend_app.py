from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import json, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

HF_URL = "https://huggingface.co/Gurbanov/New_model/resolve/main"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "models_data.json")
MODELS_DIR = os.path.join(BASE_DIR, "models")

print(BASE_DIR, JSON_PATH, MODELS_DIR, sep="\n")
with open(JSON_PATH, "r", encoding="utf-8") as f:
    MODELS_DB = json.load(f)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/models")
def get_models():
    return MODELS_DB


@app.get("/models/{model_name}")
def get_model(model_name: str):
    for m in MODELS_DB["models"]:
        if m["name"] == model_name:
            return m
    raise HTTPException(status_code=404, detail="Model not found")


@app.get("/models/{model_name}/weights")
def get_model_weights_names(model_name: str):
    for m in MODELS_DB["models"]:
        if m["name"] == model_name:
            return m["weights"]
    raise HTTPException(status_code=404, detail="Model not found")


def check_local_data(model: str, weights: str):
    for m in MODELS_DB["models"]:
        if m["name"] == model and weights in m["weights"]:
            return True
    return False


def check_remote_file_exists(url: str):
    try:
        r = requests.head(url, allow_redirects=True, timeout=5)
        if r.status_code == 200:
            return True
    except requests.RequestException:
        return False


@app.get("/download/{model}/{weights}")
def download_weights_proxy(model: str, weights: str):
    if not check_local_data(model, weights):
        raise HTTPException(status_code=404, detail="Incorrect data")
    url = f"{HF_URL}/models/{weights}.pth"
    if check_remote_file_exists(url):
        r = requests.get(url, stream=True)
        return StreamingResponse(
            r.iter_content(chunk_size=8192),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f'attachment; filename="{weights}.pth"'}
        )
    raise HTTPException(status_code=404, detail="Weights not found")
