![Piano HAT](piano-hat-logo-new.png)
https://shop.pimoroni.com/products/piano-hat

Piano HAT is a tiny Pi piano with 16 touch-sensitive buttons. It features:

* 16 Capacitive Touch Buttons
* 13 Notes from C to C
* Octave Up/Down
* Instrument Select

## Compatibility

This library supports:
- **Python:** 3.7, 3.8, 3.9, 3.10, 3.11, 3.12+
- **Raspberry Pi OS:** Bullseye (11), Bookworm (12), and newer
- **Architecture:** Both 32-bit (armhf) and 64-bit (aarch64)
- **Raspberry Pi Models:** All models with 40-pin GPIO header

## What's New in v0.3.1

- 🎯 **Fixed GPIO issues** - Replaced interrupt-based GPIO with polling to work on modern Bookworm
- 📦 **Single dependency** - Now uses actively-maintained `adafruit-circuitpython-cap1188`
- 💡 **LED control restored** - CAP1188 LED linking and manual control are supported
- ✅ **Actually works** - Button detection finally works on Bookworm 64-bit systems
- 🔧 **Simplified install** - No more GPIO configuration needed
- 🧵 **Background polling** - Non-blocking button detection with proper debouncing

## Version History

**v0.3.1** (Latest):
- Restored CAP1188 LED control (linking and manual on/off)
- Lowered minimum CAP1188 dependency to match available PyPI versions

**v0.3.0**:
- Switched from cap1xxx to Adafruit CircuitPython library (fixing GPIO interrupt issues)
- Button detection now works on modern Raspberry Pi OS Bookworm
- Removed GPIO interrupt complexity, now uses polling
- [Migration Guide: v0.2→v0.3](MIGRATION.md)

**v0.2.0**:
- Python 3 only (dropped Python 2.7 support)
- Modern packaging with `pyproject.toml`
- Type hints for IDE support

## Installing

**Important:** This library has been modernized for Python 3.7+ and modern Raspberry Pi OS (both 32-bit and 64-bit).

### Quick Install (Recommended):

Run this one-liner to install Piano HAT with all dependencies:

```bash
curl -sSL https://raw.githubusercontent.com/pimoroni/piano-hat/master/install.sh | bash
```

Or download and run the install script:

```bash
git clone https://github.com/pimoroni/piano-hat
cd piano-hat
chmod +x install.sh
./install.sh --examples
```

**Note for modern Raspberry Pi OS (Bookworm+):** Due to PEP 668 externally-managed environments, you may need to use a virtual environment:

```bash
# Create and activate a virtual environment
python3 -m venv --system-site-packages ~/pianohat-env
source ~/pianohat-env/bin/activate

# Now run the installer
./install.sh --examples
```

The installer will:
- Check your Python version (3.7+ required)
- Install system dependencies (I2C tools)
- Install the pianohat library
- Optionally install examples and their dependencies

### Manual Installation:

#### Install System Dependencies:

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-dev i2c-tools
```

#### Install Library:

Using pip:
```bash
pip3 install pianohat
```

From source:
```bash
git clone https://github.com/pimoroni/piano-hat
cd piano-hat/library
pip3 install .
```

#### Install Example Dependencies (Optional):

```bash
pip3 install pygame numpy
```

### Enable I2C:

Piano HAT requires I2C to be enabled. On modern Raspberry Pi OS:

```bash
sudo raspi-config
```

Then navigate to: `Interface Options` → `I2C` → `Enable`

Alternatively, check that this line exists in `/boot/config.txt` or `/boot/firmware/config.txt`:
```
dtparam=i2c_arm=on
```

After enabling I2C, reboot your Raspberry Pi.

### I2C Addresses

Piano HAT uses two CAP1188 chips on the I2C bus:

- `0x28` - keys C through G (indices 0-7)
- `0x2b` - keys G# through C (indices 8-15)

## Running Examples

The example scripts demonstrate Piano HAT's capabilities:

- **buttons.py** - Basic key press detection (no audio required)
- **leds.py** - LED animation (no audio required)
- **simple-piano.py** - Play piano sounds (requires audio device)
- **8bit-synth.py** - Software synthesis (requires audio device)
- **midi-piano.py** - MIDI output (requires MIDI software)
- **learn-to-play.py** - Interactive tutorial (requires audio device)

**LED Control:** The LEDs are driven by the CAP1188 chips. Use `auto_leds(True)` to link LEDs to touches, or `auto_leds(False)` and `set_led()` for manual control.

**Audio Requirements:** Examples that play sound require an audio output device. For headless setups, consider:
- USB audio adapter
- I2S audio HAT (e.g., [Pimoroni Audio boards](https://shop.pimoroni.com/collections/pimoroni-audio))
- Configure audio over HDMI
- SSH with X11 forwarding to a machine with audio

## Documentation & Support

* Guides and tutorials - https://learn.pimoroni.com/
* Function reference - http://docs.pimoroni.com/pianohat/
* GPIO Pinout - https://pinout.xyz/pinout/piano_hat
* Get help - http://forums.pimoroni.com/c/support
