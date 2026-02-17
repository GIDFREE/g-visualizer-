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

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.post("/generate")
async def generate(request: Request):
    try:
        data = await request.json()
        user_text = data.get("text", "")
        
        if len(user_text) < 10:
            return {"status": "waiting"}

        model = genai.GenerativeModel('gemini-1.5-flash')
        # הוראה למודל להוציא רק מילה אחת באנגלית שמתארת את הנושא
        prompt = f"Summarize this text into EXACTLY ONE English noun for image generation: {user_text}"
        response = model.generate_content(prompt)
        
        # ניקוי המילה מכל תו שאינו אותיות
        keyword = re.sub(r'[^a-zA-Z]', '', response.text.strip().split()[0])
        
        # שימוש במחולל תמונות יציב (Pollinations)
        image_url = f"https://pollinations.ai/p/{keyword}?width=1024&height=1024&nologo=true"
        
        return {"image_url": image_url, "keyword": keyword}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
