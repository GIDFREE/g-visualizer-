import os
import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import urllib.parse

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
    data = await request.json()
    user_text = data.get("text", "")
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # כאן אנחנו מזקקים את הטקסט הארוך לתיאור קצר באנגלית
        refining_prompt = f"Summarize this text into 3 specific English keywords for an image generator: {user_text}"
        summary_response = model.generate_content(refining_prompt)
        keywords = summary_response.text.strip().replace(" ", ",")
        
        # יצירת כתובת תקנית (Encoded) כדי שהדפדפן לא יישבר
        encoded_keywords = urllib.parse.quote(keywords)
        image_url = f"https://pollinations.ai/p/{encoded_keywords}?width=1024&height=1024&nologo=true"
        
        return {"image_url": image_url, "status": "success"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
