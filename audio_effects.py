"""
Audio Effects Processor
Uses Spotify's pedalboard library for professional audio effects
"""

import numpy as np

try:
    from pedalboard import (
        Pedalboard, Reverb, Delay, Distortion, Chorus, 
        Compressor, Gain, HighpassFilter, LowpassFilter, 
        Phaser, Limiter
    )
    PEDALBOARD_AVAILABLE = True
except ImportError:
    PEDALBOARD_AVAILABLE = False
    print("Warning: pedalboard not installed. Audio effects will be disabled.")
    print("Install with: pip install pedalboard")


class AudioEffectsProcessor:
    """Apply professional audio effects to generated sounds."""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.enabled = PEDALBOARD_AVAILABLE
    
    def apply_effects(self, audio: np.ndarray, effects_config: dict) -> np.ndarray:
        """
        Apply audio effects to the given audio samples.
        
        Args:
            audio: Input audio samples (numpy array)
            effects_config: Dictionary of effect parameters
            
        Returns:
            Processed audio samples
        """
        if not self.enabled or not effects_config.get('enabled', False):
            return audio
        
        # Build effects chain
        board = Pedalboard([])
        
        # Reverb
        if effects_config.get('reverb_enabled', False):
            room_size = effects_config.get('reverb_room_size', 0.5)
            damping = effects_config.get('reverb_damping', 0.5)
            wet_level = effects_config.get('reverb_wet_level', 0.3)
            dry_level = effects_config.get('reverb_dry_level', 0.8)
            
            board.append(Reverb(
                room_size=room_size,
                damping=damping,
                wet_level=wet_level,
                dry_level=dry_level
            ))
        
        # Delay
        if effects_config.get('delay_enabled', False):
            delay_seconds = effects_config.get('delay_time', 0.5)
            feedback = effects_config.get('delay_feedback', 0.5)
            mix = effects_config.get('delay_mix', 0.5)
            
            board.append(Delay(
                delay_seconds=delay_seconds,
                feedback=feedback,
                mix=mix
            ))
        
        # Distortion
        if effects_config.get('distortion_enabled', False):
            drive_db = effects_config.get('distortion_drive', 10.0)
            
            board.append(Distortion(drive_db=drive_db))
        
        # Chorus
        if effects_config.get('chorus_enabled', False):
            rate_hz = effects_config.get('chorus_rate', 1.0)
            depth = effects_config.get('chorus_depth', 0.25)
            centre_delay_ms = effects_config.get('chorus_delay', 7.0)
            feedback = effects_config.get('chorus_feedback', 0.0)
            mix = effects_config.get('chorus_mix', 0.5)
            
            board.append(Chorus(
                rate_hz=rate_hz,
                depth=depth,
                centre_delay_ms=centre_delay_ms,
                feedback=feedback,
                mix=mix
            ))
        
        # Phaser
        if effects_config.get('phaser_enabled', False):
            rate_hz = effects_config.get('phaser_rate', 1.0)
            depth = effects_config.get('phaser_depth', 0.5)
            centre_frequency_hz = effects_config.get('phaser_frequency', 1300.0)
            feedback = effects_config.get('phaser_feedback', 0.0)
            mix = effects_config.get('phaser_mix', 0.5)
            
            board.append(Phaser(
                rate_hz=rate_hz,
                depth=depth,
                centre_frequency_hz=centre_frequency_hz,
                feedback=feedback,
                mix=mix
            ))
        
        # Compressor
        if effects_config.get('compressor_enabled', False):
            threshold_db = effects_config.get('compressor_threshold', -20.0)
            ratio = effects_config.get('compressor_ratio', 4.0)
            attack_ms = effects_config.get('compressor_attack', 1.0)
            release_ms = effects_config.get('compressor_release', 100.0)
            
            board.append(Compressor(
                threshold_db=threshold_db,
                ratio=ratio,
                attack_ms=attack_ms,
                release_ms=release_ms
            ))
        
        # High-pass filter
        if effects_config.get('highpass_enabled', False):
            cutoff_hz = effects_config.get('highpass_cutoff', 80.0)
            board.append(HighpassFilter(cutoff_frequency_hz=cutoff_hz))
        
        # Low-pass filter
        if effects_config.get('lowpass_enabled', False):
            cutoff_hz = effects_config.get('lowpass_cutoff', 8000.0)
            board.append(LowpassFilter(cutoff_frequency_hz=cutoff_hz))
        
        # Limiter (always at the end to prevent clipping)
        if effects_config.get('limiter_enabled', True):
            threshold_db = effects_config.get('limiter_threshold', -1.0)
            release_ms = effects_config.get('limiter_release', 100.0)
            
            board.append(Limiter(
                threshold_db=threshold_db,
                release_ms=release_ms
            ))
        
        # Apply effects
        try:
            # Ensure audio is float32 and 2D (samples, channels)
            if audio.ndim == 1:
                audio = audio.reshape(-1, 1)
            
            audio_float32 = audio.astype(np.float32)
            processed = board(audio_float32, self.sample_rate)
            
            # Convert back to 1D if input was 1D
            if processed.shape[1] == 1:
                processed = processed.flatten()
            
            return processed
            
        except Exception as e:
            print(f"Error applying effects: {e}")
            return audio
    
    def get_default_effects_config(self):
        """Return default effects configuration."""
        return {
            'enabled': False,
            
            # Reverb
            'reverb_enabled': False,
            'reverb_room_size': 0.5,
            'reverb_damping': 0.5,
            'reverb_wet_level': 0.3,
            'reverb_dry_level': 0.8,
            
            # Delay
            'delay_enabled': False,
            'delay_time': 0.5,
            'delay_feedback': 0.5,
            'delay_mix': 0.5,
            
            # Distortion
            'distortion_enabled': False,
            'distortion_drive': 10.0,
            
            # Chorus
            'chorus_enabled': False,
            'chorus_rate': 1.0,
            'chorus_depth': 0.25,
            'chorus_delay': 7.0,
            'chorus_feedback': 0.0,
            'chorus_mix': 0.5,
            
            # Phaser
            'phaser_enabled': False,
            'phaser_rate': 1.0,
            'phaser_depth': 0.5,
            'phaser_frequency': 1300.0,
            'phaser_feedback': 0.0,
            'phaser_mix': 0.5,
            
            # Compressor
            'compressor_enabled': False,
            'compressor_threshold': -20.0,
            'compressor_ratio': 4.0,
            'compressor_attack': 1.0,
            'compressor_release': 100.0,
            
            # Filters
            'highpass_enabled': False,
            'highpass_cutoff': 80.0,
            'lowpass_enabled': False,
            'lowpass_cutoff': 8000.0,
            
            # Limiter
            'limiter_enabled': True,
            'limiter_threshold': -1.0,
            'limiter_release': 100.0
        }
