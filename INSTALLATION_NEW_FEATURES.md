# Sound Design Studio - Installation Guide for New Features

This guide explains how to install and set up the new audio effects and SoundFont features.

## New Features Overview

### 1. Professional Audio Effects (via Pedalboard)
- **Reverb**: Add spaciousness and depth
- **Delay**: Create echoes and rhythmic effects
- **Distortion**: Add harmonic saturation and grit
- **Chorus**: Thicken and widen sounds
- **Phaser**: Sweeping phase effects
- **Compressor**: Dynamic range control
- **Filters**: High-pass and low-pass filtering
- **Limiter**: Prevent clipping

### 2. SoundFont Support (via FluidSynth)
- Load `.sf2` SoundFont files for realistic instruments
- Access thousands of instrument sounds
- Piano, strings, brass, drums, and more
- Use frequency or MIDI note input

## Installation Instructions

### Step 1: Install Python Dependencies

Open a terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- `pedalboard` - Spotify's professional audio effects library
- `pyfluidsynth` - SoundFont player

### Step 2: Install FluidSynth (Required for SoundFont)

#### Windows:
1. Download FluidSynth from: https://github.com/FluidSynth/fluidsynth/releases
2. Extract to a folder (e.g., `C:\Program Files\FluidSynth`)
3. Add the `bin` folder to your PATH environment variable
   - Or copy `libfluidsynth-3.dll` to the same folder as the executable

#### macOS:
```bash
brew install fluid-synth
```

#### Linux:
```bash
sudo apt-get install fluidsynth libfluidsynth-dev  # Ubuntu/Debian
# OR
sudo dnf install fluidsynth fluidsynth-devel      # Fedora
```

### Step 3: Get SoundFont Files (Optional)

To use SoundFont features, you need `.sf2` files. Here are some free options:

**Recommended SoundFonts:**
1. **GeneralUser GS** (35MB) - Excellent all-around soundfont
   - Download: https://schristiancollins.com/generaluser.php

2. **FluidR3_GM** (148MB) - High quality, included with FluidSynth
   - Often found in: `/usr/share/sounds/sf2/` (Linux) or FluidSynth installation folder

3. **Timbres of Heaven** (369MB) - Very comprehensive
   - Download: http://www.timbres-of-heaven.com/

**Where to place SoundFonts:**
- Create a `soundfonts` folder in the application directory
- Or choose any location and select it in the app

## Testing the Installation

### Test Audio Effects:

```python
from audio_effects import AudioEffectsProcessor
import numpy as np

# Check if pedalboard is available
processor = AudioEffectsProcessor()
print(f"Pedalboard available: {processor.enabled}")

# Test applying reverb
if processor.enabled:
    audio = np.random.randn(44100).astype(np.float32)  # 1 second of noise
    effects_config = processor.get_default_effects_config()
    effects_config['enabled'] = True
    effects_config['reverb_enabled'] = True
    processed = processor.apply_effects(audio, effects_config)
    print("Effects working!")
```

### Test SoundFont:

```python
from soundfont_player import SoundFontPlayer

# Check if fluidsynth is available
player = SoundFontPlayer()
print(f"FluidSynth available: {player.enabled}")

# Test loading a soundfont
if player.enabled:
    success = player.load_soundfont('path/to/your/soundfont.sf2')
    print(f"SoundFont loaded: {success}")
    
    if success:
        # Generate middle C for 1 second
        audio = player.generate_note(midi_note=60, velocity=100, duration=1.0)
        print(f"Generated audio: {len(audio)} samples")
```

## Using the New Features

### In the Application

The application will automatically detect if the new features are available. If not installed:
- Effects will be silently disabled (synthesis still works)
- SoundFont will be disabled (synthesis still works)

### New UI Elements (Coming Soon)

Two new tabs will be added to the Layer Designer:
1. **Effects Tab**: Configure reverb, delay, distortion, etc.
2. **SoundFont Tab**: Select instrument and configure settings

## Troubleshooting

### "pedalboard" not found
```bash
pip install pedalboard
```
Note: Requires a C++ compiler on some platforms

### "fluidsynth" not found
- **Windows**: Make sure `libfluidsynth-3.dll` is in PATH or application folder
- **macOS/Linux**: Install system FluidSynth package (see Step 2)
- **Python binding**: `pip install pyfluidsynth`

### SoundFont doesn't load
- Check file path is correct
- Ensure `.sf2` file is valid
- Try a different SoundFont file

### Audio quality issues
- Check sample rate matches (44100 Hz default)
- Reduce effects intensity if distorted
- Enable the Limiter effect (on by default)

## Building Executable with New Features

When building with PyInstaller, the `.spec` file needs to include:
- FluidSynth DLL (Windows)
- SoundFont files (if bundling)

Update `sound_design_studio.spec`:

```python
a = Analysis(
    ...
    binaries=[
        ('C:/path/to/libfluidsynth-3.dll', '.'),  # Windows only
    ],
    datas=[
        ('soundfonts/*.sf2', 'soundfonts'),  # If bundling soundfonts
        ...
    ],
    ...
)
```

## Performance Notes

- **Effects Processing**: Adds 10-50ms latency depending on effect chain
- **SoundFont Loading**: First load takes 1-5 seconds, then instant playback
- **Memory**: SoundFonts use 35-500MB RAM depending on size
- **CPU**: Effects use 5-20% CPU per layer on modern processors

## Additional Resources

- **Pedalboard Documentation**: https://spotify.github.io/pedalboard/
- **FluidSynth Manual**: https://www.fluidsynth.org/
- **SoundFont Specifications**: https://en.wikipedia.org/wiki/SoundFont
- **Free SoundFont Collections**: https://musescore.org/en/handbook/soundfonts

## Backward Compatibility

- Old sound files will work perfectly (effects/soundfont default to disabled)
- New fields are optional in the configuration
- Application degrades gracefully if libraries aren't installed

## Next Steps

Once installed, you can:
1. Add reverb to make sounds more spacious
2. Use delay for rhythmic effects
3. Load piano SoundFonts for realistic piano sounds
4. Combine synthesis with effects for unique timbres
5. Export enhanced sounds for use in other applications

---

For questions or issues, please check the main README.md or open an issue on GitHub.
