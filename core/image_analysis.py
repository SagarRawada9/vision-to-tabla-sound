import google.generativeai as genai
from PIL import Image
import json
import re
import os

# ==========================================
# ✅ YOUR API KEY IS NOW INSERTED BELOW
# ==========================================
API_KEY = "AIzaSyBjiyLWH2B5f6DPEdgmbxvzq5Na75fkl0s"

genai.configure(api_key=API_KEY)

def analyze_image_gemini(image_path):
    print(f"\n--- Analyzing: {image_path} ---")
    
    # List of models to try in order (Flash is fastest, Pro is most reliable)
    models_to_try = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro-vision"]
    
    for model_name in models_to_try:
        try:
            # print(f"Trying model: {model_name}") 
            model = genai.GenerativeModel(model_name)
            img = Image.open(image_path)
            
            prompt = """
            Analyze this image for a musical context.
            Return ONLY a raw JSON object (no markdown formatting) with these specific keys:
            - "emotional_tone": (Select one best fit: calm, devotional, energetic, intense, joyful, melancholic, mysterious)
            - "energy_level": (A float between 0.1 and 1.0)
            - "short_description": (A single, concise sentence describing the visual scene, max 15 words.)
            """

            response = model.generate_content([prompt, img])
            
            if not response.parts:
                continue # If blocked, try next model

            text = response.text
            # Clean markdown formatting if present
            text = re.sub(r"```json|```", "", text).strip()
            
            data = json.loads(text)
            print(f"✅ Success! Detected Mood: {data.get('emotional_tone')}")
            return data

        except Exception as e:
            # print(f"Mode {model_name} failed, trying next...")
            continue

    # If we get here, all models failed. Return fallback so app doesn't crash.
    print("❌ All AI models failed. Using fallback mode.")
    return default_features()

def default_features():
    return {
        "emotional_tone": "calm", 
        "energy_level": 0.5, 
        "short_description": "Visual analysis unavailable, playing atmospheric mix."
    }