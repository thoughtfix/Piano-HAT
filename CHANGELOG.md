# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.1] - 2026-02-24

### Credits
- Pimoroni Ltd
- Daniel Gentleman <code@danielgentleman.com>

### Changed
- Restored CAP1188 LED control (linking and manual on/off)
- Lowered minimum CAP1188 dependency to match available PyPI versions

### Fixed
- LED APIs (`auto_leds`, `set_led`, `set_led_ramp_rate`) now work again

## [0.3.0] - 2026-02-24

### Changed
- **BREAKING DEPENDENCY**: Replaced `cap1xxx` with `adafruit-circuitpython-cap1188`
  - Old library had GPIO interrupt issues on modern Raspberry Pi OS (Bookworm)
  - New library uses polling (no GPIO interrupts required)
  - Works on modern 64-bit Raspberry Pi OS without GPIO configuration
- Rewrote button detection to use polling thread instead of GPIO interrupts
- LED control still handled via CAP1188 (no GPIO required)

### Added
- Polling-based button detection (background thread)
- Full support for modern Raspberry Pi OS Bookworm (64-bit and 32-bit)
- Debounce support (20ms polling interval)
- Better error messages for I2C detection failures
- CircuitPython/Blinka compatibility

### Fixed
- **MAJOR**: Button press detection on Raspberry Pi OS Bookworm
- GPIO interrupt issues that prevented button events from firing
- gpiochip512 offset compatibility issues

### Compatibility Notes
- **LED Control**: LEDs are controlled by the CAP1188 chips and do not require GPIO
- **Migration**: No code changes needed if you only use button detection
  - All example code continues to work unchanged
  - Update dependencies: `pip install adafruit-circuitpython-cap1188`

## [0.2.0] - 2026-02-23

### Added
- Type hints throughout the library for better IDE support
- Modern `pyproject.toml` packaging (PEP 517/518)
- Support for Python 3.7 through 3.12
- Support for 64-bit Raspberry Pi OS (aarch64)
- GitHub Actions CI/CD workflows
- Modern installation script (`install.sh`)
- Requirements files for easy dependency management
- Comprehensive documentation updates

### Changed
- **BREAKING**: Dropped Python 2.7 support (now requires Python 3.7+)
- Updated all examples to use Python 3
- Modernized code style and formatting
- Improved error messages and documentation strings
- Updated installation instructions for current Raspberry Pi OS

### Removed
- Python 2.7 support
- Old `setup.py` (replaced with `pyproject.toml`)
- Deprecated installation methods

### Fixed
- Integer division in examples for Python 3 compatibility
- Import statements updated for modern best practices
- Code formatting and style issues

## [0.1.0] - 2015-XX-XX

### Added
- Initial release
- Support for Piano HAT hardware
- 13-key piano functionality
- Octave up/down controls
- Instrument selector
- LED control
- Example programs (piano, synth, MIDI, etc.)
- Python 2.7 and Python 3 support
