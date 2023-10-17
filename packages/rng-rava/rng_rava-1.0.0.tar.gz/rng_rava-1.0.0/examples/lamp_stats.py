'''
This example calculates the statistics of LAMP experiments over a specific time 
interval, yielding the rate of significant events over time. In the LAMP mode, 
each significant event is visually indicated by rapid color oscillations 
spanning the entire color spectrum.

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


def measure_lamp_statistics():
    # Reset lamp stats
    if rngled.get_lamp_statistics() is None:
        return

    # Start lamp mode
    t0 = time.perf_counter()
    rngled.snd_lamp_mode(True)

    # Get elapsed time and lamp statistics
    input('\n> Press Enter to finish measuring lamp statistics...')
    t1 = time.perf_counter()
    stats = rngled.get_lamp_statistics()
    exp_n = stats['exp_n']

    # Close device
    rngled.close()

    # One experiment at least?
    if exp_n == 0:
        print('\nLamp Statistics: Not enougth LAMP experiments to process')
        return
    
    # Compute time intervals
    delta_t = t1 - t0
    delta_t_h = delta_t // 3600
    delta_t_min = (delta_t % 3600) // 60
    delta_t_s = delta_t % 60

    # Print results
    print('\nLamp Statistics' 
          '\nLasted {:.0f}h {:.0f}m {:.0f}s, yielding {} experiments'
          .format(delta_t_h, delta_t_min, delta_t_s, exp_n),
            
            '\n  where {} ({:.2f}%) reached statistical significance'
            .format(stats['exp_n_zsig'], 
                                  stats['exp_n_zsig']/exp_n*100),
                                  
            '\nMeaning one should expect to find:',
            
            '\n  {:.2f} significant events per 1 min'
            .format(stats['exp_n_zsig']/delta_t*60),
                    
            '\n  {:.2f} significant events per 5 min'
            .format(stats['exp_n_zsig']/delta_t*300),
            
            '\n  {:.2f} significant events per 10 min'
            .format(stats['exp_n_zsig']/delta_t*600),
            
            '\n  {:.2f} significant events per 30 min'
            .format(stats['exp_n_zsig']/delta_t*1800),
            
            '\n  {:.2f} significant events per 1 h'
            .format(stats['exp_n_zsig']/delta_t*3600),
            
            '\nColor distribution (%):',

            '\n  R={:.2f} O={:.2f} Y={:.2f} G={:.2f}'
            '\n  C={:.2f} B={:.2f} PU={:.2f} PI={:.2f}'
            .format(stats['red']/exp_n*100, stats['orange']/exp_n*100, 
                    stats['yellow']/exp_n*100, stats['green']/exp_n*100, 
                    stats['cyan']/exp_n*100, stats['blue']/exp_n*100, 
                    stats['purple']/exp_n*100, stats['pink']/exp_n*100))
    
measure_lamp_statistics()