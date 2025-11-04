# Sound Design Studio - User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Interface Overview](#interface-overview)
4. [Working with Layers](#working-with-layers)
5. [Sound Design](#sound-design)
6. [Playback Modes](#playback-modes)
7. [Presets](#presets)
8. [Exporting](#exporting)
9. [Keyboard Shortcuts](#keyboard-shortcuts)
10. [Tips & Tricks](#tips--tricks)

---

## Introduction

Sound Design Studio is a professional multi-layer sound synthesis application that lets you create complex sounds by combining multiple layers. Whether you're designing sound effects for games, creating musical instruments, or experimenting with audio synthesis, this tool provides a flexible and intuitive workflow.

### Key Concepts

- **Document**: A sound project containing one or more layers
- **Layer**: A single sound element with its own parameters
- **Sequential Mode**: Layers play one after another
- **Simultaneous Mode**: Layers play mixed together at the same time

---

## Getting Started

### Installation

Simply run **SoundDesignStudio.exe** to launch the application. No Python installation or setup required!

The executable is a complete, standalone application that includes all necessary dependencies.

### First Steps

1. **Double-click** SoundDesignStudio.exe to launch
2. You'll see a single default layer ready to design
3. The layer list on the right shows all properties of the current layer
4. Press **Enter** or click **Design** to open the sound designer
5. Press **Alt+P** to play your sound

---

## Interface Overview

### Main Window Components

```
┌─────────────────────────────────────────────────┐
│  File  Edit  Design  Presets  Help              │
├─────────────────────────────────────────────────┤
│  Sound Information                              │
│  Name: [Untitled Sound____________]             │
│  Description: [________________]                │
│  Playback Mode: [Sequential ▼]                  │
├─────────────────────────────────────────────────┤
│  Layer Properties               │               │
│  ═══ Layer 1/1: Layer 1 ═══    │   [Play]      │
│    Frequency: 440.0 Hz          │   [Design]    │
│    Waveform: sine               │   [Add Layer] │
│    Duration: 0.50 s             │               │
│    Volume: 0.30                 │               │
│    Attack: 0.010 s              │               │
│    ...                          │               │
└─────────────────────────────────────────────────┘
```

### Layer Property View

The layer list displays all properties of the **currently selected layer**:
- **Header**: Shows layer number, total layers, and layer name
- **Basic Parameters**: Frequency, waveform, duration, volume, overlap
- **ADSR Envelope**: Attack, Decay, Sustain, Release values
- **Harmonics**: Status and harmonic volumes (if enabled)
- **Advanced Synthesis**: Type and status (if enabled)

---

## Working with Layers

### Navigation

- **Left/Right Arrows**: Switch between layers (moves to top of new layer's list)
- **Up/Down Arrows**: Navigate through properties of current layer
- **Enter**: Open design dialog for current layer
- **Delete**: Remove current layer (with confirmation)

### Adding Layers

1. Click **"Add Layer"** button or press **Ctrl+L**
2. New layers start **blank** (volume = 0, minimal settings)
3. The first/default layer has preset values

### Managing Layers

#### Cut, Copy, Paste
- **Ctrl+X**: Cut current layer to clipboard
- **Ctrl+C**: Copy current layer to clipboard
- **Ctrl+V**: Paste layer after current position

#### Moving Layers
- **Alt+Left**: Move layer earlier in sequence (swap with previous)
- **Alt+Right**: Move layer later in sequence (swap with next)
- Also available in **Edit** menu

#### Clearing a Layer
- **Design → Clear Current Layer Values**
- Resets all parameters to blank/zero values
- Keeps the layer and its name

#### Removing a Layer
- Press **Delete** or use **Edit → Delete Layer**
- Requires confirmation
- Cannot delete the last layer (must have at least one)

---

## Sound Design

### Opening the Designer

1. Select a layer (Left/Right arrows)
2. Press **Enter** or click **"Design"** button
3. Or use **Design → Open Designer** (Ctrl+D)

### Design Dialog Tabs

#### 1. Basic Tab

**Frequency**: 20-2000 Hz
- The pitch/tone of the sound
- Lower = deeper, Higher = brighter

**Waveform**: sine, square, sawtooth, triangle
- Determines the harmonic content and timbre
- Sine = pure tone, Square = hollow, Sawtooth = bright, Triangle = mellow

**Duration**: 0.1-3.0 seconds
- How long the sound lasts

**Volume**: 0.0-1.0
- Overall loudness (0 = silent, 1 = maximum)

**Sequential Overlap**: 0-2 seconds
- In Sequential mode, how much this layer overlaps with the previous one
- Positive values create smooth transitions

#### 2. Envelope Tab

**ADSR Envelope** shapes how the sound evolves over time:

- **Attack (0-1s)**: How quickly sound reaches full volume from start
  - 0 = instant, higher = gradual fade-in
  
- **Decay (0-1s)**: Time to drop from peak to sustain level
  - Creates initial "punch" before settling
  
- **Sustain (0-1)**: Level maintained while sound plays
  - 1 = full volume, 0 = silence
  
- **Release (0-1s)**: Fade-out time after sound ends
  - 0 = abrupt stop, higher = gradual fade-out

**Example Presets:**
- Pluck: Attack=0.001, Decay=0.2, Sustain=0.1, Release=0.1
- Pad: Attack=0.3, Decay=0.2, Sustain=0.7, Release=0.5
- Percussion: Attack=0.001, Decay=0.1, Sustain=0.0, Release=0.05

#### 3. Harmonics Tab

Add richness and complexity by mixing in related frequencies:

**Enable Harmonics**: Turn on/off harmonic overtones

- **Octave (2x frequency)**: Adds brightness and clarity (0-1)
- **Fifth (1.5x frequency)**: Adds warmth and musicality (0-1)
- **Sub-bass (0.5x frequency)**: Adds depth and power (0-1)

**Use Cases:**
- Musical instruments: Enable with moderate octave/fifth
- Deep bass: High sub-bass, low octave
- Bright effects: High octave, moderate fifth

#### 4. Advanced Tab

**Enable Advanced Synthesis**: Unlock additional synthesis techniques

**Synthesis Type**: fm, noise, karplus-strong
- **FM (Frequency Modulation)**: Complex harmonic tones
- **Noise**: White, pink, or brown noise generation
- **Karplus-Strong**: String/pluck simulation

**FM Synthesis:**
- Modulation Ratio: Frequency relationship (0.1-10.0)
- Modulation Index: Intensity of modulation (0-20)

**Noise Generation:**
- Noise Type: white, pink, brown
- Filter: Bandpass, lowpass, highpass
- Cutoff: Frequency range (20-20000 Hz)

**Effects:**
- **LFO**: Low-frequency oscillator for vibrato/tremolo
  - Frequency: Speed of modulation (0.1-20 Hz)
  - Depth: Intensity (0-100%)
  
- **Echo**: Delay effect
  - Delay: Time before repeat (0-2s)
  - Feedback: Number of repeats (0-100%)

---

## Playback Modes

### Sequential Mode

Layers play **one after another** in order:
```
Layer 1 ──────▶ Layer 2 ──────▶ Layer 3 ──────▶
```

**Use Cases:**
- Sound effects with distinct stages (wind-up → impact → decay)
- Musical phrases
- Narrative sound design

**Overlap Feature:**
- Set positive overlap values to create smooth transitions
- Example: Layer 2 with 0.2s overlap starts 0.2s before Layer 1 ends

### Simultaneous Mode

All layers play **mixed together** at the same time:
```
Layer 1 ────────────────▶
Layer 2 ────────────────▶  } Mixed together
Layer 3 ────────────────▶
```

**Use Cases:**
- Rich, complex tones (fundamental + harmonics + texture)
- Layered instruments (piano with shimmer)
- Thick sound effects (multiple frequencies at once)

**Mixing:**
- Layers are automatically averaged to prevent clipping
- Adjust individual layer volumes for proper balance

### Switching Modes

Change in **Sound Information** section:
- Sequential: Dropdown → "Sequential"
- Simultaneous: Dropdown → "Simultaneous"

---

## Presets

### Preview Presets (Recommended)

The **Preview Presets** dialog is the best way to explore and audition presets:

1. Press **Alt+R** and select **Preview Presets...** (or select from menu)
2. A dialog opens showing all available presets organized by category
3. Use **Up/Down arrow keys** to navigate through presets
4. Each preset **plays automatically** as you select it - no clicking needed!
5. Review preset information at the bottom (layers, playback mode, category)
6. Click **"Use Preset"** button to add the selected preset to your sound
7. Click **"Close"** or press **Escape** to exit without adding

**Benefits:**
- 🎵 Hear presets before adding them
- ⌨️ Fast keyboard navigation
- 📋 See all presets at once
- 🔊 Instant audio preview

### Quick Add from Menu

For faster workflow when you know what you want:

1. Press **Alt+R** or open **Presets** menu
2. Navigate categories:
   - Musical Instruments (Piano & Keys, Strings, Drums & Percussion)
   - Sound Effects (Impacts, Transitions)
   - User Interface (Buttons, Notifications, Alerts)
   - Game Sounds (Power-ups, Weapons, Ambient)
3. Click a preset name to **add** its layers to your document immediately

**Important:** Presets **ADD** layers, they don't replace existing ones!

### Preset Categories

#### Musical Instruments
- **Electric Piano**: Fundamental + Brightness layers
- **Bell**: Strike + Shimmer with long decay
- **Organ**: Base + Octave + Fifth harmonics
- **Violin**: Bow + Air layers
- **Cello**: Low String + Resonance
- **Kick Drum**: Thump + Click (sequential)
- **Snare Hit**: Body + Snap
- **Hi-Hat**: High + Mid frequencies

#### Sound Effects
- **Heavy Impact**: Boom + Crack
- **Metal Clang**: Strike + Ring with harmonics
- **Whoosh**: Air + Wind transition
- **Sweep Up/Down**: Frequency sweeps

#### User Interface
- **Button Click**: Compact, precise
- **Success Chime**: Bright, positive
- **Error Beep**: Attention-grabbing

#### Game Sounds
- **Power-Up**: Rising, magical
- **Laser Shot**: Sci-fi weapon
- **Coin Collect**: Reward sound

---

## Exporting

### Export Complete Sound

**File → Export as WAV** (Ctrl+E)

1. Choose save location and filename
2. Exports based on current playback mode:
   - **Sequential**: All layers concatenated (with overlaps)
   - **Simultaneous**: All layers mixed together
3. Output: 44.1kHz, 16-bit PCM WAV file

### Export Single Layer

**File → Export Current Layer as WAV**

1. Exports only the currently selected layer
2. Useful for creating individual sound elements
3. Same format: 44.1kHz, 16-bit PCM

### Using Exported Sounds

WAV files can be used in:
- Game engines (Unity, Unreal, Godot)
- Audio editing software (Audacity, Reaper)
- Video editors
- Presentation software
- Any application that supports WAV format

See **EXPORT_GUIDE.md** for detailed integration instructions.

---

## Keyboard Shortcuts

### Global Shortcuts

| Shortcut | Action |
|----------|--------|
| **Alt+P** | Play all layers (respects playback mode) |
| **Alt+Shift+P** | Play focused layer only |
| **Alt+R** | Open Presets menu |
| **Ctrl+E** | Export as WAV |

### File Operations

| Shortcut | Action |
|----------|--------|
| **Ctrl+N** | New sound document |
| **Ctrl+S** | Save document |
| **Ctrl+Shift+S** | Save document as... |
| **Ctrl+O** | Open document |

### Layer Navigation

| Shortcut | Action |
|----------|--------|
| **Left Arrow** | Previous layer (goes to top of list) |
| **Right Arrow** | Next layer (goes to top of list) |
| **Up Arrow** | Previous property in list |
| **Down Arrow** | Next property in list |
| **Enter** | Open design dialog |
| **Delete** | Remove current layer |

### Layer Management

| Shortcut | Action |
|----------|--------|
| **Ctrl+X** | Cut layer |
| **Ctrl+C** | Copy layer |
| **Ctrl+V** | Paste layer |
| **Alt+Left** | Move layer earlier (swap with previous) |
| **Alt+Right** | Move layer later (swap with next) |
| **Ctrl+L** | Add new blank layer |

### Design Dialog

| Shortcut | Action |
|----------|--------|
| **Ctrl+D** | Open designer |
| **Tab** | Navigate between fields |
| **Space** | Play preview in dialog |

---

## Tips & Tricks

### Creating Rich Sounds

1. **Start with a foundation layer**:
   - Set the base frequency and waveform
   - Adjust ADSR for desired character

2. **Add harmonic layers**:
   - Copy the foundation (Ctrl+C, Ctrl+V)
   - Adjust frequency (2x for octave, 1.5x for fifth)
   - Lower volume (0.2-0.3)
   - Use simultaneous mode

3. **Add texture**:
   - Create a noise layer with low volume
   - Use bandpass filter to match frequency range

### Sound Effect Design

**Impact Sound (Sequential):**
1. Layer 1: Low frequency sine (60Hz), short attack, medium decay
2. Layer 2: High frequency square (800Hz), instant attack, short duration
3. Result: Deep "boom" followed by sharp "crack"

**UI Button (Simultaneous):**
1. Layer 1: 800Hz sine, instant attack, short release
2. Layer 2: 1600Hz triangle, instant attack, shorter duration
3. Result: Crisp click with harmonic richness

**Whoosh/Transition (Sequential with overlap):**
1. Layer 1: Sweep from 200Hz to 800Hz over 0.5s
2. Layer 2: Sweep from 400Hz to 1200Hz, 0.2s overlap
3. Result: Smooth accelerating whoosh

### Workflow Tips

- **Browse presets first**: Use Preview Presets (Alt+R) to audition sounds before building from scratch
- **Use presets as starting points**: Load a preset, then modify layers to customize
- **Name your layers descriptively**: "Bass", "Click", "Shimmer" etc.
- **Test frequently**: Press Alt+P often to hear changes
- **Save variations**: Use "Save As" to keep multiple versions
- **Export individual layers**: Create a library of reusable elements

### Performance

- **Blank layers are silent**: Set volume to 0 or use blank layers as placeholders
- **Limit layer count**: More layers = more processing (typically 2-5 is ideal)
- **Export for final quality**: Exported WAV files play anywhere without processing

### Troubleshooting

**No sound playing:**
- Check layer volume is > 0
- Verify ADSR envelope (sustain > 0, attack not too high)
- Ensure system audio is working

**Sound is distorted:**
- Lower individual layer volumes
- Reduce number of simultaneous layers
- Check for extreme ADSR values

**Can't delete layer:**
- Need at least one layer in document
- Use "Clear Layer Values" instead to reset

**Preset adds too many layers:**
- Presets ADD layers, they don't replace
- Delete unwanted layers with Delete key
- Use "New Document" (Ctrl+N) to start fresh

---

## File Formats

### Sound Document (.sds)

Custom JSON-based format containing:
- Document name and description
- Playback mode
- All layer configurations
- Complete parameter state

**Location**: Save anywhere, recommended to create a projects folder

### WAV Export

Standard uncompressed audio:
- Sample Rate: 44,100 Hz
- Bit Depth: 16-bit PCM
- Channels: Mono
- Compatible with all audio software

---

## Advanced Topics

### Understanding ADSR

The ADSR envelope is crucial for realistic sounds:

**Natural Instruments:**
- Piano: Very short attack, medium decay, low sustain, medium release
- String: Medium attack, short decay, high sustain, medium release
- Brass: Short attack, very short decay, high sustain, short release

**Synthetic Sounds:**
- Laser: Instant attack, no decay, full sustain, instant release
- Pad: Long attack, medium decay, medium sustain, long release
- Pluck: Instant attack, medium decay, no sustain, short release

### Layer Order Matters (Sequential Mode)

In sequential mode, layer order defines the sound's narrative:
1. **Build-up** (optional): Rising frequency/volume
2. **Impact**: Main sound event
3. **Decay/Tail**: Sound fading out

Use Alt+Left/Alt+Right to reorder layers quickly.

### Harmonic Theory

Musical intervals work well for layering:
- **Octave (2:1)**: Same note, higher register
- **Perfect Fifth (3:2)**: Harmonious, adds warmth
- **Perfect Fourth (4:3)**: Complements fifth
- **Major Third (5:4)**: Adds brightness

Calculate frequencies:
- Octave up: frequency × 2
- Fifth up: frequency × 1.5
- Fourth up: frequency × 1.33

---

## Support & Resources

### Additional Documentation

- **EXPORT_GUIDE.md**: Detailed export and integration instructions
- **PRESET_REFERENCE.md**: Complete preset library reference
- **QUICKSTART.md**: Quick 5-minute introduction

### Getting Help

If you encounter issues:
1. Check this user guide
2. Review error messages in the status bar
3. Check sound_design_debug.log (located next to the .exe) for detailed errors
4. Try restarting the application

### Best Practices

1. **Save often**: Use Ctrl+S regularly
2. **Name things well**: Clear layer and document names
3. **Start simple**: Begin with 1-2 layers, add complexity gradually
4. **Experiment**: Try different combinations and parameters
5. **Export variations**: Keep multiple versions of sounds

---

## Appendix: Parameter Ranges

| Parameter | Min | Max | Default | Unit |
|-----------|-----|-----|---------|------|
| Frequency | 20 | 2000 | 440 | Hz |
| Duration | 0.1 | 3.0 | 0.5 | seconds |
| Volume | 0.0 | 1.0 | 0.3 | ratio |
| Attack | 0.0 | 1.0 | 0.01 | seconds |
| Decay | 0.0 | 1.0 | 0.1 | seconds |
| Sustain | 0.0 | 1.0 | 0.7 | ratio |
| Release | 0.0 | 1.0 | 0.15 | seconds |
| Overlap | 0.0 | 2.0 | 0.0 | seconds |
| Harmonics | 0.0 | 1.0 | varies | ratio |
| FM Ratio | 0.1 | 10.0 | 1.4 | ratio |
| FM Index | 0.0 | 20.0 | 5.0 | depth |
| Filter Freq | 20 | 20000 | varies | Hz |
| LFO Freq | 0.1 | 20.0 | 5.0 | Hz |
| LFO Depth | 0 | 100 | 30 | percent |
| Echo Delay | 0.0 | 2.0 | 0.3 | seconds |
| Echo Feedback | 0 | 100 | 40 | percent |

---

**Version**: 1.0
**Last Updated**: November 2025

*Happy sound designing!* 🎵
