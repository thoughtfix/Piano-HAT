# Migration Guide: v0.1.0 to v0.3.x

This guide helps you migrate from the old Piano HAT library (v0.1.0) to the modernized v0.3.x.

## What Changed?

### Major: New Driver Library

**v0.1.0 & v0.2.x:**
- Used `cap1xxx` library with GPIO interrupt-based button detection
- Required GPIO pin access (pins 4 and 27)
- **Broken on modern Raspberry Pi OS Bookworm** due to GPIO interface changes

**v0.3.x:**
- Uses actively-maintained `adafruit-circuitpython-cap1188` library
- Polling-based button detection (no GPIO interrupts)
- Works perfectly on modern Raspberry Pi OS (Bookworm, 64-bit)
- No GPIO pin configuration needed

### Python Version

**Old (v0.1.0):**
- Supported Python 2.7 and Python 3.x

**New (v0.3.x):**
- **Requires Python 3.7 or higher**
- Python 2.7 is no longer supported

### Installation Method

**Old (v0.1.0):**
```bash
# The old curl script could break your system
curl https://get.pimoroni.com/pianohat | bash
```

**New (v0.3.x):**
```bash
# Safe, modern installer
curl -sSL https://raw.githubusercontent.com/pimoroni/piano-hat/master/install.sh | bash

# Or manual install
pip3 install pianohat
```

### Package Structure

**Old (v0.1.0):**
- Used `setup.py` for packaging

**New (v0.3.0):**
- Uses `pyproject.toml` (PEP 517/518)
- Supports editable installs: `pip install -e .`

## Code Changes Required

### Good News! 🎉

**No code changes are required!** The API remains completely compatible.

Your existing code will work without modification:

```python
import pianohat

def handle_note(channel, pressed):
    print(f"Note {channel} {'pressed' if pressed else 'released'}")

pianohat.on_note(handle_note)
```

### LED Control

LED control is still supported in v0.3.x and is handled directly by the CAP1188 chips.

```python
# Link LEDs to touches (default behavior)
pianohat.auto_leds(True)

# Manual LED control
pianohat.auto_leds(False)
pianohat.set_led(0, True)
pianohat.set_led_ramp_rate(250, 250)
```

If your LEDs do not respond, check that I2C is enabled and the Piano HAT is seated correctly.

### Python 3 Updates (if migrating from Python 2)

If you were using Python 2, you'll need to update your code:

**Print statements:**
```python
# Python 2
print "Hello"

# Python 3
print("Hello")
```

**Integer division:**
```python
# Python 2
result = 10 / 3  # Returns 3

# Python 3
result = 10 // 3  # Returns 3 (use // for integer division)
result = 10 / 3   # Returns 3.333... (regular division)
```

## System Requirements

### Raspberry Pi OS

**Old (v0.1.0):**
- Designed for 32-bit Raspbian Jessie/Stretch
- GPIO interrupts required

**New (v0.3.x):**
- Supports Raspberry Pi OS Bullseye (11) and Bookworm (12)
- Works on both 32-bit (armhf) and 64-bit (aarch64)
- **No GPIO configuration needed**

### I2C Setup

I2C must be enabled. On modern Raspberry Pi OS:

```bash
sudo raspi-config
# Navigate to: Interface Options → I2C → Enable
```

Or check your config file:
```bash
# On all systems:
grep "dtparam=i2c_arm=on" /boot/firmware/config.txt /boot/config.txt 2>/dev/null
```

## Uninstalling Old Version

If you have the old version installed:

```bash
# Remove old pip packages
pip uninstall pianohat cap1xxx

# Remove old apt packages (if any)
sudo apt-get remove python-pianohat python3-pianohat

# Clean up old examples (optional)
rm -rf ~/Pimoroni/pianohat
```

## Installing New Version

### Option 1: Using the new installer (Recommended)

```bash
git clone https://github.com/pimoroni/piano-hat
cd piano-hat
chmod +x install.sh
./install.sh --examples
```

### Option 2: Manual install

```bash
# System dependencies
sudo apt-get update
sudo apt-get install python3-pip python3-dev i2c-tools

# Install library
pip3 install pianohat

# Install example dependencies (optional)
pip3 install pygame numpy
```

### Option 3: From source

```bash
git clone https://github.com/pimoroni/piano-hat
cd piano-hat/library
pip3 install -e .
```

## Testing the Migration

1. **Check Python version:**
   ```bash
   python3 --version
   # Should be 3.7 or higher
   ```

2. **Verify installation:**
   ```bash
   pip3 show pianohat
   # Should show version 0.3.1 or higher
   ```

3. **Test I2C:**
   ```bash
   i2cdetect -y 1
   # Should show devices at addresses 28 and 2b
   ```

4. **Test the library:**
   ```bash
   python3 -c "import pianohat; print(pianohat.__version__)"
   # Should print: 0.3.1
   ```

5. **Run an example:**
   ```bash
   cd ~/pianohat-examples  # or wherever examples are installed
   python3 buttons.py
   ```

## Common Issues

### "ImportError: No module named pianohat"

**Solution:** Make sure you're using Python 3:
```bash
python3 your_script.py  # Not just 'python'
```

### "ImportError: No module named adafruit_cap1188"

**Solution:** Install the library:
```bash
pip3 install pianohat
# or
pip3 install adafruit-circuitpython-cap1188
```

### I2C devices not detected

**Solution:**
1. Enable I2C in `raspi-config`
2. Reboot: `sudo reboot`
3. Check connection of Piano HAT

### NetworkManager was removed (old installer issue)

If the old installer removed NetworkManager and bricked your headless Pi:

1. Boot with keyboard/monitor or from another system
2. Reinstall NetworkManager:
   ```bash
   sudo apt-get update
   sudo apt-get install network-manager
   ```

## What's New in v0.3.x?

✨ **Key Improvements:**
- ✅ Works on modern Raspberry Pi OS (Bookworm, 64-bit)
- ✅ No GPIO interrupt issues
- ✅ Actively maintained Adafruit library
- ✅ Polling-based detection (no complex GPIO wiring needed)
- ✅ Works in virtual environments without special setup
- ✅ 100% backward API compatible

## Benefits of Upgrading

- ✅ No more system-breaking installers
- ✅ Support for modern Raspberry Pi OS  
- ✅ 64-bit Raspberry Pi OS support
- ✅ Better error messages
- ✅ Type hints for IDE autocomplete
- ✅ Actively maintained
- ✅ Modern Python packaging
- ✅ CI/CD with automated testing
- ✅ **Actually works with button detection!**

## Getting Help

- **Issues:** https://github.com/pimoroni/piano-hat/issues
- **Documentation:** https://github.com/pimoroni/piano-hat
- **Forums:** https://forums.pimoroni.com
