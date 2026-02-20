import os
import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# מאפשר ל-HTML בלפטופ לדבר עם השרת ללא חסימות אבטחה
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# הגדרת ה-API Key של Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.post("/generate")
async def generate(request: Request):
    try:
        data = await request.json()
        text = data.get("text", "")
        context = data.get("context", "general")
        
        # הלוגיקה שמזקקת את הדיבור למילה אחת באנגלית
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Topic: {context}. Speech: {text}. Return ONLY one English keyword for an image."
        
        response = model.generate_content(prompt)
        keyword = response.text.strip().split()[0].replace(".", "").replace(",", "").lower()
        
        # החזרת הלינק למנוע האיורים
        image_url = f"https://pollinations.ai/p/{keyword}?width=1024&height=1024&nologo=true"
        return {"image_url": image_url, "keyword": keyword}
    except Exception as e:
        return {"error": str(e), "image_url": "https://pollinations.ai/p/error?width=1024"}
