"""
SoundFont Player Module
Provides realistic instrument sounds using SoundFont (.sf2) files
"""

import numpy as np
from pathlib import Path

try:
    import fluidsynth
    FLUIDSYNTH_AVAILABLE = True
except ImportError:
    FLUIDSYNTH_AVAILABLE = False
    print("Warning: pyfluidsynth not installed. SoundFont support will be disabled.")
    print("Install with: pip install pyfluidsynth")


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
            self.synth = fluidsynth.Synth(samplerate=float(self.sample_rate))
            self.synth.start(driver='file')  # Use file driver for rendering
        except Exception as e:
            print(f"Error initializing FluidSynth: {e}")
            self.enabled = False
    
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
            return np.zeros(int(duration * self.sample_rate))
        
        try:
            # Select program (instrument)
            self.synth.program_select(0, self.soundfont_id, bank, program)
            
            # Calculate sample count
            num_samples = int(duration * self.sample_rate)
            
            # Play note
            self.synth.noteon(0, midi_note, velocity)
            
            # Render audio
            audio = self.synth.get_samples(num_samples)
            
            # Note off
            self.synth.noteoff(0, midi_note)
            
            # Convert to numpy array and normalize
            if isinstance(audio, tuple):
                # Stereo: average the channels
                left, right = audio
                audio = (np.array(left) + np.array(right)) / 2.0
            else:
                audio = np.array(audio)
            
            # Normalize to -1.0 to 1.0 range
            max_val = np.max(np.abs(audio))
            if max_val > 0:
                audio = audio / max_val
            
            return audio.astype(np.float32)
            
        except Exception as e:
            print(f"Error generating note: {e}")
            return np.zeros(int(duration * self.sample_rate))
    
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
