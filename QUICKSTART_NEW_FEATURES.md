# Quick Start: New Features

## Installation (5 minutes)

### 1. Install Python Packages
```bash
pip install pedalboard pyfluidsynth
```

### 2. Install FluidSynth (for SoundFont)

**Windows:**
- Download: https://github.com/FluidSynth/fluidsynth/releases
- Extract and add to PATH or copy DLL to app folder

**macOS:**
```bash
brew install fluid-synth
```

**Linux:**
```bash
sudo apt-get install fluidsynth
```

### 3. Get a SoundFont (Optional)
- Download GeneralUser GS: https://schristiancollins.com/generaluser.php
- Or use FluidR3_GM (often included with FluidSynth)

### 4. Test
```bash
python test_new_features.py
```

## Quick Examples

### Add Reverb to Any Sound
```python
layer.config['effects'] = {
    'enabled': True,
    'reverb_enabled': True,
    'reverb_room_size': 0.7,  # 0.0-1.0
    'reverb_wet_level': 0.4    # Amount of reverb
}
```

### Use Piano SoundFont
```python
layer.config['soundfont'] = {
    'enabled': True,
    'soundfont_path': 'path/to/GeneralUser.sf2',
    'program': 0,  # 0 = Acoustic Grand Piano
    'velocity': 100  # Loudness (0-127)
}
```

### Combine Both
```python
# Realistic piano with concert hall reverb
layer.config['soundfont']['enabled'] = True
layer.config['effects']['enabled'] = True
layer.config['effects']['reverb_enabled'] = True
layer.config['effects']['reverb_room_size'] = 0.8
```

## What You Get

**Before:** Synthesized beeps and boops  
**After:** Professional studio-quality sounds with realistic instruments

**Available Effects:**
- Reverb (room simulation)
- Delay (echoes)
- Distortion (grit)
- Chorus (width)
- Phaser (movement)
- Compressor (punch)
- Filters (tone shaping)

**Available Instruments (via SoundFont):**
- Piano, Organ, Guitar
- Strings, Brass, Woodwinds
- Drums, Percussion
- Synths, Sound Effects
- And hundreds more...

## Documentation

- **Full Details:** `NEW_FEATURES.md`
- **Installation Help:** `INSTALLATION_NEW_FEATURES.md`
- **Test Script:** `python test_new_features.py`

## Notes

- Works without installation (features disabled gracefully)
- 100% backward compatible
- No UI changes yet (coming soon)
- Effects and SoundFont accessible via code/presets

---

Transform your synthesizer into a full production studio!
