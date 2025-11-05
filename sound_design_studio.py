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
    QMenuBar, QMenu, QSplitter
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
    
    def apply_changes(self):
        """Apply UI changes back to layer config."""
        self.layer.name = self.name_input.text() or "Untitled Layer"
        cfg = self.layer.config
        
        cfg['frequency'] = self.freq_spin.value()
        cfg['wave_type'] = self.wave_combo.currentText()
        cfg['duration'] = self.duration_spin.value()
        cfg['volume'] = self.volume_spin.value()
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
                configs = [PlayAudioConfig(**layer.config) for layer in self.document.layers]
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
        config = PlayAudioConfig(**layer.config)
        self.audio_player.play_sound(config)
    
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
