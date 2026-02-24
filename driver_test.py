#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2015-2026 Pimoroni Ltd
# SPDX-FileCopyrightText: 2026 Piano HAT Contributors
# SPDX-FileCopyrightText: 2026 Daniel Gentleman <code@danielgentleman.com>
# Adafruit CircuitPython CAP1188: https://github.com/adafruit/Adafruit_CircuitPython_CAP1188
#
# Test driver for Piano HAT using Adafruit CAP1188 library
# Maps both CAP1188 chips to logical piano keys

import time
import board
from adafruit_cap1188.i2c import CAP1188_I2C

# Button mapping for 16-key piano
BUTTON_NAMES = {
    0: "C",
    1: "C#",
    2: "D",
    3: "D#",
    4: "E",
    5: "F",
    6: "F#",
    7: "G",
    8: "G#",
    9: "A",
    10: "A#",
    11: "B",
    12: "C2",
    13: "Octave Down",
    14: "Octave Up",
    15: "Instrument",
}


def main():
    """Test both CAP1188 chips and print button presses."""
    print("Piano HAT Button Test")
    print("=" * 50)
    print("Initializing CAP1188 controllers...")

    try:
        i2c = board.I2C()
    except RuntimeError as e:
        print(f"ERROR: Could not initialize I2C: {e}")
        print("Make sure I2C is enabled and Piano HAT is connected")
        return

    # Initialize both CAP1188 chips
    try:
        cap_ctog = CAP1188_I2C(i2c, address=0x28)  # C-G
        print("✓ CAP1188 at 0x28 (C-G) initialized")
    except Exception as e:
        print(f"✗ Could not initialize CAP1188 at 0x28: {e}")
        return

    try:
        cap_atoc = CAP1188_I2C(i2c, address=0x2b)  # G#-C
        print("✓ CAP1188 at 0x2b (G#-C) initialized")
    except Exception as e:
        print(f"✗ Could not initialize CAP1188 at 0x2b: {e}")
        return

    print("\nListening for button presses...")
    print("(Press Ctrl+C to exit)\n")

    # Track previous state for debouncing
    prev_state = [[False] * 8 for _ in range(2)]

    try:
        while True:
            # Read from both chips
            current_time = time.time()

            # Check chip 1 (0x28) - keys 0-7 (C-G)
            for i in range(8):
                # CAP1188 uses 1-based pad indexing
                is_pressed = cap_ctog[i + 1].value

                if is_pressed != prev_state[0][i]:
                    button_name = BUTTON_NAMES[i]
                    state = "PRESSED" if is_pressed else "RELEASED"
                    print(f"[{current_time:.2f}] Button {i:2d} ({button_name:15s}) {state}")
                    prev_state[0][i] = is_pressed

            # Check chip 2 (0x2b) - keys 8-15 (G#-C, Octave Down, Octave Up, Instrument)
            for i in range(8):
                # CAP1188 uses 1-based pad indexing
                is_pressed = cap_atoc[i + 1].value
                button_idx = i + 8

                if is_pressed != prev_state[1][i]:
                    button_name = BUTTON_NAMES[button_idx]
                    state = "PRESSED" if is_pressed else "RELEASED"
                    print(f"[{current_time:.2f}] Button {button_idx:2d} ({button_name:15s}) {state}")
                    prev_state[1][i] = is_pressed

            # Debounce delay - check every 20ms
            time.sleep(0.02)

    except KeyboardInterrupt:
        print("\n\nTest ended by user")


if __name__ == "__main__":
    main()
