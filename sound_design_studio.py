"""
Sound Design Studio - Document-Centric Multi-Layer Sound Design

A professional sound synthesis tool with a document-based workflow.
Each "sound document" can contain multiple layers that play sequentially or simultaneously.

Features:
- Document-based workflow with sound layers
- Multi-layer composition (sequential or simultaneous playback)
- Integrated design interface accessible via menu
- Full keyboard navigation
- Menu bar for all operations

Keyboard Shortcuts:
- Alt+P: Play all layers (mixed/sequential based on playback mode)
- Alt+Shift+P: Play focused layer only
- Alt+R: Open Presets menu
- Left/Right Arrow: Navigate between sound layers
- Ctrl+N: New sound document
- Ctrl+S: Save sound document
- Ctrl+O: Open sound document
"""

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSlider, QComboBox, QPushButton, QGroupBox, QTextEdit,
    QCheckBox, QSpinBox, QDoubleSpinBox, QListWidget, QListWidgetItem,
    QMessageBox, QFileDialog, QTabWidget, QGridLayout, QLineEdit, QDialog,
    QMenuBar, QMenu, QSplitter, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QKeySequence, QShortcut, QAction, QIcon
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# Import local audio player (no external dependencies needed)
from simple_audio_player import EnhancedAudioPlayer, PlayAudioConfig
from preset_library import get_preset_library
from keyboard_recorder import KeyboardRecorderDialog


class SoundLayer:
    """Represents a single sound layer in a multi-layer sound composition."""
    
    def __init__(self, name="Untitled Layer", blank=False):
        self.name = name
        self.config = self._blank_config() if blank else self._default_config()
    
    def _default_config(self):
        """Create default sound configuration for this layer."""
        from audio_effects import AudioEffectsProcessor
        from soundfont_player import SoundFontPlayer
        
        return {
            'frequency': 440.0,
            'wave_type': 'sine',
            'duration': 0.5,
            'volume': 0.3,
            'attack': 0.01,
            'decay': 0.1,
            'sustain': 0.7,
            'release': 0.15,
            'overlap': 0.0,  # Overlap with previous layer in sequential mode (in seconds)
            'harmonics': {
                'enabled': True,
                'octave_volume': 0.3,
                'fifth_volume': 0.2,
                'sub_bass_volume': 0.0
            },
            'blending': {
                'enabled': True,
                'blend_ratio': 0.5
            },
            'advanced': {
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
            },
            'effects': AudioEffectsProcessor().get_default_effects_config(),
            'soundfont': SoundFontPlayer().get_default_soundfont_config(),
            'play_type': 'custom'
        }
    
    def _blank_config(self):
        """Create blank/minimal sound configuration for a new layer."""
        from audio_effects import AudioEffectsProcessor
        from soundfont_player import SoundFontPlayer
        
        return {
            'frequency': 440.0,
            'wave_type': 'sine',
            'duration': 0.5,
            'volume': 0.0,  # Start with no volume
            'attack': 0.0,
            'decay': 0.0,
            'sustain': 1.0,
            'release': 0.0,
            'overlap': 0.0,
            'harmonics': {
                'enabled': False,
                'octave_volume': 0.0,
                'fifth_volume': 0.0,
                'sub_bass_volume': 0.0
            },
            'blending': {
                'enabled': False,
                'blend_ratio': 0.0
            },
            'advanced': {
                'enabled': False,
                'synthesis_type': 'fm',
                'fm_mod_ratio': 1.0,
                'fm_mod_index': 0.0,
                'noise_type': 'white',
                'noise_filter_enabled': False,
                'noise_filter_type': 'bandpass',
                'noise_filter_low': 2000.0,
                'noise_filter_high': 8000.0,
                'lfo_enabled': False,
                'lfo_frequency': 5.0,
                'lfo_depth': 0.0,
                'echo_enabled': False,
                'echo_delay': 0.0,
                'echo_feedback': 0.0
            },
            'effects': AudioEffectsProcessor().get_default_effects_config(),
            'soundfont': SoundFontPlayer().get_default_soundfont_config(),
            'play_type': 'custom'
        }
    
    def copy(self):
        """Create a deep copy of this layer."""
        import copy as copy_module
        new_layer = SoundLayer(self.name + " (copy)")
        new_layer.config = copy_module.deepcopy(self.config)
        return new_layer


