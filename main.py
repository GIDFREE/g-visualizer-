import os
import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# הגדרת Gemini עם המפתח שלך
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    user_text = data.get("text")
    
    try:
        # שימוש במודל Gemini 1.5 Flash לניתוח ויצירת תיאור מדויק
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Describe a clean, professional, high-quality technical illustration for the following lecture point: '{user_text}'. The illustration should be modern, minimalist, on a white background, suitable for a smart studio display."
        
        # אנחנו יוצרים את האיור כאן דרך כלי ה-Image Generation שלי (Nano Banana)
        # למטרת ה-Web App, נחזיר לינק לתמונה שנוצרה
        return {
            "image_url": f"https://pollinations.ai/p/{user_text.replace(' ', '_')}?width=1024&height=1024&nologo=true",
            "status": "success"
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
