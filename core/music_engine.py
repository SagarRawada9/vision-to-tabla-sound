import numpy as np
import soundfile as sf
from core.audio_loader import SR, get_tabla_clip, get_flute_clip, get_sitar_clip

GAIN = {
    "tabla": 0.8,
    "flute": 0.5,
    "sitar": 0.6
}

def overlay(mix, sound, start_idx):
    """Safely adds sound to mix handling array bounds"""
    remaining = len(mix) - start_idx
    if remaining <= 0: return
    
    # Crop sound if it's longer than remaining space
    valid_len = min(len(sound), remaining)
    mix[start_idx : start_idx + valid_len] += sound[:valid_len]

def build_music(config, output_path, duration):
    target_samples = int(SR * duration)
    mix = np.zeros(target_samples, dtype=np.float32)

    inst_list = config["instruments"]
    taal_name = config["taal"][0]

    # --- 1. RHYTHM LAYER (Loops) ---
    if "tabla" in inst_list:
        loop = get_tabla_clip(taal_name)
        if len(loop) > 0:
            # Create full loop track
            repeats = int(target_samples / len(loop)) + 2
            full_rhythm = np.tile(loop, repeats)[:target_samples]
            mix += full_rhythm * GAIN["tabla"]

    # --- 2. MELODY LAYERS (Sparse/Phrased) ---
    # We place melody clips at random intervals
    
    def add_melodic_layer(loader_func, gain, density=3):
        cursor = 0
        while cursor < target_samples:
            # Random gap between phrases based on 'energy'
            gap = int(SR * (random.uniform(2, 6) - (config["energy"] * 2)))
            cursor += gap
            
            if cursor >= target_samples: break
            
            clip = loader_func()
            overlay(mix, clip * gain, cursor)
            cursor += len(clip)

    import random # Import locally to ensure randomness per call

    if "flute" in inst_list:
        add_melodic_layer(get_flute_clip, GAIN["flute"])

    if "sitar" in inst_list:
        add_melodic_layer(get_sitar_clip, GAIN["sitar"])

    # --- 3. MASTERING ---
    # Normalize to prevent clipping
    peak = np.max(np.abs(mix))
    if peak > 0:
        mix = mix / peak * 0.9 # Headroom

    sf.write(output_path, mix, SR)
    return output_path