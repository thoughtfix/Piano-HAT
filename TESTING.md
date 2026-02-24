# Installation Testing Checklist

Use this checklist to verify the Piano HAT installation works correctly.

## Pre-Installation Checks

- [ ] Raspberry Pi model identified
- [ ] Raspberry Pi OS version (run `cat /etc/os-release`)
- [ ] Python version 3.7+ (run `python3 --version`)
- [ ] I2C enabled (check `/boot/firmware/config.txt` or `/boot/config.txt`)
- [ ] Piano HAT physically connected to GPIO pins

## System Package Installation

- [ ] `i2c-tools` installed (run `which i2cdetect`)
- [ ] `python3-pip` installed (run `which pip3`)
- [ ] `python3-dev` installed
- [ ] `python3-smbus` installed (run `python3 -c "import smbus"` outside venv)

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
- [ ] Installer detected venv
- [ ] Skipped system package installation (expected in venv)
- [ ] pip packages installed successfully
- [ ] `pianohat` module importable
- [ ] `cap1xxx` dependency installed
- [ ] `smbus2` installed (or can access system `smbus`)
- [ ] Examples copied to `~/pianohat-examples`

### System-Wide Installation (Older OS)

```bash
./install.sh --examples
```

**Checklist:**
- [ ] System packages installed via apt
- [ ] Python library installed via pip
- [ ] No PEP 668 errors
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
- [ ] Version displays correctly (should be 0.2.0+)

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
**Solution:** `pip install smbus2` or use `--system-site-packages` when creating venv

### No I2C devices detected
**Solution:** 
1. Enable I2C: `sudo raspi-config` → Interface Options → I2C
2. Reboot: `sudo reboot`
3. Check Piano HAT is properly seated on GPIO pins

### pygame errors on headless system
**Solution:** This is expected. Use buttons.py or leds.py to test hardware.

### "ImportError: cap1xxx"
**Solution:** `pip install cap1xxx`

## Success Criteria

Minimum for successful install:
- ✅ Library imports without errors
- ✅ I2C devices detected
- ✅ buttons.py works (detects key presses)
- ✅ leds.py works (controls LEDs)

Full success:
- ✅ All of the above
- ✅ simple-piano.py plays sounds (if audio available)
- ✅ Examples run without errors

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
