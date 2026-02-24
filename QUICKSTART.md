# Quick Start Guide

Get your Piano HAT up and running in minutes!

## Prerequisites

- Raspberry Pi (any model with 40-pin GPIO header)
- Raspberry Pi OS (Bullseye or Bookworm recommended)
- Piano HAT properly connected
- Internet connection

## Installation (Choose One Method)

### Method 1: Quick Install (Recommended)

```bash
curl -sSL https://raw.githubusercontent.com/pimoroni/piano-hat/master/install.sh | bash
```

When prompted, choose `Y` to install examples.

### Method 2: Manual Install

```bash
# Enable I2C
sudo raspi-config
# Navigate to: Interface Options → I2C → Enable

# Reboot
sudo reboot

# Install
sudo apt-get update
sudo apt-get install python3-pip i2c-tools python3-smbus
pip3 install pianohat
```

## Verify Installation

```bash
# Check I2C devices (should show 28 and 2b)
i2cdetect -y 1

# Test library import
python3 -c "import pianohat; print('Piano HAT v' + pianohat.__version__)"
```

## Your First Program

Create a file called `test.py`:

```python
#!/usr/bin/env python3

import signal
import pianohat

print("Touch the Piano HAT keys!")
print("Press Ctrl+C to exit")

# Enable automatic LEDs
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
# Use python3, not python
python3 your_script.py
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
