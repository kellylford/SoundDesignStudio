"""
Keyboard Recorder for Sound Design Studio
Allows recording instrument sequences using computer keyboard
Fully accessible with screen reader support
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QComboBox, QGroupBox, QTextEdit)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QKeyEvent
import time
import numpy as np
from simple_audio_player import EnhancedAudioPlayer, PlayAudioConfig


class KeyboardRecorderDialog(QDialog):
    """Dialog for recording instrument sequences using computer keyboard."""
    
    # Keyboard mapping for notes
    WHITE_KEYS = {
        Qt.Key.Key_A: ('C', 0),
        Qt.Key.Key_S: ('D', 2),
        Qt.Key.Key_D: ('E', 4),
        Qt.Key.Key_F: ('F', 5),
        Qt.Key.Key_G: ('G', 7),
        Qt.Key.Key_H: ('A', 9),
        Qt.Key.Key_J: ('B', 11),
        Qt.Key.Key_K: ('C', 12),  # Higher C
    }
    
    BLACK_KEYS = {
        Qt.Key.Key_W: ('C#', 1),
        Qt.Key.Key_E: ('D#', 3),
        Qt.Key.Key_R: ('F#', 6),
        Qt.Key.Key_T: ('G#', 8),
        Qt.Key.Key_Y: ('A#', 10),
    }
    
    def __init__(self, parent, audio_player, soundfont_path):
        super().__init__(parent)
        self.parent_studio = parent
        self.audio_player = audio_player
        self.soundfont_path = soundfont_path
        
        # Recording state
        self.is_recording = False
        self.recorded_notes = []  # List of (timestamp, note_name, midi_note, duration)
        self.recording_start_time = 0
        self.pressed_keys = {}  # Track key press times
        
        # Playback state
        self.current_octave = 4  # Middle C octave
        self.current_instrument = 0  # Acoustic Grand Piano
        self.currently_playing = set()  # Track which keys are currently pressed
        
        # Focus mode
        self.keyboard_focus_mode = True  # True = keyboard plays notes, False = controls focused
        
        self.setup_ui()
        self.setWindowTitle("Record Instrument Sequence")
        self.resize(700, 600)
        
    def setup_ui(self):
        """Build the user interface."""
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel(
            "Use your computer keyboard to play and record instrument sequences.\n"
            "Press Tab to switch between keyboard play mode and controls.\n"
            "Use arrow keys to navigate controls when focused."
        )
        instructions.setWordWrap(True)
        instructions.setAccessibleName("Instructions for keyboard recorder")
        layout.addWidget(instructions)
        
        # Instrument selector
        instrument_group = QGroupBox("Instrument Selection")
        instrument_layout = QVBoxLayout()
        
        instrument_label = QLabel("Select Instrument:")
        instrument_layout.addWidget(instrument_label)
        
        self.instrument_combo = QComboBox()
        self.instrument_combo.setAccessibleName("Instrument selector")
        self.instrument_combo.setAccessibleDescription("Choose which instrument to play and record")
        
        # Add all 128 General MIDI instruments
        gm_instruments = [
            "0 - Acoustic Grand Piano", "1 - Bright Acoustic Piano", "2 - Electric Grand Piano",
            "3 - Honky-tonk Piano", "4 - Electric Piano 1", "5 - Electric Piano 2",
            "6 - Harpsichord", "7 - Clavinet", "8 - Celesta", "9 - Glockenspiel",
            "10 - Music Box", "11 - Vibraphone", "12 - Marimba", "13 - Xylophone",
            "14 - Tubular Bells", "15 - Dulcimer", "16 - Drawbar Organ", "17 - Percussive Organ",
            "18 - Rock Organ", "19 - Church Organ", "20 - Reed Organ", "21 - Accordion",
            "22 - Harmonica", "23 - Tango Accordion", "24 - Acoustic Guitar (nylon)",
            "25 - Acoustic Guitar (steel)", "26 - Electric Guitar (jazz)", "27 - Electric Guitar (clean)",
            "28 - Electric Guitar (muted)", "29 - Overdriven Guitar", "30 - Distortion Guitar",
            "31 - Guitar Harmonics", "32 - Acoustic Bass", "33 - Electric Bass (finger)",
            "34 - Electric Bass (pick)", "35 - Fretless Bass", "36 - Slap Bass 1",
            "37 - Slap Bass 2", "38 - Synth Bass 1", "39 - Synth Bass 2",
            "40 - Violin", "41 - Viola", "42 - Cello", "43 - Contrabass",
            "44 - Tremolo Strings", "45 - Pizzicato Strings", "46 - Orchestral Harp",
            "47 - Timpani", "48 - String Ensemble 1", "49 - String Ensemble 2",
            "50 - Synth Strings 1", "51 - Synth Strings 2", "52 - Choir Aahs",
            "53 - Voice Oohs", "54 - Synth Choir", "55 - Orchestra Hit",
            "56 - Trumpet", "57 - Trombone", "58 - Tuba", "59 - Muted Trumpet",
            "60 - French Horn", "61 - Brass Section", "62 - Synth Brass 1",
            "63 - Synth Brass 2", "64 - Soprano Sax", "65 - Alto Sax",
            "66 - Tenor Sax", "67 - Baritone Sax", "68 - Oboe", "69 - English Horn",
            "70 - Bassoon", "71 - Clarinet", "72 - Piccolo", "73 - Flute",
            "74 - Recorder", "75 - Pan Flute", "76 - Blown bottle", "77 - Shakuhachi",
            "78 - Whistle", "79 - Ocarina", "80 - Lead 1 (square)", "81 - Lead 2 (sawtooth)",
            "82 - Lead 3 (calliope)", "83 - Lead 4 (chiff)", "84 - Lead 5 (charang)",
            "85 - Lead 6 (voice)", "86 - Lead 7 (fifths)", "87 - Lead 8 (bass + lead)",
            "88 - Pad 1 (new age)", "89 - Pad 2 (warm)", "90 - Pad 3 (polysynth)",
            "91 - Pad 4 (choir)", "92 - Pad 5 (bowed)", "93 - Pad 6 (metallic)",
            "94 - Pad 7 (halo)", "95 - Pad 8 (sweep)", "96 - FX 1 (rain)",
            "97 - FX 2 (soundtrack)", "98 - FX 3 (crystal)", "99 - FX 4 (atmosphere)",
            "100 - FX 5 (brightness)", "101 - FX 6 (goblins)", "102 - FX 7 (echoes)",
            "103 - FX 8 (sci-fi)", "104 - Sitar", "105 - Banjo", "106 - Shamisen",
            "107 - Koto", "108 - Kalimba", "109 - Bagpipe", "110 - Fiddle",
            "111 - Shanai", "112 - Tinkle Bell", "113 - Agogo", "114 - Steel Drums",
            "115 - Woodblock", "116 - Taiko Drum", "117 - Melodic Tom", "118 - Synth Drum",
            "119 - Reverse Cymbal", "120 - Guitar Fret Noise", "121 - Breath Noise",
            "122 - Seashore", "123 - Bird Tweet", "124 - Telephone Ring",
            "125 - Helicopter", "126 - Applause", "127 - Gunshot"
        ]
        
        self.instrument_combo.addItems(gm_instruments)
        self.instrument_combo.currentIndexChanged.connect(self.on_instrument_changed)
        instrument_layout.addWidget(self.instrument_combo)
        
        instrument_group.setLayout(instrument_layout)
        layout.addWidget(instrument_group)
        
        # Octave controls
        octave_group = QGroupBox("Octave Control")
        octave_layout = QHBoxLayout()
        
        self.octave_down_btn = QPushButton("Decrease Octave (Minus key)")
        self.octave_down_btn.setAccessibleName("Decrease octave")
        self.octave_down_btn.setAccessibleDescription("Lower the octave by 1. Keyboard shortcut: Minus key")
        self.octave_down_btn.clicked.connect(self.decrease_octave)
        octave_layout.addWidget(self.octave_down_btn)
        
        self.octave_label = QLabel(f"Current Octave: {self.current_octave}")
        self.octave_label.setAccessibleName("Current octave display")
        self.octave_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        octave_layout.addWidget(self.octave_label)
        
        self.octave_up_btn = QPushButton("Increase Octave (Plus key)")
        self.octave_up_btn.setAccessibleName("Increase octave")
        self.octave_up_btn.setAccessibleDescription("Raise the octave by 1. Keyboard shortcut: Plus or Equals key")
        self.octave_up_btn.clicked.connect(self.increase_octave)
        octave_layout.addWidget(self.octave_up_btn)
        
        octave_group.setLayout(octave_layout)
        layout.addWidget(octave_group)
        
        # Keyboard layout display
        keyboard_group = QGroupBox("Keyboard Layout")
        keyboard_layout = QVBoxLayout()
        
        keyboard_info = QLabel(
            "WHITE KEYS (Home row):\n"
            "A=C, S=D, D=E, F=F, G=G, H=A, J=B, K=C (higher)\n\n"
            "BLACK KEYS (Top row):\n"
            "W=C#, E=D#, R=F#, T=G#, Y=A#"
        )
        keyboard_info.setAccessibleName("Keyboard layout reference")
        keyboard_info.setWordWrap(True)
        keyboard_layout.addWidget(keyboard_info)
        
        keyboard_group.setLayout(keyboard_layout)
        layout.addWidget(keyboard_group)
        
        # Recording controls
        recording_group = QGroupBox("Recording Controls")
        recording_layout = QVBoxLayout()
        
        self.recording_status = QLabel("Status: Ready to record")
        self.recording_status.setAccessibleName("Recording status")
        self.recording_status.setAccessibleDescription("Shows current recording status and note count")
        recording_layout.addWidget(self.recording_status)
        
        btn_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Start Recording")
        self.start_btn.setAccessibleName("Start recording button")
        self.start_btn.setAccessibleDescription("Begin recording your keyboard performance")
        self.start_btn.clicked.connect(self.start_recording)
        btn_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("Stop Recording")
        self.stop_btn.setAccessibleName("Stop recording button")
        self.stop_btn.setAccessibleDescription("Stop recording and review your performance")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_recording)
        btn_layout.addWidget(self.stop_btn)
        
        self.clear_btn = QPushButton("Clear Recording")
        self.clear_btn.setAccessibleName("Clear recording button")
        self.clear_btn.setAccessibleDescription("Delete the current recording and start over")
        self.clear_btn.clicked.connect(self.clear_recording)
        btn_layout.addWidget(self.clear_btn)
        
        recording_layout.addLayout(btn_layout)
        recording_group.setLayout(recording_layout)
        layout.addWidget(recording_group)
        
        # Notes display
        notes_group = QGroupBox("Recorded Notes")
        notes_layout = QVBoxLayout()
        
        self.notes_display = QTextEdit()
        self.notes_display.setAccessibleName("Recorded notes display")
        self.notes_display.setAccessibleDescription("Shows all notes that have been recorded with timing")
        self.notes_display.setReadOnly(True)
        self.notes_display.setMaximumHeight(100)
        notes_layout.addWidget(self.notes_display)
        
        notes_group.setLayout(notes_layout)
        layout.addWidget(notes_group)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        self.use_btn = QPushButton("Use Recording")
        self.use_btn.setAccessibleName("Use recording button")
        self.use_btn.setAccessibleDescription("Convert your recording into a sound layer")
        self.use_btn.clicked.connect(self.use_recording)
        self.use_btn.setEnabled(False)
        action_layout.addWidget(self.use_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setAccessibleName("Cancel button")
        self.cancel_btn.setAccessibleDescription("Close this dialog without using the recording")
        self.cancel_btn.clicked.connect(self.reject)
        action_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(action_layout)
        
        # Set focus mode indicator
        self.focus_indicator = QLabel("Mode: Keyboard Play (Press Tab to switch to controls)")
        self.focus_indicator.setAccessibleName("Focus mode indicator")
        self.focus_indicator.setStyleSheet("font-weight: bold; color: blue;")
        layout.insertWidget(1, self.focus_indicator)
        
    def keyPressEvent(self, event: QKeyEvent):
        """Handle key press events."""
        key = event.key()
        
        # Tab switches between keyboard play and controls
        if key == Qt.Key.Key_Tab:
            self.keyboard_focus_mode = not self.keyboard_focus_mode
            if self.keyboard_focus_mode:
                self.focus_indicator.setText("Mode: Keyboard Play (Press Tab to switch to controls)")
                self.setFocus()
            else:
                self.focus_indicator.setText("Mode: Controls (Use arrows to navigate, Tab to return to keyboard)")
                self.instrument_combo.setFocus()
            event.accept()
            return
        
        # If in control focus mode, let Qt handle it
        if not self.keyboard_focus_mode:
            super().keyPressEvent(event)
            return
        
        # Handle octave changes
        if key in (Qt.Key.Key_Plus, Qt.Key.Key_Equal):
            self.increase_octave()
            event.accept()
            return
        elif key in (Qt.Key.Key_Minus, Qt.Key.Key_Underscore):
            self.decrease_octave()
            event.accept()
            return
        
        # Prevent repeated key events (when key is held down)
        if event.isAutoRepeat():
            event.accept()
            return
        
        # Check if this is a note key
        note_info = None
        if key in self.WHITE_KEYS:
            note_info = self.WHITE_KEYS[key]
        elif key in self.BLACK_KEYS:
            note_info = self.BLACK_KEYS[key]
        
        if note_info:
            note_name, semitone_offset = note_info
            midi_note = 12 * self.current_octave + semitone_offset
            
            # Play the note
            self.play_note(midi_note, note_name)
            
            # Track key press for recording
            if self.is_recording:
                press_time = time.time() - self.recording_start_time
                self.pressed_keys[key] = (press_time, note_name, midi_note)
            
            event.accept()
        else:
            super().keyPressEvent(event)
    
    def keyReleaseEvent(self, event: QKeyEvent):
        """Handle key release events."""
        if event.isAutoRepeat():
            event.accept()
            return
        
        key = event.key()
        
        # If in control focus mode, let Qt handle it
        if not self.keyboard_focus_mode:
            super().keyReleaseEvent(event)
            return
        
        # Check if this was a note key
        if key in self.pressed_keys:
            press_time, note_name, midi_note = self.pressed_keys[key]
            release_time = time.time() - self.recording_start_time
            duration = release_time - press_time
            
            # Record the note with duration
            if self.is_recording:
                self.recorded_notes.append((press_time, note_name, midi_note, duration))
                self.update_notes_display()
            
            del self.pressed_keys[key]
            event.accept()
        else:
            super().keyReleaseEvent(event)
    
    def play_note(self, midi_note, note_name):
        """Play a single note immediately."""
        try:
            # Use the audio player's soundfont player
            if hasattr(self.audio_player, 'soundfont_player') and self.audio_player.soundfont_player:
                sp = self.audio_player.soundfont_player
                
                # Load soundfont if needed
                if sp.current_soundfont_path != self.soundfont_path:
                    sp.load_soundfont(self.soundfont_path)
                
                # Generate short note
                audio = sp.generate_note(midi_note, 100, 0.3, self.current_instrument, 0)
                
                # Play it
                import sounddevice as sd
                sd.play(audio * 0.5, 44100)  # Lower volume for live playing
        except Exception as e:
            print(f"Error playing note: {e}")
    
    def on_instrument_changed(self, index):
        """Handle instrument selection change."""
        self.current_instrument = index
    
    def increase_octave(self):
        """Increase the current octave."""
        if self.current_octave < 7:
            self.current_octave += 1
            self.octave_label.setText(f"Current Octave: {self.current_octave}")
            self.octave_label.setAccessibleDescription(f"Current octave is {self.current_octave}")
    
    def decrease_octave(self):
        """Decrease the current octave."""
        if self.current_octave > 1:
            self.current_octave -= 1
            self.octave_label.setText(f"Current Octave: {self.current_octave}")
            self.octave_label.setAccessibleDescription(f"Current octave is {self.current_octave}")
    
    def start_recording(self):
        """Start recording notes."""
        self.is_recording = True
        self.recorded_notes = []
        self.pressed_keys = {}
        self.recording_start_time = time.time()
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.use_btn.setEnabled(False)
        
        self.recording_status.setText("Status: RECORDING - Play your sequence")
        self.recording_status.setAccessibleDescription("Recording in progress. Play notes on the keyboard.")
        self.recording_status.setStyleSheet("color: red; font-weight: bold;")
        
        # Switch to keyboard mode for recording
        self.keyboard_focus_mode = True
        self.focus_indicator.setText("Mode: Keyboard Play - RECORDING")
        self.setFocus()
    
    def stop_recording(self):
        """Stop recording notes."""
        self.is_recording = False
        
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        note_count = len(self.recorded_notes)
        self.recording_status.setText(f"Status: Recording complete - {note_count} notes captured")
        self.recording_status.setAccessibleDescription(f"Recording stopped. {note_count} notes were recorded.")
        self.recording_status.setStyleSheet("")
        
        if note_count > 0:
            self.use_btn.setEnabled(True)
        
        self.focus_indicator.setText("Mode: Keyboard Play (Press Tab to switch to controls)")
    
    def clear_recording(self):
        """Clear the current recording."""
        self.recorded_notes = []
        self.pressed_keys = {}
        self.notes_display.clear()
        self.recording_status.setText("Status: Ready to record")
        self.recording_status.setAccessibleDescription("Ready to start recording")
        self.use_btn.setEnabled(False)
    
    def update_notes_display(self):
        """Update the display of recorded notes."""
        text = ""
        for i, (timestamp, note_name, midi_note, duration) in enumerate(self.recorded_notes, 1):
            text += f"{i}. {note_name} (MIDI {midi_note}) at {timestamp:.2f}s, duration {duration:.2f}s\n"
        self.notes_display.setPlainText(text)
    
    def use_recording(self):
        """Convert recording into layers and close dialog."""
        if not self.recorded_notes:
            return
        
        # Store the recording data for the parent to use
        self.recording_data = {
            'instrument': self.current_instrument,
            'instrument_name': self.instrument_combo.currentText(),
            'notes': self.recorded_notes,
            'soundfont_path': self.soundfont_path
        }
        
        self.accept()
