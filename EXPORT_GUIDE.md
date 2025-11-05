# Exporting and Using Sounds Outside the App

## Quick Start

### Export Your Sound
1. **Create or load a sound** in Sound Design Studio
2. **Click "Export WAV"** button (or press **Ctrl+E**)
3. Choose where to save your `.wav` file
4. Done! Your sound is now a standard WAV audio file

---

## Export Options

### 1. Export Complete Sound (Ctrl+E)
**Menu**: File → Export as WAV  
**Button**: "Export WAV"

Exports your entire sound according to its playback mode:
- **Sequential Mode**: Layers play one after another → Single WAV file
- **Simultaneous Mode**: Layers mixed together → Single WAV file

**Use this when**:
- You want the final mixed sound
- Ready to use in your app/game/video
- Need a single audio file

**Example**: 
- Load preset "Power Up" (3 sequential layers)
- Export as `powerup.wav`
- Result: Complete rising sound effect in one file

### 2. Export Current Layer Only
**Menu**: File → Export Current Layer as WAV

Exports only the selected layer (ignores other layers).

**Use this when**:
- You want individual layer files
- Building your own mix elsewhere
- Need component sounds separately
- Want to experiment with different combinations

**Example**:
- Load preset "Bell"
- Select "Strike" layer → Export as `bell_strike.wav`
- Select "Shimmer" layer → Export as `bell_shimmer.wav`
- Mix them yourself in other software

---

## Technical Specifications

### WAV File Format
- **Sample Rate**: 44,100 Hz (CD quality)
- **Bit Depth**: 16-bit PCM
- **Channels**: Mono (1 channel)
- **Format**: Uncompressed WAV
- **Compatibility**: Universal - works everywhere

### File Sizes
Approximate sizes for reference:
- **0.5 seconds**: ~45 KB
- **1 second**: ~90 KB
- **2 seconds**: ~180 KB
- **5 seconds**: ~450 KB

Formula: `Duration (sec) × 44,100 × 2 bytes = file size`

---

## Using Exported Sounds

### In Your Sports App

#### Original Method (Python)
```python
# If your app uses the original enhanced_audio_player
from enhanced_audio_player import EnhancedAudioPlayer
import soundfile as sf

# Load the WAV file
audio_data, sample_rate = sf.read('powerup.wav')

# Play it
import sounddevice as sd
sd.play(audio_data, sample_rate)
sd.wait()
```

#### Simple Method (Python)
```python
# Using pygame (easier)
import pygame
pygame.mixer.init()
sound = pygame.mixer.Sound('powerup.wav')
sound.play()
```

#### Standard Library Method (Python)
```python
# Using winsound (Windows only, very simple)
import winsound
winsound.PlaySound('powerup.wav', winsound.SND_FILENAME)
```

### In Web Apps (JavaScript)
```javascript
// HTML5 Audio
const audio = new Audio('powerup.wav');
audio.play();

// Or preload for faster playback
const sounds = {
    powerup: new Audio('powerup.wav'),
    coin: new Audio('coin.wav')
};

// Play instantly
sounds.powerup.play();
```

### In Unity (C#)
```csharp
// Drag WAV into Unity Assets folder
public AudioSource audioSource;
public AudioClip powerUpSound;

void PlaySound() {
    audioSource.PlayOneShot(powerUpSound);
}
```

### In React Native (Mobile)
```javascript
import Sound from 'react-native-sound';

const powerUp = new Sound('powerup.wav', Sound.MAIN_BUNDLE, (error) => {
    if (!error) {
        powerUp.play();
    }
});
```

### In HTML
```html
<audio src="powerup.wav" preload="auto" id="powerup"></audio>

<script>
    document.getElementById('powerup').play();
</script>
```

---

## Workflow Examples

### Example 1: Game Sound Effects

**Goal**: Create sound effects for a game

1. **Create sounds in Studio**:
   - Load preset "Laser Gun" → Customize → Export as `laser.wav`
   - Load preset "Coin" → Customize → Export as `coin.wav`
   - Load preset "Power Up" → Export as `powerup.wav`
   - Load preset "Error" → Export as `error.wav`

2. **Import to Unity/Godot**:
   - Drag WAV files into Assets folder
   - Attach to game objects
   - Trigger with code

3. **Done!**

### Example 2: Sports App Audio

**Goal**: Add touchdown/goal sounds to your app

1. **Create custom sounds**:
   - Create "Touchdown Fanfare" using sequential layers
   - Create "Whistle" using single high-frequency layer
   - Create "Buzzer" using simultaneous harsh layers
   - Create "Crowd Cheer" using simultaneous complex layers

2. **Export all as WAV**

3. **In your Python sports app**:
```python
import pygame
pygame.mixer.init()

sounds = {
    'touchdown': pygame.mixer.Sound('touchdown.wav'),
    'whistle': pygame.mixer.Sound('whistle.wav'),
    'buzzer': pygame.mixer.Sound('buzzer.wav'),
    'cheer': pygame.mixer.Sound('cheer.wav')
}

# When touchdown happens
sounds['touchdown'].play()
```

