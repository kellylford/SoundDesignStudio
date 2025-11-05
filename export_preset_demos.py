"""
Export Preset Demo Generator
Automatically exports all presets from the preset library as WAV files
for demonstration purposes.
"""

import os
import sys
from pathlib import Path
from preset_library import get_preset_library
from simple_audio_player import EnhancedAudioPlayer, PlayAudioConfig
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def sanitize_filename(name):
    """Convert preset name to safe filename."""
    # Replace spaces with underscores, remove special characters
    safe_name = name.replace(' ', '_')
    safe_name = ''.join(c for c in safe_name if c.isalnum() or c in ('_', '-'))
    return safe_name


def export_preset_to_wav(preset_name, preset_data, output_path, player):
    """
    Export a single preset to WAV file.
    
    Args:
        preset_name: Name of the preset
        preset_data: Preset configuration dictionary
        output_path: Path object for output file
        player: EnhancedAudioPlayer instance
    """
    try:
        logger.info(f"Exporting: {preset_name}")
        
        # Convert layers to PlayAudioConfig objects
        configs = []
        for layer in preset_data.get('layers', []):
            layer_config = layer.get('config', {})
            
            # Create PlayAudioConfig from layer config
            config = PlayAudioConfig(
                frequency=layer_config.get('frequency', 440.0),
                wave_type=layer_config.get('wave_type', 'sine'),
                duration=layer_config.get('duration', 0.5),
                volume=layer_config.get('volume', 0.3),
                attack=layer_config.get('attack', 0.01),
                decay=layer_config.get('decay', 0.1),
                sustain=layer_config.get('sustain', 0.7),
                release=layer_config.get('release', 0.15),
                overlap=layer_config.get('overlap', 0.0),
                harmonics=layer_config.get('harmonics', {
                    'enabled': False,
                    'octave_volume': 0.0,
                    'fifth_volume': 0.0,
                    'sub_bass_volume': 0.0
                }),
                blending=layer_config.get('blending', {
                    'enabled': False,
                    'blend_ratio': 0.0
                }),
                advanced=layer_config.get('advanced', {
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
                })
            )
            configs.append(config)
        
        # Export based on playback mode
        playback_mode = preset_data.get('playback_mode', 'simultaneous')
        
        if playback_mode == 'simultaneous' or len(configs) == 1:
            # Export mixed/simultaneous
            player.export_mixed_to_wav(configs, str(output_path))
        else:
            # For sequential, we'll export as mixed too for demo purposes
            # (Sequential playback is more of an interactive feature)
            player.export_mixed_to_wav(configs, str(output_path))
        
        logger.info(f"  ✓ Exported to: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"  ✗ Failed to export {preset_name}: {e}")
        return False


def export_all_presets(output_dir="preset_demos"):
    """
    Export all presets from the preset library to WAV files.
    
    Args:
        output_dir: Directory name for exported files (default: "preset_demos")
    """
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Initialize audio player
    player = EnhancedAudioPlayer()
    
    # Load preset library
    logger.info("Loading preset library...")
    preset_library = get_preset_library()
    
    # Statistics
    total_presets = 0
    successful_exports = 0
    failed_exports = 0
    
    # Traverse the hierarchical preset structure
    logger.info(f"\nExporting presets to: {output_path.absolute()}\n")
    logger.info("=" * 70)
    
    for main_category, subcategories in preset_library.items():
        logger.info(f"\n{main_category}")
        logger.info("-" * 70)
        
        # Create category subdirectory
        category_dir = output_path / sanitize_filename(main_category)
        category_dir.mkdir(exist_ok=True)
        
        for subcategory, presets in subcategories.items():
            logger.info(f"\n  {subcategory}:")
            
            # Create subcategory directory
            subcategory_dir = category_dir / sanitize_filename(subcategory)
            subcategory_dir.mkdir(exist_ok=True)
            
            for preset_name, preset_data in presets.items():
                total_presets += 1
                
                # Generate safe filename
                safe_name = sanitize_filename(preset_name)
                wav_filename = f"{safe_name}.wav"
                wav_path = subcategory_dir / wav_filename
                
                # Export preset
                if export_preset_to_wav(preset_name, preset_data, wav_path, player):
                    successful_exports += 1
                else:
                    failed_exports += 1
    
    # Print summary
    logger.info("\n" + "=" * 70)
    logger.info("EXPORT SUMMARY")
    logger.info("=" * 70)
    logger.info(f"Total presets processed: {total_presets}")
    logger.info(f"Successfully exported:   {successful_exports}")
    logger.info(f"Failed exports:          {failed_exports}")
    logger.info(f"\nAll files saved to: {output_path.absolute()}")
    logger.info("=" * 70)
    
    return successful_exports == total_presets


def main():
    """Main entry point."""
    print("\n" + "=" * 70)
    print("Sound Design Studio - Preset Demo Exporter")
    print("=" * 70)
    print("\nThis script will export all presets as WAV files for demonstration.")
    print("The export process may take a few minutes...\n")
    
    # Allow custom output directory from command line
    output_dir = "preset_demos"
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
    
    try:
        success = export_all_presets(output_dir)
        
        if success:
            print("\n✓ All presets exported successfully!")
            print(f"\nYou can find the WAV files in the '{output_dir}' directory.")
            print("The files are organized by category and subcategory.")
            return 0
        else:
            print("\n⚠ Some presets failed to export. Check the log above for details.")
            return 1
            
    except KeyboardInterrupt:
        print("\n\nExport cancelled by user.")
        return 1
    except Exception as e:
        logger.exception(f"Fatal error during export: {e}")
        print(f"\n✗ Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
