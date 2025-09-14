from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import json, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "models_data.json")
MODELS_DIR = os.path.join(BASE_DIR, "models")

print(BASE_DIR, JSON_PATH, MODELS_DIR, sep="\n")
with open(JSON_PATH, "r", encoding="utf-8") as f:
    MODELS_DB = json.load(f)


@app.get("/models")
def get_models():
    return MODELS_DB


@app.get("/models/{model_name}")
def get_model(model_name: str):
    for m in MODELS_DB["models"]:
        if m["name"] == model_name:
            return m
    raise HTTPException(status_code=404, detail="Model not found")


@app.get("/download/{model}/{type}/{weights}")
def download_weights(model: str, type: str, weights: str):
    for m in MODELS_DB["models"]:
        if m["name"] == model and weights in m["weights"]:
            path = os.path.join(MODELS_DIR, type, weights)
            if not os.path.exists(path):
                raise HTTPException(status_code=404, detail="Weights not found")
            return FileResponse(path, media_type="application/octet-stream", filename=weights)
    raise HTTPException(status_code=404, detail="Weights not found")
