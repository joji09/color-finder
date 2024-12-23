from fastapi import FastAPI, File, UploadFile
from PIL import Image
from io import BytesIO
from collections import Counter
from fastapi.middleware.cors import CORSMiddleware
from sklearn.cluster import KMeans
import numpy as np

app = FastAPI()
num_colors = 5

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_colors(image: Image.Image, num_colors: int =5):
    image = image.resize((100, 100)) # minimize the image so it can work faster processing pixels
    image = image.convert("RGB")
    pixels = np.array(image).reshape(-1, 3)

    kmeans = KMeans(n_clusters= num_colors, random_state=0)
    kmeans.fit(pixels)
    centers = kmeans.cluster_centers_

    labels, counts = np.unique(kmeans.labels_, return_counts=True)
    sort_indx = np.argsort(-counts)
    sort_colors = [centers[i] for i in sort_indx]

    hex_colors = [
        {
            "rgb": tuple(map(int, color)),
            "hex": "#{:02x}{:02x}{:02x}".format(
                int(color[0]), int(color[1]), int(color[2])
            ),
        }
        for color in sort_colors
    ]
    return hex_colors


# def get_dominant(image: Image.Image):
#     image = image.convert("RGB")
#     pixels = list(image.getdata())
#     common_color = Counter(pixels).most_common(5)
#     return [{'rgb': color, 'hex': f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"} for color, e in common_color]

@app.post("/api/colors/")
async def extract_colors(image: UploadFile = File(...)):
    image_bytes = await image.read()
    image = Image.open(BytesIO(image_bytes))
    # colors = get_dominant(image)
    colors = get_colors(image, num_colors)
    return {"colors": colors}
