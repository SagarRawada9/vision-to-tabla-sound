import random  # <--- CRITICAL IMPORT

def map_features_to_music(features, user_preferences=None):
    # Safety: Ensure features is a dict
    if not features or not isinstance(features, dict):
        features = {"emotional_tone": "calm", "energy_level": 0.5}

    mood = features.get("emotional_tone", "calm")
    # Safety: Ensure mood is a string before .lower()
    if not isinstance(mood, str): mood = "calm"
    mood = mood.lower()

    energy = features.get("energy_level", 0.5)

    taal_map = {
        "calm": ["rupak", "ektal", "deepchandi"],
        "devotional": ["bhajani", "dadra", "rupak"],
        "energetic": ["teentaal", "jhaptal", "kaherva"],
        "joyful": ["dadra", "kaherva", "teentaal"],
        "intense": ["rudra", "teentaal", "jhaptal"],
        "melancholic": ["rupak", "deepchandi"],
        "mysterious": ["rudra", "rupak"]
    }

    possible_taals = taal_map.get(mood, ["teentaal"])
    selected_taal = random.choice(possible_taals)

    # --- Instrument Logic ---
    ai_instruments = ["tabla"]
    
    # Flute Logic
    if mood in ["calm", "devotional", "melancholic", "joyful"] or energy < 0.6:
         if random.random() < 0.8:
             ai_instruments.append("flute")

    # Sitar Logic (Increased probability)
    if mood in ["devotional", "joyful", "energetic", "intense", "mysterious"]:
        if random.random() < 0.85:
             ai_instruments.append("sitar")
    elif mood == "calm" and energy > 0.3:
         if random.random() < 0.5:
             ai_instruments.append("sitar")

    # Ensure diversity
    if len(ai_instruments) == 1:
         ai_instruments.append(random.choice(["sitar", "flute"]))

    ai_instruments = list(set(ai_instruments))

    # --- User Override ---
    final_instruments = ai_instruments
    if user_preferences and not user_preferences.get("auto_mode", True):
        manual_selection = user_preferences.get("instruments", [])
        if manual_selection:
            final_instruments = manual_selection
            # Force rhythm if missing
            if "tabla" not in final_instruments:
                 final_instruments.insert(0, "tabla")

    return {
        "taal": selected_taal,
        "instruments": final_instruments,
        "energy": energy,
        "mood": mood
    }