import base64
import io
import json
import re
from typing import List, Tuple, Optional, Dict, Any
import numpy as np
from PIL import Image

def decode_base64_image(image_input: str) -> Image.Image:
    """Decodes a base64 string (with or without data URL header) into a PIL Image."""
    clean_base64 = re.sub(r"^data:image\/[a-zA-Z]+;base64,", "", image_input.strip())
    image_bytes = base64.b64decode(clean_base64)
    img = Image.open(io.BytesIO(image_bytes))
    return img.convert("RGB")

def extract_face_embedding(image: Image.Image) -> List[float]:
    """
    Extracts a standardized 128-dimensional facial representation vector
    using normalized spatial block luminance, color distribution, and edge gradients.
    """
    resized = image.resize((112, 112))
    rgb_arr = np.asarray(resized, dtype=np.float32) / 255.0
    gray_arr = np.asarray(resized.convert("L"), dtype=np.float32) / 255.0

    blocks = []
    block_h, block_w = 28, 28
    for r in range(4):
        for c in range(4):
            block_gray = gray_arr[r*block_h:(r+1)*block_h, c*block_w:(c+1)*block_w]
            block_rgb = rgb_arr[r*block_h:(r+1)*block_h, c*block_w:(c+1)*block_w]

            mean_val = float(np.mean(block_gray))
            std_val = float(np.std(block_gray))
            dy, dx = np.gradient(block_gray)
            energy_x = float(np.mean(np.abs(dx)))
            energy_y = float(np.mean(np.abs(dy)))
            r_mean = float(np.mean(block_rgb[:, :, 0]))
            g_mean = float(np.mean(block_rgb[:, :, 1]))
            b_mean = float(np.mean(block_rgb[:, :, 2]))
            color_var = float(np.std(block_rgb))

            blocks.extend([mean_val, std_val, energy_x, energy_y, r_mean, g_mean, b_mean, color_var])

    vector = np.array(blocks[:128], dtype=np.float32)
    norm = np.linalg.norm(vector)
    if norm > 0:
        vector = vector / norm
    return [round(float(x), 5) for x in vector]

def compute_cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculates cosine similarity between two normalized vectors (-1.0 to 1.0)."""
    v1 = np.asarray(vec1, dtype=np.float32)
    v2 = np.asarray(vec2, dtype=np.float32)
    dot = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    similarity = float(dot / (norm1 * norm2))
    return round(max(0.0, min(1.0, similarity)), 4)

def match_face_against_gallery(
    query_vector: List[float],
    gallery: List[Dict[str, Any]],
    threshold: float = 0.70
) -> Tuple[Optional[Dict[str, Any]], float]:
    best_match = None
    best_score = -1.0

    for candidate in gallery:
        emb = candidate.get("embedding")
        if not emb:
            continue
        score = compute_cosine_similarity(query_vector, emb)
        if score > best_score:
            best_score = score
            if score >= threshold:
                best_match = candidate

    return best_match, best_score
