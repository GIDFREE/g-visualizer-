import os
import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    text = data.get("text", "")
    context = data.get("context", "general")
    
    # זיקוק קשוח: מהמשפט שלך למילה אחת באנגלית
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Topic: {context}. Speaker said: '{text}'. Return ONLY ONE English noun representing this."
    
    response = model.generate_content(prompt)
    keyword = response.text.strip().split()[0].replace(".", "")
    
    return {"image_url": f"https://pollinations.ai/p/{keyword}?width=1024&height=1024", "keyword": keyword}
