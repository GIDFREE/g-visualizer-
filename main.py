import os
import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.post("/generate")
async def generate(request: Request):
    try:
        data = await request.json()
        user_text = data.get("text", "")
        
        # זיקוק המשפט למילת מפתח אחת באנגלית
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Summarize this text into EXACTLY ONE English noun for image generation: {user_text}"
        response = model.generate_content(prompt)
        
        # ניקוי המילה מסימנים מיותרים
        keyword = response.text.strip().split()[0].replace(".", "").replace(",", "")
        image_url = f"https://pollinations.ai/p/{keyword}?width=1024&height=1024&nologo=true&model=flux"
        
        return {"image_url": image_url, "keyword": keyword}
    except Exception as e:
        # אם יש שגיאה, ננסה לפחות לייצר משהו מהטקסט המקורי
        return {"image_url": f"https://pollinations.ai/p/art?width=1024"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
