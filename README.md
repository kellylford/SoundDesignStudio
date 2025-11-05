# Sound Design Studio

A multi-layer sound synthesis and design tool for creating custom audio effects and musical instruments.

## Overview

Sound Design Studio is a standalone Windows application with a document-based workflow supporting multi-layer sound composition. Create complex, professional-quality sounds by layering multiple synthesized elements.

📖 **[Full User Guide](USER_GUIDE.md)** - Complete documentation with tutorials and examples

## Key Features

## Key Features

### Multi-Layer Composition
- Create complex sounds by layering multiple synthesized sounds
- Two playback modes:
  - **Sequential**: Layers play one after another with optional overlap
  - **Simultaneous**: Layers play together (mixed)
- Navigate between layers with **Left/Right arrow keys**
- Cut, copy, paste, and reorder layers

### Sound Synthesis
- **Basic Waveforms**: Sine, square, sawtooth, triangle
- **ADSR Envelope**: Full attack, decay, sustain, release control
- **Harmonic Layering**: Octave, fifth, and sub-bass harmonics
- **Advanced Synthesis**: FM synthesis, noise generation with filtering
- **Effects**: LFO tremolo, echo/delay

### Preset Library
- **Preview Presets**: Browse and audition presets with auto-play navigation
- 40+ built-in presets organized by category:
  - Musical Instruments (Piano, Strings, Drums)
  - Sound Effects (Impacts, Transitions)
  - UI Sounds (Buttons, Notifications, Alerts)
  - Game Sounds (Power-ups, Weapons, Ambient)

### Professional Export
- **Export complete sounds** to standard WAV audio files
- **Export individual layers** for more control
- **44.1 kHz, 16-bit** professional quality
- **Use anywhere**: Games, apps, videos, websites, presentations
- See **[EXPORT_GUIDE.md](EXPORT_GUIDE.md)** for detailed integration examples

## Quick Start

### For End Users

Simply run **SoundDesignStudio.exe** - no installation required!

The executable is a complete, standalone application.

### For Developers

1. **Clone the repository**
2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:
   ```bash
   .venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   python sound_design_studio.py
   ```

## Documentation

- **[USER_GUIDE.md](USER_GUIDE.md)** - Complete user guide with tutorials
- **[EXPORT_GUIDE.md](EXPORT_GUIDE.md)** - Export and integration guide
- **[PRESET_REFERENCE.md](PRESET_REFERENCE.md)** - Complete preset library reference
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute quick start guide

## Basic Usage

### Creating a Sound

1. **Start with a new document** (opens by default as "Untitled Sound")
2. **Add layers** using the "Add Layer" button or Ctrl+L
3. **Design each layer**:
   - Select a layer and press Enter or click "Design"
   - Configure parameters in the design dialog
4. **Configure layer parameters**:
   - **Basic**: Frequency, waveform, duration, volume
   - **Envelope**: ADSR (Attack, Decay, Sustain, Release)
   - **Harmonics**: Octave, fifth, sub-bass components
   - **Advanced**: FM synthesis, noise, effects
5. **Preview presets**: Press Alt+R → Preview Presets to browse with auto-play
6. **Play your sound** with Alt+P or the Play button
7. **Save your document** (Ctrl+S)

For detailed instructions, see the **[USER_GUIDE.md](USER_GUIDE.md)**

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Alt+P** | Play all layers |
| **Alt+Shift+P** | Play focused layer only |
| **Alt+R** | Open Presets menu |
| **Ctrl+N** | New document |
| **Ctrl+O** | Open document |
| **Ctrl+S** | Save document |
| **Ctrl+Shift+S** | Save As |
| **Ctrl+E** | Export as WAV |
| **Ctrl+L** | Add new layer |
| **Ctrl+D** | Open designer |
| **Ctrl+X/C/V** | Cut/Copy/Paste layer |
| **Alt+Left/Right** | Move layer in sequence |
| **Delete** | Remove selected layer |
| **Left/Right Arrow** | Navigate between layers |
| **Up/Down Arrow** | Navigate within layer properties |
| **Enter** | Edit selected layer |

See **[USER_GUIDE.md](USER_GUIDE.md)** for complete keyboard shortcut reference.

### Navigating Layers

- Use **arrow keys** (Left/Right) to move between layers
- Press **Enter** to edit the selected layer
- Press **Delete** to remove a layer (minimum 1 required)

### Playback Modes

**Sequential Mode** (default):
- Layers play one after another in order
- Great for creating sound sequences or transitions

**Simultaneous Mode**:
- All layers play at the same time (mixed)
- Perfect for building complex timbres and rich sounds

### Saving and Loading

Sound documents are saved in JSON format (`.sds` or `.json`) with all layer configurations preserved.

**File format includes**:
- Document name and description
- Playback mode (sequential/simultaneous)
- All layer names and complete synthesis configurations

### Exporting Sounds

Your sounds can be exported as standard WAV audio files for use anywhere!

**Export Complete Sound** (Ctrl+E):
- Exports all layers according to playback mode
- Sequential: Layers concatenated into one file
- Simultaneous: Layers mixed together
- Use in games, apps, videos, websites, etc.

**Export Individual Layer**:
- Menu: File → Export Current Layer as WAV
- Export just the selected layer
- Useful for component sounds or remixing

**WAV File Specs**:
- Sample Rate: 44,100 Hz (CD quality)
- Bit Depth: 16-bit PCM
- Format: Uncompressed WAV
- Compatible with: Everything!

**See EXPORT_GUIDE.md** for:
- Integration examples (Python, JavaScript, Unity, etc.)
- Usage in sports apps, games, web, mobile
- Converting to MP3/OGG if needed
- Workflow examples and best practices
- All layer names and complete synthesis configurations

## Building an Executable

To distribute your application as a standalone `.exe` file:

1. **Ensure your virtual environment is activated**
2. **Run the build script**:
   ```bash
   build.bat
   ```
3. **Find your executable** in `dist\SoundDesignStudio.exe`

The executable can be distributed to users who don't have Python installed!

### Build Requirements

The build process uses PyInstaller to create a single executable file. All dependencies are included:
- PyQt6 GUI framework
- NumPy for audio processing
- SoundDevice for audio playback
- SciPy for advanced signal processing

## Technical Details

### Dependencies

- **Python 3.10+**
- **PyQt6** - Modern GUI framework
- **NumPy** - Audio processing
- **SoundDevice** - Audio playback
- **SciPy** - Signal processing
- **PyInstaller** - Executable builder (for development)

See `requirements.txt` for exact versions.

### Building from Source

To create a standalone executable:

1. **Activate your virtual environment**
2. **Run the build script**:
   ```bash
   build.bat
   ```
3. **Find the executable** in `dist\SoundDesignStudio.exe`

The build uses PyInstaller to bundle all dependencies into a single `.exe` file.

## License

See LICENSE file for details.

## Support

For questions, issues, or feature requests, please open an issue on GitHub.

**Documentation:**
- [User Guide](USER_GUIDE.md) - Complete usage guide
- [Export Guide](EXPORT_GUIDE.md) - Integration examples
- [Preset Reference](PRESET_REFERENCE.md) - All built-in presets
- [Quick Start](QUICKSTART.md) - Get started in 5 minutes

### v1.0
- Single-sound preset system
- Tabbed parameter interface
- Preset library management
- Export/import capabilities
