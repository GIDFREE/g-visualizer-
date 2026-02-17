import os
import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# הגדרת Gemini עם המפתח שלך
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.post("/generate")
async def generate(request: Request):
    try:
        data = await request.json()
        user_text = data.get("text", "")
        
        if not user_text:
            return {"error": "No text"}

        # שלב הזיקוק: הופכים עברית למילת מפתח באנגלית
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Convert this Hebrew text into ONE descriptive English noun for image generation: {user_text}"
        response = model.generate_content(prompt)
        
        # ניקוי המילה
        keyword = response.text.strip().split()[0].replace(".", "").replace(",", "")
        
        # יצירת הכתובת לאיור
        image_url = f"https://pollinations.ai/p/{keyword}?width=1024&height=1024&nologo=true&model=flux"
        
        return {"image_url": image_url, "keyword": keyword}
    except Exception as e:
        return {"image_url": "https://pollinations.ai/p/error?width=1024", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
