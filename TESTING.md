# Installation Testing Checklist

Use this checklist to verify the Piano HAT installation works correctly on v0.3.x.

**Key Changes in v0.3.x:**
- Uses `adafruit-circuitpython-cap1188` (actively maintained CircuitPython library)
- No longer requires GPIO interrupts (works on modern Bookworm)
- `smbus` is no longer needed (Adafruit handles all dependencies)

## Pre-Installation Checks

- [ ] Raspberry Pi model identified
- [ ] Raspberry Pi OS Bullseye (11) or Bookworm (12)
- [ ] Architecture noted (32-bit armhf or 64-bit aarch64)
- [ ] Python version 3.7+ (run `python3 --version`)
- [ ] I2C enabled (check `/boot/firmware/config.txt` or `/boot/config.txt`)
- [ ] Piano HAT physically connected and I2C address visible (0x28, 0x2b)

## System Package Installation

- [ ] `i2c-tools` installed (run `which i2cdetect`)
- [ ] `python3-pip` installed (run `which pip3`)
- [ ] `python3-dev` installed
- [ ] I2C bus visible with i2cdetect (run `i2cdetect -y 1`, should show 28 and 2b)

## Library Installation Tests

### In Virtual Environment (Recommended for Bookworm+)

```bash
python3 -m venv --system-site-packages ~/pianohat-test
source ~/pianohat-test/bin/activate
cd ~/piano-hat-test  # or wherever you cloned
./install.sh --examples
```

**Checklist:**
- [ ] Virtual environment created successfully
- [ ] Installer detected venv configuration
- [ ] Skipped system package installation (expected in venv)
- [ ] pip packages installed successfully
- [ ] `pianohat` module importable
- [ ] `adafruit-circuitpython-cap1188` dependency installed
- [ ] `board` module accessible (Adafruit's I2C interface)
- [ ] Examples copied to `~/pianohat-examples`

### System-Wide Installation (Not recommended on Bookworm due to PEP 668)

```bash
./install.sh --examples
```

**Checklist:**
- [ ] System packages installed via apt
- [ ] Python library installed via pip
- [ ] No PEP 668 errors (if using Bookworm, venv recommended)
- [ ] Examples copied

## Hardware Detection

```bash
# Should show devices at 0x28 and 0x2b
i2cdetect -y 1
```

**Checklist:**
- [ ] I2C bus 1 accessible
- [ ] Device at address 0x28 detected (first CAP1188)
- [ ] Device at address 0x2b detected (second CAP1188)

## Library Import Test

```bash
python3 -c "import pianohat; print('Piano HAT v' + pianohat.__version__)"
```

**Checklist:**
- [ ] Import successful (no errors)
- [ ] Version displays correctly (should be 0.3.1+)

## Button Detection Test (v0.3.x)

**Important:** v0.3.x uses polling-based button detection (no GPIO interrupts). This is more reliable on modern systems.

```bash
# Test with driver_test.py (if available in repo)
python3 driver_test.py
```

**Expected output:**
```
✓ CAP1188 at 0x28 detected
✓ CAP1188 at 0x2b detected
[timestamp] Button 0 (C) PRESSED
[timestamp] Button 0 (C) RELEASED
```

**Checklist:**
- [ ] Both CAP1188 chips detected
- [ ] Button presses show timestamp and name
- [ ] Debouncing working (no double-presses at 20ms interval)
- [ ] All 16 buttons respond to touch

## Example Tests

### buttons.py (No audio required)

```bash
cd ~/pianohat-examples
python3 buttons.py
```

**Test:**
- [ ] Script runs without errors
- [ ] Touch each piano key (C through C)
- [ ] Key presses appear in terminal
- [ ] Touch octave up/down buttons
- [ ] Touch instrument button
- [ ] LED lights when key touched (if auto_leds enabled)
- [ ] Press Ctrl+C to exit cleanly

### leds.py (No audio required)

```bash
python3 leds.py
```

**Test:**
- [ ] Script runs without errors
- [ ] LEDs animate in sequence
- [ ] All 16 LEDs light up
- [ ] Press Ctrl+C to exit cleanly

### simple-piano.py (Requires audio)

```bash
python3 simple-piano.py
```

**Test:**
- [ ] Script runs without errors
- [ ] pygame initializes
- [ ] Sounds load from `sounds/piano/` directory
- [ ] Pressing keys plays piano sounds
- [ ] Octave up/down buttons work
- [ ] Press Ctrl+C to exit cleanly

**If audio fails:**
- [ ] Check audio device available: `aplay -l`
- [ ] Test audio: `speaker-test -t wav -c 2`
- [ ] Configure alsa if needed

## Common Issues

### "externally-managed-environment" error
**Solution:** Use a virtual environment (see above)

### "No module named 'smbus'" in venv
**Solution:** This is no longer needed in v0.3.0. If you see this, update the library: `pip install --upgrade pianohat`

### No I2C devices detected
**Solution:** 
1. Enable I2C: `sudo raspi-config` → Interface Options → I2C
2. Reboot: `sudo reboot`
3. Check Piano HAT is properly seated on GPIO pins

### pygame errors on headless system
**Solution:** This is expected. Use buttons.py or leds.py to test hardware.

### "ImportError: adafruit_circuitpython_cap1188"
**Solution:** `pip install adafruit-circuitpython-cap1188`

### Buttons not responding
**Solution (v0.3.x):**
- The new polling system requires 20ms per check cycle
- Touch a button distinctly (hold for 50ms+)
- Test with driver_test.py to verify hardware communication
- Check I2C is enabled and working

## Success Criteria

**Minimum for successful install (v0.3.x):**
- ✅ Library imports without errors
- ✅ I2C devices detected (i2cdetect shows 0x28 and 0x2b)
- ✅ Both CAP1188 chips detected and working
- ✅ buttons.py works (detects key presses)
- ✅ Adafruit CircuitPython library installed correctly

**Full success:**
- ✅ All of the above
- ✅ driver_test.py shows debounced button presses
- ✅ leds.py works (controls LEDs - should run without errors)
- ✅ simple-piano.py plays sounds (if audio available)
- ✅ All 16 buttons respond to touch
- ✅ Octave and Instrument buttons work

**Key Changes in v0.3.x:**
- ✅ GPIO interrupts are no longer used (polling instead)
- ✅ Works on modern Bookworm 64-bit systems
- ✅ No GPIO pin conflicts
- ✅ More reliable button detection

## Report Template

When reporting issues, include:

```
**Hardware:**
- Raspberry Pi Model: 
- Piano HAT connected: Yes/No
- Other HATs/devices: 

**Software:**
- OS: (output of `cat /etc/os-release`)
- Python: (output of `python3 --version`)
- pianohat version: (output of `pip show pianohat`)
- Installation method: [venv / system-wide]

**I2C Detection:**
(paste output of `i2cdetect -y 1`)

**Error:**
(paste full error message and traceback)

**What works:**
- [ ] buttons.py
- [ ] leds.py
- [ ] simple-piano.py
- [ ] Other: ___________
```
