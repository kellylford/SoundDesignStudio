# Sound Design Studio v2 - Quick Start Guide

## Installation (One-Time Setup)

1. **Activate your virtual environment**:
   ```bash
   .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   setup.bat
   ```

## Running the Application

**Double-click**: `run_studio_v2.bat`

Or from command line:
```bash
python sound_design_studio_v2.py
```

## Essential Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **Alt+P** | ▶️ Play sound |
| **Ctrl+S** | 💾 Save document |
| **Ctrl+L** | ➕ Add layer |
| **Left/Right** | 🔄 Navigate layers |
| **Enter** | ✏️ Edit layer |
| **Delete** | 🗑️ Remove layer |

## Workflow

1. **Name your sound** at the top
2. **Add layers** (each layer is one sound)
3. **Design each layer**:
   - Double-click the layer, or
   - Select and press Enter
4. **Set parameters**:
   - Frequency: Pitch (Hz)
   - Waveform: sine, square, sawtooth, triangle
   - Duration: Length in seconds
   - Volume: 0.0 to 1.0
   - ADSR: Shape the sound envelope
5. **Play** to hear the result (Alt+P)
6. **Save** your document (Ctrl+S)

## Playback Modes

- **Sequential**: Layers play one after another (great for sequences)
- **Simultaneous**: Layers play together (great for rich timbres)

## Tips

- Start with 1-2 layers and experiment
- Use sequential mode for sound effects with multiple stages
- Use simultaneous mode for complex musical tones
- Save often - your documents are in JSON format
- Press Alt+P frequently to hear your changes

## Building an Executable

Want to share your creation?

```bash
build.bat
```

Creates: `dist\SoundDesignStudio.exe`

## Need Help?

- Check **README_v2.md** for full documentation
- Open an issue on GitHub
- Menu → Help → About for version info

---

**Pro Tip**: Hold Shift while navigating to select multiple layers (future feature)
