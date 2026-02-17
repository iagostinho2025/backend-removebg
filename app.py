from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ← libera Vercel, localhost, tudo
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

REMOVE_BG_API_KEY = "64b2Fp2iTvmZTmzwk184MiQJ"


@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    image_data = await file.read()

    response = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": image_data},
        data={"size": "full"},
        headers={"X-Api-Key": REMOVE_BG_API_KEY},
        timeout=120,
    )

    if response.status_code != 200:
        return Response(
            content=response.text,
            status_code=response.status_code
        )

    return Response(
        content=response.content,
        media_type="image/png"
    )
