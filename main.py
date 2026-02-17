import os
import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# הגדרת Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.post("/generate")
async def generate(request: Request):
    try:
        data = await request.json()
        user_text = data.get("text", "")
        
        # דילוג על מקטעים קצרים מדי
        if len(user_text) < 10:
            return {"status": "waiting", "message": "More text needed"}

        model = genai.GenerativeModel('gemini-1.5-flash')
        # הוראה מפורשת למודל להוציא רק מילה אחת באנגלית
        prompt = f"Summary this text into EXACTLY ONE simple English noun for an image: {user_text}"
        response = model.generate_content(prompt)
        
        # ניקוי המילה מכל תו שאינו אותיות באנגלית
        raw_keyword = response.text.strip().split()[0]
        keyword = re.sub(r'[^a-zA-Z]', '', raw_keyword)
        
        # יצירת ה-URL הישיר לאיור
        image_url = f"https://pollinations.ai/p/{keyword}?width=1024&height=1024&nologo=true"
        
        return {"image_url": image_url, "keyword": keyword, "status": "success"}
    except Exception as e:
        return {"error": str(e), "status": "failed"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
