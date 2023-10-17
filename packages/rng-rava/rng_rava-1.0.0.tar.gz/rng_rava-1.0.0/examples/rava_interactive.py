'''
This file should be opened in an interactive Python environment. In VSCode, the 
users can utilize the F6 shortcut to execute the initial code, establishing a 
connection with the device. Next, users can navigate the code and execute each 
line by positioning the cursor and pressing Shift + Enter. This approach 
facilitates comprehensive testing of the RAVA's functionality.

This example code is in the public domain.
Author: Gabriel Guerrer
'''

import rng_rava as rava

# Set logging level
rava.lg.setLevel(10) # DEBUG
# rava.lg.setLevel(20) # INFO

# Find RAVA device and connect
rava_sns = rava.find_rava_sns()
rng = rava.RAVA_RNG_LED()
if len(rava_sns):
    rng.connect(serial_number=rava_sns[0])
else:
    rava.lg.error('No device found')


def DEVICE():

    rng.connect(serial_number=rava_sns[0])

    rng.connected()

    rng.close()

    rng.get_device_serial_number()
    
    rng.get_device_temperature()

    rng.get_device_free_ram()

    rng.snd_device_reboot()
    

def EEPROM():

    rng.snd_eeprom_reset_to_default()

    rng.get_eeprom_device()
    rng.snd_eeprom_device(temp_calib_slope=397, temp_calib_intercept=-280)
    rng.snd_eeprom_device(temp_calib_slope=300, temp_calib_intercept=-200)

    rng.get_eeprom_firmware()

    rng.get_eeprom_pwm()
    rng.snd_eeprom_pwm(freq_id=rava.D_PWM_FREQ['30_KHZ'], duty=12)
    rng.snd_eeprom_pwm(freq_id=rava.D_PWM_FREQ['40_KHZ'], duty=12)
    rng.snd_eeprom_pwm(freq_id=rava.D_PWM_FREQ['50_KHZ'], duty=20)
    rng.snd_eeprom_pwm(freq_id=rava.D_PWM_FREQ['60_KHZ'], duty=25)
    rng.snd_eeprom_pwm(freq_id=rava.D_PWM_FREQ['75_KHZ'], duty=25)

    rng.get_eeprom_rng()
    rng.snd_eeprom_rng(sampling_interval_us=5)
    rng.snd_eeprom_rng(sampling_interval_us=10)
    rng.snd_eeprom_rng(sampling_interval_us=15)

    rng.get_eeprom_led()
    rng.snd_eeprom_led(led_attached=0)
    rng.snd_eeprom_led(led_attached=1)

    rng.get_eeprom_lamp()
    rng.snd_eeprom_lamp(exp_dur_max_ms=5*60*1000, exp_z_significant=3.925, exp_mag_smooth_n_trials=20)
    rng.snd_eeprom_lamp(exp_dur_max_ms=1*60*1000, exp_z_significant=3.925, exp_mag_smooth_n_trials=10)


def PWM():

    rng.get_pwm_setup()

    rng.snd_pwm_setup(freq_id=rava.D_PWM_FREQ['30_KHZ'], duty=12)
    rng.snd_pwm_setup(freq_id=rava.D_PWM_FREQ['40_KHZ'], duty=12)
    rng.snd_pwm_setup(freq_id=rava.D_PWM_FREQ['50_KHZ'], duty=20)
    rng.snd_pwm_setup(freq_id=rava.D_PWM_FREQ['60_KHZ'], duty=25)
    rng.snd_pwm_setup(freq_id=rava.D_PWM_FREQ['75_KHZ'], duty=25)


