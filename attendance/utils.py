import math
from functools import lru_cache
from pathlib import Path

import numpy as np
import cv2
import insightface
import chromadb
import onnxruntime as ort

# Resolve paths from this file, not from the working directory.
# This assumes models/ sits at the project root; adjust the parents[] index if not.
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
ANTISPOOF_PATH = MODELS_DIR / "modelrgb.onnx"
CHROMA_PATH = BASE_DIR / "chroma_face_db"

# -------- Load Face Model --------
model = insightface.app.FaceAnalysis(
    name="buffalo_l",
    root=str(MODELS_DIR),
    providers=["CPUExecutionProvider"],
)
model.prepare(ctx_id=0)


# -------- Anti-spoof model (lazy) --------
@lru_cache(maxsize=1)
def get_session():
    if not ANTISPOOF_PATH.exists():
        raise FileNotFoundError(
            f"Anti-spoof model not found at {ANTISPOOF_PATH}. "
            "Add modelrgb.onnx to the models/ folder."
        )
    return ort.InferenceSession(
        str(ANTISPOOF_PATH), providers=["CPUExecutionProvider"]
    )


# -------- Setup ChromaDB --------
client = chromadb.PersistentClient(path=str(CHROMA_PATH))
collection = client.get_or_create_collection(
    "faces", metadata={"hnsw:space": "cosine"}
)


# -------- Helpers --------
def read_image(file):
    contents = file.file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image")
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def preprocess(img):
    img = cv2.resize(img, (112, 112))
    img = img.astype(np.float32) / 255.0
    img = np.transpose(img, (2, 0, 1))
    return np.expand_dims(img, axis=0)


def is_live(img):
    session = get_session()
    input_name = session.get_inputs()[0].name  # avoids hardcoding "input"
    outputs = session.run(None, {input_name: preprocess(img)})
    real_score = outputs[0][0][1]
    return real_score > 0.5


def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (math.sin(dphi / 2) ** 2
         + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))