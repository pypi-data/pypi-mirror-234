'''
This example showcases the generation of a binary file containing random bytes.

This example code is in the public domain.
Author: Gabriel Guerrer
'''

import rng_rava as rava

# Variables
FILE_OUTPUT = 'random.bin'
N_BYTES = 1000000 # 1MB

# Find RAVA device and connect
rng = rava.RAVA_RNG()
dev_sns = rava.find_rava_sns()
if len(dev_sns):
    rng.connect(serial_number=dev_sns[0])    
else:
    rava.lg.error('No device found')
    exit()

# Open file
with open(FILE_OUTPUT, mode='bw') as f:

    # Generate bytes
    bytes_a, bytes_b = rng.get_rng_bytes(n_bytes=N_BYTES//2, 
                                    postproc_id=rava.D_RNG_POSTPROC['NONE'],
                                    out_type=rava.D_RNG_BYTE_OUT['NUMPY_ARRAY'],
                                    timeout=100)
    
    # Write to file
    f.write(bytes_a)
    f.write(bytes_b)

# Close device
rng.close()