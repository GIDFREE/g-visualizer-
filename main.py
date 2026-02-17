import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

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
    try:
        data = await request.json()
        user_text = data.get("text", "")
        
        if not user_text:
            return {"error": "No text provided"}

        model = genai.GenerativeModel('gemini-1.5-flash')
        # הפקודה ליצירת מילת מפתח אחת באנגלית מכל מקטע טקסט
        prompt = f"Convert this text into ONE simple English noun for image generation: {user_text}"
        response = model.generate_content(prompt)
        
        # ניקוי המילה מסימנים מיותרים
        keyword = response.text.strip().split()[0]
        image_url = f"https://pollinations.ai/p/{keyword}?width=1024&height=1024&nologo=true"
        
        return {"image_url": image_url, "keyword": keyword}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    # שימוש בפורט ש-Render דורש
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
