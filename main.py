import os
import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# פתיחת חסימות דפדפן (CORS) - קריטי לעבודה מהלפטופ
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# הגדרת ה-API Key של Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.get("/")
async def health():
    return {"status": "G-Visualizer Online"}

@app.post("/generate")
async def generate(request: Request):
    try:
        data = await request.json()
        text = data.get("text", "")
        context = data.get("context", "general")
        
        # זיקוק המשפט למילה אחת באנגלית בעזרת Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Topic: {context}. Speaker said: '{text}'. Return ONLY one English noun for an image."
        
        response = model.generate_content(prompt)
        # ניקוי המילה מרווחים או נקודות
        keyword = response.text.strip().split()[0].replace(".", "").lower()
        
        # בניית הכתובת למנוע האיורים
        image_url = f"https://pollinations.ai/p/{keyword}?width=1024&height=1024&nologo=true"
        
        # החזרת נתונים בשמות שתואמים ל-HTML
        return {"image_url": image_url, "keyword": keyword}
        
    except Exception as e:
        return {"error": str(e), "image_url": "https://pollinations.ai/p/error?width=1024", "keyword": "error"}
