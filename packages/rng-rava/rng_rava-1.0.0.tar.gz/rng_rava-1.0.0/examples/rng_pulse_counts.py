'''
This example showcases RNG pulse count measurements for different values of the
sampling interval configuration. 

This example code is in the public domain.
Author: Gabriel Guerrer
'''

import rng_rava as rava

# Find RAVA device and connect
rng = rava.RAVA_RNG()
dev_sns = rava.find_rava_sns()
if len(dev_sns):
    rng.connect(serial_number=dev_sns[0])    
else:
    rava.lg.error('No device found')
    exit()

# Config PWM
rng.snd_pwm_setup(freq_id=rava.D_PWM_FREQ['50_KHZ'], duty=20)

# Vary sampling intervals 
sampling_intervals = range(1, 20+1)

print()
for si in sampling_intervals:
    rng.snd_rng_setup(sampling_interval_us=si)

    # Measure pulse counts
    pcs_a, pcs_b = rng.get_rng_pulse_counts(n_counts=5000)

    # Inform mean values
    print('si={} us; pc_a={:.2f}, pc_b={:.2f}'
          .format(si, pcs_a.mean(), pcs_b.mean()))
    
# Close device
rng.close()