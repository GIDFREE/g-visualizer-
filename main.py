import os
import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# הגדרת Gemini בצורה בטוחה
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

@app.post("/generate")
async def generate(request: Request):
    try:
        data = await request.json()
        text = data.get("text", "")
        context = data.get("context", "general")
        
        # בניית פרומפט שמוודא שנקבל רק מילה אחת באנגלית
        prompt = f"Topic: {context}. Speech: {text}. Return ONLY one English keyword for an image."
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        # ניקוי התשובה מסימני פיסוק ורווחים
        keyword = response.text.strip().split()[0].replace(".", "").replace(",", "").lower()
        
        image_url = f"https://pollinations.ai/p/{keyword}?width=1024&height=1024&nologo=true"
        return {"image_url": image_url, "keyword": keyword}
        
    except Exception as e:
        # במקרה של שגיאה, נחזיר תמונה כללית כדי שה-App לא יתקע
        return {"image_url": "https://pollinations.ai/p/science?width=1024", "keyword": "science", "error": str(e)}
