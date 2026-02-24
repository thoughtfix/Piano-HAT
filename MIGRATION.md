# Migration Guide: v0.1.0 to v0.2.0

This guide helps you migrate from the old Piano HAT library (v0.1.0) to the modernized v0.2.0.

## What Changed?

### Python Version

**Old (v0.1.0):**
- Supported Python 2.7 and Python 3.x

**New (v0.2.0):**
- **Requires Python 3.7 or higher**
- Python 2.7 is no longer supported

### Installation Method

**Old (v0.1.0):**
```bash
# The old curl script could break your system
curl https://get.pimoroni.com/pianohat | bash
```

**New (v0.2.0):**
```bash
# Safe, modern installer
curl -sSL https://raw.githubusercontent.com/pimoroni/piano-hat/master/install.sh | bash

# Or manual install
pip3 install pianohat
```

### Package Structure

**Old (v0.1.0):**
- Used `setup.py` for packaging

**New (v0.2.0):**
- Uses `pyproject.toml` (PEP 517/518)
- Supports editable installs: `pip install -e .`

## Code Changes Required

### Good News! 🎉

**No code changes are required!** The API remains completely compatible.

Your existing code will work without modification:

```python
import pianohat

pianohat.auto_leds(True)

def handle_note(channel, pressed):
    print(f"Note {channel} {'pressed' if pressed else 'released'}")

pianohat.on_note(handle_note)
```

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

**New (v0.2.0):**
- Supports Raspberry Pi OS Bullseye (11) and Bookworm (12)
- Works on both 32-bit (armhf) and 64-bit (aarch64)

### I2C Setup

I2C must be enabled. On modern Raspberry Pi OS:

```bash
sudo raspi-config
# Navigate to: Interface Options → I2C → Enable
```

Or check your config file:
```bash
# On older systems:
grep "dtparam=i2c_arm=on" /boot/config.txt

# On newer systems (Bookworm+):
grep "dtparam=i2c_arm=on" /boot/firmware/config.txt
```

## Uninstalling Old Version

If you have the old version installed:

```bash
# Remove old pip packages
sudo pip uninstall pianohat
sudo pip3 uninstall pianohat

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
sudo apt-get install python3-pip python3-dev i2c-tools python3-smbus

# Install library
pip3 install pianohat

# Install example dependencies (optional)
pip3 install pygame numpy
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
   # Should show version 0.2.0 or higher
   ```

3. **Test I2C:**
   ```bash
   i2cdetect -y 1
   # Should show devices at addresses 28 and 2b
   ```

4. **Test the library:**
   ```bash
   python3 -c "import pianohat; print(pianohat.__version__)"
   # Should print: 0.2.0
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

### "ImportError: No module named cap1xxx"

**Solution:** Install the cap1xxx dependency:
```bash
pip3 install cap1xxx
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

## Getting Help

- **Issues:** https://github.com/pimoroni/piano-hat/issues
- **Documentation:** https://github.com/pimoroni/piano-hat
- **Forums:** https://forums.pimoroni.com

## Benefits of Upgrading

- ✅ No more system-breaking installers
- ✅ Support for modern Raspberry Pi OS
- ✅ 64-bit Raspberry Pi OS support
- ✅ Better error messages
- ✅ Type hints for IDE autocomplete
- ✅ Actively maintained
- ✅ Modern Python packaging
- ✅ CI/CD with automated testing
