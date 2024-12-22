from fastapi import FastAPI, File, UploadFile
from PIL import Image
from io import BytesIO
from collections import Counter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_dominant(image: Image.Image):
    image = image.convert("RGB")
    pixels = list(image.getdata())
    common_color = Counter(pixels).most_common(5)
    return [{'rgb': color, 'hex': f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"} for color, e in common_color]

@app.post("/api/colors/")
async def extract_colors(image: UploadFile = File(...)):
    image_bytes = await image.read()
    image = Image.open(BytesIO(image_bytes))
    colors = get_dominant(image)
    return {"colors": colors}
