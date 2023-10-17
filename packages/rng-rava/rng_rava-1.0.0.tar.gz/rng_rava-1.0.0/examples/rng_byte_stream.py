'''
This example showcases RNG byte stream.

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

# Generate 3 bytes every 0.5s
rng.snd_rng_byte_stream_start(n_bytes=3, stream_delay_ms=500)    

# Print 10 first values
print()
for i in range(10):
    rnd_a, rnd_b = rng.get_rng_byte_stream_data(
        out_type=rava.D_RNG_BYTE_OUT['NUMPY_ARRAY'])
    print('RNG A, B = {}, {}'.format(rnd_a, rnd_b))

# Stop stream
rng.snd_rng_byte_stream_stop()

# Close device
rng.close()