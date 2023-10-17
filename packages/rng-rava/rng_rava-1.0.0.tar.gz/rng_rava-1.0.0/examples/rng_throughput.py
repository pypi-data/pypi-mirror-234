'''
This example showcases RNG byte stream.

This example code is in the public domain.
Author: Gabriel Guerrer
'''

import time
import numpy as np
import rng_rava as rava

N_BYTES = 12500
N_REPEAT = 3

# Find RAVA device and connect
rng = rava.RAVA_RNG()
dev_sns = rava.find_rava_sns()
if len(dev_sns):
    rng.connect(serial_number=dev_sns[0])    
else:
    rava.lg.error('No device found')
    exit()

def rng_bytes_throughput(n_bytes, n_repeat, postproc_id):
    deltas = np.zeros(n_repeat)
    for i in range(n_repeat):
        t0 = time.perf_counter()
        rng.get_rng_bytes(n_bytes, postproc_id, timeout=None)
        t1 = time.perf_counter()
        deltas[i] = t1-t0

    delta_s = deltas.mean()
    freq = (n_bytes / delta_s) * 8 / 1000
    freq *= 2 # Considering both channels
    interv = (delta_s/ n_bytes) * 1e6        
    print('Throughput: Produced {} x {} bytes in each channel'
          .format(n_bytes, n_repeat))
    print('  Freq Kbit/s = {:.3f}'.format(freq) ) 
    print('  Byte interval (us) = {:.3f}'.format(interv))

# Obtain the throughput for different post-processing options
for pp_str in ['NONE', 'XOR', 'XOR_DICHTL', 'VON_NEUMANN']:
    print('\n> PP {}'.format(pp_str))
    rng_bytes_throughput(n_bytes=N_BYTES, n_repeat=N_REPEAT, 
                         postproc_id=rava.D_RNG_POSTPROC[pp_str])

# Close device
rng.close()