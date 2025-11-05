# New Features: Professional Audio Effects & SoundFont Support

This document describes the major new features added to Sound Design Studio.

## Overview

Two powerful features have been added to dramatically expand sound capabilities:

1. **Professional Audio Effects** (via Spotify's Pedalboard library)
2. **SoundFont Support** (via FluidSynth for realistic instruments)

## 1. Professional Audio Effects

### What is it?
Uses Spotify's `pedalboard` library - the same effects used in professional audio production.

### Available Effects:

| Effect | Description | Use Cases |
|--------|-------------|-----------|
| **Reverb** | Adds spaciousness and ambience | Make sounds feel like they're in a room/hall |
| **Delay** | Time-based echoes | Rhythmic effects, spaciousness |
| **Distortion** | Harmonic saturation | Aggressive sounds, warmth |
| **Chorus** | Thickens and widens | Richer strings, lush pads |
| **Phaser** | Sweeping phase shifts | Psychedelic effects, movement |
| **Compressor** | Controls dynamic range | Even out volumes, punch |
| **High-pass Filter** | Removes low frequencies | Clean up muddy sounds |
| **Low-pass Filter** | Removes high frequencies | Warmth, darkness |
| **Limiter** | Prevents clipping | Protection, loudness |

### How to Use:
```python
config = PlayAudioConfig()
config.effects = {
    'enabled': True,
    'reverb_enabled': True,
    'reverb_room_size': 0.7,  # Bigger room
    'reverb_wet_level': 0.4,  # More reverb
    'delay_enabled': True,
    'delay_time': 0.5,  # Half-second delay
    'delay_feedback': 0.4,  # Number of repeats
}
```

### Parameters:

**Reverb:**
- `room_size`: 0.0-1.0 (small to large room)
- `damping`: 0.0-1.0 (bright to dark)
- `wet_level`: 0.0-1.0 (effect amount)
- `dry_level`: 0.0-1.0 (original signal)

**Delay:**
- `delay_time`: 0.0-2.0 seconds
- `delay_feedback`: 0.0-1.0 (number of repeats)
- `delay_mix`: 0.0-1.0 (dry/wet blend)

**Distortion:**
- `distortion_drive`: 0-50 dB (amount of drive)

**Chorus:**
- `chorus_rate`: 0.1-10.0 Hz (modulation speed)
- `chorus_depth`: 0.0-1.0 (modulation intensity)
- `chorus_delay`: 1-50 ms (center delay time)
- `chorus_mix`: 0.0-1.0 (dry/wet blend)

**Compressor:**
- `compressor_threshold`: -60 to 0 dB (where compression starts)
- `compressor_ratio`: 1.0-20.0 (compression amount)
- `compressor_attack`: 0.1-100 ms (how fast it kicks in)
- `compressor_release`: 10-1000 ms (how fast it releases)

## 2. SoundFont Support

### What is it?
SoundFonts (.sf2 files) contain real recordings of instruments that can be played at any pitch. Used in professional MIDI production.

### Benefits:
- **Realistic Instruments**: Piano, strings, brass, drums, etc.
- **Huge Libraries**: Thousands of sounds in single files
- **Professional Quality**: Studio-grade samples
- **Free Available**: Many excellent free SoundFonts

### Recommended SoundFonts:

| Name | Size | Description | Source |
|------|------|-------------|--------|
| **GeneralUser GS** | 35 MB | Excellent all-around | schristiancollins.com/generaluser.php |
| **FluidR3_GM** | 148 MB | High quality GM set | Often included with FluidSynth |
| **Timbres of Heaven** | 369 MB | Very comprehensive | timbres-of-heaven.com |
| **Arachno** | 148 MB | Good balance | arachnosoft.com/main/soundfont.php |

### How to Use:
```python
config = PlayAudioConfig()
config.soundfont = {
    'enabled': True,
    'soundfont_path': 'path/to/soundfont.sf2',
    'use_frequency': True,  # Use layer frequency
    'program': 0,  # Instrument (0=Piano, 40=Violin, etc.)
    'velocity': 100,  # Loudness (0-127)
}
```

### MIDI Programs (Instruments):
- 0-7: Piano
- 8-15: Chromatic Percussion
- 16-23: Organ
- 24-31: Guitar
- 32-39: Bass
- 40-47: Strings
- 48-55: Ensemble
- 56-63: Brass
- 64-71: Reed
- 72-79: Pipe
- 80-87: Synth Lead
- 88-95: Synth Pad
- 96-103: Synth Effects
- 104-111: Ethnic
- 112-119: Percussive
- 120-127: Sound Effects

Full list: https://en.wikipedia.org/wiki/General_MIDI#Program_change_events

## Integration

### Both features work together:
1. Generate sound (synthesis OR SoundFont)
2. Apply effects (reverb, delay, etc.)
3. Mix with other layers
4. Export to WAV

### Example - Realistic Piano with Reverb:
```python
layer = SoundLayer("Grand Piano")
layer.config['soundfont'] = {
    'enabled': True,
    'soundfont_path': 'GeneralUser.sf2',
    'program': 0,  # Acoustic Grand Piano
    'velocity': 100
}
layer.config['effects'] = {
    'enabled': True,
    'reverb_enabled': True,
    'reverb_room_size': 0.8,  # Concert hall
    'reverb_wet_level': 0.3
}
```

### Example - Distorted Synth Bass:
```python
layer = SoundLayer("Distorted Bass")
layer.config['frequency'] = 110  # Low A
layer.config['wave_type'] = 'sawtooth'
layer.config['effects'] = {
    'enabled': True,
    'distortion_enabled': True,
    'distortion_drive': 15.0,
    'compressor_enabled': True,
    'compressor_threshold': -15.0,
    'compressor_ratio': 6.0
}
```

## Installation

See `INSTALLATION_NEW_FEATURES.md` for detailed installation instructions.

**Quick Start:**
```bash
# Install Python packages
pip install -r requirements.txt

# Install FluidSynth (for SoundFont)
# Windows: Download from GitHub releases
# macOS: brew install fluid-synth
# Linux: sudo apt-get install fluidsynth

# Test installation
python test_new_features.py
```

## Backward Compatibility

- **100% compatible** with existing sound files
- Effects and SoundFont are **disabled by default**
- App works perfectly even if libraries aren't installed
- Existing presets unchanged

## Performance

| Feature | CPU Usage | Memory | Latency |
|---------|-----------|--------|---------|
| Effects (per layer) | 5-20% | Minimal | 10-50ms |
| SoundFont loading | Low | 35-500MB | 1-5 sec (once) |
| SoundFont playback | Low | 0 (after load) | Real-time |

## Use Cases

### Before (Synthesis Only):
- ✓ Electronic/synthesized sounds
- ✓ Simple waveforms
- ✓ Basic envelopes
- ✗ Realistic instruments
- ✗ Professional effects

### After (With New Features):
- ✓ All synthesis capabilities
- ✓ **Realistic piano, strings, brass, drums**
- ✓ **Professional reverb and effects**
- ✓ **Studio-quality processing**
- ✓ **Hybrid synthesis + samples**

## Examples

### 1. Concert Piano
- SoundFont: Grand Piano
- Effects: Large reverb, slight compression

### 2. Epic String Pad
- SoundFont: String Ensemble
- Effects: Reverb + Chorus for width

### 3. Gritty Synth Lead
- Synthesis: Sawtooth wave with FM
- Effects: Distortion + Delay

### 4. Ambient Texture
- Synthesis: Multiple layers
- Effects: Heavy reverb + delay feedback

## Future Enhancements

Potential additions:
- More effects (EQ, flanger, ring mod)
- Multiple SoundFonts simultaneously
- Custom effect chains
- Effect automation/LFO
- VST plugin support
- Convolution reverb with custom impulse responses

## Resources

- **Pedalboard**: https://spotify.github.io/pedalboard/
- **FluidSynth**: https://www.fluidsynth.org/
- **Free SoundFonts**: https://musescore.org/en/handbook/soundfonts
- **MIDI Specifications**: https://www.midi.org/specifications

---

These features transform Sound Design Studio from a synthesis tool into a full-featured audio workstation!
