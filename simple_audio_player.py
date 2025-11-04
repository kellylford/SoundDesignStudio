"""
Simple Audio Player for Sound Design Studio
A standalone audio synthesis and playback module that doesn't require external dependencies
"""

import numpy as np
import sounddevice as sd
from scipy.io import wavfile
from dataclasses import dataclass
from typing import Optional
from pathlib import Path
import logging

# Set up logging to file
logging.basicConfig(
    filename='sound_design_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'  # Overwrite log file each time
)
logger = logging.getLogger(__name__)


@dataclass
class PlayAudioConfig:
    """Configuration for audio playback."""
    frequency: float = 440.0
    wave_type: str = 'sine'
    duration: float = 0.5
    volume: float = 0.3
    attack: float = 0.01
    decay: float = 0.1
    sustain: float = 0.7
    release: float = 0.15
    overlap: float = 0.0  # Overlap with previous layer in sequential mode (seconds)
    harmonics: dict = None
    blending: dict = None
    advanced: dict = None
    play_type: str = 'custom'
    
    def __post_init__(self):
        if self.harmonics is None:
            self.harmonics = {
                'enabled': True,
                'octave_volume': 0.3,
                'fifth_volume': 0.2,
                'sub_bass_volume': 0.0
            }
        if self.blending is None:
            self.blending = {
                'enabled': True,
                'blend_ratio': 0.5
            }
        if self.advanced is None:
            self.advanced = {
                'enabled': False,
                'synthesis_type': 'fm',
                'fm_mod_ratio': 1.4,
                'fm_mod_index': 5.0,
                'noise_type': 'white',
                'noise_filter_enabled': False,
                'noise_filter_type': 'bandpass',
                'noise_filter_low': 2000.0,
                'noise_filter_high': 8000.0,
                'lfo_enabled': False,
                'lfo_frequency': 5.0,
                'lfo_depth': 0.3,
                'echo_enabled': False,
                'echo_delay': 0.3,
                'echo_feedback': 0.4
            }


