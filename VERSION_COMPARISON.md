# Sound Design Studio - Version Comparison

## Which Version Should I Use?

### Version 1 (Original) - `sound_design_studio.py`
**Best for**: Quick sound experimentation, preset management

**Features**:
- Single sound focus
- Extensive preset library (22 built-in presets)
- Quick preset switching (number keys 1-9)
- A/B comparison testing
- Comprehensive parameter tabs always visible
- Export/import presets

**Use when**:
- You want to quickly try different sounds
- You're building a preset library
- You need to compare variations side-by-side
- You're learning synthesis basics

**Launch**: `run_studio.bat`

---

### Version 2 (Document-Based) - `sound_design_studio_v2.py`
**Best for**: Complex multi-layer compositions, sound design projects

**Features**:
- Document-based workflow (save/load projects)
- Multi-layer composition
- Sequential and simultaneous playback
- Clean list-focused interface
- Menu-driven operations
- Layer management
- File format: .sds (Sound Design Studio documents)

**Use when**:
- You're creating complex layered sounds
- You want to save complete sound projects
- You need to organize multiple sound variations
- You're working on a sound design project

**Launch**: `run_studio_v2.bat`

---

## Feature Comparison Table

| Feature | V1 (Preset-Based) | V2 (Document-Based) |
|---------|-------------------|---------------------|
| **Interface** | Tabs always visible | List-first, design on-demand |
| **Focus** | Single sound + presets | Multi-layer documents |
| **Save Format** | Presets (JSON array) | Documents (JSON with layers) |
| **Playback** | Single sound | Sequential or simultaneous |
| **Navigation** | Tab through controls | Arrow keys through layers |
| **Quick Access** | Number keys (1-9 presets) | Alt+P (play anywhere) |
| **Menu Bar** | No | Yes (File, Edit, Design, Help) |
| **File Operations** | Import/Export presets | New/Open/Save/Save As documents |
| **Complexity** | Medium | Higher |
| **Learning Curve** | Gentle | Moderate |
| **Best For** | Experimentation | Composition |

## Workflow Examples

### V1: Creating a Sound Effect Library
```
1. Adjust parameters in visible tabs
2. Press Alt+P to play
3. Like it? Save as preset (Ctrl+S)
4. Repeat for different variations
5. Export all presets to JSON
6. Use presets in other applications
```

### V2: Creating a Complex Game Sound
```
1. Create new document: "Enemy Hit Sound"
2. Add Layer 1: "Impact" (low frequency, short)
3. Add Layer 2: "Metal Ring" (high frequency, decay)
4. Add Layer 3: "Rumble" (sub-bass, long)
5. Set playback mode: Sequential
6. Press Alt+P to hear complete sound
7. Save document: enemy_hit.sds
8. Build variations: enemy_hit_v2.sds, etc.
```

## Migration Between Versions

### From V1 to V2
1. Open a preset in V1
2. Note all parameters
3. Open V2, create a new layer
4. Manually enter parameters in design dialog
5. Save as new document

### From V2 to V1
1. Open a document in V2
2. Select a layer, open designer
3. Note all parameters
4. Open V1, enter parameters
5. Save as preset

**Note**: Direct file conversion not currently supported. This is a manual process.

## When to Switch Versions

### Switch to V1 if:
- V2 feels too complex
- You just want to experiment quickly
- You prefer seeing all controls at once
- You're using the preset library heavily

### Switch to V2 if:
- You need multi-layer sounds
- You want to save complete projects
- You prefer a cleaner, focused interface
- You're building complex compositions

## Can I Use Both?

**Yes!** Both versions can coexist:
- They use different main files
- They can read each other's preset/layer configurations (manually)
- Use V1 for quick experiments, V2 for serious projects
- Keep both launchers available

## Recommendation

**New Users**: Start with V1
- Simpler interface
- Built-in presets to learn from
- Immediate feedback
- Less overwhelming

**Experienced Users**: Try V2
- More powerful composition tools
- Better project organization
- Professional workflow
- Document-based saves

**Professional Use**: V2
- Project management
- Complex compositions
- Repeatable workflows
- Better for collaboration

## Future Direction

V2 is the future of Sound Design Studio:
- Active development focus
- New features will target V2 architecture
- V1 will remain available for simplicity
- Eventually V2 will incorporate V1's preset library

## Quick Decision Guide

**I want to...**
- ...learn synthesis basics → **V1**
- ...build a preset library → **V1**
- ...create a single sound quickly → **V1**
- ...compare sounds side-by-side → **V1**
- ...compose multi-layer sounds → **V2**
- ...save and organize projects → **V2**
- ...build complex sound effects → **V2**
- ...work on a sound design project → **V2**

---

**Still not sure?** Try both! Launch times are fast, and you can switch between them easily.