class SoundDocument:
    """Represents a sound document containing multiple layers."""
    
    def __init__(self, name="Untitled Sound"):
        self.name = name
        self.description = ""
        self.layers: List[SoundLayer] = []
        self.playback_mode = "sequential"  # "sequential" or "simultaneous"
        self.file_path = None
        
        # Start with no layers - user must add them
    
    def add_layer(self, name=None, blank=True):
        """Add a new sound layer to this document. New layers are blank by default."""
        if name is None:
            name = f"Layer {len(self.layers) + 1}"
        layer = SoundLayer(name, blank=blank)
        self.layers.append(layer)
        return layer
    
    def remove_layer(self, index):
        """Remove a layer by index. Can now remove all layers."""
        if 0 <= index < len(self.layers):
            del self.layers[index]
            return True
        return False
    
    def to_dict(self):
        """Convert document to dictionary for saving."""
        return {
            'name': self.name,
            'description': self.description,
            'playback_mode': self.playback_mode,
            'layers': [
                {'name': layer.name, 'config': layer.config}
                for layer in self.layers
            ]
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create document from dictionary."""
        doc = cls(data.get('name', 'Untitled Sound'))
        doc.description = data.get('description', '')
        doc.playback_mode = data.get('playback_mode', 'sequential')
        doc.layers = []
        
        for layer_data in data.get('layers', []):
            layer = SoundLayer(layer_data.get('name', 'Layer'))
            layer.config = layer_data.get('config', layer._default_config())
            doc.layers.append(layer)
        
        # Don't add a default layer - allow empty documents
        
        return doc


def load_parameter_help():
    """Load parameter help from JSON file."""
    help_file = Path(__file__).parent / "parameter_help.json"
    try:
        with open(help_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: parameter_help.json not found at {help_file}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Warning: Error parsing parameter_help.json: {e}")
        return {}


class ParameterHelpDialog(QDialog):
    """Dialog for displaying context-sensitive parameter help."""
    
    def __init__(self, parameter_key, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Parameter Help")
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(self)
        
        # Load help data from JSON file
        parameter_help = load_parameter_help()
        
        # Get help information
        help_info = parameter_help.get(parameter_key, {
            'title': 'Help',
            'description': 'No help available for this parameter.',
            'details': [],
            'tips': ''
        })
        
        # Title
        title_label = QLabel(f"<h2>{help_info['title']}</h2>")
        layout.addWidget(title_label)
        
        # Create list widget for screen reader compatibility
        help_list = QListWidget()
        help_list.setWordWrap(True)
        
        # Description
        desc_item = QListWidgetItem(f"📖 {help_info['description']}")
        help_list.addItem(desc_item)
        
        # Details
        if help_info.get('details'):
            help_list.addItem(QListWidgetItem(""))  # Spacer
            header_item = QListWidgetItem("Details:")
            header_item.setFlags(header_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            help_list.addItem(header_item)
            
            for detail in help_info['details']:
                detail_item = QListWidgetItem(f"  • {detail}")
                help_list.addItem(detail_item)
        
        # Tips
        if help_info.get('tips'):
            help_list.addItem(QListWidgetItem(""))  # Spacer
            tip_header = QListWidgetItem("💡 Tips:")
            tip_header.setFlags(tip_header.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            help_list.addItem(tip_header)
            tip_item = QListWidgetItem(f"  {help_info['tips']}")
            help_list.addItem(tip_item)
        
        layout.addWidget(help_list)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        # Set first item as selected
        help_list.setCurrentRow(0)


class PresetPreviewDialog(QDialog):
    """Dialog for previewing and selecting presets."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_studio = parent
        self.audio_player = parent.audio_player
        self.selected_preset_data = None
        self.selected_preset_name = None
        self.preset_map = {}  # Maps list items to preset data
        
        self.setWindowTitle("Preview Presets")
        self.setMinimumSize(600, 500)
        
        self.setup_ui()
        self.load_presets()
    
    def setup_ui(self):
        """Build the dialog UI."""
        layout = QVBoxLayout(self)
        
        # Info label
        info_label = QLabel("Use arrow keys to navigate and preview presets automatically")
        info_label.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(info_label)
        
        # Preset list
        self.preset_list = QListWidget()
        self.preset_list.currentItemChanged.connect(self.on_preset_selected)
        layout.addWidget(self.preset_list)
        
        # Preset info display
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setMaximumHeight(100)
        layout.addWidget(self.info_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.use_preset_btn = QPushButton("Use Preset")
        self.use_preset_btn.clicked.connect(self.use_preset)
        self.use_preset_btn.setEnabled(False)
        button_layout.addWidget(self.use_preset_btn)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.reject)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
    
    def load_presets(self):
        """Load all presets into the list."""
        preset_library = get_preset_library()
        
        # Flatten the hierarchical structure into a flat list
        for category, subcategories in preset_library.items():
            # Add category header (non-selectable)
            category_item = QListWidgetItem(f"═══ {category} ═══")
            category_item.setFlags(category_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            category_item.setData(Qt.ItemDataRole.UserRole, None)  # No preset data
            self.preset_list.addItem(category_item)
            
            for subcategory, presets in subcategories.items():
                # Add subcategory header (non-selectable)
                subcat_item = QListWidgetItem(f"  ── {subcategory} ──")
                subcat_item.setFlags(subcat_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                subcat_item.setData(Qt.ItemDataRole.UserRole, None)
                self.preset_list.addItem(subcat_item)
                
                for preset_name, preset_data in presets.items():
                    # Add preset item (selectable)
                    preset_item = QListWidgetItem(f"    {preset_name}")
                    preset_item.setData(Qt.ItemDataRole.UserRole, {
                        'name': preset_name,
                        'data': preset_data,
                        'category': category,
                        'subcategory': subcategory
                    })
                    self.preset_list.addItem(preset_item)
        
        # Select first selectable item
        for i in range(self.preset_list.count()):
            item = self.preset_list.item(i)
            if item.flags() & Qt.ItemFlag.ItemIsSelectable:
                self.preset_list.setCurrentItem(item)
                break
    
    def on_preset_selected(self, current, previous):
        """Handle preset selection - auto-play the preset."""
        if not current:
            self.use_preset_btn.setEnabled(False)
            self.info_text.clear()
            return
        
        preset_info = current.data(Qt.ItemDataRole.UserRole)
        if not preset_info:
            self.use_preset_btn.setEnabled(False)
            self.info_text.clear()
            return
        
        # Store selection
        self.selected_preset_name = preset_info['name']
        self.selected_preset_data = preset_info['data']
        self.use_preset_btn.setEnabled(True)
        
        # Display preset info
        info_html = f"<b>{preset_info['name']}</b><br>"
        info_html += f"<i>{preset_info['category']} → {preset_info['subcategory']}</i><br>"
        info_html += f"Layers: {len(preset_info['data'].get('layers', []))}, "
        info_html += f"Mode: {preset_info['data'].get('playback_mode', 'sequential').capitalize()}"
        self.info_text.setHtml(info_html)
        
        # Auto-play the preset
        self.play_preset(preset_info['data'])
    
    def play_preset(self, preset_data):
        """Play the selected preset."""
        try:
            playback_mode = preset_data.get('playback_mode', 'sequential')
            layers = preset_data.get('layers', [])
            
            if not layers:
                return
            
            if playback_mode == "sequential":
                # Play layers one after another
                for layer_data in layers:
                    config_dict = layer_data.get('config', {})
                    config = PlayAudioConfig(**config_dict)
                    self.audio_player.play_sound(config)
            else:
                # Simultaneous playback - mix all layers together
                configs = []
                for layer_data in layers:
                    config_dict = layer_data.get('config', {})
                    config = PlayAudioConfig(**config_dict)
                    configs.append(config)
                self.audio_player.play_mixed_sounds(configs)
        except Exception as e:
            # Silently fail for preview - don't interrupt navigation
            print(f"Preview error: {e}")
    
    def use_preset(self):
        """Add the selected preset to the parent's document."""
        if self.selected_preset_data and self.selected_preset_name:
            self.parent_studio.load_preset(self.selected_preset_data, self.selected_preset_name)
            self.accept()


class DesignDialog(QDialog):
    """Dialog containing the tabbed design interface from the original studio."""
    
    def __init__(self, parent, layer: SoundLayer):
        super().__init__(parent)
        self.layer = layer
        self.parent_studio = parent
        self.setWindowTitle(f"Design - {layer.name}")
        self.setMinimumSize(900, 700)
        
        # Map widgets to help keys for context-sensitive help
        self.widget_help_map = {}
        
        self.setup_ui()
        self.load_config_to_ui()
        self.setup_help_system()
    
    def setup_help_system(self):
        """Setup Shift+F1 context-sensitive help."""
        # Create shortcut for Shift+F1
        help_shortcut = QShortcut(QKeySequence("Shift+F1"), self)
        help_shortcut.activated.connect(self.show_context_help)
    
    def setup_ui(self):
        """Build the design interface."""
        layout = QVBoxLayout(self)
        
        # Top info section
        info_group = QGroupBox("Layer Information")
        info_layout = QVBoxLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setText(self.layer.name)
        self.name_input.setPlaceholderText("Layer name...")
        info_layout.addWidget(QLabel("Name:"))
        info_layout.addWidget(self.name_input)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Tabs for parameters
        tabs = QTabWidget()
        
        # Import the tab building methods from original studio
        # For now, we'll create a simplified version
        self.build_basic_tab(tabs)
        self.build_envelope_tab(tabs)
        self.build_harmonics_tab(tabs)
        self.build_fm_tab(tabs)
        self.build_noise_tab(tabs)
        self.build_effects_tab(tabs)
        self.build_audio_effects_tab(tabs)  # NEW: Professional audio effects
        self.build_soundfont_tab(tabs)      # NEW: SoundFont instruments
        
        layout.addWidget(tabs)
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        
        play_btn = QPushButton("Play")
        play_btn.clicked.connect(self.play_preview)
        button_layout.addWidget(play_btn)
        
        button_layout.addStretch()
        
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.apply_changes)
        button_layout.addWidget(apply_btn)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
    
    def build_basic_tab(self, tabs):
        """Build basic parameters tab."""
        basic_tab = QWidget()
        layout = QVBoxLayout(basic_tab)
        
        # Frequency
        freq_group = QGroupBox("Frequency")
        freq_layout = QVBoxLayout()
        self.freq_spin = QDoubleSpinBox()
        self.freq_spin.setRange(20, 2000)
        self.freq_spin.setValue(440)
        self.freq_spin.setSuffix(" Hz")
        self.widget_help_map[self.freq_spin] = 'frequency'
        freq_layout.addWidget(self.freq_spin)
        freq_group.setLayout(freq_layout)
        layout.addWidget(freq_group)
        
        # Wave type
        wave_group = QGroupBox("Waveform")
        wave_layout = QVBoxLayout()
        self.wave_combo = QComboBox()
        self.wave_combo.addItems(['sine', 'square', 'sawtooth', 'triangle'])
        self.widget_help_map[self.wave_combo] = 'waveform'
        wave_layout.addWidget(self.wave_combo)
        wave_group.setLayout(wave_layout)
        layout.addWidget(wave_group)
        
        # Duration
        dur_group = QGroupBox("Duration")
        dur_layout = QVBoxLayout()
        self.duration_spin = QDoubleSpinBox()
        self.duration_spin.setRange(0.1, 3.0)
        self.duration_spin.setValue(0.5)
        self.duration_spin.setSuffix(" sec")
        self.duration_spin.setSingleStep(0.1)
        self.widget_help_map[self.duration_spin] = 'duration'
        dur_layout.addWidget(self.duration_spin)
        dur_group.setLayout(dur_layout)
        layout.addWidget(dur_group)
        
        # Volume
        vol_group = QGroupBox("Volume")
        vol_layout = QVBoxLayout()
        self.volume_spin = QDoubleSpinBox()
        self.volume_spin.setRange(0.0, 1.0)
        self.volume_spin.setValue(0.3)
        self.volume_spin.setSingleStep(0.1)
        self.widget_help_map[self.volume_spin] = 'volume'
        vol_layout.addWidget(self.volume_spin)
        vol_group.setLayout(vol_layout)
        layout.addWidget(vol_group)
        
        # Overlap (for sequential playback)
        overlap_group = QGroupBox("Sequential Overlap")
        overlap_layout = QVBoxLayout()
        overlap_help = QLabel("Amount to overlap with previous layer (seconds)")
        overlap_help.setWordWrap(True)
        overlap_help.setStyleSheet("color: gray; font-size: 9pt;")
        overlap_layout.addWidget(overlap_help)
        self.overlap_spin = QDoubleSpinBox()
        self.overlap_spin.setRange(0.0, 2.0)
        self.overlap_spin.setValue(0.0)
        self.overlap_spin.setSuffix(" sec")
        self.overlap_spin.setSingleStep(0.05)
        self.widget_help_map[self.overlap_spin] = 'overlap'
        overlap_layout.addWidget(self.overlap_spin)
        overlap_group.setLayout(overlap_layout)
        layout.addWidget(overlap_group)
        
        layout.addStretch()
        tabs.addTab(basic_tab, "Basic")
    
    def build_envelope_tab(self, tabs):
        """Build ADSR envelope tab."""
        envelope_tab = QWidget()
        layout = QVBoxLayout(envelope_tab)
        
        self.attack_spin = self._create_param_spin("Attack", 0.0, 1.0, 0.01, 0.01)
        self.decay_spin = self._create_param_spin("Decay", 0.0, 1.0, 0.1, 0.01)
        self.sustain_spin = self._create_param_spin("Sustain", 0.0, 1.0, 0.7, 0.1)
        self.release_spin = self._create_param_spin("Release", 0.0, 1.0, 0.15, 0.01)
        
        # Register help for envelope parameters
        self.widget_help_map[self.attack_spin[1]] = 'attack'
        self.widget_help_map[self.decay_spin[1]] = 'decay'
        self.widget_help_map[self.sustain_spin[1]] = 'sustain'
        self.widget_help_map[self.release_spin[1]] = 'release'
        
        layout.addWidget(self.attack_spin[0])
        layout.addWidget(self.decay_spin[0])
        layout.addWidget(self.sustain_spin[0])
        layout.addWidget(self.release_spin[0])
        layout.addStretch()
        
        tabs.addTab(envelope_tab, "Envelope")
    
    def build_harmonics_tab(self, tabs):
        """Build harmonics tab."""
        harmonics_tab = QWidget()
        layout = QVBoxLayout(harmonics_tab)
        
        self.harmonics_enabled = QCheckBox("Enable Harmonics")
        self.harmonics_enabled.setChecked(True)
        layout.addWidget(self.harmonics_enabled)
        
        self.octave_spin = self._create_param_spin("Octave Volume", 0.0, 1.0, 0.3, 0.1)
        self.fifth_spin = self._create_param_spin("Fifth Volume", 0.0, 1.0, 0.2, 0.1)
        self.subbass_spin = self._create_param_spin("Sub-bass Volume", 0.0, 1.0, 0.0, 0.1)
        
        layout.addWidget(self.octave_spin[0])
        layout.addWidget(self.fifth_spin[0])
        layout.addWidget(self.subbass_spin[0])
        layout.addStretch()
        
        tabs.addTab(harmonics_tab, "Harmonics")
    
    def build_fm_tab(self, tabs):
        """Build FM synthesis tab."""
        fm_tab = QWidget()
        layout = QVBoxLayout(fm_tab)
        
        info_label = QLabel("FM (Frequency Modulation) synthesis creates complex harmonic timbres by using one oscillator to modulate the frequency of another.")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #666; font-style: italic; margin-bottom: 10px;")
        layout.addWidget(info_label)
        
        # FM parameters
        layout.addWidget(QLabel("Modulator Ratio:"))
        self.fm_ratio_spin = QDoubleSpinBox()
        self.fm_ratio_spin.setRange(0.5, 5.0)
        self.fm_ratio_spin.setValue(1.4)
        self.fm_ratio_spin.setSingleStep(0.1)
        self.widget_help_map[self.fm_ratio_spin] = 'fm_ratio'
        layout.addWidget(self.fm_ratio_spin)
        
        layout.addWidget(QLabel("Modulation Index:"))
        self.fm_index_spin = QDoubleSpinBox()
        self.fm_index_spin.setRange(0.0, 10.0)
        self.fm_index_spin.setValue(5.0)
        self.fm_index_spin.setSingleStep(0.5)
        self.widget_help_map[self.fm_index_spin] = 'fm_index'
        layout.addWidget(self.fm_index_spin)
        
        # Quick presets guide
        presets_group = QGroupBox("Quick FM Presets")
        presets_layout = QVBoxLayout()
        fm_desc = QLabel(
            "Common FM combinations:\n\n"
            "• Ratio 1.4, Index 5 → Bell-like tone\n"
            "• Ratio 14, Index 3 → Electric Piano\n"
            "• Ratio 1, Index 5 → Brass instrument\n"
            "• Ratio 0.5, Index 2 → Organ sound"
        )
        fm_desc.setWordWrap(True)
        presets_layout.addWidget(fm_desc)
        presets_group.setLayout(presets_layout)
        layout.addWidget(presets_group)
        
        layout.addStretch()
        tabs.addTab(fm_tab, "FM Synthesis")
    
    def build_noise_tab(self, tabs):
        """Build noise synthesis tab."""
        noise_tab = QWidget()
        layout = QVBoxLayout(noise_tab)
        
        info_label = QLabel("Noise generators create random waveforms useful for percussion, wind, and atmospheric effects.")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #666; font-style: italic; margin-bottom: 10px;")
        layout.addWidget(info_label)
        
        # Noise type
        layout.addWidget(QLabel("Noise Type:"))
        self.noise_type_combo = QComboBox()
        self.noise_type_combo.addItems(['white', 'pink', 'brown'])
        self.widget_help_map[self.noise_type_combo] = 'noise_type'
        layout.addWidget(self.noise_type_combo)
        
        noise_desc = QLabel(
            "• White: Equal energy across all frequencies (hi-hats, cymbals)\n"
            "• Pink: More energy in lower frequencies (ocean waves, wind)\n"
            "• Brown: Even more bass energy (thunder, rumble)"
        )
        noise_desc.setWordWrap(True)
        noise_desc.setStyleSheet("color: #666; font-size: 9pt; margin: 10px 0;")
        layout.addWidget(noise_desc)
        
        # Filter controls
        filter_group = QGroupBox("Noise Filter")
        filter_layout = QVBoxLayout()
        
        self.noise_filter_enabled = QCheckBox("Enable Noise Filter")
        self.widget_help_map[self.noise_filter_enabled] = 'noise_filter'
        filter_layout.addWidget(self.noise_filter_enabled)
        
        filter_layout.addWidget(QLabel("Filter Type:"))
        self.noise_filter_combo = QComboBox()
        self.noise_filter_combo.addItems(['bandpass', 'highpass', 'lowpass'])
        filter_layout.addWidget(self.noise_filter_combo)
        
        filter_layout.addWidget(QLabel("Filter Low Cutoff (Hz):"))
        self.filter_low_spin = QDoubleSpinBox()
        self.filter_low_spin.setRange(100, 10000)
        self.filter_low_spin.setValue(2000)
        self.filter_low_spin.setSuffix(" Hz")
        filter_layout.addWidget(self.filter_low_spin)
        
        filter_layout.addWidget(QLabel("Filter High Cutoff (Hz):"))
        self.filter_high_spin = QDoubleSpinBox()
        self.filter_high_spin.setRange(100, 10000)
        self.filter_high_spin.setValue(8000)
        self.filter_high_spin.setSuffix(" Hz")
        filter_layout.addWidget(self.filter_high_spin)
        
        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)
        
        layout.addStretch()
        tabs.addTab(noise_tab, "Noise")
    
    def build_effects_tab(self, tabs):
        """Build effects tab."""
        effects_tab = QWidget()
        layout = QVBoxLayout(effects_tab)
        
        info_label = QLabel("Apply modulation and time-based effects to any sound.")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #666; font-style: italic; margin-bottom: 10px;")
        layout.addWidget(info_label)
        
        # LFO controls
        lfo_group = QGroupBox("LFO Tremolo")
        lfo_layout = QVBoxLayout()
        
        self.lfo_enabled = QCheckBox("Enable LFO Tremolo")
        self.widget_help_map[self.lfo_enabled] = 'lfo'
        lfo_layout.addWidget(self.lfo_enabled)
        
        lfo_layout.addWidget(QLabel("LFO Frequency (Hz):"))
        self.lfo_freq_spin = QDoubleSpinBox()
        self.lfo_freq_spin.setRange(0.5, 10.0)
        self.lfo_freq_spin.setValue(5.0)
        self.lfo_freq_spin.setSingleStep(0.5)
        self.widget_help_map[self.lfo_freq_spin] = 'lfo'
        lfo_layout.addWidget(self.lfo_freq_spin)
        
        lfo_layout.addWidget(QLabel("LFO Depth (%):"))
        self.lfo_depth_spin = QDoubleSpinBox()
        self.lfo_depth_spin.setRange(0, 100)
        self.lfo_depth_spin.setValue(30)
        self.lfo_depth_spin.setSuffix("%")
        self.widget_help_map[self.lfo_depth_spin] = 'lfo'
        lfo_layout.addWidget(self.lfo_depth_spin)
        
        lfo_desc = QLabel("Tremolo creates rhythmic volume variations. Try 5-8 Hz for vibrato effects.")
        lfo_desc.setWordWrap(True)
        lfo_desc.setStyleSheet("color: #666; font-size: 9pt;")
        lfo_layout.addWidget(lfo_desc)
        
        lfo_group.setLayout(lfo_layout)
        layout.addWidget(lfo_group)
        
        # Echo controls
        echo_group = QGroupBox("Echo / Delay")
        echo_layout = QVBoxLayout()
        
        self.echo_enabled = QCheckBox("Enable Echo/Delay")
        self.widget_help_map[self.echo_enabled] = 'echo'
        echo_layout.addWidget(self.echo_enabled)
        
        echo_layout.addWidget(QLabel("Echo Delay (seconds):"))
        self.echo_delay_spin = QDoubleSpinBox()
        self.echo_delay_spin.setRange(0.05, 1.0)
        self.echo_delay_spin.setValue(0.3)
        self.echo_delay_spin.setSingleStep(0.05)
        self.echo_delay_spin.setSuffix(" sec")
        self.widget_help_map[self.echo_delay_spin] = 'echo'
        echo_layout.addWidget(self.echo_delay_spin)
        
        echo_layout.addWidget(QLabel("Echo Feedback (%):"))
        self.echo_feedback_spin = QDoubleSpinBox()
        self.echo_feedback_spin.setRange(0, 90)
        self.echo_feedback_spin.setValue(40)
        self.echo_feedback_spin.setSuffix("%")
        self.widget_help_map[self.echo_feedback_spin] = 'echo'
        echo_layout.addWidget(self.echo_feedback_spin)
        
        echo_desc = QLabel("Echo creates repeating delays. Lower feedback for subtle echoes, higher for dramatic repeats.")
        echo_desc.setWordWrap(True)
        echo_desc.setStyleSheet("color: #666; font-size: 9pt;")
        echo_layout.addWidget(echo_desc)
        
        echo_group.setLayout(echo_layout)
        layout.addWidget(echo_group)
        
        layout.addStretch()
        tabs.addTab(effects_tab, "Effects")
    
    def build_audio_effects_tab(self, tabs):
        """Build professional audio effects tab (Pedalboard)."""
        from audio_effects import PEDALBOARD_AVAILABLE
        
        effects_tab = QWidget()
        layout = QVBoxLayout(effects_tab)
        
        # Check if available
        if not PEDALBOARD_AVAILABLE:
            warning = QLabel("⚠️ Professional audio effects require 'pedalboard' library.\n\n"
                           "Install with: pip install pedalboard\n\n"
                           "These effects provide studio-quality reverb, delay, distortion, and more.")
            warning.setWordWrap(True)
            warning.setStyleSheet("color: #cc6600; padding: 20px;")
            layout.addWidget(warning)
            layout.addStretch()
            tabs.addTab(effects_tab, "🎛️ Audio FX")
            return
        
        info_label = QLabel("Professional studio-quality audio effects powered by Spotify's Pedalboard.")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #666; font-style: italic; margin-bottom: 10px;")
        layout.addWidget(info_label)
        
        # Create scroll area for all effects
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Master enable
        self.audio_effects_enabled = QCheckBox("Enable Audio Effects")
        self.audio_effects_enabled.setStyleSheet("font-weight: bold;")
        scroll_layout.addWidget(self.audio_effects_enabled)
        
        # Reverb
        reverb_group = QGroupBox("Reverb")
        reverb_layout = QVBoxLayout()
        
        self.reverb_enabled = QCheckBox("Enable Reverb")
        reverb_layout.addWidget(self.reverb_enabled)
        
        reverb_layout.addWidget(QLabel("Room Size:"))
        self.reverb_room_spin = QDoubleSpinBox()
        self.reverb_room_spin.setRange(0.0, 1.0)
        self.reverb_room_spin.setValue(0.5)
        self.reverb_room_spin.setSingleStep(0.1)
        reverb_layout.addWidget(self.reverb_room_spin)
        
        reverb_layout.addWidget(QLabel("Damping:"))
        self.reverb_damping_spin = QDoubleSpinBox()
        self.reverb_damping_spin.setRange(0.0, 1.0)
        self.reverb_damping_spin.setValue(0.5)
        self.reverb_damping_spin.setSingleStep(0.1)
        reverb_layout.addWidget(self.reverb_damping_spin)
        
        reverb_layout.addWidget(QLabel("Wet Level:"))
        self.reverb_wet_spin = QDoubleSpinBox()
        self.reverb_wet_spin.setRange(0.0, 1.0)
        self.reverb_wet_spin.setValue(0.3)
        self.reverb_wet_spin.setSingleStep(0.1)
        reverb_layout.addWidget(self.reverb_wet_spin)
        
        reverb_group.setLayout(reverb_layout)
        scroll_layout.addWidget(reverb_group)
        
        # Delay
        delay_group = QGroupBox("Delay")
        delay_layout = QVBoxLayout()
        
        self.delay_enabled = QCheckBox("Enable Delay")
        delay_layout.addWidget(self.delay_enabled)
        
        delay_layout.addWidget(QLabel("Delay Time (sec):"))
        self.delay_time_spin = QDoubleSpinBox()
        self.delay_time_spin.setRange(0.01, 2.0)
        self.delay_time_spin.setValue(0.5)
        self.delay_time_spin.setSingleStep(0.05)
        self.delay_time_spin.setSuffix(" sec")
        delay_layout.addWidget(self.delay_time_spin)
        
        delay_layout.addWidget(QLabel("Feedback:"))
        self.delay_feedback_spin = QDoubleSpinBox()
        self.delay_feedback_spin.setRange(0.0, 0.95)
        self.delay_feedback_spin.setValue(0.5)
        self.delay_feedback_spin.setSingleStep(0.05)
        delay_layout.addWidget(self.delay_feedback_spin)
        
        delay_layout.addWidget(QLabel("Mix:"))
        self.delay_mix_spin = QDoubleSpinBox()
        self.delay_mix_spin.setRange(0.0, 1.0)
        self.delay_mix_spin.setValue(0.5)
        self.delay_mix_spin.setSingleStep(0.1)
        delay_layout.addWidget(self.delay_mix_spin)
        
        delay_group.setLayout(delay_layout)
        scroll_layout.addWidget(delay_group)
        
        # Distortion
        distortion_group = QGroupBox("Distortion")
        distortion_layout = QVBoxLayout()
        
        self.distortion_enabled = QCheckBox("Enable Distortion")
        distortion_layout.addWidget(self.distortion_enabled)
        
        distortion_layout.addWidget(QLabel("Drive (dB):"))
        self.distortion_drive_spin = QDoubleSpinBox()
        self.distortion_drive_spin.setRange(0.0, 50.0)
        self.distortion_drive_spin.setValue(10.0)
        self.distortion_drive_spin.setSingleStep(1.0)
        self.distortion_drive_spin.setSuffix(" dB")
        distortion_layout.addWidget(self.distortion_drive_spin)
        
        distortion_group.setLayout(distortion_layout)
        scroll_layout.addWidget(distortion_group)
        
        # Chorus
        chorus_group = QGroupBox("Chorus")
        chorus_layout = QVBoxLayout()
        
        self.chorus_enabled = QCheckBox("Enable Chorus")
        chorus_layout.addWidget(self.chorus_enabled)
        
        chorus_layout.addWidget(QLabel("Rate (Hz):"))
        self.chorus_rate_spin = QDoubleSpinBox()
        self.chorus_rate_spin.setRange(0.1, 10.0)
        self.chorus_rate_spin.setValue(1.0)
        self.chorus_rate_spin.setSingleStep(0.1)
        self.chorus_rate_spin.setSuffix(" Hz")
        chorus_layout.addWidget(self.chorus_rate_spin)
        
        chorus_layout.addWidget(QLabel("Depth:"))
        self.chorus_depth_spin = QDoubleSpinBox()
        self.chorus_depth_spin.setRange(0.0, 1.0)
        self.chorus_depth_spin.setValue(0.25)
        self.chorus_depth_spin.setSingleStep(0.05)
        chorus_layout.addWidget(self.chorus_depth_spin)
        
        chorus_layout.addWidget(QLabel("Mix:"))
        self.chorus_mix_spin = QDoubleSpinBox()
        self.chorus_mix_spin.setRange(0.0, 1.0)
        self.chorus_mix_spin.setValue(0.5)
        self.chorus_mix_spin.setSingleStep(0.1)
        chorus_layout.addWidget(self.chorus_mix_spin)
        
        chorus_group.setLayout(chorus_layout)
        scroll_layout.addWidget(chorus_group)
        
        # Compressor
        compressor_group = QGroupBox("Compressor")
        compressor_layout = QVBoxLayout()
        
        self.compressor_enabled = QCheckBox("Enable Compressor")
        compressor_layout.addWidget(self.compressor_enabled)
        
        compressor_layout.addWidget(QLabel("Threshold (dB):"))
        self.compressor_threshold_spin = QDoubleSpinBox()
        self.compressor_threshold_spin.setRange(-60.0, 0.0)
        self.compressor_threshold_spin.setValue(-20.0)
        self.compressor_threshold_spin.setSingleStep(1.0)
        self.compressor_threshold_spin.setSuffix(" dB")
        compressor_layout.addWidget(self.compressor_threshold_spin)
        
        compressor_layout.addWidget(QLabel("Ratio:"))
        self.compressor_ratio_spin = QDoubleSpinBox()
        self.compressor_ratio_spin.setRange(1.0, 20.0)
        self.compressor_ratio_spin.setValue(4.0)
        self.compressor_ratio_spin.setSingleStep(0.5)
        compressor_layout.addWidget(self.compressor_ratio_spin)
        
        compressor_group.setLayout(compressor_layout)
        scroll_layout.addWidget(compressor_group)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        tabs.addTab(effects_tab, "🎛️ Audio FX")
    
    def build_soundfont_tab(self, tabs):
        """Build SoundFont instruments tab."""
        from soundfont_player import FLUIDSYNTH_AVAILABLE
        from PyQt6.QtWidgets import QFileDialog, QPushButton
        
        soundfont_tab = QWidget()
        layout = QVBoxLayout(soundfont_tab)
        
        # Check if available
        if not FLUIDSYNTH_AVAILABLE:
            warning = QLabel("⚠️ SoundFont support requires 'pyfluidsynth' and FluidSynth.\n\n"
                           "Install with: pip install pyfluidsynth\n"
                           "Plus system FluidSynth library (see INSTALLATION_NEW_FEATURES.md)\n\n"
                           "SoundFonts provide realistic piano, strings, brass, drums, and more.")
            warning.setWordWrap(True)
            warning.setStyleSheet("color: #cc6600; padding: 20px;")
            layout.addWidget(warning)
            layout.addStretch()
            tabs.addTab(soundfont_tab, "🎹 SoundFont")
            return
        
        info_label = QLabel("Use realistic instrument sounds from SoundFont (.sf2) files instead of synthesis.")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #666; font-style: italic; margin-bottom: 10px;")
        layout.addWidget(info_label)
        
        # Master enable
        self.soundfont_enabled = QCheckBox("Use SoundFont Instead of Synthesis")
        self.soundfont_enabled.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.soundfont_enabled)
        
        # SoundFont file selection
        sf_file_group = QGroupBox("SoundFont File")
        sf_file_layout = QVBoxLayout()
        
        file_layout = QHBoxLayout()
        self.soundfont_path_label = QLabel("No SoundFont loaded")
        self.soundfont_path_label.setStyleSheet("color: #999; font-style: italic;")
        file_layout.addWidget(self.soundfont_path_label)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_soundfont)
        file_layout.addWidget(browse_btn)
        
        sf_file_layout.addLayout(file_layout)
        
        tip = QLabel("💡 Tip: Download free SoundFonts from:\n• schristiancollins.com/generaluser.php (35MB)\n• musescore.org/en/handbook/soundfonts")
        tip.setWordWrap(True)
        tip.setStyleSheet("color: #666; font-size: 9pt; margin-top: 5px;")
        sf_file_layout.addWidget(tip)
        
        sf_file_group.setLayout(sf_file_layout)
        layout.addWidget(sf_file_group)
        
        # Instrument selection
        instrument_group = QGroupBox("Instrument")
        instrument_layout = QVBoxLayout()
        
        instrument_layout.addWidget(QLabel("Select Instrument:"))
        self.soundfont_program_combo = QComboBox()
        self.soundfont_program_combo.setMaxVisibleItems(15)
        
        # Add all 128 General MIDI instruments with names
        gm_instruments = [
            "0 - Acoustic Grand Piano",
            "1 - Bright Acoustic Piano",
            "2 - Electric Grand Piano",
            "3 - Honky-tonk Piano",
            "4 - Electric Piano 1",
            "5 - Electric Piano 2",
            "6 - Harpsichord",
            "7 - Clavinet",
            "8 - Celesta",
            "9 - Glockenspiel",
            "10 - Music Box",
            "11 - Vibraphone",
            "12 - Marimba",
            "13 - Xylophone",
            "14 - Tubular Bells",
            "15 - Dulcimer",
            "16 - Drawbar Organ",
            "17 - Percussive Organ",
            "18 - Rock Organ",
            "19 - Church Organ",
            "20 - Reed Organ",
            "21 - Accordion",
            "22 - Harmonica",
            "23 - Tango Accordion",
            "24 - Acoustic Guitar (nylon)",
            "25 - Acoustic Guitar (steel)",
            "26 - Electric Guitar (jazz)",
            "27 - Electric Guitar (clean)",
            "28 - Electric Guitar (muted)",
            "29 - Overdriven Guitar",
            "30 - Distortion Guitar",
            "31 - Guitar Harmonics",
            "32 - Acoustic Bass",
            "33 - Electric Bass (finger)",
            "34 - Electric Bass (pick)",
            "35 - Fretless Bass",
            "36 - Slap Bass 1",
            "37 - Slap Bass 2",
            "38 - Synth Bass 1",
            "39 - Synth Bass 2",
            "40 - Violin",
            "41 - Viola",
            "42 - Cello",
            "43 - Contrabass",
            "44 - Tremolo Strings",
            "45 - Pizzicato Strings",
            "46 - Orchestral Harp",
            "47 - Timpani",
            "48 - String Ensemble 1",
            "49 - String Ensemble 2",
            "50 - Synth Strings 1",
            "51 - Synth Strings 2",
            "52 - Choir Aahs",
            "53 - Voice Oohs",
            "54 - Synth Voice",
            "55 - Orchestra Hit",
            "56 - Trumpet",
            "57 - Trombone",
            "58 - Tuba",
            "59 - Muted Trumpet",
            "60 - French Horn",
            "61 - Brass Section",
            "62 - Synth Brass 1",
            "63 - Synth Brass 2",
            "64 - Soprano Sax",
            "65 - Alto Sax",
            "66 - Tenor Sax",
            "67 - Baritone Sax",
            "68 - Oboe",
            "69 - English Horn",
            "70 - Bassoon",
            "71 - Clarinet",
            "72 - Piccolo",
            "73 - Flute",
            "74 - Recorder",
            "75 - Pan Flute",
            "76 - Blown Bottle",
            "77 - Shakuhachi",
            "78 - Whistle",
            "79 - Ocarina",
            "80 - Lead 1 (square)",
            "81 - Lead 2 (sawtooth)",
            "82 - Lead 3 (calliope)",
            "83 - Lead 4 (chiff)",
            "84 - Lead 5 (charang)",
            "85 - Lead 6 (voice)",
            "86 - Lead 7 (fifths)",
            "87 - Lead 8 (bass + lead)",
            "88 - Pad 1 (new age)",
            "89 - Pad 2 (warm)",
            "90 - Pad 3 (polysynth)",
            "91 - Pad 4 (choir)",
            "92 - Pad 5 (bowed)",
            "93 - Pad 6 (metallic)",
            "94 - Pad 7 (halo)",
            "95 - Pad 8 (sweep)",
            "96 - FX 1 (rain)",
            "97 - FX 2 (soundtrack)",
            "98 - FX 3 (crystal)",
            "99 - FX 4 (atmosphere)",
            "100 - FX 5 (brightness)",
            "101 - FX 6 (goblins)",
            "102 - FX 7 (echoes)",
            "103 - FX 8 (sci-fi)",
            "104 - Sitar",
            "105 - Banjo",
            "106 - Shamisen",
            "107 - Koto",
            "108 - Kalimba",
            "109 - Bagpipe",
            "110 - Fiddle",
            "111 - Shanai",
            "112 - Tinkle Bell",
            "113 - Agogo",
            "114 - Steel Drums",
            "115 - Woodblock",
            "116 - Taiko Drum",
            "117 - Melodic Tom",
            "118 - Synth Drum",
            "119 - Reverse Cymbal",
            "120 - Guitar Fret Noise",
            "121 - Breath Noise",
            "122 - Seashore",
            "123 - Bird Tweet",
            "124 - Telephone Ring",
            "125 - Helicopter",
            "126 - Applause",
            "127 - Gunshot"
        ]
        
        self.soundfont_program_combo.addItems(gm_instruments)
        self.soundfont_program_combo.setCurrentIndex(0)  # Default to Piano
        instrument_layout.addWidget(self.soundfont_program_combo)
        
        instrument_layout.addWidget(QLabel("Velocity (Loudness):"))
        self.soundfont_velocity_spin = QSpinBox()
        self.soundfont_velocity_spin.setRange(1, 127)
        self.soundfont_velocity_spin.setValue(100)
        instrument_layout.addWidget(self.soundfont_velocity_spin)
        
        instrument_group.setLayout(instrument_layout)
        layout.addWidget(instrument_group)
        
        # Note Selection
        note_group = QGroupBox("Note to Play")
        note_layout = QVBoxLayout()
        
        note_layout.addWidget(QLabel("Select Note:"))
        self.soundfont_note_combo = QComboBox()
        self.soundfont_note_combo.setMaxVisibleItems(15)
        
        # Add common notes with frequencies
        notes = [
            ("C2 - 65.41 Hz (Low C)", 65.41),
            ("C3 - 130.81 Hz", 130.81),
            ("C4 - 261.63 Hz (Middle C)", 261.63),
            ("D4 - 293.66 Hz", 293.66),
            ("E4 - 329.63 Hz", 329.63),
            ("F4 - 349.23 Hz", 349.23),
            ("G4 - 392.00 Hz", 392.00),
            ("A4 - 440.00 Hz (Concert A)", 440.00),
            ("B4 - 493.88 Hz", 493.88),
            ("C5 - 523.25 Hz", 523.25),
            ("D5 - 587.33 Hz", 587.33),
            ("E5 - 659.25 Hz", 659.25),
            ("F5 - 698.46 Hz", 698.46),
            ("G5 - 783.99 Hz", 783.99),
            ("A5 - 880.00 Hz", 880.00),
            ("C6 - 1046.50 Hz (High C)", 1046.50),
        ]
        
        for note_name, freq in notes:
            self.soundfont_note_combo.addItem(note_name, freq)
        
        # Default to Middle C
        self.soundfont_note_combo.setCurrentIndex(2)
        note_layout.addWidget(self.soundfont_note_combo)
        
        # Connect to update frequency automatically (only if freq_spin exists)
        try:
            self.soundfont_note_combo.currentIndexChanged.connect(self.on_soundfont_note_changed)
        except:
            pass  # freq_spin might not exist yet
        
        note_layout.addWidget(QLabel("Duration (seconds):"))
        self.soundfont_duration_spin = QDoubleSpinBox()
        self.soundfont_duration_spin.setRange(0.1, 10.0)
        self.soundfont_duration_spin.setValue(1.0)
        self.soundfont_duration_spin.setSingleStep(0.1)
        self.soundfont_duration_spin.setSuffix(" sec")
        note_layout.addWidget(self.soundfont_duration_spin)
        
        note_group.setLayout(note_layout)
        layout.addWidget(note_group)
        
        # Play button right in the SoundFont tab
        play_btn = QPushButton("▶ Play SoundFont")
        play_btn.setStyleSheet("font-weight: bold; font-size: 12pt; padding: 10px; background: #4CAF50; color: white;")
        play_btn.clicked.connect(self.play_soundfont_preview)
        layout.addWidget(play_btn)
        
        layout.addStretch()
        tabs.addTab(soundfont_tab, "🎹 SoundFont")
    
    def browse_soundfont(self):
        """Open file dialog to select SoundFont file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select SoundFont File",
            "",
            "SoundFont Files (*.sf2);;All Files (*.*)"
        )
        if file_path:
            self.soundfont_path_label.setText(file_path)
            self.soundfont_path_label.setStyleSheet("color: #000;")
    
    def on_soundfont_note_changed(self):
        """Update frequency when note selection changes."""
        if hasattr(self, 'soundfont_note_combo') and hasattr(self, 'freq_spin'):
            # Get frequency from combo box data
            freq = self.soundfont_note_combo.currentData()
            if freq:
                # Update the frequency in Basic tab
                self.freq_spin.setValue(freq)
    
    def play_soundfont_preview(self):
        """Play SoundFont with current settings directly."""
        try:
            # Check if SoundFont is enabled
            if not self.soundfont_enabled.isChecked():
                QMessageBox.warning(
                    self,
                    "SoundFont Not Enabled",
                    "Please check 'Use SoundFont Instead of Synthesis' first."
                )
                return
            
            # Check if file is loaded
            sf_path = self.soundfont_path_label.text()
            if sf_path == "No SoundFont loaded" or not sf_path:
                QMessageBox.warning(
                    self,
                    "No SoundFont File",
                    "Please click 'Browse...' and select a .sf2 file first."
                )
                return
            
            # Get settings from SoundFont tab
            freq = self.soundfont_note_combo.currentData()
            duration = self.soundfont_duration_spin.value()
            program = self.soundfont_program_combo.currentIndex()
            velocity = self.soundfont_velocity_spin.value()
            
            print(f"Playing SoundFont: {sf_path}")
            print(f"  Program: {program}, Note freq: {freq}, Velocity: {velocity}, Duration: {duration}")
            
            # Get current config or create default
            if not hasattr(self.layer, 'config') or not self.layer.config:
                self.layer.config = self.parent_studio._default_config()
            
            # Update config with SoundFont settings
            self.layer.config['frequency'] = freq
            self.layer.config['duration'] = duration
            # Make sure volume is set to a reasonable level
            if 'volume' not in self.layer.config or self.layer.config['volume'] <= 0:
                self.layer.config['volume'] = 0.7
            print(f"  Volume: {self.layer.config['volume']}")
            
            # Ensure effects config exists
            if 'effects' not in self.layer.config:
                self.layer.config['effects'] = {
                    'enabled': False,
                    'reverb_enabled': False,
                    'reverb_room_size': 0.5,
                    'reverb_damping': 0.5,
                    'reverb_wet_level': 0.3,
                    'reverb_dry_level': 0.8,
                    'delay_enabled': False,
                    'delay_time': 0.5,
                    'delay_feedback': 0.5,
                    'delay_mix': 0.5,
                    'distortion_enabled': False,
                    'distortion_drive': 25,
                    'chorus_enabled': False,
                    'chorus_rate': 1.0,
                    'chorus_depth': 0.25,
                    'chorus_mix': 0.5
                }
            
            # Update soundfont config
            if 'soundfont' not in self.layer.config:
                self.layer.config['soundfont'] = {
                    'enabled': False,
                    'soundfont_path': '',
                    'program': 0,
                    'bank': 0,
                    'midi_note': 60,
                    'velocity': 100,
                    'use_frequency': True
                }
            
            self.layer.config['soundfont']['enabled'] = True
            self.layer.config['soundfont']['soundfont_path'] = sf_path
            self.layer.config['soundfont']['program'] = program
            self.layer.config['soundfont']['velocity'] = velocity
            self.layer.config['soundfont']['use_frequency'] = True
            
            print(f"Config ready. Calling play_layer...")
            
            # Play it
            self.parent_studio.play_layer(self.layer)
            
            print("Play command sent.")
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            QMessageBox.critical(
                self,
                "Playback Error",
                f"Failed to play SoundFont:\n\n{str(e)}\n\nSee console for details."
            )
            print(f"SoundFont playback error: {e}")
            print(error_details)
    
    def _create_param_spin(self, label, min_val, max_val, default, step):
        """Create a parameter spinbox with label."""
        group = QGroupBox(label)
        layout = QVBoxLayout()
        spin = QDoubleSpinBox()
        spin.setRange(min_val, max_val)
        spin.setValue(default)
        spin.setSingleStep(step)
        layout.addWidget(spin)
        group.setLayout(layout)
        return (group, spin)
    
    def load_config_to_ui(self):
        """Load layer config into UI controls."""
        cfg = self.layer.config
        self.freq_spin.setValue(cfg['frequency'])
        self.wave_combo.setCurrentText(cfg['wave_type'])
        self.duration_spin.setValue(cfg['duration'])
        self.volume_spin.setValue(cfg['volume'])
        self.overlap_spin.setValue(cfg.get('overlap', 0.0))
        self.attack_spin[1].setValue(cfg['attack'])
        self.decay_spin[1].setValue(cfg['decay'])
        self.sustain_spin[1].setValue(cfg['sustain'])
        self.release_spin[1].setValue(cfg['release'])
        
        self.harmonics_enabled.setChecked(cfg['harmonics']['enabled'])
        self.octave_spin[1].setValue(cfg['harmonics']['octave_volume'])
        self.fifth_spin[1].setValue(cfg['harmonics']['fifth_volume'])
        self.subbass_spin[1].setValue(cfg['harmonics']['sub_bass_volume'])
        
        # Synthesis parameters
        self.fm_ratio_spin.setValue(cfg['advanced'].get('fm_mod_ratio', 1.4))
        self.fm_index_spin.setValue(cfg['advanced'].get('fm_mod_index', 5.0))
        self.noise_type_combo.setCurrentText(cfg['advanced'].get('noise_type', 'white'))
        self.noise_filter_enabled.setChecked(cfg['advanced'].get('noise_filter_enabled', False))
        self.noise_filter_combo.setCurrentText(cfg['advanced'].get('noise_filter_type', 'bandpass'))
        self.filter_low_spin.setValue(cfg['advanced'].get('noise_filter_low', 2000.0))
        self.filter_high_spin.setValue(cfg['advanced'].get('noise_filter_high', 8000.0))
        self.lfo_enabled.setChecked(cfg['advanced'].get('lfo_enabled', False))
        self.lfo_freq_spin.setValue(cfg['advanced'].get('lfo_frequency', 5.0))
        self.lfo_depth_spin.setValue(cfg['advanced'].get('lfo_depth', 0.3) * 100)  # Convert to percentage
        self.echo_enabled.setChecked(cfg['advanced'].get('echo_enabled', False))
        self.echo_delay_spin.setValue(cfg['advanced'].get('echo_delay', 0.3))
        self.echo_feedback_spin.setValue(cfg['advanced'].get('echo_feedback', 0.4) * 100)  # Convert to percentage
        
        # Audio Effects (if available)
        from audio_effects import PEDALBOARD_AVAILABLE
        if PEDALBOARD_AVAILABLE and hasattr(self, 'audio_effects_enabled'):
            effects = cfg.get('effects', {})
            self.audio_effects_enabled.setChecked(effects.get('enabled', False))
            
            reverb = effects.get('reverb', {})
            self.reverb_enabled.setChecked(reverb.get('enabled', False))
            self.reverb_room_spin.setValue(reverb.get('room_size', 0.5))
            self.reverb_damping_spin.setValue(reverb.get('damping', 0.5))
            self.reverb_wet_spin.setValue(reverb.get('wet_level', 0.3))
            
            delay = effects.get('delay', {})
            self.delay_enabled.setChecked(delay.get('enabled', False))
            self.delay_time_spin.setValue(delay.get('delay_seconds', 0.5))
            self.delay_feedback_spin.setValue(delay.get('feedback', 0.5))
            self.delay_mix_spin.setValue(delay.get('mix', 0.5))
            
            distortion = effects.get('distortion', {})
            self.distortion_enabled.setChecked(distortion.get('enabled', False))
            self.distortion_drive_spin.setValue(distortion.get('drive_db', 10.0))
            
            chorus = effects.get('chorus', {})
            self.chorus_enabled.setChecked(chorus.get('enabled', False))
            self.chorus_rate_spin.setValue(chorus.get('rate_hz', 1.0))
            self.chorus_depth_spin.setValue(chorus.get('depth', 0.25))
            self.chorus_mix_spin.setValue(chorus.get('mix', 0.5))
            
            compressor = effects.get('compressor', {})
            self.compressor_enabled.setChecked(compressor.get('enabled', False))
            self.compressor_threshold_spin.setValue(compressor.get('threshold_db', -20.0))
            self.compressor_ratio_spin.setValue(compressor.get('ratio', 4.0))
        
        # SoundFont (if available)
        from soundfont_player import FLUIDSYNTH_AVAILABLE
        if FLUIDSYNTH_AVAILABLE and hasattr(self, 'soundfont_enabled'):
            soundfont = cfg.get('soundfont', {})
            self.soundfont_enabled.setChecked(soundfont.get('enabled', False))
            
            sf_path = soundfont.get('soundfont_path', '')
            if sf_path:
                self.soundfont_path_label.setText(sf_path)
                self.soundfont_path_label.setStyleSheet("color: #000;")
            else:
                self.soundfont_path_label.setText("No SoundFont loaded")
                self.soundfont_path_label.setStyleSheet("color: #999; font-style: italic;")
            
            # Set program using combobox (extract number from text "0 - Acoustic Grand Piano")
            program = soundfont.get('program', 0)
            self.soundfont_program_combo.setCurrentIndex(program)
            self.soundfont_velocity_spin.setValue(soundfont.get('velocity', 100))
            
            # Set note/duration if controls exist
            if hasattr(self, 'soundfont_duration_spin'):
                self.soundfont_duration_spin.setValue(cfg.get('duration', 1.0))
            
            # Try to match frequency to a note
            if hasattr(self, 'soundfont_note_combo'):
                current_freq = cfg.get('frequency', 261.63)
                # Find closest matching note
                best_match = 0
                min_diff = float('inf')
                for i in range(self.soundfont_note_combo.count()):
                    note_freq = self.soundfont_note_combo.itemData(i)
                    diff = abs(note_freq - current_freq)
                    if diff < min_diff:
                        min_diff = diff
                        best_match = i
                self.soundfont_note_combo.setCurrentIndex(best_match)
    
    def apply_changes(self):
        """Apply UI changes back to layer config."""
        cfg = self.layer.config
        
        # Check if SoundFont is enabled - if so, use SoundFont tab settings
        soundfont_enabled = (hasattr(self, 'soundfont_enabled') and 
                           self.soundfont_enabled.isChecked())
        
        if soundfont_enabled:
            # Use settings from SoundFont tab
            note_freq = self.soundfont_note_combo.currentData()
            if note_freq:
                cfg['frequency'] = note_freq
            cfg['duration'] = self.soundfont_duration_spin.value()
            # Keep a reasonable volume for SoundFont playback
            if cfg.get('volume', 0) <= 0:
                cfg['volume'] = 0.7
            
            # Auto-generate layer name from instrument and note
            instrument_name = self.soundfont_program_combo.currentText()
            note_name = self.soundfont_note_combo.currentText()
            # Extract just the note part (e.g., "C4" from "C4 - 261.63 Hz (Middle C)")
            note_short = note_name.split(' -')[0] if ' -' in note_name else note_name.split()[0]
            # Extract just the instrument name (e.g., "Acoustic Grand Piano" from "0 - Acoustic Grand Piano")
            instrument_short = instrument_name.split(' - ', 1)[1] if ' - ' in instrument_name else instrument_name
            self.layer.name = f"{instrument_short} - {note_short}"
            self.name_input.setText(self.layer.name)
            
            # Store the note name in config for display purposes
            cfg['note_name'] = note_short
        else:
            # Use settings from Basic tab
            cfg['frequency'] = self.freq_spin.value()
            cfg['duration'] = self.duration_spin.value()
            cfg['volume'] = self.volume_spin.value()
            # Use manually entered name
            self.layer.name = self.name_input.text() or "Untitled Layer"
        
        # Common settings
        cfg['wave_type'] = self.wave_combo.currentText()
        cfg['overlap'] = self.overlap_spin.value()
        cfg['attack'] = self.attack_spin[1].value()
        cfg['decay'] = self.decay_spin[1].value()
        cfg['sustain'] = self.sustain_spin[1].value()
        cfg['release'] = self.release_spin[1].value()
        
        cfg['harmonics']['enabled'] = self.harmonics_enabled.isChecked()
        cfg['harmonics']['octave_volume'] = self.octave_spin[1].value()
        cfg['harmonics']['fifth_volume'] = self.fifth_spin[1].value()
        cfg['harmonics']['sub_bass_volume'] = self.subbass_spin[1].value()
        
        # Synthesis parameters - save all values
        cfg['advanced']['fm_mod_ratio'] = self.fm_ratio_spin.value()
        cfg['advanced']['fm_mod_index'] = self.fm_index_spin.value()
        cfg['advanced']['noise_type'] = self.noise_type_combo.currentText()
        cfg['advanced']['noise_filter_enabled'] = self.noise_filter_enabled.isChecked()
        cfg['advanced']['noise_filter_type'] = self.noise_filter_combo.currentText()
        cfg['advanced']['noise_filter_low'] = self.filter_low_spin.value()
        cfg['advanced']['noise_filter_high'] = self.filter_high_spin.value()
        cfg['advanced']['lfo_enabled'] = self.lfo_enabled.isChecked()
        cfg['advanced']['lfo_frequency'] = self.lfo_freq_spin.value()
        cfg['advanced']['lfo_depth'] = self.lfo_depth_spin.value() / 100.0  # Convert from percentage
        cfg['advanced']['echo_enabled'] = self.echo_enabled.isChecked()
        cfg['advanced']['echo_delay'] = self.echo_delay_spin.value()
        cfg['advanced']['echo_feedback'] = self.echo_feedback_spin.value() / 100.0  # Convert from percentage
        
        # Audio Effects (if available)
        from audio_effects import PEDALBOARD_AVAILABLE
        if PEDALBOARD_AVAILABLE and hasattr(self, 'audio_effects_enabled'):
            if 'effects' not in cfg:
                cfg['effects'] = {
                    'enabled': False,
                    'reverb_enabled': False,
                    'reverb_room_size': 0.5,
                    'reverb_damping': 0.5,
                    'reverb_wet_level': 0.3,
                    'reverb_dry_level': 0.8,
                    'delay_enabled': False,
                    'delay_time': 0.5,
                    'delay_feedback': 0.5,
                    'delay_mix': 0.5,
                    'distortion_enabled': False,
                    'distortion_drive': 25,
                    'chorus_enabled': False,
                    'chorus_rate': 1.0,
                    'chorus_depth': 0.25,
                    'chorus_mix': 0.5
                }
            
            cfg['effects']['enabled'] = self.audio_effects_enabled.isChecked()
            
            cfg['effects']['reverb_enabled'] = self.reverb_enabled.isChecked()
            cfg['effects']['reverb_room_size'] = self.reverb_room_spin.value()
            cfg['effects']['reverb_damping'] = self.reverb_damping_spin.value()
            cfg['effects']['reverb_wet_level'] = self.reverb_wet_spin.value()
            
            cfg['effects']['delay_enabled'] = self.delay_enabled.isChecked()
            cfg['effects']['delay_time'] = self.delay_time_spin.value()
            cfg['effects']['delay_feedback'] = self.delay_feedback_spin.value()
            cfg['effects']['delay_mix'] = self.delay_mix_spin.value()
            
            cfg['effects']['distortion_enabled'] = self.distortion_enabled.isChecked()
            cfg['effects']['distortion_drive'] = self.distortion_drive_spin.value()
            
            cfg['effects']['chorus_enabled'] = self.chorus_enabled.isChecked()
            cfg['effects']['chorus_rate'] = self.chorus_rate_spin.value()
            cfg['effects']['chorus_depth'] = self.chorus_depth_spin.value()
            cfg['effects']['chorus_mix'] = self.chorus_mix_spin.value()
            
            cfg['effects']['compressor_enabled'] = self.compressor_enabled.isChecked()
            cfg['effects']['compressor_threshold'] = self.compressor_threshold_spin.value()
            cfg['effects']['compressor_ratio'] = self.compressor_ratio_spin.value()
        
        # SoundFont (if available)
        from soundfont_player import FLUIDSYNTH_AVAILABLE
        if FLUIDSYNTH_AVAILABLE and hasattr(self, 'soundfont_enabled'):
            if 'soundfont' not in cfg:
                cfg['soundfont'] = {
                    'enabled': False,
                    'soundfont_path': '',
                    'program': 0,
                    'bank': 0,
                    'midi_note': 60,
                    'velocity': 100,
                    'use_frequency': True
                }
            
            cfg['soundfont']['enabled'] = self.soundfont_enabled.isChecked()
            
            sf_path = self.soundfont_path_label.text()
            if sf_path != "No SoundFont loaded":
                cfg['soundfont']['soundfont_path'] = sf_path
            
            # Get program number from combobox index (index = program number)
            cfg['soundfont']['program'] = self.soundfont_program_combo.currentIndex()
            cfg['soundfont']['velocity'] = self.soundfont_velocity_spin.value()
            
            # Ensure use_frequency is True so it uses the frequency setting
            cfg['soundfont']['use_frequency'] = True
        
        # Notify parent to refresh
        self.parent_studio.refresh_layer_list()
    
    def show_context_help(self):
        """Show help for the currently focused widget."""
        focused_widget = self.focusWidget()
        
        # Find the help key for this widget
        help_key = self.widget_help_map.get(focused_widget)
        
        # If not found, check parent widget (for spinbox internal widgets)
        if not help_key and focused_widget:
            parent = focused_widget.parent()
            help_key = self.widget_help_map.get(parent)
            
            # Also check grandparent (for deeply nested widgets)
            if not help_key and parent:
                grandparent = parent.parent()
                help_key = self.widget_help_map.get(grandparent)
        
        if help_key:
            dialog = ParameterHelpDialog(help_key, self)
            dialog.exec()
        else:
            # Show general help message with widget info for debugging
            widget_info = f"Focused widget: {type(focused_widget).__name__}" if focused_widget else "No widget focused"
            QMessageBox.information(
                self,
                "Help",
                f"Press Shift+F1 while focused on a parameter control to see detailed help.\n\n"
                f"You can navigate through controls with Tab key and use Shift+F1 on any parameter.\n\n"
                f"({widget_info})"
            )
    
    def play_preview(self):
        """Play preview of this layer."""
        self.apply_changes()
        self.parent_studio.play_layer(self.layer)


class SoundDesignStudioV2(QMainWindow):
    """Main window for document-centric sound design."""
    
    def __init__(self):
        super().__init__()
        
        # Current document
        self.document = SoundDocument()
        self.current_layer_index = 0
        self.file_path = None
        
        # Audio system
        self.audio_player = EnhancedAudioPlayer()
        
        # Clipboard for cut/copy/paste
        self.layer_clipboard = None
        
        self.setup_ui()
        self.setup_menu()
        self.setup_shortcuts()
        self.update_title()
        self.refresh_layer_list()
        
        # Focus on layer list by default
        self.layer_list.setFocus()
    
    def setup_ui(self):
        """Build the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Document info section
        info_group = QGroupBox("Sound Information")
        info_layout = QVBoxLayout()
        
        # Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.doc_name_input = QLineEdit()
        self.doc_name_input.setText(self.document.name)
        self.doc_name_input.textChanged.connect(self.on_name_changed)
        name_layout.addWidget(self.doc_name_input)
        info_layout.addLayout(name_layout)
        
        # Description
        info_layout.addWidget(QLabel("Description:"))
        self.doc_description = QTextEdit()
        self.doc_description.setMaximumHeight(60)
        self.doc_description.setPlaceholderText("Describe this sound...")
        self.doc_description.setTabChangesFocus(True)
        self.doc_description.textChanged.connect(self.on_description_changed)
        info_layout.addWidget(self.doc_description)
        
        # Playback mode
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Playback Mode:"))
        self.playback_mode_combo = QComboBox()
        self.playback_mode_combo.addItems(['Sequential', 'Simultaneous'])
        self.playback_mode_combo.setCurrentText('Sequential')
        self.playback_mode_combo.currentTextChanged.connect(self.on_playback_mode_changed)
        mode_layout.addWidget(self.playback_mode_combo)
        mode_layout.addStretch()
        info_layout.addLayout(mode_layout)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Layer list section
        list_group = QGroupBox("Sound Layers")
        list_layout = QVBoxLayout()
        
        self.layer_list = QListWidget()
        self.layer_list.setAccessibleName("Sound layers")
        self.layer_list.setAccessibleDescription("List of sound layers. Use arrow keys to navigate, Enter to edit, Delete to remove.")
        self.layer_list.itemDoubleClicked.connect(self.open_design_dialog)
        self.layer_list.itemClicked.connect(self.on_layer_selected)
        self.layer_list.currentRowChanged.connect(self.on_layer_changed)
        list_layout.addWidget(self.layer_list)
        
        # Layer control buttons
        button_layout = QHBoxLayout()
        
        add_layer_btn = QPushButton("Add Layer")
        add_layer_btn.clicked.connect(self.add_new_layer)
        button_layout.addWidget(add_layer_btn)
        
        design_btn = QPushButton("Design")
        design_btn.clicked.connect(self.open_design_dialog)
        button_layout.addWidget(design_btn)
        
        remove_layer_btn = QPushButton("Remove Layer")
        remove_layer_btn.clicked.connect(self.remove_current_layer)
        button_layout.addWidget(remove_layer_btn)
        
        button_layout.addStretch()
        
        self.play_btn = QPushButton("Play")
        self.play_btn.clicked.connect(self.play_current_sound)
        self.play_btn.setToolTip("Play all layers (Alt+P) | Play focused layer (Alt+Shift+P)")
        button_layout.addWidget(self.play_btn)
        
        list_layout.addLayout(button_layout)
        list_group.setLayout(list_layout)
        layout.addWidget(list_group)
        
        # Status bar
        self.statusBar().showMessage("Ready - Alt+P: Play All | Alt+Shift+P: Play Layer | Alt+R: Presets | Ctrl+E: Export WAV")
    
    def setup_menu(self):
        """Create menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction("&New", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.new_document)
        file_menu.addAction(new_action)
        
        open_action = QAction("&Open...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_document)
        file_menu.addAction(open_action)
        
        save_action = QAction("&Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_document)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save &As...", self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.triggered.connect(self.save_document_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        export_wav_action = QAction("Export as &WAV...", self)
        export_wav_action.setShortcut("Ctrl+E")
        export_wav_action.triggered.connect(self.export_to_wav)
        file_menu.addAction(export_wav_action)
        
        export_layer_action = QAction("Export Current &Layer as WAV...", self)
        export_layer_action.triggered.connect(self.export_layer_to_wav)
        file_menu.addAction(export_layer_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        cut_action = QAction("Cu&t Layer", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self.cut_layer)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("&Copy Layer", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy_layer)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("&Paste Layer", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste_layer)
        edit_menu.addAction(paste_action)
        
        edit_menu.addSeparator()
        
        move_left_action = QAction("Move Layer &Left", self)
        move_left_action.setShortcut("Alt+Left")
        move_left_action.triggered.connect(self.move_layer_left)
        edit_menu.addAction(move_left_action)
        
        move_right_action = QAction("Move Layer &Right", self)
        move_right_action.setShortcut("Alt+Right")
        move_right_action.triggered.connect(self.move_layer_right)
        edit_menu.addAction(move_right_action)
        
        edit_menu.addSeparator()
        
        delete_action = QAction("&Delete Layer", self)
        delete_action.setShortcut("Delete")
        delete_action.triggered.connect(self.remove_current_layer)
        edit_menu.addAction(delete_action)
        
        # Design menu
        design_menu = menubar.addMenu("&Design")
        
        open_designer_action = QAction("&Open Designer...", self)
        open_designer_action.setShortcut("Ctrl+D")
        open_designer_action.triggered.connect(self.open_design_dialog)
        design_menu.addAction(open_designer_action)
        
        design_menu.addSeparator()
        
        clear_layer_action = QAction("&Clear Current Layer Values", self)
        clear_layer_action.triggered.connect(self.clear_current_layer)
        design_menu.addAction(clear_layer_action)
        
        design_menu.addSeparator()
        
        # Keyboard recorder for SoundFont sequences
        recorder_action = QAction("&Record Instrument Sequence...", self)
        recorder_action.setShortcut("Ctrl+R")
        recorder_action.triggered.connect(self.open_keyboard_recorder)
        design_menu.addAction(recorder_action)
        
        design_menu.addSeparator()
        
        add_layer_action = QAction("Add &New Layer", self)
        add_layer_action.setShortcut("Ctrl+L")
        add_layer_action.triggered.connect(self.add_new_layer)
        design_menu.addAction(add_layer_action)
        
        remove_layer_action = QAction("&Remove Layer", self)
        remove_layer_action.setShortcut(QKeySequence.StandardKey.Delete)
        remove_layer_action.triggered.connect(self.remove_current_layer)
        design_menu.addAction(remove_layer_action)
        
        design_menu.addSeparator()
        
        sequential_action = QAction("Sequential Playback", self)
        sequential_action.triggered.connect(lambda: self.set_playback_mode('sequential'))
        design_menu.addAction(sequential_action)
        
        simultaneous_action = QAction("Simultaneous Playback", self)
        simultaneous_action.triggered.connect(lambda: self.set_playback_mode('simultaneous'))
        design_menu.addAction(simultaneous_action)
        
        # Presets menu
        self.setup_presets_menu(menubar)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_presets_menu(self, menubar):
        """Create hierarchical presets menu."""
        presets_menu = menubar.addMenu("P&resets")  # Alt+R shortcut
        
        # Add Preview Presets option at the top
        preview_action = QAction("Preview Presets...", self)
        preview_action.triggered.connect(self.open_preset_preview)
        presets_menu.addAction(preview_action)
        
        presets_menu.addSeparator()
        
        # Load preset library
        preset_library = get_preset_library()
        
        # Create hierarchical menu structure
        for category, subcategories in preset_library.items():
            category_menu = presets_menu.addMenu(category)
            
            for subcategory, presets in subcategories.items():
                subcategory_menu = category_menu.addMenu(subcategory)
                
                for preset_name, preset_data in presets.items():
                    preset_action = QAction(preset_name, self)
                    preset_action.triggered.connect(
                        lambda checked, data=preset_data, name=preset_name: self.load_preset(data, name)
                    )
                    subcategory_menu.addAction(preset_action)
    
    def load_preset(self, preset_data, preset_name):
        """Load a preset into the current document (adds layers to existing document)."""
        try:
            # Don't clear existing layers - add to them instead
            # Note: Keep existing document name and playback mode
            
            # Load and add new layers from preset
            for layer_data in preset_data.get('layers', []):
                layer = SoundLayer(layer_data['name'])
                layer.config.update(layer_data['config'])
                self.document.layers.append(layer)
            
            # Refresh UI
            # Keep current selection if possible
            if self.current_layer_index >= len(self.document.layers):
                self.current_layer_index = len(self.document.layers) - 1
            self.refresh_layer_list()
            
            self.statusBar().showMessage(f"Added {len(preset_data.get('layers', []))} layers from preset: {preset_name}", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error Loading Preset", f"Could not load preset:\n{str(e)}")
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts."""
        # Play all layers shortcut (Alt+P)
        play_all_shortcut = QShortcut(QKeySequence("Alt+P"), self)
        play_all_shortcut.activated.connect(self.play_current_sound)
        
        # Play focused layer only shortcut (Alt+Shift+P)
        play_layer_shortcut = QShortcut(QKeySequence("Alt+Shift+P"), self)
        play_layer_shortcut.activated.connect(self.play_focused_layer)
        
        # Navigate layers with arrow keys when list has focus
        self.layer_list.keyPressEvent = self.layer_list_key_handler
    
    def layer_list_key_handler(self, event):
        """Handle key press events in layer list."""
        # Check for Alt modifier
        if event.modifiers() & Qt.KeyboardModifier.AltModifier:
            if event.key() == Qt.Key.Key_Left:
                # Alt+Left: Move layer left (earlier in sequence)
                self.move_layer_left()
                return
            elif event.key() == Qt.Key.Key_Right:
                # Alt+Right: Move layer right (later in sequence)
                self.move_layer_right()
                return
        
        # Regular navigation without Alt
        if event.key() == Qt.Key.Key_Left:
            # Move to previous layer and go to top of its list
            if self.current_layer_index > 0:
                self.current_layer_index -= 1
                self.refresh_layer_list()  # Refresh to show new layer's properties
                self.layer_list.setCurrentRow(1)  # Set to first item (skip header at 0)
        elif event.key() == Qt.Key.Key_Right:
            # Move to next layer and go to top of its list
            if self.current_layer_index < len(self.document.layers) - 1:
                self.current_layer_index += 1
                self.refresh_layer_list()  # Refresh to show new layer's properties
                self.layer_list.setCurrentRow(1)  # Set to first item (skip header at 0)
        elif event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            # Open design dialog for current layer
            self.open_design_dialog()
        elif event.key() == Qt.Key.Key_Delete:
            # Remove current layer
            self.remove_current_layer()
        else:
            # Let Up/Down and other keys work normally within the property list
            QListWidget.keyPressEvent(self.layer_list, event)
    
    def update_title(self):
        """Update window title with document name."""
        title = f"{self.document.name} - Sound Design Studio"
        if self.file_path:
            title += f" [{self.file_path.name}]"
        self.setWindowTitle(title)
    
    def on_name_changed(self):
        """Handle document name change."""
        self.document.name = self.doc_name_input.text() or "Untitled Sound"
        self.update_title()
    
    def on_description_changed(self):
        """Handle description change."""
        self.document.description = self.doc_description.toPlainText()
    
    def on_playback_mode_changed(self):
        """Handle playback mode change."""
        mode = self.playback_mode_combo.currentText().lower()
        self.document.playback_mode = mode
    
    def on_layer_selected(self, item):
        """Handle layer selection."""
        self.current_layer_index = self.layer_list.currentRow()
    
    def on_layer_changed(self, row):
        """Handle property selection change (not layer change - layers change via Left/Right arrows)."""
        # Row changes within property list don't change the layer
        # Layer changes happen via Left/Right arrow keys only
        pass
    
    def refresh_layer_list(self):
        """Refresh the layer list display with detailed layer information."""
        self.layer_list.clear()
        
        if self.current_layer_index >= len(self.document.layers):
            self.current_layer_index = max(0, len(self.document.layers) - 1)
        
        # If no layers, show a helpful message
        if not self.document.layers:
            empty_item = QListWidgetItem("No layers yet. Press Ctrl+L to add a layer or click 'Add Layer'.")
            empty_item.setFlags(empty_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.layer_list.addItem(empty_item)
            return
        
        # Display only the current layer with all its properties
        layer = self.document.layers[self.current_layer_index]
        cfg = layer.config
        
        # Check if layer is blank (volume is 0)
        is_blank = cfg.get('volume', 0.0) == 0.0
        
        # Layer header
        header = QListWidgetItem(f"═══ Layer {self.current_layer_index + 1}/{len(self.document.layers)} ═══")
        header.setFlags(header.flags() & ~Qt.ItemFlag.ItemIsSelectable)  # Make it non-selectable
        self.layer_list.addItem(header)
        
        # Layer name (selectable)
        self.layer_list.addItem(QListWidgetItem(f"  Name: {layer.name}"))
        
        if is_blank:
            # Show parameter names without values for blank layers
            self.layer_list.addItem(QListWidgetItem(f"  Frequency: (not set)"))
            self.layer_list.addItem(QListWidgetItem(f"  Waveform: (not set)"))
            self.layer_list.addItem(QListWidgetItem(f"  Duration: (not set)"))
            self.layer_list.addItem(QListWidgetItem(f"  Volume: (not set)"))
            self.layer_list.addItem(QListWidgetItem(f"  Overlap: (not set)"))
            self.layer_list.addItem(QListWidgetItem(f"  Attack: (not set)"))
            self.layer_list.addItem(QListWidgetItem(f"  Decay: (not set)"))
            self.layer_list.addItem(QListWidgetItem(f"  Sustain: (not set)"))
            self.layer_list.addItem(QListWidgetItem(f"  Release: (not set)"))
            self.layer_list.addItem(QListWidgetItem(f"  Harmonics: (not set)"))
            self.layer_list.addItem(QListWidgetItem(f"  Synthesis: (not set)"))
            self.layer_list.addItem(QListWidgetItem(f"  Effects: (not set)"))
            
            # Add helpful message
            hint = QListWidgetItem("  → Press Enter or click 'Design' to configure")
            hint.setFlags(hint.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.layer_list.addItem(hint)
        else:
            # Show actual values for configured layers
            # Basic parameters
            
            # Check if this is a SoundFont layer and show note name if available
            soundfont_cfg = cfg.get('soundfont', {})
            is_soundfont = soundfont_cfg.get('enabled', False)
            
            if is_soundfont:
                # For SoundFont layers, show the note name instead of frequency
                # First try to get stored note name
                note_name = cfg.get('note_name')
                
                if not note_name:
                    # Fall back to frequency lookup
                    freq = cfg['frequency']
                    # Map common frequencies to note names
                    note_map = {
                        65.41: "C2", 130.81: "C3", 261.63: "C4", 
                        293.66: "D4", 329.63: "E4", 349.23: "F4", 
                        392.00: "G4", 440.00: "A4", 493.88: "B4",
                        523.25: "C5", 587.33: "D5", 659.25: "E5",
                        698.46: "F5", 783.99: "G5", 880.00: "A5",
                        1046.50: "C6"
                    }
                    # Find closest match
                    for note_freq, name in note_map.items():
                        if abs(freq - note_freq) < 1.0:  # Within 1 Hz
                            note_name = name
                            break
                
                if note_name:
                    self.layer_list.addItem(QListWidgetItem(f"  Note: {note_name}"))
                else:
                    self.layer_list.addItem(QListWidgetItem(f"  Frequency: {cfg['frequency']:.1f} Hz"))
                
                # Show instrument info
                instrument_num = soundfont_cfg.get('program', 0)
                self.layer_list.addItem(QListWidgetItem(f"  Instrument: #{instrument_num}"))
            else:
                # Regular synthesis layer
                self.layer_list.addItem(QListWidgetItem(f"  Frequency: {cfg['frequency']:.1f} Hz"))
            
            self.layer_list.addItem(QListWidgetItem(f"  Waveform: {cfg['wave_type']}"))
            self.layer_list.addItem(QListWidgetItem(f"  Duration: {cfg['duration']:.2f} s"))
            self.layer_list.addItem(QListWidgetItem(f"  Volume: {cfg['volume']:.2f}"))
            self.layer_list.addItem(QListWidgetItem(f"  Overlap: {cfg.get('overlap', 0.0):.2f} s"))
            
            # ADSR Envelope
            self.layer_list.addItem(QListWidgetItem(f"  Attack: {cfg['attack']:.3f} s"))
            self.layer_list.addItem(QListWidgetItem(f"  Decay: {cfg['decay']:.3f} s"))
            self.layer_list.addItem(QListWidgetItem(f"  Sustain: {cfg['sustain']:.2f}"))
            self.layer_list.addItem(QListWidgetItem(f"  Release: {cfg['release']:.3f} s"))
            
            # Harmonics
            self.layer_list.addItem(QListWidgetItem(f"  Harmonics Enabled: {'ON' if cfg.get('harmonics', {}).get('enabled') else 'OFF'}"))
            if cfg.get('harmonics', {}).get('enabled'):
                self.layer_list.addItem(QListWidgetItem(f"    Octave: {cfg['harmonics'].get('octave_volume', 0):.2f}"))
                self.layer_list.addItem(QListWidgetItem(f"    Fifth: {cfg['harmonics'].get('fifth_volume', 0):.2f}"))
                self.layer_list.addItem(QListWidgetItem(f"    Sub-bass: {cfg['harmonics'].get('sub_bass_volume', 0):.2f}"))
            
            # Synthesis Parameters - show all types
            adv = cfg.get('advanced', {})
            
            # FM Synthesis
            fm_ratio = adv.get('fm_mod_ratio', 1.4)
            fm_index = adv.get('fm_mod_index', 5.0)
            self.layer_list.addItem(QListWidgetItem(f"  FM Synthesis:"))
            self.layer_list.addItem(QListWidgetItem(f"    Ratio: {fm_ratio:.2f}, Index: {fm_index:.2f}"))
            
            # Noise
            noise_type = adv.get('noise_type', 'white')
            self.layer_list.addItem(QListWidgetItem(f"  Noise: {noise_type}"))
            if adv.get('noise_filter_enabled'):
                filter_type = adv.get('noise_filter_type', 'bandpass')
                low_cut = adv.get('noise_filter_low', 2000)
                high_cut = adv.get('noise_filter_high', 8000)
                self.layer_list.addItem(QListWidgetItem(f"    Filter: {filter_type} ({low_cut:.0f}-{high_cut:.0f} Hz)"))
            
            # Effects
            self.layer_list.addItem(QListWidgetItem(f"  LFO: {'ON' if adv.get('lfo_enabled') else 'OFF'}"))
            if adv.get('lfo_enabled'):
                self.layer_list.addItem(QListWidgetItem(f"    Freq: {adv.get('lfo_frequency', 5.0):.1f} Hz, Depth: {adv.get('lfo_depth', 0.3)*100:.0f}%"))
            
            self.layer_list.addItem(QListWidgetItem(f"  Echo: {'ON' if adv.get('echo_enabled') else 'OFF'}"))
            if adv.get('echo_enabled'):
                self.layer_list.addItem(QListWidgetItem(f"    Delay: {adv.get('echo_delay', 0.3):.2f} s, Feedback: {adv.get('echo_feedback', 0.4)*100:.0f}%"))
        
        # Select first selectable item by default
        self.layer_list.setCurrentRow(1)  # Skip header
    
    def add_new_layer(self):
        """Add a new blank sound layer."""
        layer_num = len(self.document.layers) + 1
        self.document.add_layer(f"Layer {layer_num}", blank=True)
        # Select the new layer (switch to it)
        self.current_layer_index = len(self.document.layers) - 1
        self.refresh_layer_list()
        self.statusBar().showMessage(f"Added blank Layer {layer_num}", 3000)
    
    def clear_current_layer(self):
        """Clear all values in the current layer (reset to blank)."""
        if not self.document.layers:
            return
        
        layer = self.document.layers[self.current_layer_index]
        reply = QMessageBox.question(
            self,
            "Clear Layer Values",
            f"Clear all values for '{layer.name}'?\nThe layer will remain but all settings will be reset.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Clear the existing config dictionary in place
            layer.config.clear()
            
            # Now add the blank config values
            layer.config.update({
                'frequency': 440.0,
                'wave_type': 'sine',
                'duration': 0.5,
                'volume': 0.0,
                'attack': 0.0,
                'decay': 0.0,
                'sustain': 1.0,
                'release': 0.0,
                'overlap': 0.0,
                'harmonics': {
                    'enabled': False,
                    'octave_volume': 0.0,
                    'fifth_volume': 0.0,
                    'sub_bass_volume': 0.0
                },
                'blending': {
                    'enabled': False,
                    'blend_ratio': 0.0
                },
                'advanced': {
                    'enabled': False,
                    'synthesis_type': 'fm',
                    'fm_mod_ratio': 1.0,
                    'fm_mod_index': 0.0,
                    'noise_type': 'white',
                    'noise_filter_enabled': False,
                    'noise_filter_type': 'bandpass',
                    'noise_filter_low': 2000.0,
                    'noise_filter_high': 8000.0,
                    'lfo_enabled': False,
                    'lfo_frequency': 5.0,
                    'lfo_depth': 0.0,
                    'echo_enabled': False,
                    'echo_delay': 0.0,
                    'echo_feedback': 0.0
                },
                'play_type': 'custom'
            })
            
            # Force refresh the layer list
            self.refresh_layer_list()
            self.statusBar().showMessage(f"Cleared '{layer.name}'", 3000)
    
    def remove_current_layer(self):
        """Remove the currently selected layer. Can remove all layers."""
        if not self.document.layers:
            return
        
        layer_name = self.document.layers[self.current_layer_index].name
        reply = QMessageBox.question(
            self,
            "Remove Layer",
            f"Remove '{layer_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.document.remove_layer(self.current_layer_index)
            # Adjust index if needed
            if self.current_layer_index >= len(self.document.layers) and len(self.document.layers) > 0:
                self.current_layer_index = len(self.document.layers) - 1
            elif len(self.document.layers) == 0:
                self.current_layer_index = 0
            self.refresh_layer_list()
            self.statusBar().showMessage(f"Removed '{layer_name}'", 3000)
    
    def cut_layer(self):
        """Cut the current layer to clipboard."""
        if not self.document.layers:
            return
        
        # Copy to clipboard
        self.layer_clipboard = self.document.layers[self.current_layer_index].copy()
        
        # Remove if there's more than one layer
        if len(self.document.layers) > 1:
            layer_name = self.document.layers[self.current_layer_index].name
            self.document.remove_layer(self.current_layer_index)
            if self.current_layer_index >= len(self.document.layers):
                self.current_layer_index = len(self.document.layers) - 1
            self.refresh_layer_list()
            self.statusBar().showMessage(f"Cut '{layer_name}' to clipboard", 3000)
        else:
            QMessageBox.warning(self, "Cannot Cut", "A sound must have at least one layer.")
    
    def copy_layer(self):
        """Copy the current layer to clipboard."""
        if not self.document.layers:
            return
        
        self.layer_clipboard = self.document.layers[self.current_layer_index].copy()
        layer_name = self.layer_clipboard.name
        self.statusBar().showMessage(f"Copied '{layer_name}' to clipboard", 3000)
    
    def paste_layer(self):
        """Paste layer from clipboard."""
        if self.layer_clipboard is None:
            self.statusBar().showMessage("Clipboard is empty", 3000)
            return
        
        # Create a copy and insert after current layer
        new_layer = self.layer_clipboard.copy()
        insert_position = self.current_layer_index + 1
        self.document.layers.insert(insert_position, new_layer)
        self.current_layer_index = insert_position
        self.refresh_layer_list()
        self.statusBar().showMessage(f"Pasted '{new_layer.name}'", 3000)
    
    def move_layer_left(self):
        """Move current layer earlier in the sequence (swap with previous)."""
        if self.current_layer_index > 0:
            # Swap with previous layer
            idx = self.current_layer_index
            self.document.layers[idx], self.document.layers[idx - 1] = \
                self.document.layers[idx - 1], self.document.layers[idx]
            self.current_layer_index = idx - 1
            self.refresh_layer_list()
            self.statusBar().showMessage("Moved layer left", 3000)
    
    def move_layer_right(self):
        """Move current layer later in the sequence (swap with next)."""
        if self.current_layer_index < len(self.document.layers) - 1:
            # Swap with next layer
            idx = self.current_layer_index
            self.document.layers[idx], self.document.layers[idx + 1] = \
                self.document.layers[idx + 1], self.document.layers[idx]
            self.current_layer_index = idx + 1
            self.refresh_layer_list()
            self.statusBar().showMessage("Moved layer right", 3000)
    
    def open_design_dialog(self):
        """Open the design dialog for the current layer."""
        if not self.document.layers:
            return
        
        layer = self.document.layers[self.current_layer_index]
        dialog = DesignDialog(self, layer)
        dialog.exec()
        self.refresh_layer_list()
    
    def open_keyboard_recorder(self):
        """Open the keyboard recorder dialog for recording instrument sequences."""
        from soundfont_player import FLUIDSYNTH_AVAILABLE
        
        if not FLUIDSYNTH_AVAILABLE:
            QMessageBox.warning(
                self,
                "SoundFont Not Available",
                "The keyboard recorder requires FluidSynth for SoundFont playback.\n\n"
                "Please install FluidSynth and pyfluidsynth to use this feature."
            )
            return
        
        # Check if we have a soundfont file
        soundfont_path = "SoundFonts/GeneralUser-GS.sf2"
        if not Path(soundfont_path).exists():
            QMessageBox.warning(
                self,
                "SoundFont File Not Found",
                f"Could not find SoundFont file at: {soundfont_path}\n\n"
                "Please make sure you have a .sf2 file in the SoundFonts folder."
            )
            return
        
        # Open the keyboard recorder dialog
        dialog = KeyboardRecorderDialog(self, self.audio_player, soundfont_path)
        result = dialog.exec()
        
        if result == QDialog.DialogCode.Accepted and hasattr(dialog, 'recording_data'):
            # Convert the recording into layers
            self.create_layers_from_recording(dialog.recording_data)
    
    def create_layers_from_recording(self, recording_data):
        """Create layers from a keyboard recording."""
        notes = recording_data['notes']
        instrument = recording_data['instrument']
        instrument_name = recording_data['instrument_name']
        soundfont_path = recording_data['soundfont_path']
        
        if not notes:
            return
        
        # Calculate total duration
        max_end_time = max(timestamp + duration for timestamp, _, _, duration in notes)
        
        # Generate the full audio sequence
        try:
            import numpy as np
            from soundfont_player import SoundFontPlayer
            
            sample_rate = 44100
            total_samples = int((max_end_time + 0.5) * sample_rate)
            mixed_audio = np.zeros(total_samples)
            
            # Get soundfont player
            sp = SoundFontPlayer()
            if not sp.enabled:
                raise Exception("SoundFont player not available")
            
            # Load the soundfont
            sp.load_soundfont(soundfont_path)
            
            # Generate each note and place it at the correct time
            for timestamp, note_name, midi_note, duration in notes:
                # Generate this note
                note_audio = sp.generate_note(midi_note, 100, duration, instrument, 0)
                
                # Calculate where to place it in the timeline
                start_sample = int(timestamp * sample_rate)
                end_sample = start_sample + len(note_audio)
                
                # Make sure we don't exceed the buffer
                if end_sample > len(mixed_audio):
                    # Extend the buffer if needed
                    mixed_audio = np.concatenate([mixed_audio, np.zeros(end_sample - len(mixed_audio))])
                
                # Mix this note into the timeline
                mixed_audio[start_sample:end_sample] += note_audio
            
            # Normalize to prevent clipping
            max_val = np.max(np.abs(mixed_audio))
            if max_val > 0:
                mixed_audio = mixed_audio / max_val * 0.8  # Leave some headroom
            
            # Save the generated audio as a WAV file temporarily
            import tempfile
            import soundfile as sf
            from pathlib import Path
            
            # Create recordings directory if it doesn't exist
            recordings_dir = Path("recordings")
            recordings_dir.mkdir(exist_ok=True)
            
            # Generate unique filename
            import time
            timestamp_str = time.strftime("%Y%m%d_%H%M%S")
            wav_filename = recordings_dir / f"recording_{timestamp_str}.wav"
            
            # Save as WAV file
            sf.write(wav_filename, mixed_audio, sample_rate)
            
            # Create a layer that references this WAV file
            layer_name = f"{instrument_name} - Recording ({len(notes)} notes)"
            self.document.add_layer(layer_name, blank=False)
            layer = self.document.layers[-1]
            
            # Configure the layer to use the recorded audio
            cfg = layer.config
            cfg['duration'] = len(mixed_audio) / sample_rate
            cfg['volume'] = 0.7
            cfg['play_type'] = 'recorded_sequence'
            
            # Store the recording information
            cfg['recorded_audio_file'] = str(wav_filename)
            cfg['recording_notes'] = notes  # Store for reference
            cfg['note_name'] = f"{len(notes)} notes"
            
            # Set up SoundFont configuration for display
            if 'soundfont' not in cfg:
                cfg['soundfont'] = {}
            
            cfg['soundfont']['enabled'] = True
            cfg['soundfont']['soundfont_path'] = soundfont_path
            cfg['soundfont']['program'] = instrument
            
            # Switch to the new layer
            self.current_layer_index = len(self.document.layers) - 1
            self.refresh_layer_list()
            
            self.statusBar().showMessage(
                f"Created layer '{layer_name}' - Full sequence ready to play!",
                5000
            )
            
            QMessageBox.information(
                self,
                "Recording Saved",
                f"Your recording has been saved as a new layer.\n\n"
                f"Layer: {layer_name}\n"
                f"Notes recorded: {len(notes)}\n"
                f"Duration: {max_end_time:.2f} seconds\n"
                f"Audio file: {wav_filename.name}\n\n"
                f"The full sequence will play back exactly as you recorded it!"
            )
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self,
                "Error Creating Recording",
                f"Failed to create recording layer:\n\n{str(e)}\n\n"
                f"Check console for details."
            )
    
    def open_preset_preview(self):
        """Open the preset preview dialog."""
        dialog = PresetPreviewDialog(self)
        dialog.exec()
    
    def play_current_sound(self):
        """Play the current sound (all layers according to playback mode)."""
        if not self.document.layers:
            return
        
        try:
            if self.document.playback_mode == "sequential":
                # Play layers one after another
                for i, layer in enumerate(self.document.layers):
                    self.statusBar().showMessage(f"Playing layer {i + 1}/{len(self.document.layers)}: {layer.name}")
                    self.play_layer(layer)
                self.statusBar().showMessage("Playback complete", 3000)
            else:
                # Simultaneous playback - mix all layers together
                self.statusBar().showMessage(f"Playing {len(self.document.layers)} layers simultaneously...")
                # Filter out display-only fields from each layer config
                configs = [PlayAudioConfig(**{k: v for k, v in layer.config.items() if k != 'note_name'}) 
                          for layer in self.document.layers]
                self.audio_player.play_mixed_sounds(configs)
                self.statusBar().showMessage("Playback complete", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Playback Error", f"Error playing sound: {str(e)}")
    
    def play_focused_layer(self):
        """Play only the currently focused layer (Alt+Shift+P)."""
        if not self.document.layers:
            return
        
        try:
            layer = self.document.layers[self.current_layer_index]
            self.statusBar().showMessage(f"Playing layer: {layer.name}")
            self.play_layer(layer)
            self.statusBar().showMessage("Playback complete", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Playback Error", f"Error playing layer: {str(e)}")
    
    def play_layer(self, layer: SoundLayer):
        """Play a single sound layer."""
        try:
            print(f"\n=== play_layer called ===")
            print(f"Layer name: {layer.name}")
            print(f"Layer config keys: {layer.config.keys()}")
            print(f"SoundFont enabled: {layer.config.get('soundfont', {}).get('enabled', False)}")
            print(f"SoundFont path: {layer.config.get('soundfont', {}).get('soundfont_path', 'N/A')}")
            print(f"Frequency: {layer.config.get('frequency')}")
            print(f"Duration: {layer.config.get('duration')}")
            print(f"Volume: {layer.config.get('volume')}")
            
            # Filter out display-only fields that aren't audio config parameters
            audio_config = {k: v for k, v in layer.config.items() if k != 'note_name'}
            
            config = PlayAudioConfig(**audio_config)
            print(f"PlayAudioConfig created successfully")
            print(f"Calling audio_player.play_sound...")
            self.audio_player.play_sound(config)
            print(f"play_sound returned")
        except Exception as e:
            import traceback
            error_msg = f"Error playing sound: {str(e)}\n\n{traceback.format_exc()}"
            print(error_msg)
            QMessageBox.critical(
                self,
                "Playback Error",
                f"Failed to play sound:\n\n{str(e)}\n\nCheck console for details.\n\n"
                f"Try:\n"
                f"1. Disable SoundFont in Layer Designer\n"
                f"2. Use synthesis mode instead\n"
                f"3. Check that .sf2 file is valid"
            )
            # Try to continue with a safe fallback
            self.statusBar().showMessage(f"Playback failed: {str(e)}", 5000)
    
    def new_document(self):
        """Create a new sound document."""
        # Check for unsaved changes
        # For now, just create new
        self.document = SoundDocument()
        self.current_layer_index = 0
        self.file_path = None
        self.doc_name_input.setText(self.document.name)
        self.doc_description.setText(self.document.description)
        self.playback_mode_combo.setCurrentText(self.document.playback_mode.capitalize())
        self.update_title()
        self.refresh_layer_list()
        self.statusBar().showMessage("New document created", 3000)
    
    def open_document(self):
        """Open a sound document from file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Sound Document",
            "",
            "Sound Documents (*.sds);;JSON Files (*.json);;All Files (*.*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                self.document = SoundDocument.from_dict(data)
                self.file_path = Path(file_path)
                self.current_layer_index = 0
                self.doc_name_input.setText(self.document.name)
                self.doc_description.setText(self.document.description)
                self.playback_mode_combo.setCurrentText(self.document.playback_mode.capitalize())
                self.update_title()
                self.refresh_layer_list()
                self.statusBar().showMessage(f"Opened {self.file_path.name}", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error Opening File", f"Could not open file:\n{str(e)}")
    
    def save_document(self):
        """Save the current document."""
        if self.file_path:
            self._save_to_file(self.file_path)
        else:
            self.save_document_as()
    
    def save_document_as(self):
        """Save the document to a new file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Sound Document",
            f"{self.document.name}.sds",
            "Sound Documents (*.sds);;JSON Files (*.json);;All Files (*.*)"
        )
        
        if file_path:
            self.file_path = Path(file_path)
            self._save_to_file(self.file_path)
    
    def _save_to_file(self, file_path):
        """Save document to specified file."""
        try:
            with open(file_path, 'w') as f:
                json.dump(self.document.to_dict(), f, indent=2)
            self.update_title()
            self.statusBar().showMessage(f"Saved {file_path.name}", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error Saving File", f"Could not save file:\n{str(e)}")
    
    def export_to_wav(self):
        """Export the complete sound (all layers) to WAV file."""
        if not self.document.layers:
            QMessageBox.warning(self, "No Layers", "Cannot export - no layers in document.")
            return
        
        # Suggest filename
        default_name = f"{self.document.name}.wav"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Sound as WAV",
            default_name,
            "WAV Files (*.wav);;All Files (*.*)"
        )
        
        if not file_path:
            return
        
        try:
            # Create configs for all layers
            configs = [PlayAudioConfig(**layer.config) for layer in self.document.layers]
            
            # Export based on playback mode
            if self.document.playback_mode == "sequential":
                self.audio_player.export_sequential_to_wav(configs, file_path)
                mode_desc = "sequential"
            else:
                self.audio_player.export_mixed_to_wav(configs, file_path)
                mode_desc = "mixed"
            
            QMessageBox.information(
                self,
                "Export Successful",
                f"Sound exported successfully!\n\n"
                f"File: {Path(file_path).name}\n"
                f"Layers: {len(self.document.layers)}\n"
                f"Mode: {mode_desc}\n"
                f"Sample Rate: 44100 Hz\n"
                f"Format: 16-bit WAV"
            )
            self.statusBar().showMessage(f"Exported to {Path(file_path).name}", 5000)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Export Error",
                f"Failed to export sound:\n{str(e)}"
            )
    
    def export_layer_to_wav(self):
        """Export the currently selected layer to WAV file."""
        if not self.document.layers:
            QMessageBox.warning(self, "No Layers", "Cannot export - no layers in document.")
            return
        
        layer = self.document.layers[self.current_layer_index]
        
        # Suggest filename
        default_name = f"{self.document.name}_{layer.name}.wav"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            f"Export Layer '{layer.name}' as WAV",
            default_name,
            "WAV Files (*.wav);;All Files (*.*)"
        )
        
        if not file_path:
            return
        
        try:
            config = PlayAudioConfig(**layer.config)
            self.audio_player.export_to_wav(config, file_path)
            
            QMessageBox.information(
                self,
                "Export Successful",
                f"Layer exported successfully!\n\n"
                f"File: {Path(file_path).name}\n"
                f"Layer: {layer.name}\n"
                f"Frequency: {config.frequency} Hz\n"
                f"Duration: {config.duration} sec\n"
                f"Format: 16-bit WAV"
            )
            self.statusBar().showMessage(f"Exported {layer.name} to {Path(file_path).name}", 5000)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Export Error",
                f"Failed to export layer:\n{str(e)}"
            )
    
    def set_playback_mode(self, mode):
        """Set playback mode."""
        self.document.playback_mode = mode
        self.playback_mode_combo.setCurrentText(mode.capitalize())
        self.statusBar().showMessage(f"Playback mode: {mode}", 3000)
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About Sound Design Studio",
            "Sound Design Studio v2.0\n\n"
            "A professional sound synthesis tool with multi-layer composition.\n\n"
            "Create complex sounds by layering multiple synthesized sounds\n"
            "that can play sequentially or simultaneously.\n\n"
            "© 2025 Sound Design Studio"
        )


def main():
    """Main entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("Sound Design Studio")
    
    studio = SoundDesignStudioV2()
    studio.setMinimumSize(800, 600)
    studio.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
