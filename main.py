import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
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
    try:
        data = await request.json()
        user_text = data.get("text", "")
        
        if len(user_text) < 5:
            return {"status": "skip", "reason": "text too short"}

        model = genai.GenerativeModel('gemini-1.5-flash')
        # הפקודה שמזקקת את המקטע למילה אחת ברורה
        prompt = f"Summarize this lecture snippet into ONE simple English noun for an image: {user_text}"
        response = model.generate_content(prompt)
        
        # ניקוי תווים מיוחדים מהתשובה
        keyword = re.sub(r'[^a-zA-Z]', '', response.text.split()[0])
        image_url = f"https://pollinations.ai/p/{keyword}?width=1024&height=1024&nologo=true"
        
        return {"image_url": image_url, "keyword": keyword, "status": "success"}
    except Exception as e:
        return {"error": str(e), "status": "failed"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
