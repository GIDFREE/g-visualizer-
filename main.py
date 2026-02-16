import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

app = FastAPI()

# מאפשר לממשק ה-Web שלך לדבר עם השרת
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# הגדרת Gemini (השתמש ב-API Key שלך ב-Render מאוחר יותר)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    user_text = data.get("text")
    
    # ניתוח והפקת איור באמצעות Nano Banana
    prompt = f"Create a professional, clean educational illustration for: {user_text}"
    response = model.generate_content(prompt)
    
    # החזרת URL של התמונה (בפועל יגיע מהמודל)
    return {"image_url": "URL_FROM_NANO_BANANA", "text": user_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
