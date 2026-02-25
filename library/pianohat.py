#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2015-2026 Pimoroni Ltd
# Adafruit CircuitPython CAP1188: https://github.com/adafruit/Adafruit_CircuitPython_CAP1188
# SPDX-FileCopyrightText: 2026 Daniel Gentleman <code@danielgentleman.com>
"""Piano HAT library for Raspberry Pi.

This library provides an interface to the Piano HAT, a 13-key capacitive
touch piano with additional control buttons.

Uses the Adafruit CAP1188 library for I2C communication with the capacitive
touch controllers. No GPIO interrupts required - uses polling instead.
"""

import time
import threading
from typing import Callable, List, Optional, Union

try:
    import board
    from adafruit_cap1188.i2c import CAP1188_I2C
except ImportError as exc:
    raise ImportError(
        "This library requires the adafruit-circuitpython-cap1188 module\n"
        "Install with: pip3 install adafruit-circuitpython-cap1188"
    ) from exc

__version__ = '0.3.1'

# Event handler type
EventHandler = Optional[Callable[[int, bool], None]]

# Piano key constants
C = 0
CSHARP = 1
D = 2
DSHARP = 3
E = 4
F = 5
FSHARP = 6
G = 7
GSHARP = 8
A = 9
ASHARP = 10
B = 11
C2 = 12

# Control buttons
OCTAVE_DOWN = 13
OCTAVE_UP = 14
INSTRUMENT = 15

# Event states
PRESSED = True
RELEASED = False

# CAP1188 LED register map (from cap1xxx)
R_LED_LINKING = 0x72
R_LED_OUTPUT_CON = 0x74
R_LED_BEHAVIOUR_1 = 0x81  # LEDs 1-4
R_LED_BEHAVIOUR_2 = 0x82  # LEDs 5-8
R_LED_DIRECT_RAMP = 0x94

LED_BEHAVIOUR_DIRECT = 0b00


class PianoHAT:
    """Piano HAT controller using Adafruit CAP1188 library.
    
    Provides polling-based button detection (no GPIO interrupts required).
    Works on modern Raspberry Pi OS (Bullseye, Bookworm, etc.)
    """

    def __init__(self):
        """Initialize Piano HAT with both CAP1188 controllers."""
        try:
            i2c = board.I2C()
        except RuntimeError as exc:
            raise RuntimeError(
                "Could not initialize I2C. Make sure I2C is enabled and accessible."
            ) from exc

        # Initialize both CAP1188 chips
        try:
            self._cap_ctog = CAP1188_I2C(i2c, address=0x28)  # C-G
            self._cap_atoc = CAP1188_I2C(i2c, address=0x2b)  # G#-C
        except RuntimeError as exc:
            raise RuntimeError(
                "Could not find Piano HAT on I2C bus. "
                "Verify it's connected and I2C is enabled."
            ) from exc

        # State tracking
        self._pressed = [False] * 16
        self._prev_pressed = [False] * 16

        # LED control
        self._auto_leds = True
        self._configure_leds()

        # Event handlers
        self._on_note: EventHandler = None
        self._on_octave_up: EventHandler = None
        self._on_octave_down: EventHandler = None
        self._on_instrument: EventHandler = None

        # Polling configuration
        self._polling_enabled = False
        self._polling_thread: Optional[threading.Thread] = None
        self._polling_interval = 0.02  # 20ms poll interval
        self._stop_polling = False

    def _configure_leds(self) -> None:
        """Configure default LED behavior and linking."""
        self._set_led_behaviour(self._cap_ctog, LED_BEHAVIOUR_DIRECT)
        self._set_led_behaviour(self._cap_atoc, LED_BEHAVIOUR_DIRECT)
        self._set_led_linking(self._cap_ctog, True)
        self._set_led_linking(self._cap_atoc, True)

    def _set_led_behaviour(self, cap: CAP1188_I2C, behaviour: int) -> None:
        """Set LED behaviour for all LEDs on a chip."""
        value = (behaviour & 0b11)
        packed = (value | (value << 2) | (value << 4) | (value << 6))
        cap._write_register(R_LED_BEHAVIOUR_1, packed)
        cap._write_register(R_LED_BEHAVIOUR_2, packed)

    def _set_led_linking(self, cap: CAP1188_I2C, enable: bool) -> None:
        """Enable or disable LED linking for all LEDs on a chip."""
        cap._write_register(R_LED_LINKING, 0xFF if enable else 0x00)

    def _set_led_state(self, cap: CAP1188_I2C, led_index: int, state: bool) -> None:
        """Set a single LED state on a chip."""
        current = cap._read_register(R_LED_OUTPUT_CON)
        if state:
            current |= (1 << led_index)
        else:
            current &= ~(1 << led_index)
        cap._write_register(R_LED_OUTPUT_CON, current)

    def _set_led_ramp_rate(self, cap: CAP1188_I2C, rise: int, fall: int) -> None:
        """Set LED rise/fall ramp rate for a chip."""
        rise_rate = min(7, max(0, int(round(rise / 250.0))))
        fall_rate = min(7, max(0, int(round(fall / 250.0))))
        cap._write_register(R_LED_DIRECT_RAMP, (rise_rate << 4) | fall_rate)

    def _cap_for_led(self, index: int) -> CAP1188_I2C:
        return self._cap_ctog if index < 8 else self._cap_atoc

    def _led_index_for_cap(self, index: int) -> int:
        return index if index < 8 else index - 8

    def setup(self) -> bool:
        """Initialize polling thread. Called automatically on first handler registration."""
        if not self._polling_enabled:
            self._polling_enabled = True
            self._stop_polling = False
            self._polling_thread = threading.Thread(
                target=self._poll_loop, daemon=True
            )
            self._polling_thread.start()
        return True

    def _poll_loop(self) -> None:
        """Background polling thread - checks button state and fires events."""
        while not self._stop_polling:
            self._check_buttons()
            time.sleep(self._polling_interval)

    def _check_buttons(self) -> None:
        """Check all 16 buttons and fire events on state changes."""
        # Check first CAP1188 (0x28) - buttons 0-7
        for i in range(8):
            pressed = self._cap_ctog[i + 1].value  # CAP1188 uses 1-based indexing
            if pressed != self._prev_pressed[i]:
                self._pressed[i] = pressed
                self._prev_pressed[i] = pressed
                self._handle_event(i, pressed)

        # Check second CAP1188 (0x2b) - buttons 8-15
        for i in range(8):
            pressed = self._cap_atoc[i + 1].value
            button_idx = i + 8
            if pressed != self._prev_pressed[button_idx]:
                self._pressed[button_idx] = pressed
                self._prev_pressed[button_idx] = pressed
                self._handle_event(button_idx, pressed)

    def _handle_event(self, channel: int, pressed: bool) -> None:
        """Route button events to appropriate handlers."""
        if channel <= 12 and callable(self._on_note):
            self._on_note(channel, pressed)
        elif channel == OCTAVE_UP and callable(self._on_octave_up):
            self._on_octave_up(channel, pressed)
        elif channel == OCTAVE_DOWN and callable(self._on_octave_down):
            self._on_octave_down(channel, pressed)
        elif channel == INSTRUMENT and callable(self._on_instrument):
            self._on_instrument(channel, pressed)


