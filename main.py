import os
import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# פתיחת חסימות דפדפן (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# הגדרת ה-API Key מה-Environment של Render
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

@app.post("/generate")
async def generate(request: Request):
    try:
        data = await request.json()
        user_text = data.get("text", "")
        context = data.get("context", "general")
        
        # הגדרה ישירה של המודל בנתיב המלא למניעת שגיאת 404
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        
        prompt = f"Topic: {context}. Speaker said: '{user_text}'. Return ONLY one English noun for an image."
        
        # יצירת התוכן בצורה מפורשת
        response = model.generate_content(prompt)
        
        # זיקוק המילה
        keyword = response.text.strip().split()[0].replace(".", "").replace(",", "").lower()
        
        image_url = f"https://pollinations.ai/p/{keyword}?width=1024&height=1024&nologo=true"
        return {"image_url": image_url, "keyword": keyword}
        
    except Exception as e:
        # שליחת השגיאה המדויקת חזרה ללפטופ לצורך ניפוי
        return {"error": str(e), "keyword": "error"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
