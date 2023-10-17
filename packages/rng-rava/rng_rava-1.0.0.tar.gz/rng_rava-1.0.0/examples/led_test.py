'''
This example showcases LED capabilities.

This example code is in the public domain.
Author: Gabriel Guerrer
'''

import time
import rng_rava as rava

# Find RAVA device and connect
rngled = rava.RAVA_RNG_LED()
dev_sns = rava.find_rava_sns()
if len(dev_sns):
    rngled.connect(serial_number=dev_sns[0])    
else:
    rava.lg.error('No device found')
    exit()

# Set color as blue (intensity=0)
rngled.snd_led_color(color_hue=rava.D_LED_COLOR['BLUE'], intensity=0)

# Fade to full intensity
rngled.snd_led_intensity_fade(intensity_tgt=255, duration_ms=1000)
time.sleep(2)

# Oscilate colors
rngled.snd_led_color_oscillate(n_cycles=3, duration_ms=4000)
time.sleep(5)

# Oscilate intensities
for i in range(2):
    rngled.snd_led_intensity_fade(intensity_tgt=10, duration_ms=2000)
    time.sleep(2)
    rngled.snd_led_intensity_fade(intensity_tgt=255, duration_ms=2000)
    time.sleep(2)
time.sleep(1)

# Fade color to red
rngled.snd_led_color_fade(color_hue_tgt=rava.D_LED_COLOR['RED'], duration_ms=2000)
time.sleep(3)

# Turn off lights
rngled.snd_led_intensity(intensity=0)

# Close device
rngled.close()