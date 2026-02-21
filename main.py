import os
import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# פתיחת חסימות דפדפן (CORS) - מאפשר ל-HTML בלפטופ לתקשר עם השרת ב-Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# חיבור למפתח ה-API שהגדרת ב-Render תחת השם GEMINI_API_KEY
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

@app.get("/")
async def root():
    return {"status": "G-Visualizer Server is Online"}

@app.post("/generate")
async def generate(request: Request):
    try:
        data = await request.json()
        user_text = data.get("text", "")
        context = data.get("context", "general")
        
        # לוגיקת זיקוק: הופכת את המשפט שלך למילת מפתח אחת באנגלית בעזרת Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Topic: {context}. Speaker said: '{user_text}'. Return ONLY one English noun representing this."
        
        response = model.generate_content(prompt)
        # ניקוי התשובה מסימני פיסוק ורווחים מיותרים
        keyword = response.text.strip().split()[0].replace(".", "").replace(",", "").lower()
        
        # יצירת הכתובת למנוע האיורים Pollinations
        image_url = f"https://pollinations.ai/p/{keyword}?width=1024&height=1024&nologo=true"
        
        return {"image_url": image_url, "keyword": keyword}
        
    except Exception as e:
        # במקרה של תקלה (למשל מפתח API לא תקין), נחזיר תמונת שגיאה גנרית
        return {"error": str(e), "image_url": "https://pollinations.ai/p/error_icon?width=1024", "keyword": "error"}

if __name__ == "__main__":
    # הגדרת פורט דינמי עבור Render
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
