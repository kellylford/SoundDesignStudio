"""
SoundFont Player Module
Provides realistic instrument sounds using SoundFont (.sf2) files
"""

import numpy as np
from pathlib import Path

try:
    import fluidsynth
    FLUIDSYNTH_AVAILABLE = True
except (ImportError, FileNotFoundError, OSError) as e:
    FLUIDSYNTH_AVAILABLE = False
    print("Warning: FluidSynth not available. SoundFont support will be disabled.")
    if isinstance(e, FileNotFoundError):
        print("  FluidSynth system library not found.")
        print("  See INSTALLATION_NEW_FEATURES.md for installation instructions.")
    else:
        print("  Install with: pip install pyfluidsynth")
        print("  Plus FluidSynth system library (see INSTALLATION_NEW_FEATURES.md)")


class SoundFontPlayer:
    """Play realistic instrument sounds using SoundFont files."""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.enabled = FLUIDSYNTH_AVAILABLE
        self.synth = None
        self.soundfont_id = None
        self.current_soundfont_path = None
        
        if self.enabled:
            self._initialize_synth()
    
    def _initialize_synth(self):
        """Initialize FluidSynth synthesizer."""
        try:
            # Create synth with gain set to avoid clipping
            self.synth = fluidsynth.Synth(gain=0.5, samplerate=float(self.sample_rate))
            
            # Start with 'file' driver for offline rendering (no audio device needed)
            # This avoids SDL/MIDI device warnings
            try:
                self.synth.start(driver='file')
            except:
                # If 'file' driver fails, try without driver (will use default)
                self.synth.start()
                
        except Exception as e:
            print(f"Error initializing FluidSynth: {e}")
            self.enabled = False
            self.synth = None
    
    def load_soundfont(self, soundfont_path: str) -> bool:
        """
        Load a SoundFont file.
        
        Args:
            soundfont_path: Path to .sf2 file
            
        Returns:
            True if loaded successfully
        """
        if not self.enabled or not self.synth:
            return False
        
        try:
            # Unload previous soundfont if any
            if self.soundfont_id is not None:
                self.synth.sfunload(self.soundfont_id)
            
            # Load new soundfont
            path = Path(soundfont_path)
            if not path.exists():
                print(f"SoundFont file not found: {soundfont_path}")
                return False
            
            self.soundfont_id = self.synth.sfload(str(path.absolute()))
            self.current_soundfont_path = str(path.absolute())
            
            # Select first program (instrument) on channel 0
            self.synth.program_select(0, self.soundfont_id, 0, 0)
            
            return True
            
        except Exception as e:
            print(f"Error loading SoundFont: {e}")
            return False
    
    def generate_note(self, midi_note: int, velocity: int, duration: float, 
                     program: int = 0, bank: int = 0) -> np.ndarray:
        """
        Generate audio for a MIDI note using loaded SoundFont.
        
        Args:
            midi_note: MIDI note number (0-127, middle C = 60)
            velocity: Note velocity (0-127, loudness)
            duration: Duration in seconds
            program: Instrument program number (0-127)
            bank: Bank number (usually 0)
            
        Returns:
            Audio samples as numpy array
        """
        if not self.enabled or not self.synth or self.soundfont_id is None:
            print("SoundFont not loaded or not enabled")
            return np.zeros(int(duration * self.sample_rate), dtype=np.float32)
        
        try:
            # Validate inputs
            midi_note = max(0, min(127, int(midi_note)))
            velocity = max(1, min(127, int(velocity)))
            duration = max(0.1, duration)
            program = max(0, min(127, int(program)))
            
            # Select program (instrument)
            self.synth.program_select(0, self.soundfont_id, bank, program)
            
            # Calculate sample count
            num_samples = int(duration * self.sample_rate)
            
            # Play note
            self.synth.noteon(0, midi_note, velocity)
            
            # Render audio with extra samples for release
            extra_samples = int(0.5 * self.sample_rate)  # 0.5 second extra for note release
            audio = self.synth.get_samples(num_samples + extra_samples)
            
            # Note off
            self.synth.noteoff(0, midi_note)
            
            # Convert to numpy array
            if isinstance(audio, tuple):
                # Stereo: average the channels
                left, right = audio
                left_arr = np.array(left, dtype=np.float32)
                right_arr = np.array(right, dtype=np.float32)
                audio = (left_arr + right_arr) / 2.0
            else:
                audio = np.array(audio, dtype=np.float32)
            
            # Trim to requested duration
            audio = audio[:num_samples]
            
            # Safety check for empty or invalid audio
            if len(audio) == 0:
                print("Generated audio is empty")
                return np.zeros(num_samples, dtype=np.float32)
            
            # Normalize to -1.0 to 1.0 range
            max_val = np.max(np.abs(audio))
            if max_val > 0:
                audio = audio / max_val
            
            return audio.astype(np.float32)
            
        except Exception as e:
            print(f"Error generating note: {e}")
            import traceback
            traceback.print_exc()
            return np.zeros(int(duration * self.sample_rate), dtype=np.float32)
    
    def frequency_to_midi(self, frequency: float) -> int:
        """Convert frequency (Hz) to MIDI note number."""
        # MIDI note = 69 + 12 * log2(frequency / 440)
        # 69 is A4 (440 Hz)
        import math
        midi_note = 69 + 12 * math.log2(frequency / 440.0)
        return int(round(midi_note))
    
    def midi_to_frequency(self, midi_note: int) -> float:
        """Convert MIDI note number to frequency (Hz)."""
        # frequency = 440 * 2^((midi_note - 69) / 12)
        return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))
    
    def get_available_programs(self) -> list:
        """
        Get list of available instruments in loaded SoundFont.
        
        Returns:
            List of (bank, program, name) tuples
        """
        if not self.enabled or not self.synth or self.soundfont_id is None:
            return []
        
        try:
            programs = []
            # Most SoundFonts use bank 0, check first 128 programs
            for program in range(128):
                # Try to get program info (this may not be supported by all versions)
                try:
                    self.synth.program_select(0, self.soundfont_id, 0, program)
                    # If we got here, the program exists
                    programs.append((0, program, f"Program {program}"))
                except:
                    pass
            
            return programs
            
        except Exception as e:
            print(f"Error getting programs: {e}")
            return []
    
    def get_default_soundfont_config(self):
        """Return default SoundFont configuration."""
        return {
            'enabled': False,
            'soundfont_path': '',
            'midi_note': 60,  # Middle C
            'velocity': 100,  # Loudness (0-127)
            'program': 0,     # Instrument number
            'bank': 0         # Bank number
        }
    
    def close(self):
        """Clean up resources."""
        if self.synth:
            try:
                self.synth.delete()
            except:
                pass
