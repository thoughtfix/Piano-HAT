# Piano HAT Function Reference

This library lets you use Piano HAT in Python to control whatever project you might assemble.

See `buttons.py` for an example of how to handle buttons. The library has 4 different events you can bind to:

* `on_note` - triggers when a piano key is touched
* `on_octave_up` - triggers when the Octave Up key is touched
* `on_octave_down` - triggers when the Octave Down key is touched
* `on_instrument` - triggers when the Instrument key is touched

Piano HAT uses two CAP1188 chips on the I2C bus:

* `0x28` - keys C through G (indices 0-7)
* `0x2b` - keys G# through C (indices 8-15)

See `leds.py` for an example of how to take command of the Piano HAT LEDs. You can turn all of the LEDs on and off at will, useful for creating a visual metronome, prompting a user which key to press and more.

* `auto_leds(True)` - link LEDs to touch events (default behavior)
* `auto_leds(False)` - unlink LEDs so you can control them manually
* `set_led(x, True/False)` - set a particular LED on or off when manual control is enabled
