import os
import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import urllib.parse
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    user_text = data.get("text", "")
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # פקודה שמכריחה את המודל להוציא רק 2-3 מילים באנגלית
        refining_prompt = f"Convert this text into exactly 3 English keywords for an image: {user_text}. Output ONLY keywords."
        summary_response = model.generate_content(refining_prompt)
        
        # ניקוי הטקסט מסימנים מיוחדים
        clean_keywords = re.sub(r'[^a-zA-Z\s]', '', summary_response.text).strip().replace(" ", ",")
        
        # יצירת הכתובת בצורה בטוחה
        encoded_keywords = urllib.parse.quote(clean_keywords)
        image_url = f"https://pollinations.ai/p/{encoded_keywords}?width=1024&height=1024&nologo=true"
        
        return {"image_url": image_url, "status": "success"}
    except Exception as e:
        return {"error": str(e), "status": "failed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