class EnhancedAudioPlayer:
    """Simple audio player with waveform synthesis."""
    
    SAMPLE_RATE = 44100
    
    def __init__(self):
        self.sample_rate = self.SAMPLE_RATE
    
    def play_sound(self, config: PlayAudioConfig):
        """Play a sound based on configuration."""
        try:
            # Generate the audio samples
            samples = self._generate_audio(config)
            
            # Ensure volume is in valid range
            samples = samples * config.volume
            
            # Clip to prevent distortion
            samples = np.clip(samples, -1.0, 1.0)
            
            # Play the sound
            sd.play(samples, self.sample_rate)
            sd.wait()
            
        except Exception as e:
            print(f"Error playing sound: {e}")
            raise
    
    def play_mixed_sounds(self, configs: list):
        """Play multiple sounds mixed together (simultaneous playback)."""
        try:
            if not configs:
                return
            
            logger.info(f"=== Starting mixed playback with {len(configs)} layers ===")
            
            # Generate audio for all configs
            all_audio = []
            max_duration = 0
            
            for config in configs:
                audio = self._generate_audio(config)
                audio = audio * config.volume
                all_audio.append(audio)
                max_duration = max(max_duration, len(audio))
            
            logger.info(f"Generated {len(all_audio)} audio arrays, max_duration = {max_duration} samples")
            
            # Pad all audio to same length and store in new list
            padded_audio = []
            for i, audio in enumerate(all_audio):
                logger.debug(f"Layer {i}: original length = {len(audio)}, max_duration = {max_duration}")
                if len(audio) < max_duration:
                    padding = np.zeros(max_duration - len(audio))
                    audio = np.concatenate([audio, padding])
                    logger.debug(f"Layer {i}: after padding length = {len(audio)}")
                padded_audio.append(audio)
            
            # Debug: Check all lengths
            lengths = [len(a) for a in padded_audio]
            logger.info(f"All padded lengths: {lengths}")
            
            # Mix by averaging (to prevent clipping)
            if len(padded_audio) == 1:
                mixed = padded_audio[0]
                logger.info("Single layer - no mixing needed")
            else:
                # Stack arrays vertically then average
                try:
                    shapes = [a.shape for a in padded_audio]
                    logger.info(f"Array shapes before vstack: {shapes}")
                    mixed = np.mean(np.vstack(padded_audio), axis=0)
                    logger.info(f"Mixed audio shape: {mixed.shape}")
                except Exception as e:
                    logger.error(f"Error in vstack: {e}")
                    logger.error(f"Padded audio shapes: {[a.shape for a in padded_audio]}")
                    raise
            
            # Normalize to prevent distortion
            max_val = np.max(np.abs(mixed))
            if max_val > 0.8:  # Leave some headroom
                mixed = mixed * (0.8 / max_val)
            
            # Clip just in case
            mixed = np.clip(mixed, -1.0, 1.0)
            
            logger.info(f"Playing mixed audio, shape: {mixed.shape}")
            # Play the mixed sound
            sd.play(mixed, self.sample_rate)
            sd.wait()
            logger.info("Playback complete")
            
        except Exception as e:
            logger.exception(f"Error playing mixed sounds: {e}")
            print(f"Error playing mixed sounds: {e}")
            raise
    
    def export_to_wav(self, config: PlayAudioConfig, file_path: str):
        """Export a single sound configuration to WAV file."""
        try:
            # Generate the audio samples
            samples = self._generate_audio(config)
            
            # Apply volume
            samples = samples * config.volume
            
            # Clip to prevent distortion
            samples = np.clip(samples, -1.0, 1.0)
            
            # Convert to 16-bit PCM format
            samples_int = np.int16(samples * 32767)
            
            # Write WAV file
            wavfile.write(file_path, self.sample_rate, samples_int)
            
            return True
        except Exception as e:
            print(f"Error exporting to WAV: {e}")
            raise
    
    def export_mixed_to_wav(self, configs: list, file_path: str):
        """Export multiple mixed sounds to WAV file."""
        try:
            if not configs:
                return False
            
            logger.info(f"=== Starting mixed export with {len(configs)} layers to {file_path} ===")
            
            # Generate audio for all configs
            all_audio = []
            max_duration = 0
            
            for config in configs:
                audio = self._generate_audio(config)
                audio = audio * config.volume
                all_audio.append(audio)
                max_duration = max(max_duration, len(audio))
            
            logger.info(f"Generated {len(all_audio)} audio arrays, max_duration = {max_duration} samples")
            
            # Pad all audio to same length and store in new list
            padded_audio = []
            for i, audio in enumerate(all_audio):
                logger.debug(f"Layer {i}: original length = {len(audio)}, max_duration = {max_duration}")
                if len(audio) < max_duration:
                    padding = np.zeros(max_duration - len(audio))
                    audio = np.concatenate([audio, padding])
                    logger.debug(f"Layer {i}: after padding length = {len(audio)}")
                padded_audio.append(audio)
            
            # Debug: Check all lengths
            lengths = [len(a) for a in padded_audio]
            logger.info(f"All padded lengths: {lengths}")
            
            # Mix by averaging (to prevent clipping)
            if len(padded_audio) == 1:
                mixed = padded_audio[0]
                logger.info("Single layer - no mixing needed")
            else:
                # Stack arrays vertically then average
                try:
                    shapes = [a.shape for a in padded_audio]
                    logger.info(f"Array shapes before vstack: {shapes}")
                    mixed = np.mean(np.vstack(padded_audio), axis=0)
                    logger.info(f"Mixed audio shape: {mixed.shape}")
                except Exception as e:
                    logger.error(f"Error in vstack: {e}")
                    logger.error(f"Padded audio shapes: {[a.shape for a in padded_audio]}")
                    raise
            
            # Normalize to prevent distortion
            max_val = np.max(np.abs(mixed))
            if max_val > 0.8:  # Leave some headroom
                mixed = mixed * (0.8 / max_val)
            
            # Clip just in case
            mixed = np.clip(mixed, -1.0, 1.0)
            
            # Convert to 16-bit PCM format
            mixed_int = np.int16(mixed * 32767)
            
            # Write WAV file
            wavfile.write(file_path, self.sample_rate, mixed_int)
            logger.info(f"Successfully exported to {file_path}")
            
            return True
        except Exception as e:
            logger.exception(f"Error exporting mixed to WAV: {e}")
            print(f"Error exporting mixed to WAV: {e}")
            raise
    
    def export_sequential_to_wav(self, configs: list, file_path: str):
        """Export multiple sounds played sequentially to WAV file."""
        try:
            if not configs:
                return False
            
            # Generate audio for all configs
            all_audio = []
            
            for config in configs:
                audio = self._generate_audio(config)
                audio = audio * config.volume
                audio = np.clip(audio, -1.0, 1.0)
                all_audio.append(audio)
            
            # Concatenate all audio
            sequential = np.concatenate(all_audio)
            
            # Convert to 16-bit PCM format
            sequential_int = np.int16(sequential * 32767)
            
            # Write WAV file
            wavfile.write(file_path, self.sample_rate, sequential_int)
            
            return True
        except Exception as e:
            print(f"Error exporting sequential to WAV: {e}")
            raise
    
    def _generate_audio(self, config: PlayAudioConfig) -> np.ndarray:
        """Generate audio samples based on configuration."""
        num_samples = int(self.sample_rate * config.duration)
        t = np.linspace(0, config.duration, num_samples, False)
        
        # Generate base waveform
        audio = self._generate_waveform(t, config.frequency, config.wave_type)
        
        # Apply harmonics if enabled
        if config.harmonics.get('enabled', False):
            audio = self._apply_harmonics(audio, t, config)
        
        # Apply blending if enabled
        if config.blending.get('enabled', False) and config.wave_type != 'sine':
            audio = self._apply_blending(audio, t, config)
        
        # Apply ADSR envelope
        audio = self._apply_adsr(audio, config)
        
        # Apply advanced synthesis if enabled
        if config.advanced.get('enabled', False):
            audio = self._apply_advanced(audio, t, config)
        
        return audio
    
    def _generate_waveform(self, t: np.ndarray, frequency: float, wave_type: str) -> np.ndarray:
        """Generate basic waveform."""
        if wave_type == 'sine':
            return np.sin(2 * np.pi * frequency * t)
        elif wave_type == 'square':
            return np.sign(np.sin(2 * np.pi * frequency * t))
        elif wave_type == 'sawtooth':
            return 2 * (t * frequency - np.floor(t * frequency + 0.5))
        elif wave_type == 'triangle':
            return 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1
        else:
            return np.sin(2 * np.pi * frequency * t)
    
    def _apply_harmonics(self, audio: np.ndarray, t: np.ndarray, config: PlayAudioConfig) -> np.ndarray:
        """Apply harmonic overtones."""
        harmonics = config.harmonics
        freq = config.frequency
        wave_type = config.wave_type
        
        result = audio.copy()
        
        # Octave (2x frequency)
        if harmonics.get('octave_volume', 0) > 0:
            octave = self._generate_waveform(t, freq * 2, wave_type)
            result += octave * harmonics['octave_volume']
        
        # Fifth (1.5x frequency)
        if harmonics.get('fifth_volume', 0) > 0:
            fifth = self._generate_waveform(t, freq * 1.5, wave_type)
            result += fifth * harmonics['fifth_volume']
        
        # Sub-bass (0.5x frequency)
        if harmonics.get('sub_bass_volume', 0) > 0:
            subbass = self._generate_waveform(t, freq * 0.5, wave_type)
            result += subbass * harmonics['sub_bass_volume']
        
        # Normalize to prevent clipping
        max_val = np.max(np.abs(result))
        if max_val > 1.0:
            result = result / max_val
        
        return result
    
    def _apply_blending(self, audio: np.ndarray, t: np.ndarray, config: PlayAudioConfig) -> np.ndarray:
        """Blend waveforms for warmer tones."""
        wave_type = config.wave_type
        blend_ratio = config.blending.get('blend_ratio', 0.5) / 100.0  # Convert percentage
        
        # Determine blend pair
        if wave_type == 'square':
            secondary = self._generate_waveform(t, config.frequency, 'triangle')
        elif wave_type == 'sawtooth':
            secondary = self._generate_waveform(t, config.frequency, 'sine')
        else:
            return audio  # No blending for sine or triangle
        
        # Blend
        return audio * (1 - blend_ratio) + secondary * blend_ratio
    
    def _apply_adsr(self, audio: np.ndarray, config: PlayAudioConfig) -> np.ndarray:
        """Apply ADSR envelope."""
        num_samples = len(audio)
        envelope = np.zeros(num_samples)
        
        # Calculate sample counts for each phase
        attack_samples = int(config.attack * self.sample_rate)
        decay_samples = int(config.decay * self.sample_rate)
        release_samples = int(config.release * self.sample_rate)
        
        # Ensure we don't exceed array bounds
        attack_samples = min(attack_samples, num_samples)
        decay_samples = min(decay_samples, num_samples - attack_samples)
        
        # Calculate remaining space for sustain and release
        remaining = num_samples - attack_samples - decay_samples
        release_samples = min(release_samples, remaining)
        
        sustain_samples = remaining - release_samples
        sustain_samples = max(0, sustain_samples)
        
        current_idx = 0
        
        # Attack phase
        if attack_samples > 0:
            envelope[current_idx:current_idx + attack_samples] = np.linspace(0, 1, attack_samples)
            current_idx += attack_samples
        
        # Decay phase
        if decay_samples > 0:
            envelope[current_idx:current_idx + decay_samples] = np.linspace(1, config.sustain, decay_samples)
            current_idx += decay_samples
        
        # Sustain phase
        if sustain_samples > 0:
            envelope[current_idx:current_idx + sustain_samples] = config.sustain
            current_idx += sustain_samples
        
        # Release phase
        if release_samples > 0:
            # Make sure we don't exceed the envelope bounds
            actual_release = min(release_samples, num_samples - current_idx)
            if actual_release > 0:
                start_level = config.sustain if current_idx > 0 else 1.0
                envelope[current_idx:current_idx + actual_release] = np.linspace(start_level, 0, actual_release)
        
        return audio * envelope
    
    def _apply_advanced(self, audio: np.ndarray, t: np.ndarray, config: PlayAudioConfig) -> np.ndarray:
        """Apply advanced synthesis techniques."""
        advanced = config.advanced
        synth_type = advanced.get('synthesis_type', 'fm')
        
        # For now, just return the original audio
        # Advanced synthesis would be implemented here
        return audio
