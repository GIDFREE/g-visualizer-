import os
import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# מאפשר לממשק הוובי לדבר עם השרת
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# הגדרת המודל עם ה-API Key שלך מה-Environment
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    user_text = data.get("text")
    
    try:
        # ניתוח הטקסט ליצירת תיאור איור מקצועי
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt_refiner = f"Describe a clean, professional, high-quality technical illustration for: '{user_text}'. Minimalist, white background, digital art style."
        response = model.generate_content(prompt_refiner)
        visual_description = response.text.replace(" ", "_").replace(".", "")
        
        # יצירת ה-URL עבור Nano Banana (דרך שירות יציב)
        image_url = f"https://pollinations.ai/p/{visual_description[:100]}?width=1024&height=1024&nologo=true"
        
        return {"image_url": image_url, "status": "success"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
