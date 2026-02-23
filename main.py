import os
import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def root():
    key = os.environ.get("GEMINI_API_KEY", "NOT FOUND")
    return {"status": "online", "key_starts_with": key[:8] if len(key) > 8 else key}

@app.post("/generate")
async def generate(request: Request):
    try:
        data = await request.json()
        text = data.get("text", "")
        context = data.get("context", "general")

        api_key = os.environ.get("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        
        # נסה את המודל החדש
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        prompt = f"Topic: {context}. Speaker said: '{text}'. Return ONLY one English noun for an image."
        response = model.generate_content(prompt)
        keyword = response.text.strip().split()[0].replace(".", "").lower()

        return {
            "image_url": f"https://pollinations.ai/p/{keyword}?width=1024&height=1024&nologo=true",
            "keyword": keyword
        }
    except Exception as e:
        return {"error": str(e), "keyword": "error"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

ו-`requirements.txt`:
```
fastapi
uvicorn
google-generativeai
