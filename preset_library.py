"""
Preset Library for Sound Design Studio v2
Contains hierarchical presets organized by category
"""

def get_preset_library():
    """Return the complete preset library organized by category."""
    return {
        "Musical Instruments": {
            "Piano & Keys": {
                "Electric Piano": {
                    "playback_mode": "simultaneous",
                    "layers": [
                        {"name": "Fundamental", "config": {"frequency": 261.63, "wave_type": "sine", "duration": 1.5, "volume": 0.4, "attack": 0.01, "decay": 0.3, "sustain": 0.5, "release": 0.4}},
                        {"name": "Brightness", "config": {"frequency": 523.26, "wave_type": "triangle", "duration": 1.2, "volume": 0.2, "attack": 0.02, "decay": 0.2, "sustain": 0.3, "release": 0.3}}
                    ]
                },
                "Bell": {
                    "playback_mode": "simultaneous",
                    "layers": [
                        {"name": "Strike", "config": {"frequency": 440, "wave_type": "sine", "duration": 2.0, "volume": 0.5, "attack": 0.001, "decay": 0.8, "sustain": 0.2, "release": 1.2}},
                        {"name": "Shimmer", "config": {"frequency": 880, "wave_type": "sine", "duration": 2.0, "volume": 0.3, "attack": 0.01, "decay": 0.6, "sustain": 0.1, "release": 1.0, "harmonics": {"enabled": True, "octave_volume": 0.4, "fifth_volume": 0.3, "sub_bass_volume": 0.0}}}
                    ]
                },
                "Organ": {
                    "playback_mode": "simultaneous",
                    "layers": [
                        {"name": "Base", "config": {"frequency": 220, "wave_type": "sine", "duration": 1.0, "volume": 0.4, "attack": 0.05, "decay": 0.1, "sustain": 0.9, "release": 0.2}},
                        {"name": "Octave", "config": {"frequency": 440, "wave_type": "sine", "duration": 1.0, "volume": 0.3, "attack": 0.05, "decay": 0.1, "sustain": 0.9, "release": 0.2}},
                        {"name": "Fifth", "config": {"frequency": 330, "wave_type": "sine", "duration": 1.0, "volume": 0.2, "attack": 0.05, "decay": 0.1, "sustain": 0.9, "release": 0.2}}
                    ]
                }
            },
            "Strings": {
                "Violin": {
                    "playback_mode": "simultaneous",
                    "layers": [
                        {"name": "Bow", "config": {"frequency": 440, "wave_type": "sawtooth", "duration": 1.5, "volume": 0.4, "attack": 0.15, "decay": 0.2, "sustain": 0.8, "release": 0.3}},
                        {"name": "Air", "config": {"frequency": 880, "wave_type": "triangle", "duration": 1.5, "volume": 0.15, "attack": 0.2, "decay": 0.2, "sustain": 0.7, "release": 0.3}}
                    ]
                },
                "Cello": {
                    "playback_mode": "simultaneous",
                    "layers": [
                        {"name": "Low String", "config": {"frequency": 196, "wave_type": "sawtooth", "duration": 2.0, "volume": 0.5, "attack": 0.2, "decay": 0.3, "sustain": 0.8, "release": 0.5}},
                        {"name": "Resonance", "config": {"frequency": 98, "wave_type": "sine", "duration": 2.0, "volume": 0.2, "attack": 0.25, "decay": 0.3, "sustain": 0.7, "release": 0.5}}
                    ]
                }
            },
            "Drums & Percussion": {
                "Kick Drum": {
                    "playback_mode": "sequential",
                    "layers": [
                        {"name": "Thump", "config": {"frequency": 60, "wave_type": "sine", "duration": 0.3, "volume": 0.8, "attack": 0.001, "decay": 0.2, "sustain": 0.1, "release": 0.1}},
                        {"name": "Click", "config": {"frequency": 150, "wave_type": "square", "duration": 0.05, "volume": 0.4, "attack": 0.001, "decay": 0.04, "sustain": 0.0, "release": 0.01}}
                    ]
                },
                "Snare Hit": {
                    "playback_mode": "simultaneous",
                    "layers": [
                        {"name": "Body", "config": {"frequency": 200, "wave_type": "square", "duration": 0.2, "volume": 0.5, "attack": 0.001, "decay": 0.1, "sustain": 0.1, "release": 0.1}},
                        {"name": "Snap", "config": {"frequency": 1000, "wave_type": "triangle", "duration": 0.15, "volume": 0.4, "attack": 0.001, "decay": 0.08, "sustain": 0.05, "release": 0.06}}
                    ]
                },
                "Hi-Hat": {
                    "playback_mode": "simultaneous",
                    "layers": [
                        {"name": "High", "config": {"frequency": 8000, "wave_type": "square", "duration": 0.1, "volume": 0.3, "attack": 0.001, "decay": 0.05, "sustain": 0.1, "release": 0.04}},
                        {"name": "Mid", "config": {"frequency": 4000, "wave_type": "sawtooth", "duration": 0.1, "volume": 0.2, "attack": 0.001, "decay": 0.05, "sustain": 0.1, "release": 0.04}}
                    ]
                }
            }
        },
        "Sound Effects": {
            "Impacts": {
                "Heavy Impact": {
                    "playback_mode": "sequential",
                    "layers": [
                        {"name": "Boom", "config": {"frequency": 40, "wave_type": "sine", "duration": 0.5, "volume": 0.8, "attack": 0.001, "decay": 0.3, "sustain": 0.2, "release": 0.2}},
                        {"name": "Crack", "config": {"frequency": 800, "wave_type": "square", "duration": 0.15, "volume": 0.5, "attack": 0.001, "decay": 0.1, "sustain": 0.05, "release": 0.04}}
                    ]
                },
                "Metal Clang": {
                    "playback_mode": "sequential",
                    "layers": [
                        {"name": "Strike", "config": {"frequency": 600, "wave_type": "square", "duration": 0.8, "volume": 0.6, "attack": 0.001, "decay": 0.4, "sustain": 0.2, "release": 0.4}},
                        {"name": "Ring", "config": {"frequency": 1200, "wave_type": "sine", "duration": 1.5, "volume": 0.4, "attack": 0.01, "decay": 0.8, "sustain": 0.3, "release": 0.7, "harmonics": {"enabled": True, "octave_volume": 0.5, "fifth_volume": 0.3, "sub_bass_volume": 0.0}}}
                    ]
                }
            },
            "Transitions": {
                "Whoosh": {
                    "playback_mode": "simultaneous",
                    "layers": [
                        {"name": "Air", "config": {"frequency": 300, "wave_type": "sawtooth", "duration": 0.8, "volume": 0.4, "attack": 0.1, "decay": 0.3, "sustain": 0.3, "release": 0.4}},
                        {"name": "Wind", "config": {"frequency": 150, "wave_type": "triangle", "duration": 0.8, "volume": 0.3, "attack": 0.15, "decay": 0.25, "sustain": 0.3, "release": 0.3}}
                    ]
                },
                "Sweep Up": {
                    "playback_mode": "sequential",
                    "layers": [
                        {"name": "Low", "config": {"frequency": 100, "wave_type": "sine", "duration": 0.3, "volume": 0.5, "attack": 0.05, "decay": 0.1, "sustain": 0.6, "release": 0.15}},
                        {"name": "Mid", "config": {"frequency": 300, "wave_type": "sine", "duration": 0.3, "volume": 0.5, "attack": 0.05, "decay": 0.1, "sustain": 0.6, "release": 0.15}},
                        {"name": "High", "config": {"frequency": 900, "wave_type": "sine", "duration": 0.3, "volume": 0.4, "attack": 0.05, "decay": 0.1, "sustain": 0.5, "release": 0.15}}
                    ]
                }
            },
            "Atmosphere": {
                "Rumble": {
                    "playback_mode": "simultaneous",
                    "layers": [
                        {"name": "Sub Bass", "config": {"frequency": 30, "wave_type": "sine", "duration": 3.0, "volume": 0.6, "attack": 0.5, "decay": 1.0, "sustain": 0.7, "release": 1.5}},
                        {"name": "Texture", "config": {"frequency": 80, "wave_type": "sawtooth", "duration": 3.0, "volume": 0.3, "attack": 0.6, "decay": 1.0, "sustain": 0.6, "release": 1.4}}
                    ]
                },
                "Drone": {
                    "playback_mode": "simultaneous",
                    "layers": [
                        {"name": "Base", "config": {"frequency": 110, "wave_type": "sawtooth", "duration": 4.0, "volume": 0.4, "attack": 0.8, "decay": 0.5, "sustain": 0.9, "release": 1.5}},
                        {"name": "Overtone", "config": {"frequency": 220, "wave_type": "triangle", "duration": 4.0, "volume": 0.25, "attack": 1.0, "decay": 0.5, "sustain": 0.85, "release": 1.5}},
                        {"name": "Whisper", "config": {"frequency": 440, "wave_type": "sine", "duration": 4.0, "volume": 0.15, "attack": 1.2, "decay": 0.5, "sustain": 0.8, "release": 1.5}}
                    ]
                }
            }
        },
        "User Interface": {
            "Clicks": {
                "Button Click": {
                    "playback_mode": "sequential",
                    "layers": [
                        {"name": "Click", "config": {"frequency": 800, "wave_type": "sine", "duration": 0.05, "volume": 0.5, "attack": 0.001, "decay": 0.03, "sustain": 0.2, "release": 0.02}},
                        {"name": "Tail", "config": {"frequency": 400, "wave_type": "sine", "duration": 0.03, "volume": 0.3, "attack": 0.001, "decay": 0.02, "sustain": 0.1, "release": 0.01}}
                    ]
                },
                "Toggle On": {
                    "playback_mode": "sequential",
                    "layers": [
                        {"name": "Low", "config": {"frequency": 400, "wave_type": "sine", "duration": 0.08, "volume": 0.4, "attack": 0.01, "decay": 0.04, "sustain": 0.3, "release": 0.03}},
                        {"name": "High", "config": {"frequency": 800, "wave_type": "sine", "duration": 0.08, "volume": 0.4, "attack": 0.01, "decay": 0.04, "sustain": 0.3, "release": 0.03}}
                    ]
                },
                "Toggle Off": {
                    "playback_mode": "sequential",
                    "layers": [
                        {"name": "High", "config": {"frequency": 800, "wave_type": "sine", "duration": 0.08, "volume": 0.4, "attack": 0.01, "decay": 0.04, "sustain": 0.3, "release": 0.03}},
                        {"name": "Low", "config": {"frequency": 400, "wave_type": "sine", "duration": 0.08, "volume": 0.4, "attack": 0.01, "decay": 0.04, "sustain": 0.3, "release": 0.03}}
                    ]
                }
            },
            "Notifications": {
                "Success": {
                    "playback_mode": "sequential",
                    "layers": [
                        {"name": "Ding 1", "config": {"frequency": 523.25, "wave_type": "sine", "duration": 0.2, "volume": 0.5, "attack": 0.01, "decay": 0.1, "sustain": 0.4, "release": 0.09}},
                        {"name": "Ding 2", "config": {"frequency": 659.25, "wave_type": "sine", "duration": 0.25, "volume": 0.5, "attack": 0.01, "decay": 0.12, "sustain": 0.4, "release": 0.12}}
                    ]
                },
                "Error": {
                    "playback_mode": "simultaneous",
                    "layers": [
                        {"name": "Buzz", "config": {"frequency": 150, "wave_type": "square", "duration": 0.3, "volume": 0.5, "attack": 0.01, "decay": 0.15, "sustain": 0.3, "release": 0.14}},
                        {"name": "Harsh", "config": {"frequency": 200, "wave_type": "sawtooth", "duration": 0.3, "volume": 0.3, "attack": 0.01, "decay": 0.15, "sustain": 0.3, "release": 0.14}}
                    ]
                },
                "Message": {
                    "playback_mode": "sequential",
                    "layers": [
                        {"name": "Tone 1", "config": {"frequency": 440, "wave_type": "sine", "duration": 0.15, "volume": 0.4, "attack": 0.01, "decay": 0.08, "sustain": 0.3, "release": 0.06}},
                        {"name": "Tone 2", "config": {"frequency": 554.37, "wave_type": "sine", "duration": 0.2, "volume": 0.4, "attack": 0.01, "decay": 0.1, "sustain": 0.3, "release": 0.09}}
                    ]
                }
            }
        },
        "Game Sounds": {
            "Weapons": {
                "Laser Gun": {
                    "playback_mode": "simultaneous",
                    "layers": [
                        {"name": "Beam", "config": {"frequency": 1200, "wave_type": "square", "duration": 0.25, "volume": 0.6, "attack": 0.001, "decay": 0.1, "sustain": 0.3, "release": 0.14}},
                        {"name": "Zap", "config": {"frequency": 2400, "wave_type": "sawtooth", "duration": 0.2, "volume": 0.4, "attack": 0.001, "decay": 0.08, "sustain": 0.2, "release": 0.11}}
                    ]
                },
                "Sword Swing": {
                    "playback_mode": "sequential",
                    "layers": [
                        {"name": "Whoosh", "config": {"frequency": 400, "wave_type": "sawtooth", "duration": 0.3, "volume": 0.5, "attack": 0.05, "decay": 0.1, "sustain": 0.4, "release": 0.15}},
                        {"name": "Whistle", "config": {"frequency": 800, "wave_type": "sine", "duration": 0.2, "volume": 0.3, "attack": 0.03, "decay": 0.08, "sustain": 0.3, "release": 0.09}}
                    ]
                }
            },
            "Pickups": {
                "Coin": {
                    "playback_mode": "sequential",
                    "layers": [
                        {"name": "Pling 1", "config": {"frequency": 987.77, "wave_type": "sine", "duration": 0.15, "volume": 0.5, "attack": 0.01, "decay": 0.08, "sustain": 0.2, "release": 0.06}},
                        {"name": "Pling 2", "config": {"frequency": 1318.51, "wave_type": "sine", "duration": 0.2, "volume": 0.4, "attack": 0.01, "decay": 0.1, "sustain": 0.2, "release": 0.09}}
                    ]
                },
                "Power Up": {
                    "playback_mode": "sequential",
                    "layers": [
                        {"name": "Rise 1", "config": {"frequency": 200, "wave_type": "triangle", "duration": 0.15, "volume": 0.5, "attack": 0.02, "decay": 0.06, "sustain": 0.4, "release": 0.07}},
                        {"name": "Rise 2", "config": {"frequency": 400, "wave_type": "triangle", "duration": 0.15, "volume": 0.5, "attack": 0.02, "decay": 0.06, "sustain": 0.4, "release": 0.07}},
                        {"name": "Rise 3", "config": {"frequency": 800, "wave_type": "sine", "duration": 0.2, "volume": 0.5, "attack": 0.02, "decay": 0.08, "sustain": 0.4, "release": 0.1}}
                    ]
                }
            },
            "Enemies": {
                "Alien Growl": {
                    "playback_mode": "simultaneous",
                    "layers": [
                        {"name": "Low", "config": {"frequency": 80, "wave_type": "sawtooth", "duration": 0.8, "volume": 0.6, "attack": 0.1, "decay": 0.3, "sustain": 0.5, "release": 0.4}},
                        {"name": "Growl", "config": {"frequency": 120, "wave_type": "square", "duration": 0.8, "volume": 0.4, "attack": 0.12, "decay": 0.28, "sustain": 0.5, "release": 0.4}},
                        {"name": "Texture", "config": {"frequency": 240, "wave_type": "triangle", "duration": 0.8, "volume": 0.2, "attack": 0.15, "decay": 0.25, "sustain": 0.4, "release": 0.4}}
                    ]
                },
                "Robot Beep": {
                    "playback_mode": "sequential",
                    "layers": [
                        {"name": "Beep 1", "config": {"frequency": 600, "wave_type": "square", "duration": 0.1, "volume": 0.5, "attack": 0.01, "decay": 0.05, "sustain": 0.3, "release": 0.04}},
                        {"name": "Beep 2", "config": {"frequency": 800, "wave_type": "square", "duration": 0.1, "volume": 0.5, "attack": 0.01, "decay": 0.05, "sustain": 0.3, "release": 0.04}},
                        {"name": "Beep 3", "config": {"frequency": 600, "wave_type": "square", "duration": 0.15, "volume": 0.5, "attack": 0.01, "decay": 0.08, "sustain": 0.3, "release": 0.06}}
                    ]
                }
            }
        }
    }
