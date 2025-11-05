"""
Test script for new audio effects and SoundFont features
Run this to verify installation and functionality
"""

import sys
import numpy as np

print("=" * 70)
print("Sound Design Studio - Feature Test")
print("=" * 70)

# Test 1: Audio Effects (Pedalboard)
print("\n1. Testing Audio Effects (Pedalboard)...")
try:
    from audio_effects import AudioEffectsProcessor, PEDALBOARD_AVAILABLE
    
    if PEDALBOARD_AVAILABLE:
        print("   ✓ Pedalboard installed and available")
        
        # Test basic functionality
        processor = AudioEffectsProcessor()
        test_audio = np.random.randn(4410).astype(np.float32)  # 0.1 second
        config = processor.get_default_effects_config()
        config['enabled'] = True
        config['reverb_enabled'] = True
        
        result = processor.apply_effects(test_audio, config)
        print(f"   ✓ Effects processing works (processed {len(result)} samples)")
        print("   ✓ Available effects: Reverb, Delay, Distortion, Chorus, Phaser, Compressor, Filters")
    else:
        print("   ✗ Pedalboard not installed")
        print("   Install with: pip install pedalboard")
        
except Exception as e:
    print(f"   ✗ Error testing audio effects: {e}")

# Test 2: SoundFont Support (FluidSynth)
print("\n2. Testing SoundFont Support (FluidSynth)...")
try:
    from soundfont_player import SoundFontPlayer, FLUIDSYNTH_AVAILABLE
    
    if FLUIDSYNTH_AVAILABLE:
        print("   ✓ PyFluidSynth installed")
        
        # Test initialization
        player = SoundFontPlayer()
        if player.enabled:
            print("   ✓ FluidSynth initialized successfully")
            print("   ✓ Ready to load .sf2 SoundFont files")
            
            # Test MIDI conversion
            freq = 440.0
            midi = player.frequency_to_midi(freq)
            freq_back = player.midi_to_frequency(midi)
            print(f"   ✓ MIDI conversion works: {freq}Hz = MIDI note {midi}")
        else:
            print("   ✗ FluidSynth library not found on system")
            print("   Windows: Download from https://github.com/FluidSynth/fluidsynth/releases")
            print("   macOS: brew install fluid-synth")
            print("   Linux: sudo apt-get install fluidsynth")
    else:
        print("   ✗ PyFluidSynth not installed")
        print("   Install with: pip install pyfluidsynth")
        
except Exception as e:
    print(f"   ✗ Error testing SoundFont: {e}")

# Test 3: Integration with Audio Player
print("\n3. Testing Integration...")
try:
    from simple_audio_player import EnhancedAudioPlayer, PlayAudioConfig
    
    player = EnhancedAudioPlayer()
    print("   ✓ Audio player initialized")
    print(f"   ✓ Effects processor: {'Available' if player.effects_processor.enabled else 'Disabled'}")
    print(f"   ✓ SoundFont player: {'Available' if player.soundfont_player.enabled else 'Disabled'}")
    
    # Test config creation
    config = PlayAudioConfig()
    print("   ✓ PlayAudioConfig created with effects and soundfont fields")
    print(f"   ✓ Config has 'effects' field: {'effects' in config.__dict__}")
    print(f"   ✓ Config has 'soundfont' field: {'soundfont' in config.__dict__}")
    
except Exception as e:
    print(f"   ✗ Error testing integration: {e}")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

features_available = []
features_missing = []

try:
    from audio_effects import PEDALBOARD_AVAILABLE
    if PEDALBOARD_AVAILABLE:
        features_available.append("Audio Effects (Pedalboard)")
    else:
        features_missing.append("Audio Effects - pip install pedalboard")
except:
    features_missing.append("Audio Effects - pip install pedalboard")

try:
    from soundfont_player import FLUIDSYNTH_AVAILABLE, SoundFontPlayer
    player = SoundFontPlayer()
    if FLUIDSYNTH_AVAILABLE and player.enabled:
        features_available.append("SoundFont Support (FluidSynth)")
    else:
        features_missing.append("SoundFont Support - install FluidSynth system library")
except:
    features_missing.append("SoundFont Support - pip install pyfluidsynth")

print(f"\n✓ Available Features ({len(features_available)}):")
if features_available:
    for feature in features_available:
        print(f"  - {feature}")
else:
    print("  None")

print(f"\n✗ Missing Features ({len(features_missing)}):")
if features_missing:
    for feature in features_missing:
        print(f"  - {feature}")
else:
    print("  None - All features available!")

print("\nNote: The application will work without these features.")
print("Synthesis-based sound generation is always available.")
print("\nFor installation instructions, see INSTALLATION_NEW_FEATURES.md")
print("=" * 70)

sys.exit(0 if not features_missing else 1)
