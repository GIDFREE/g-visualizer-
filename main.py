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

# הגדרת Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.post("/generate")
async def generate(request: Request):
    try:
        data = await request.json()
        user_text = data.get("text", "")
        
        if not user_text or len(user_text) < 5:
            return {"error": "Text too short"}

        model = genai.GenerativeModel('gemini-1.5-flash')
        # הפקודה שמזקקת מקטע טקסט למילת מפתח אחת באנגלית
        prompt = f"Summarize this lecture snippet into ONE simple English noun for image generation: {user_text}"
        response = model.generate_content(prompt)
        
        keyword = response.text.strip().split()[0].replace(".", "").replace(",", "")
        image_url = f"https://pollinations.ai/p/{keyword}?width=1024&height=1024&nologo=true"
        
        return {"image_url": image_url, "keyword": keyword}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
