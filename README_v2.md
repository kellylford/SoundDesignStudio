# Sound Design Studio v2.0 - Document-Centric Edition

A professional sound synthesis and design tool with a document-based workflow supporting multi-layer sound composition.

## What's New in v2.0

### Document-Based Workflow
- Each sound is now a **document** that can contain multiple layers
- Sound documents can be saved, loaded, and shared
- Title bar shows the current document name (e.g., "Untitled Sound")

### Multi-Layer Composition
- Create complex sounds by layering multiple synthesized sounds
- Two playback modes:
  - **Sequential**: Layers play one after another
  - **Simultaneous**: Layers play together (mixed)
- Navigate between layers with **Left/Right arrow keys**

### Menu-Driven Interface
- **File Menu**: New, Open, Save, Save As operations
- **Design Menu**: 
  - Open Designer for detailed layer editing
  - Add New Layer (Ctrl+L)
  - Remove Layer (Delete)
  - Switch playback modes
- **Help Menu**: About and documentation

### Redesigned UI
- **List View**: Primary interface shows all sound layers
- Focus on the layer list for quick keyboard navigation
- **Play Button**: Easily accessible with Alt+P shortcut
- **Export Button**: Export to WAV with one click (Ctrl+E)
- **Design Dialog**: Opens the full synthesis interface when needed

### WAV Export
- **Export complete sounds** to standard WAV audio files
- **Export individual layers** for more control
- **44.1 kHz, 16-bit** professional quality
- **Use anywhere**: Games, apps, videos, websites, presentations
- See **EXPORT_GUIDE.md** for detailed integration examples

## Quick Start

### Installation

1. **Create a virtual environment** (if not already done):
   ```bash
   python -m venv .venv
   ```

2. **Activate the virtual environment**:
   ```bash
   .venv\Scripts\activate
   ```

3. **Run the setup script**:
   ```bash
   setup.bat
   ```
   
   This will install all required dependencies from `requirements.txt`.

### Running the Application

**Option 1 - Use the launcher** (recommended):
```bash
run_studio_v2.bat
```

**Option 2 - Run directly**:
```bash
python sound_design_studio_v2.py
```

## Usage Guide

### Creating a Sound

1. **Start with a new document** (opens by default as "Untitled Sound")
2. **Add layers** using the "➕ Add Layer" button or Design menu
3. **Design each layer**:
   - Double-click a layer to open the design dialog
   - Or select a layer and click "🎨 Design"
4. **Configure layer parameters**:
   - Basic: Frequency, waveform, duration, volume
   - Envelope: ADSR (Attack, Decay, Sustain, Release)
   - Harmonics: Octave, fifth, sub-bass components
   - Advanced: FM synthesis, noise, effects (coming soon)
5. **Play your sound** with Alt+P or the Play button
6. **Save your document** (Ctrl+S)

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Alt+P** | Play current sound |
| **Ctrl+N** | New document |
| **Ctrl+O** | Open document |
| **Ctrl+S** | Save document |
| **Ctrl+Shift+S** | Save As |
| **Ctrl+E** | Export as WAV |
| **Ctrl+L** | Add new layer |
| **Ctrl+D** | Open designer |
| **Delete** | Remove selected layer |
| **Left/Right Arrow** | Navigate between layers |
| **Enter** | Edit selected layer |

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

## Architecture

### Sound Document Structure

```
SoundDocument
├── name: "My Complex Sound"
├── description: "Layered bell with bass"
├── playback_mode: "sequential" or "simultaneous"
└── layers: [
    SoundLayer
    ├── name: "Bell Layer"
    └── config: {frequency, wave_type, envelope, harmonics, etc.}
    
    SoundLayer
    ├── name: "Bass Layer"
    └── config: {frequency, wave_type, envelope, harmonics, etc.}
]
```

### Design Dialog

The Design Dialog contains the full synthesis interface with tabs:
- **Basic**: Frequency, waveform, duration, volume
- **Envelope**: ADSR envelope shaping
- **Harmonics**: Harmonic layer controls
- **Advanced**: FM synthesis, noise, effects (future)

## File Structure

```
SoundDesignStudio/
├── sound_design_studio_v2.py  # New document-based main application
├── sound_design_studio.py      # Original preset-based application
├── advanced_synthesis.py        # Synthesis algorithms
├── sound_export_system.py       # Export/import utilities
├── export_dialog.py             # Export dialog
├── requirements.txt             # Python dependencies
├── sound_design_studio.spec     # PyInstaller build configuration
├── setup.bat                    # Installation script
├── build.bat                    # Build executable script
├── run_studio_v2.bat           # V2 launcher
└── run_studio.bat              # Original launcher
```

## Migration from v1

The original Sound Design Studio (v1) is still available as `sound_design_studio.py`. Both versions can coexist:

**V1 (Original)**: Preset-based workflow, single-sound focus
**V2 (New)**: Document-based workflow, multi-layer composition

Sound configurations from v1 presets can be manually copied into v2 layers through the design dialog.

## Dependencies

- **Python 3.8+**
- **PyQt6** - Modern GUI framework
- **NumPy** - Numerical processing
- **SoundDevice** - Audio playback
- **SoundFile** - Audio file operations
- **SciPy** - Signal processing
- **PyInstaller** - Executable builder

See `requirements.txt` for exact versions.

## Troubleshooting

### "Module not found" errors
- Make sure your virtual environment is activated
- Run `setup.bat` to install dependencies

### Audio not playing
- Check your system audio settings
- Ensure no other application is blocking audio
- Try adjusting the volume in the layer configuration

### Build fails
- Ensure PyInstaller is installed: `pip install pyinstaller`
- Check that all dependencies are installed
- Look for error messages in the console output

## Future Features

- [ ] Complete advanced synthesis tab in design dialog
- [ ] Waveform visualization
- [ ] Real-time audio preview during parameter adjustment
- [ ] Layer duplication and copying
- [ ] Undo/redo functionality
- [ ] Export to WAV/MP3 files
- [ ] Sound presets library
- [ ] Drag-and-drop layer reordering
- [ ] Layer volume mixing controls
- [ ] MIDI input support

## Contributing

This is an open-source project. Contributions welcome!

## License

See LICENSE file for details.

## Version History

### v2.0 (Current)
- Document-based workflow
- Multi-layer sound composition
- Menu bar interface
- Sequential and simultaneous playback
- Keyboard-driven navigation

### v1.0
- Single-sound preset system
- Tabbed parameter interface
- Preset library management
- Export/import capabilities
