"""
Copyright (c) 2023 Gabriel Guerrer

Distributed under the MIT license - See LICENSE for details
"""

"""
Definitions and variables used by the RAVA modules.
"""

import logging

#####################
## LOGGING

# RAVA_LOG_LEVEL = logging.DEBUG
RAVA_LOG_LEVEL = logging.INFO

LOG_FILL = 14 * ' '

logging.basicConfig(level=RAVA_LOG_LEVEL, 
                    format='%(asctime)s %(levelname)s %(message)s', 
                    datefmt='%H:%M:%S')

lg = logging.getLogger(__name__)


#####################
# DEFINITIONS

RAVA_USB_VID = 0x1209 # https://pid.codes
RAVA_USB_PID = 0x4884 

COMM_MSG_START = b'$'

COMM_MSG_LEN = 8

GET_TIMEOUT_S = 3.

SERIAL_LISTEN_LOOP_DELAY_S = 0.02 # 20 ms, 50 Hz readings

RNG_BYTE_STREAM_MAX_DELAY_MS = 4194 

D_DEV_COMM = {
    'DEVICE_SERIAL_NUMBER':1,
    'DEVICE_TEMPERATURE':2,
    'DEVICE_FREE_RAM':3,
    'DEVICE_REBOOT':4, 
    'DEVICE_DEBUG':5,

    'EEPROM_RESET_TO_DEFAULT':10,
    'EEPROM_DEVICE':11,
    'EEPROM_FIRMWARE':12,
    'EEPROM_PWM':13,
    'EEPROM_RNG':14,    
    'EEPROM_LED':15,
    'EEPROM_LAMP':16,

    'PWM_SETUP':30,

    'RNG_SETUP':40,
    'RNG_PULSE_COUNTS':41,
    'RNG_BITS':42,
    'RNG_BYTES':43,
    'RNG_TIMING_DEBUG_D1':44,
    
    'RNG_INT8S':50,
    'RNG_INT16S':51,

    'RNG_STREAM_START':60,
    'RNG_STREAM_STOP':61,
    'RNG_STREAM_BYTES':62,
    'RNG_STREAM_STATUS':63,    

    'HEALTH_STARTUP_RUN':70,
    'HEALTH_STARTUP_RESULTS':71,
    'HEALTH_CONTINUOUS_ERRORS':72,

    'LED_COLOR':80,
    'LED_COLOR_FADE':81,
    'LED_COLOR_OSCILLATE':82,
    'LED_INTENSITY':83,
    'LED_INTENSITY_FADE':84,
    'LED_FADE_STOP':85,
    'LED_STATUS':86,

    'LAMP_MODE':90,
    'LAMP_STATISTICS':91,
    'LAMP_DEBUG':92,
    
    'PERIPH_MODE':100,
    'PERIPH_READ':101,
    'PERIPH_WRITE':102,
    'PERIPH_PULSE':103,

    'PERIPH_D1_TRIGGER_INPUT':110,
    'PERIPH_D1_COMPARATOR':111,
    'PERIPH_D1_DELAY_US_TEST':112,
    'PERIPH_D2_TIMER3_INPUT_CAPTURE':113,
    'PERIPH_D3_TIMER3_TRIGGER_OUTPUT':114,
    'PERIPH_D3_TIMER3_PWM':115,
    'PERIPH_D4_PIN_CHANGE':116,
    'PERIPH_D5_ADC':117,

    'INTERFACE_DS18B20':130
    }
D_DEV_COMM_INV = {v: k for k, v in D_DEV_COMM.items()}

D_PWM_FREQ = {
    '30_KHZ':1,
    '40_KHZ':2,
    '50_KHZ':3,
    '60_KHZ':4,
    '75_KHZ':5
    }
D_PWM_FREQ_INV = {v: k for k, v in D_PWM_FREQ.items()}

D_RNG_BIT_SRC = {
    'AB':1,
    'A':2,
    'B':3,
    'AB_XOR':4,
    'AB_RND':5
}
D_RNG_BIT_SRC_INV = {v: k for k, v in D_RNG_BIT_SRC.items()}

D_RNG_BYTE_OUT = {
    'PY_BYTES':1,
    'PY_LIST':2,
    'NUMPY_ARRAY':3,
}
D_RNG_BYTE_OUT_INV = {v: k for k, v in D_RNG_BYTE_OUT.items()}

D_RNG_POSTPROC = {
    'NONE':0,
    'XOR':1,
    'XOR_DICHTL':2,
    'VON_NEUMANN':3
    }
D_RNG_POSTPROC_INV = {v: k for k, v in D_RNG_POSTPROC.items()}

D_PERIPH_MODES = {
    'INPUT':0,
    'OUTPUT':1 
}
D_PERIPH_MODES_INV = {v: k for k, v in D_PERIPH_MODES.items()}

D_LED_COLOR = {
    'RED':0,
    'ORANGE':16,
    'YELLOW':32,
    'GREEN':96,
    'CYAN':128,
    'BLUE':160,
    'PURPLE':192,
    'PINK':224
    }
D_LED_COLOR_INV = {v: k for k, v in D_LED_COLOR.items()}