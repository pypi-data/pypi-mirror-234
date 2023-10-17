"""
Copyright (c) 2023 Gabriel Guerrer

Distributed under the MIT license - See LICENSE for details
"""

"""
The RAVA_RNG_LED class implements the code for controlling the LED and LAMP 
modules within the RAVA circuit. It allows users to adjust the color and the 
intensity of the attached LED. Users can also activate the LAMP mode and 
retrieve statistical information on its operation.

For more information on how LED and LAMP modules operate, refer to the firmware 
documentation.
"""

from rng_rava.rava_defs import *
from rng_rava.rava_rng import *


class RAVA_RNG_LED(RAVA_RNG):

    def __init__(self):
        super().__init__(dev_name='RAVA_RNG_LED')


    def connect(self, serial_number):
        if not super().connect(serial_number=serial_number):
            return False

        # LED firmware enabled?
        if not self.dev_firmware_led:
            lg.warning('{} Connect: LED code is disabled in the firmware'
                .format(self.dev_name))

        # LED attached?
        if not self.get_led_attached():
            lg.warning('{} Connect: Firmware claims no LED is attached.'
                '\n{}   If false, fix it with snd_eeprom_led(led_attached=True)'
                .format(self.dev_name, LOG_FILL))
                
        return True
        

    def process_serial_comm(self, comm_id, comm_data):
        super().process_serial_comm(comm_id=comm_id, comm_data=comm_data)

        # LED_STATUS
        if comm_id == D_DEV_COMM['LED_STATUS']:
            # color, intensity, color_fading, intensity_fading
            self.put_queue_data('LED_STATUS', 
                                self.unpack_rava_msgdata(comm_data, 'BBBB'))
   
        # LAMP_DEBUG
        elif comm_id == D_DEV_COMM['LAMP_DEBUG']:     
            z, mag, mag_avg = self.unpack_rava_msgdata(comm_data, 'fBB')
            lg.debug('> LAMP DBG: z={:.2f}, mag={}, mag_avg={}'
                     .format(z, mag, mag_avg))

        # LAMP_STATISTICS
        elif comm_id == D_DEV_COMM['LAMP_STATISTICS']:
            exp_n, exp_n_zsig, n_extra_bytes = \
                self.unpack_rava_msgdata(comm_data, 'HHB')
            exp_colors_bytes = self.read_serial(n_extra_bytes)
            exp_colors = struct.unpack('<HHHHHHHH', exp_colors_bytes)
            self.put_queue_data('LAMP_STATISTICS', 
                                (exp_n, exp_n_zsig, *exp_colors))

    
    #####################
    ## LED

    def get_led_attached(self):
        return self.get_eeprom_led()['led_attached']
    

    def snd_led_color(self, color_hue, intensity=255):
        if color_hue >= 2**8:
            lg.error('{} LED Color: Provide color_hue as a 8-bit integer'
                     .format(self.dev_name))
            return None
        if intensity >= 2**8:
            lg.error('{} LED Color: Provide intensity as a 8-bit integer'
                     .format(self.dev_name))
            return None
        
        comm = 'LED_COLOR'
        return self.snd_rava_msg(comm, [color_hue, intensity], 'BB')


    def snd_led_color_fade(self, color_hue_tgt, duration_ms):
        if color_hue_tgt >= 2**8:
            lg.error('{} LED Color: Provide color_hue_tgt as a 8-bit '
                     'integer'.format(self.dev_name))
            return None
        if duration_ms >= 2**16:
            lg.error('{} LED Color: Provide duration_ms as a 16-bit integer'
                     .format(self.dev_name))
            return None
        
        comm = 'LED_COLOR_FADE'
        return self.snd_rava_msg(comm, [color_hue_tgt, duration_ms], 'BH')


    def snd_led_color_oscillate(self, n_cycles, duration_ms):
        if n_cycles >= 2**8:
            lg.error('{} LED Color: Provide n_cycles as a 8-bit integer'
                     .format(self.dev_name))
            return None
        if duration_ms >= 2**16:
            lg.error('{} LED Color: Provide duration_ms as a 16-bit integer'
                     .format(self.dev_name))
            return None
        
        comm = 'LED_COLOR_OSCILLATE'
        return self.snd_rava_msg(comm, [n_cycles, duration_ms], 'BH')


    def snd_led_intensity(self, intensity):
        if intensity >= 2**8:
            lg.error('{} LED Intensity: Provide intensity as a 8-bit '
                     'integer'.format(self.dev_name))
            return None
        
        comm = 'LED_INTENSITY'
        return self.snd_rava_msg(comm, [intensity], 'B')


    def snd_led_intensity_fade(self, intensity_tgt, duration_ms):
        if intensity_tgt >= 2**8:
            lg.error('{} LED Intensity: Provide intensity_tgt as a 8-bit '
                     'integer'.format(self.dev_name))
            return None
        if duration_ms >= 2**16:
            lg.error('{} LED Intensity: Provide duration_ms as a 16-bit '
                     'integer'.format(self.dev_name))
            return None
        
        comm = 'LED_INTENSITY_FADE'
        return self.snd_rava_msg(comm, [intensity_tgt, duration_ms], 'BH')    


    def snd_led_fade_stop(self):
        comm = 'LED_FADE_STOP'
        return self.snd_rava_msg(comm)


    def get_led_status(self, timeout=GET_TIMEOUT_S):
        comm = 'LED_STATUS'
        if self.snd_rava_msg(comm):
            color_hue, intensity, color_fading, intensity_fading = \
                self.get_queue_data(comm, timeout=timeout)
            if color_hue in D_LED_COLOR_INV:
                color_str = D_LED_COLOR_INV[color_hue]
            else:
                color_str = ''
            return {'color_hue':color_hue, 
                    'color':color_str, 
                    'intensity':intensity, 
                    'color_fading':color_fading, 
                    'intensity_fading':intensity_fading}
   

    #####################
    ## LAMP

    def snd_lamp_mode(self, on=True):
        comm = 'LAMP_MODE'
        return self.snd_rava_msg(comm, [on], 'B')


    def get_lamp_statistics(self, timeout=GET_TIMEOUT_S):
        # Every get command resets the statistics values 
        comm = 'LAMP_STATISTICS'
        if self.snd_rava_msg(comm):
            data_vars = self.get_queue_data(comm, timeout=timeout)
            data_names = ['exp_n', 'exp_n_zsig', 
                          'red', 'orange', 'yellow', 'green', 
                          'cyan', 'blue', 'purple', 'pink']
            return dict(zip(data_names, data_vars))
        
        
    def snd_lamp_debug(self, on=True):
        # Set lg.setLevel(10), and then run snd_lamp_mode(True)
        comm = 'LAMP_DEBUG'
        return self.snd_rava_msg(comm, [on], 'B')