import os
import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

@app.get("/")
async def root():
    return {"status": "online"}

@app.post("/generate")
async def generate(request: Request):
    try:
        data = await request.json()
        text = data.get("text", "")
        context = data.get("context", "general")
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt = f"Topic: {context}. Speaker said: '{text}'. Return ONLY one English noun for an image."
        response = model.generate_content(prompt)
        keyword = response.text.strip().split()[0].replace(".", "").lower()
        return {
            "image_url": f"https://pollinations.ai/p/{keyword}?width=1024&height=1024&nol