# Global singleton instance
_piano: Optional[PianoHAT] = None


def setup() -> bool:
    """Initialize Piano HAT.

    Called automatically by event registration functions.
    Safe to call multiple times.
    """
    global _piano
    if _piano is None:
        _piano = PianoHAT()
        _piano.setup()
    return True


def on_note(handler: EventHandler) -> None:
    """Register handler for note key press/release.

    :param handler: Function(channel, pressed) where:
        - channel: 0-12 (C to C)
        - pressed: True for press, False for release
    """
    setup()
    _piano._on_note = handler


def on_octave_up(handler: EventHandler) -> None:
    """Register handler for octave up button.

    :param handler: Function(channel, pressed)
    """
    setup()
    _piano._on_octave_up = handler


def on_octave_down(handler: EventHandler) -> None:
    """Register handler for octave down button.

    :param handler: Function(channel, pressed)
    """
    setup()
    _piano._on_octave_down = handler


def on_instrument(handler: EventHandler) -> None:
    """Register handler for instrument button.

    :param handler: Function(channel, pressed)
    """
    setup()
    _piano._on_instrument = handler


def get_state(index: int = -1) -> Union[bool, List[bool]]:
    """Get the state of buttons.

    :param index: Button index (0-15) or -1 for all buttons
    :return: Single boolean if index specified, list of booleans otherwise
    """
    setup()
    if 0 <= index < 16:
        return _piano._pressed[index]
    return _piano._pressed.copy()


def auto_leds(enable: bool = True) -> None:
    """Enable or disable automatic LED control.

    :param enable: True to link LEDs to touches, False for manual control
    """
    setup()
    _piano._auto_leds = enable
    _piano._set_led_behaviour(_piano._cap_ctog, LED_BEHAVIOUR_DIRECT)
    _piano._set_led_behaviour(_piano._cap_atoc, LED_BEHAVIOUR_DIRECT)
    _piano._set_led_linking(_piano._cap_ctog, enable)
    _piano._set_led_linking(_piano._cap_atoc, enable)


def set_led(index: int, state: bool) -> None:
    """Control an individual LED.

    :param index: LED index (0-15)
    :param state: True to turn on, False to turn off
    """
    if not 0 <= index < 16:
        return
    setup()
    cap = _piano._cap_for_led(index)
    led_index = _piano._led_index_for_cap(index)
    _piano._set_led_state(cap, led_index, state)


def set_led_ramp_rate(rise: int, fall: int) -> None:
    """Set LED fade rate.

    :param rise: Rise time in milliseconds
    :param fall: Fall time in milliseconds
    """
    setup()
    _piano._set_led_ramp_rate(_piano._cap_ctog, rise, fall)
    _piano._set_led_ramp_rate(_piano._cap_atoc, rise, fall)
