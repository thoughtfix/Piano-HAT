# Quick Start Guide

Get your Piano HAT up and running in minutes!

**Piano HAT v0.2.0 uses the cap1xxx library for modern Python 3 support on Raspberry Pi OS Bookworm.**

## Prerequisites

- Raspberry Pi (any model with 40-pin GPIO header)
- Raspberry Pi OS Bullseye or Bookworm (32-bit or 64-bit)
- Piano HAT properly connected to GPIO header
- Internet connection
- Python 3.7 or higher

## Installation (Choose One Method)

### Method 1: From Scratch (Recommended for new installations)

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3 git python3-dev python3-smbus i2c-tools

# Enable I2C
sudo raspi-config
# Navigate to: Interface Options → I2C → Enable

# Reboot
sudo reboot

# Clone repository
git clone https://github.com/pimoroni/piano-hat.git
cd piano-hat

# Create virtual environment with system site packages
python3 -m venv --system-site-packages venv
source venv/bin/activate

# Run installer
./install.sh
```

When prompted, choose `Y` to install examples.

### Method 2: Quick Install (Alternative)

```bash
curl -sSL https://raw.githubusercontent.com/pimoroni/piano-hat/master/install.sh | bash
```

**Note:** The installer automatically handles virtual environment creation and installs required system packages (python3-dev, python3-smbus, i2c-tools).

## Verify Installation

```bash
# Check I2C devices (should show 28 and 2b)
sudo i2cdetect -y 1

# Test library import (make sure venv is activated if you used one)
python3 -c "import pianohat; print('Piano HAT ready!')"
```

**I2C Addresses:**
- `0x28` - CAP1188 chip for keys C through G (indices 0-7)
- `0x2b` - CAP1188 chip for keys G# through C (indices 8-15)

**Note:** If you installed using a virtual environment, remember to activate it first:
```bash
source venv/bin/activate  # or wherever you created your venv
```

## Your First Program

Create a file called `test.py`:

```python
#!/usr/bin/env python3

import signal
import pianohat

print("Touch the Piano HAT keys!")
print("Press Ctrl+C to exit")

# Enable automatic LEDs (links LEDs to touches)
# Use auto_leds(False) + set_led() for manual control.
pianohat.auto_leds(True)

# Handle note presses
def handle_note(channel, pressed):
    if pressed:
        print(f"Note {channel} pressed")
    else:
        print(f"Note {channel} released")

# Handle octave buttons
def handle_octave_up(channel, pressed):
    if pressed:
        print("Octave UP!")

def handle_octave_down(channel, pressed):
    if pressed:
        print("Octave DOWN!")

# Handle instrument button
def handle_instrument(channel, pressed):
    if pressed:
        print("Instrument!")

# Register event handlers
pianohat.on_note(handle_note)
pianohat.on_octave_up(handle_octave_up)
pianohat.on_octave_down(handle_octave_down)
pianohat.on_instrument(handle_instrument)

# Wait for events
signal.pause()
```

Run it:
```bash
chmod +x test.py
python3 test.py
```

## Try the Examples

If you installed with examples:

```bash
cd ~/pianohat-examples

# Simple button test
python3 buttons.py

# LED animations
python3 leds.py

# Piano with sound (requires pygame)
pip3 install pygame
python3 simple-piano.py
```

## Common Issues

### "No module named 'pianohat'"
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Or use python3 if installed system-wide
python3 your_script.py
```

### "No module named 'smbus'"
```bash
# Install system package (required even in venv)
sudo apt-get install python3-smbus

# If using venv, recreate with --system-site-packages
python3 -m venv --system-site-packages venv
source venv/bin/activate
```

### "Python.h: No such file or directory"
```bash
# Install development headers
sudo apt-get install python3-dev

# Then retry installation
./install.sh
```

### "No such file or directory: '/dev/i2c-1'"
```bash
# Enable I2C
sudo raspi-config
# Interface Options → I2C → Enable
sudo reboot
```

### No devices detected at 0x28 and 0x2b
- Check Piano HAT is properly seated on GPIO pins
- Verify I2C is enabled
- Try: `sudo i2cdetect -y 1`

## Next Steps

- Read the [API Reference](documentation/REFERENCE.md)
- Explore the [examples](examples/)
- Build your own piano project!

## Getting Help

- [GitHub Issues](https://github.com/pimoroni/piano-hat/issues)
- [Pimoroni Forums](https://forums.pimoroni.com)

## Learn More

- [Full README](README.md)
- [Migration Guide](MIGRATION.md) (if upgrading)
- [Contributing Guide](CONTRIBUTING.md) (to help develop)

Enjoy your Piano HAT! 🎹