def RNG():

    rng.get_rng_setup()

    rng.snd_rng_setup(sampling_interval_us=5)
    rng.snd_rng_setup(sampling_interval_us=10)
    rng.snd_rng_setup(sampling_interval_us=15)

    rng.snd_rng_timing_debug_d1(on=True)
    rng.snd_rng_timing_debug_d1(on=False)
    
    rng.get_rng_pulse_counts(n_counts=100)
    
    rng.get_rng_bits(bit_type_id=rava.D_RNG_BIT_SRC['AB'])
    rng.get_rng_bits(bit_type_id=rava.D_RNG_BIT_SRC['A'])
    rng.get_rng_bits(bit_type_id=rava.D_RNG_BIT_SRC['B'])
    rng.get_rng_bits(bit_type_id=rava.D_RNG_BIT_SRC['AB_XOR'])
    rng.get_rng_bits(bit_type_id=rava.D_RNG_BIT_SRC['AB_RND'])

    rng.get_rng_bytes(n_bytes=100, postproc_id=rava.D_RNG_POSTPROC['NONE'], out_type=rava.D_RNG_BYTE_OUT['NUMPY_ARRAY'])
    rng.get_rng_bytes(n_bytes=100, postproc_id=rava.D_RNG_POSTPROC['XOR'], out_type=rava.D_RNG_BYTE_OUT['PY_LIST']) 
    rng.get_rng_bytes(n_bytes=100, postproc_id=rava.D_RNG_POSTPROC['XOR_DICHTL'], out_type=rava.D_RNG_BYTE_OUT['PY_BYTES']) 
    rng.get_rng_bytes(n_bytes=100, postproc_id=rava.D_RNG_POSTPROC['VON_NEUMANN'], out_type=rava.D_RNG_BYTE_OUT['NUMPY_ARRAY'])

    rng.get_rng_int8s(n_ints=100, int_max=99)
    rng.get_rng_int16s(n_ints=100, int_max=999)
    rng.get_rng_floats(n_floats=100)
    rng.get_rng_doubles(n_doubles=100)

    rng.get_rng_byte_stream_status()

    rng.snd_rng_byte_stream_start(n_bytes=1, stream_delay_ms=50, postproc_id=rava.D_RNG_POSTPROC['NONE'])    
    rng.snd_rng_byte_stream_start(n_bytes=10000, stream_delay_ms=0, postproc_id=rava.D_RNG_POSTPROC['NONE'])   

    rng.get_rng_byte_stream_data(out_type=rava.D_RNG_BYTE_OUT['PY_BYTES'])
    rng.get_rng_byte_stream_data(out_type=rava.D_RNG_BYTE_OUT['NUMPY_ARRAY'])

    rng.snd_rng_byte_stream_stop()


def HEALTH():

    rng.snd_health_startup_run()

    rng.get_health_startup_results()

    rava.print_health_startup_results(*rng.get_health_startup_results())
    
    rng.get_health_continuous_errors()


def PERIPHERALS_DIGITAL_IO():

    rng.snd_periph_digi_mode(periph_id=1, mode_id=rava.D_PERIPH_MODES['INPUT'])
    rng.snd_periph_digi_mode(periph_id=1, mode_id=rava.D_PERIPH_MODES['OUTPUT'])
    rng.get_periph_digi_state(periph_id=1)
    rng.snd_periph_digi_state(periph_id=1, digi_state=0)
    rng.snd_periph_digi_state(periph_id=1, digi_state=1)
    rng.snd_periph_digi_pulse(periph_id=1, pulse_duration_us=100)

    rng.snd_periph_digi_mode(periph_id=2, mode_id=rava.D_PERIPH_MODES['INPUT'])
    rng.snd_periph_digi_mode(periph_id=2, mode_id=rava.D_PERIPH_MODES['OUTPUT'])
    rng.get_periph_digi_state(periph_id=2)
    rng.snd_periph_digi_state(periph_id=2, digi_state=0)
    rng.snd_periph_digi_state(periph_id=2, digi_state=1)
    rng.snd_periph_digi_pulse(periph_id=2, pulse_duration_us=100)

    rng.snd_periph_digi_mode(periph_id=3, mode_id=rava.D_PERIPH_MODES['INPUT'])
    rng.snd_periph_digi_mode(periph_id=3, mode_id=rava.D_PERIPH_MODES['OUTPUT'])
    rng.get_periph_digi_state(periph_id=3)
    rng.snd_periph_digi_state(periph_id=3, digi_state=0)
    rng.snd_periph_digi_state(periph_id=3, digi_state=1)
    rng.snd_periph_digi_pulse(periph_id=3, pulse_duration_us=100)

    rng.snd_periph_digi_mode(periph_id=4, mode_id=rava.D_PERIPH_MODES['INPUT'])
    rng.snd_periph_digi_mode(periph_id=4, mode_id=rava.D_PERIPH_MODES['OUTPUT'])
    rng.get_periph_digi_state(periph_id=4)
    rng.snd_periph_digi_state(periph_id=4, digi_state=0)
    rng.snd_periph_digi_state(periph_id=4, digi_state=1)
    rng.snd_periph_digi_pulse(periph_id=4, pulse_duration_us=100)

    rng.snd_periph_digi_mode(periph_id=5, mode_id=rava.D_PERIPH_MODES['INPUT'])
    rng.snd_periph_digi_mode(periph_id=5, mode_id=rava.D_PERIPH_MODES['OUTPUT'])
    rng.get_periph_digi_state(periph_id=5)
    rng.snd_periph_digi_state(periph_id=5, digi_state=0)
    rng.snd_periph_digi_state(periph_id=5, digi_state=1)
    rng.snd_periph_digi_pulse(periph_id=5, pulse_duration_us=100)


