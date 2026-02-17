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
        text = data.get("text", "")
        if len(text) < 5: return {"status": "skip"}

        # זיקוק הטקסט למילה אחת באנגלית
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Translate to one English noun: {text}")
        keyword = res.text.strip().split()[0].replace(".", "")
        
        return {"image_url": f"https://pollinations.ai/p/{keyword}?width=1024&height=1024&nologo=true"}
    except:
        return {"image_url": "https://pollinations.ai/p/abstract?width=1024"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
