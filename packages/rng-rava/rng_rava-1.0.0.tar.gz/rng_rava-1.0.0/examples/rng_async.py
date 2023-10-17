'''
This example showcases asynchronous RNG functionality. 

This example code is in the public domain.
Author: Gabriel Guerrer
'''

import asyncio
import rng_rava as rava

rava.lg.setLevel(10) # DEBUG

async def main():
    # Find RAVA device and connect
    rng = rava.RAVA_RNG_AIO()
    dev_sns = rava.find_rava_sns()
    if len(dev_sns):
        await rng.connect(dev_sns[0])    
    else:
        rava.lg.error('No device found')
        exit()

    # Request configuration
    print('\nPWM setup: {}\n'.format(await rng.get_pwm_setup()))
    print('\nRNG setup: {}\n'.format(await rng.get_rng_setup()))

    # Generate random data
    results = await asyncio.gather(
        rng.get_rng_pulse_counts(n_counts=10),
        rng.get_rng_bits(bit_type_id=rava.D_RNG_BIT_SRC['AB']),
        rng.get_rng_bytes(n_bytes=10, postproc_id=rava.D_RNG_POSTPROC['NONE'], 
                          out_type=rava.D_RNG_BYTE_OUT['NUMPY_ARRAY']),
        rng.get_rng_int8s(n_ints=10, int_max=99),
        rng.get_rng_int16s(n_ints=10, int_max=999),
        rng.get_rng_floats(n_floats=10),
        rng.get_rng_doubles(n_doubles=10)
    )
    print('\nRNG data: {}\n'.format(results))

    # Close device
    rng.close()

asyncio.run(main())