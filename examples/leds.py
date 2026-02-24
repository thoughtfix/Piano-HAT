#!/usr/bin/env python3

import time

import pianohat


pianohat.auto_leds(False)

while True:
    for x in range(16):
        pianohat.set_led(x, True)
        time.sleep(0.1)
        pianohat.set_led(x, False)
        time.sleep(0.1)    