def PERIPHERALS():

    rng.snd_periph_d1_trigger_input(on=True)
    rng.snd_periph_d1_trigger_input(on=False)

    rng.snd_periph_d1_comparator(neg_to_adc12=False)
    rng.snd_periph_d1_comparator(neg_to_adc12=True)
    rng.snd_periph_d1_comparator(on=False)

    rng.snd_periph_digi_mode(periph_id=1, mode_id=rava.D_PERIPH_MODES['OUTPUT'])
    rng.snd_periph_d1_delay_us_test(delay_us=1)
    rng.snd_periph_d1_delay_us_test(delay_us=5)
    rng.snd_periph_d1_delay_us_test(delay_us=10)

    # Running with an unconnected D2 may flood the driver with random signaling
    rng.snd_periph_d2_input_capture(on=True) 
    rng.snd_periph_d2_input_capture(on=False)
    rng.get_periph_d2_input_capture() 

    rng.snd_periph_d3_timer3_trigger_output(delay_ms=1)
    rng.snd_periph_d3_timer3_trigger_output(delay_ms=10)
    rng.snd_periph_d3_timer3_trigger_output(delay_ms=100)
    rng.snd_periph_d3_timer3_trigger_output(on=False)

    rng.snd_periph_d3_timer3_pwm(freq_prescaler=1, top=2**16-1, duty=1000)
    rng.snd_periph_d3_timer3_pwm(freq_prescaler=1, top=2**8-1, duty=10)
    rng.snd_periph_d3_timer3_pwm(freq_prescaler=1, top=2**5-1, duty=10)
    rng.snd_periph_d3_timer3_pwm(on=False)

    rng.snd_periph_d4_pin_change(on=True)
    rng.snd_periph_d4_pin_change(on=False)        

    rng.get_periph_d5_adc_read(ref_5v=0, clk_prescaler=1, oversampling_n_bits=0)
    rng.get_periph_d5_adc_read(ref_5v=0, clk_prescaler=6, oversampling_n_bits=0)
    rng.get_periph_d5_adc_read(ref_5v=0, clk_prescaler=6, oversampling_n_bits=6)
    rng.get_periph_d5_adc_read(on=False)


def INTERFACES():    

    rng.get_interface_ds18bs0()


def LED():

    rng.snd_led_color(color_hue=rava.D_LED_COLOR['RED'], intensity=255)
    rng.snd_led_color(color_hue=rava.D_LED_COLOR['ORANGE'], intensity=255)
    rng.snd_led_color(color_hue=rava.D_LED_COLOR['YELLOW'], intensity=255)
    rng.snd_led_color(color_hue=rava.D_LED_COLOR['GREEN'], intensity=255)
    rng.snd_led_color(color_hue=rava.D_LED_COLOR['BLUE'], intensity=255)
    rng.snd_led_color(color_hue=rava.D_LED_COLOR['PURPLE'], intensity=255)
    rng.snd_led_color(color_hue=rava.D_LED_COLOR['PINK'], intensity=255)

    rng.snd_led_color_fade(color_hue_tgt=rava.D_LED_COLOR['RED'], duration_ms=1000)
    rng.snd_led_color_fade(color_hue_tgt=rava.D_LED_COLOR['ORANGE'], duration_ms=1000)
    rng.snd_led_color_fade(color_hue_tgt=rava.D_LED_COLOR['YELLOW'], duration_ms=1000)
    rng.snd_led_color_fade(color_hue_tgt=rava.D_LED_COLOR['GREEN'], duration_ms=1000)
    rng.snd_led_color_fade(color_hue_tgt=rava.D_LED_COLOR['BLUE'], duration_ms=1000)
    rng.snd_led_color_fade(color_hue_tgt=rava.D_LED_COLOR['PINK'], duration_ms=1000)

    rng.snd_led_color_oscillate(n_cycles=3, duration_ms=3000)
    rng.snd_led_color_oscillate(n_cycles=10, duration_ms=10000)

    rng.snd_led_intensity(intensity=0)
    rng.snd_led_intensity(intensity=63)
    rng.snd_led_intensity(intensity=127)
    rng.snd_led_intensity(intensity=190)
    rng.snd_led_intensity(intensity=255)

    rng.snd_led_intensity_fade(intensity_tgt=0, duration_ms=1000)
    rng.snd_led_intensity_fade(intensity_tgt=255, duration_ms=1000)

    rng.snd_led_fade_stop()

    rng.get_led_status()


def LAMP():

    rng.snd_lamp_mode(on=True)
    rng.snd_lamp_mode(on=False)

    rng.snd_lamp_debug(on=True)
    rng.snd_lamp_debug(on=False)

    rng.get_lamp_statistics()