### Example 3: UI Feedback Sounds

**Goal**: Add click sounds to a website

1. **Create in Studio**:
   - Load "Button Click" → Export as `click.wav`
   - Load "Success" → Export as `success.wav`
   - Load "Error" → Export as `error.wav`

2. **In your website**:
```html
<button onclick="playSound('click')">Click Me</button>

<script>
const sounds = {
    click: new Audio('click.wav'),
    success: new Audio('success.wav'),
    error: new Audio('error.wav')
};

function playSound(name) {
    sounds[name].currentTime = 0; // Reset to start
    sounds[name].play();
}
</script>
```

### Example 4: Video Production

**Goal**: Add sound effects to a video

1. **Create sounds in Studio**:
   - Create dramatic whoosh → Export as `whoosh.wav`
   - Create impact sound → Export as `impact.wav`

2. **Import to video editor**:
   - Drag WAV into Adobe Premiere timeline
   - Sync with video
   - Adjust volume/effects as needed

---

## Advanced Tips

### Batch Export
Want to export multiple presets at once?
1. Load preset → Export (Ctrl+E) → Save
2. Load next preset → Export → Save
3. Repeat

### Organizing Exports
Suggested folder structure:
```
my_sounds/
├── ui/
│   ├── click.wav
│   ├── success.wav
│   └── error.wav
├── game/
│   ├── laser.wav
│   ├── coin.wav
│   └── powerup.wav
└── music/
    ├── bell.wav
    └── piano.wav
```

### Converting to Other Formats
Need MP3 or OGG? Use a converter:
- **Audacity** (free): Import WAV → Export as MP3/OGG
- **FFmpeg** (command line): `ffmpeg -i input.wav output.mp3`
- **Online**: CloudConvert, Online-Convert, etc.

**Why WAV first?**
- Lossless quality
- Maximum compatibility
- Can convert to any format later
- Professional standard

### Quality Considerations
Our WAV files are:
- ✅ CD quality (44.1 kHz)
- ✅ Professional bit depth (16-bit)
- ✅ Compatible with all platforms
- ✅ No compression artifacts

For most uses, this is perfect! For audiophile/mastering use, you might want:
- Higher sample rate (96 kHz)
- Higher bit depth (24-bit)
- But 99% of apps won't need this

---

## Troubleshooting

### "File not playing in my app"
**Solution**:
- Check file path is correct
- Ensure WAV format supported (it should be)
- Try playing in Windows Media Player first to verify file

### "Sound is too quiet/loud"
**Solution**:
- Adjust volume in layer settings before export
- Or adjust in your app's audio player
- Or use audio editing software (Audacity) to normalize

### "Need stereo, not mono"
**Solution**:
- Our exports are mono (single channel)
- Use Audacity: Import → Tracks → Make Stereo Track
- Or duplicate channel programmatically in your app

### "File size too large"
**Solution**:
- Reduce duration in layer settings
- Export as MP3 instead (compress after export)
- Use lower sample rate converter (not recommended)

---

## Integration Examples

### Python Sports App (Your Use Case!)
```python
import pygame
from pathlib import Path

class SportsAudio:
    def __init__(self, sound_folder='sounds'):
        pygame.mixer.init()
        self.sounds = {}
        
        # Load all WAV files from folder
        sound_path = Path(sound_folder)
        for wav_file in sound_path.glob('*.wav'):
            name = wav_file.stem
            self.sounds[name] = pygame.mixer.Sound(str(wav_file))
    
    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def stop_all(self):
        pygame.mixer.stop()

# Usage
audio = SportsAudio('exported_sounds')
audio.play('touchdown')
audio.play('whistle')
```

### Electron App
```javascript
const { app } = require('electron');
const sound = require('sound-play');

sound.play('powerup.wav');
```

### Android (Java)
```java
MediaPlayer mp = MediaPlayer.create(context, R.raw.powerup);
mp.start();
```

---

## Summary

✅ **Export as WAV** → Universal compatibility  
✅ **44.1 kHz, 16-bit** → Professional quality  
✅ **Works everywhere** → Apps, games, web, video  
✅ **Convert if needed** → MP3, OGG, etc.  
✅ **Small file sizes** → Fast loading  
✅ **Easy integration** → Standard audio file  

**You're no longer limited to the app!** 🎉

Your sounds can now be used in:
- Production apps
- Commercial games  
- Professional videos
- Live websites
- Mobile applications
- Desktop software
- Anywhere audio is needed!

---

## Need Help?

**Can't export**: Check if you have layers in your document  
**App crashes**: Make sure scipy is installed (`pip install scipy`)  
**Integration issues**: Check the examples above for your platform  
**Quality concerns**: Our WAV files are professional-grade for most uses  

Happy exporting! 🎵
