@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    user_text = data.get("text", "")
    context = data.get("context", "general") # קבלת ההקשר
    
    # הנחיה ל-Gemini לשלב בין הדיבור להקשר
    prompt = f"The lecture topic is: {context}. The speaker said: {user_text}. " \
             f"Summarize this into ONE English keyword for an image, maintaining the lecture's context."
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    keyword = response.text.strip().split()[0]
    
    image_url = f"https://pollinations.ai/p/{keyword}?width=1024&height=1024&model=flux"
    return {"image_url": image_url}
