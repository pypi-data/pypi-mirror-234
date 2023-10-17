"""
Copyright (c) 2023 Gabriel Guerrer

Distributed under the MIT license - See LICENSE for details
"""

"""
The RAVA driver implements the code for communicating with an RAVA device 
running the RAVA firmware. The computer running the driver assumes the role of 
the leader device, sending command requests and reading the data replies.

The RAVA_RNG class enables the request of pulse counts, random bits, random 
bytes, and random numbers (integers and floats). Additionally, it establishes 
the circuit's basic functionality encompassing key modules such as EEPROM, PWM, 
heath tests, peripherals, and interfaces.

The functions that provide access to RAVA's functionality are prefixed with 
"snd" and "get". "Snd" commands are unidirectional and do not expect a device's
response. Conversely, "get" commands are bidirectional, where the driver 
immediately attempts to retrieve the expected information after signaling the 
RAVA device.

The communication exchanges start with an 8-byte message. The first byte holds 
the character '$' (00100100), signifying the message start. The second byte 
encodes the command's identification code, while the subsequent bytes house the 
command's specific data. The commands are sent to the RAVA device using the
snd_rava_msg() function, which generates the 8-byte information with the 
pack_rava_msg() function.

The driver operates with a parallel thread running the loop_serial_listen() 
function to continuously monitor RAVA responses. When a new message is detected, 
it undergoes further processing within the process_serial_comm() function. This 
function stores the command's variables in a queue object associated with the 
respective command ID. To achieve this, the 6-byte data is transformed into the 
command's specific variables using the unpack_rava_msgdata() function. These 
variables are then available for retrieval by employing the get_queue_data() 
function.

The queue-based design not only mitigates read-ordering conflicts but also 
serves as the foundation for the asynchronous driver version, which uses asyncio 
queues and implements get_queue_data() as an async function. This capability is 
realized in the RAVA_RNG_AIO class.
"""

import struct
import time
import threading
import queue
import weakref

import serial
from serial.tools.list_ports import comports
import numpy as np

from rng_rava.rava_defs import *


def find_rava_sns(usb_vid=RAVA_USB_VID, usb_pid=RAVA_USB_PID):
    return [port_info.serial_number for port_info in comports() 
            if (port_info.vid == usb_vid and port_info.pid == usb_pid)]


def find_rava_port(serial_number):
    if isinstance(serial_number, bytes):
        serial_number = serial_number.decode()

    ports = [port_info.device for port_info in comports() 
                if port_info.serial_number == serial_number]
    if len(ports):
        return ports[0]
    else:        
        return None


def find_usb_info(port):
    return [(port_info.product, port_info.vid, port_info.pid) for port_info 
        in comports() if (port_info.device == port)][0]


def process_bytes(bytes_data, out_type):
    if not out_type in D_RNG_BYTE_OUT_INV:
        lg.error('Process Bytes: Unknown out_type {}'.format(out_type))
        return None
    
    if out_type == D_RNG_BYTE_OUT['PY_BYTES']:
        bytes_proc = bytes_data
    elif out_type == D_RNG_BYTE_OUT['PY_LIST']:
        bytes_proc = list(struct.unpack('<{}B'.format(len(bytes_data)), bytes_data))
    elif out_type == D_RNG_BYTE_OUT['NUMPY_ARRAY']:
        bytes_tuple = struct.unpack('<{}B'.format(len(bytes_data)), bytes_data)
        bytes_proc = np.array(bytes_tuple, dtype=np.uint8)
    return bytes_proc


def print_health_startup_results(test_success, test_vars_dict):
    success_str = 'Success' if test_success else 'Failed'

    (pc_avg_a, pc_avg_b, pc_avg_dif_a, pc_avg_dif_b, 
      pc_avg_min, pc_avg_diff_min, pc_result) = \
        test_vars_dict['pulse_count']
    (bias_a, bias_b, bias_abs_treshold, bias_result) = \
        test_vars_dict['bit_bias']
    (chisq_a, chisq_b, chisq_max_treshold, chisq_result) = \
        test_vars_dict['byte_bias']
    
    lg.info('Startup Health Tests: {}'.format(success_str) + \
            '\n{}Pulse count: {}'.format(LOG_FILL, bool(pc_result)) + \
            '\n{}  pc_a={:.2f}, pc_b={:.2f}, pc_tresh={:.2f}'\
                .format(LOG_FILL, pc_avg_a, pc_avg_b, pc_avg_min) + \
            '\n{}  pc_diff_a={:.2f}, pc_diff_b={:.2f}, pc_diff_tresh={:.2f}'\
                .format(LOG_FILL, pc_avg_dif_a, pc_avg_dif_b, 
                        pc_avg_diff_min) + \
            '\n{}Bit bias: {}'.format(LOG_FILL, bool(bias_result)) + \
            '\n{}  bias_a={:.4f}, bias_b={:.4f}, bias_tresh={:.2f}'\
                .format(LOG_FILL, bias_a, bias_b, bias_abs_treshold) + \
            '\n{}Byte bias: {}'.format(LOG_FILL, bool(chisq_result)) + \
            '\n{}  chisq_a={:.4f}, chisq_b={:.4f}, chisq_tresh={:.2f}'
                .format(LOG_FILL, chisq_a, chisq_b, chisq_max_treshold))


class RAVA_RNG:
    
    rava_instances = weakref.WeakSet()
    
    def __init__(self, dev_name='RAVA_RNG'):
        self.dev_name = dev_name
        self.queue_type = queue.Queue
        
        # Debug
        lg.debug('> {} INIT'.format(self.dev_name))
        
        # Variables defined upon connection
        self.dev_serial_number = ''
        self.dev_firmware_version = 0.
        self.dev_firmware_led = None
        self.dev_usb_port = ''
        self.dev_usb_name = ''
        self.dev_usb_vid = None
        self.dev_usb_pid = None

        # Serial variables
        self.serial = serial.Serial()
        self.serial_connected = threading.Event() # Used by loop_serial_listen()
        self.serial_read_lock = threading.Lock()
        self.serial_write_lock = threading.Lock()
        self.serial_data = {}
        self.serial_listen_thread = None

        # Byte streaming variables
        self.rng_streaming = False

        # Finalize any previous RAVA instance
        for rava_instance in self.rava_instances.copy():
            rava_instance.close()
            self.rava_instances.remove(rava_instance)

        # Add new instance to weakref list
        self.rava_instances.add(self) 


    def __del__(self):
        # Debug
        lg.debug('> {} DEL'.format(self.dev_name))


    def connect(self, serial_number):
        # Debug
        lg.debug('> {} CONNECT'.format(self.dev_name))

        # Find serial port
        port = find_rava_port(serial_number)
        if port is None:
            lg.error('{} Connect: No device found with SN {}'
                     .format(self.dev_name, serial_number))
            return False

        # Open serial connection
        if not self.open_serial(port):
            return False
        
        # Save SN info
        self.dev_serial_number = serial_number

        # Reset serial data queues
        self.init_queue_data()
        
        # Start listening for serial commands
        self.serial_listen_thread = \
            threading.Thread(target=self.loop_serial_listen)        
        self.serial_listen_thread.start()

        # Stop any active RNG byte stream
        self.snd_rng_byte_stream_stop()

        # Request firmware info
        firmw_info = self.get_eeprom_firmware()
        self.dev_firmware_version = firmw_info['version']
        self.dev_firmware_led = firmw_info['led_enabled']

        # Print connection info
        lg.info('{} Connect: Success'
                '\n{}{}, Firmware v{:.2f}, SN={}, at {}'
                .format(self.dev_name, LOG_FILL, self.dev_usb_name, 
                        self.dev_firmware_version, self.dev_serial_number, 
                        self.serial.port))

        # Request Health startup info
        if firmw_info['health_startup_enabled']:
            test_success, test_vars = self.get_health_startup_results()

            # Print test info
            print_health_startup_results(test_success, test_vars)

            # Error? Users have then a limited command variety (see Firmware)
            if not test_success: 
                lg.warning('{} Connect: Startup tests failed'
                           .format(self.dev_name))

        return True

        
    def connected(self):
        return self.serial.is_open


    def close(self):
        # Debug
        lg.debug('> {} CLOSE'.format(self.dev_name))

        # Stop loop_serial_listen
        self.serial_connected.clear() 

        # Close serial connection
        self.serial.close()


    def init_queue_data(self):
        # Create one queue for each command
        self.serial_data = {}
        for comm in D_DEV_COMM.keys():
            self.serial_data[comm] = self.queue_type()


    def put_queue_data(self, comm, value, comm_ext_id=0):
        # Check key
        if not (comm in self.serial_data):
            lg.error('{} Data: Unknown comm {}'.format(self.dev_name, comm))
            return False

        # Extended key
        if comm_ext_id:
            comm_ext = '{}_{}'.format(comm, comm_ext_id)

            # Queue exists?
            if not (comm_ext in self.serial_data):
                self.serial_data[comm_ext] = self.queue_type()
        else:
            comm_ext = comm
        
        # Try writing to queue
        try:
            self.serial_data[comm_ext].put(value)
            return True
        
        except queue.Full:
            lg.error('{} Data: {} Queue full'.format(self.dev_name, comm_ext))
            return False


    def get_queue_data(self, comm, comm_ext_id=0, timeout=GET_TIMEOUT_S):
        # Check key
        if not (comm in self.serial_data):
            lg.error('{} Data: Unknown comm {}'.format(self.dev_name, comm))
            return None

        # Extended key
        if comm_ext_id:
            comm_ext = '{}_{}'.format(comm, comm_ext_id)

            # Queue exists?
            if not (comm_ext in self.serial_data):
                self.serial_data[comm_ext] = self.queue_type()
        else:
            comm_ext = comm
        
        # Try reading from queue
        try:
            return self.serial_data[comm_ext].get(timeout=timeout)
        
        except queue.Empty:
            lg.error('{} Data: Timeout retrieving {}'
                     .format(self.dev_name, comm_ext))
            return None
        

    def open_serial(self, port):
        # Set serial port
        self.serial.port = port

        # Open serial connection
        try:
            self.serial.open()
            self.serial_connected.set()

            # Get USB parameters
            self.dev_usb_port = port
            self.dev_usb_name, self.dev_usb_vid, self.dev_usb_pid = \
                find_usb_info(port)
            return True
        
        except Exception as err:
            lg.error('{} Serial: Failed opening {}'
                     '\n {}{} - {}'
                     .format(self.dev_name, port, 
                             LOG_FILL, type(err).__name__, err))
            return False


    def inwaiting_serial(self):
        # Read in_waiting
        try:
            return self.serial.in_waiting
        
        except Exception as err:
            lg.error('{} Serial: Failed reading in_waiting'
                    '\n {}{} - {}'
                    .format(self.dev_name, 
                            LOG_FILL, type(err).__name__, err))
            # Close device
            self.close()
            return None


    def read_serial(self, n_bytes):
        # Read serial
        try:
            with self.serial_read_lock:
                data = self.serial.read(n_bytes)
            return data
        
        except Exception as err:
            lg.error('{} Serial: Failed reading'
                    '\n {}{} - {}'
                    .format(self.dev_name, 
                            LOG_FILL, type(err).__name__, err))
            # Close device
            self.close()
            return None


    def write_serial(self, comm_bytes):
        # Write serial
        try:
            with self.serial_write_lock:
                self.serial.write(comm_bytes)        
            return True
        
        except Exception as err:
            lg.error('{} Serial: Failed writing'
                    '\n {}{} - {}'
                    .format(self.dev_name, 
                            LOG_FILL, type(err).__name__, err))
            # Close device
            self.close()
            return False
    

    def loop_serial_listen(self):
        try:
            # Debug
            lg.debug('> {} SERIAL LISTEN LOOP'.format(self.dev_name))

            # Loop while connected
            while self.serial_connected.is_set():

                # Command available?
                if self.inwaiting_serial():
                    if self.read_serial(1) == COMM_MSG_START:
                        comm_msg = self.read_serial(COMM_MSG_LEN-1)
                        comm_id = comm_msg[0]
                        comm_data = comm_msg[1:]

                        # Debug
                        lg.debug('> COMM RCV {}'.
                                    format([D_DEV_COMM_INV[comm_id], 
                                           *[c for c in comm_data]]))
                        
                        # Process Command
                        self.process_serial_comm(comm_id, comm_data)
                
                # The non-blocking method is prefered for finishing the thread 
                # when closing the device
                else:
                    time.sleep(SERIAL_LISTEN_LOOP_DELAY_S)

        except Exception as err:
            lg.error('{} Serial Listen Loop: Error'
                     '\n{}{} - {}'
                     .format(self.dev_name, 
                             LOG_FILL, type(err).__name__, err))
            # Close device
            self.close()


    def process_serial_comm(self, comm_id, comm_data):        
        # DEVICE_SERIAL_NUMBER
        if comm_id == D_DEV_COMM['DEVICE_SERIAL_NUMBER']:            
            sn_n_bytes = self.unpack_rava_msgdata(comm_data, 'B')
            sn = self.read_serial(sn_n_bytes).decode()
            self.put_queue_data('DEVICE_SERIAL_NUMBER', sn)
            

        # DEVICE_TEMPERATURE
        elif comm_id == D_DEV_COMM['DEVICE_TEMPERATURE']:            
            # temperature
            self.put_queue_data('DEVICE_TEMPERATURE', 
                                self.unpack_rava_msgdata(comm_data, 'f'))

        # DEVICE_FREE_RAM
        elif comm_id == D_DEV_COMM['DEVICE_FREE_RAM']:            
            # free_ram
            self.put_queue_data('DEVICE_FREE_RAM', 
                                self.unpack_rava_msgdata(comm_data, 'H'))

        # DEVICE_DEBUG
        elif comm_id == D_DEV_COMM['DEVICE_DEBUG']:            
            debug_bytes = self.unpack_rava_msgdata(comm_data, 'BBBBBB')
            debug_ints = [x for x in debug_bytes]
            lg.debug('> RAVA DEBUG MSG {} {} {} {} {} {}'.format(*debug_ints))

        # EEPROM_DEVICE
        elif comm_id == D_DEV_COMM['EEPROM_DEVICE']:
            # temp_calib_slope, temp_calib_intercept
            self.put_queue_data('EEPROM_DEVICE', 
                                self.unpack_rava_msgdata(comm_data, 'Hh'))

        # EEPROM_FIRMWARE
        elif comm_id == D_DEV_COMM['EEPROM_FIRMWARE']:
            # version_hi, version_lo, parameters
            self.put_queue_data('EEPROM_FIRMWARE', 
                                self.unpack_rava_msgdata(comm_data, 'BBB'))

        # EEPROM_PWM
        elif comm_id == D_DEV_COMM['EEPROM_PWM']:
            # freq_id, duty
            self.put_queue_data('EEPROM_PWM', 
                                self.unpack_rava_msgdata(comm_data, 'BB'))

        # EEPROM_RNG
        elif comm_id == D_DEV_COMM['EEPROM_RNG']:
            # sampling_interval_us
            self.put_queue_data('EEPROM_RNG', 
                                self.unpack_rava_msgdata(comm_data, 'B'))

        # EEPROM_LED
        elif comm_id == D_DEV_COMM['EEPROM_LED']:
            # led_attached
            self.put_queue_data('EEPROM_LED', 
                                self.unpack_rava_msgdata(comm_data, 'B'))

        # EEPROM_LAMP
        elif comm_id == D_DEV_COMM['EEPROM_LAMP']:
            exp_mag_smooth_n_trials, extra_n_bytes = \
                self.unpack_rava_msgdata(comm_data, 'BB')
            extra_bytes = self.read_serial(extra_n_bytes)
            exp_dur_max_ms, exp_z_significant = \
                struct.unpack('<Lf', extra_bytes)
            self.put_queue_data('EEPROM_LAMP', 
                (exp_dur_max_ms, exp_z_significant, exp_mag_smooth_n_trials))

        # PWM_SETUP
        elif comm_id == D_DEV_COMM['PWM_SETUP']:
            # freq_id, duty
            self.put_queue_data('PWM_SETUP', 
                                self.unpack_rava_msgdata(comm_data, 'BB'))
       
        # RNG_SETUP
        elif comm_id == D_DEV_COMM['RNG_SETUP']:
            # sampling_interval_us
            self.put_queue_data('RNG_SETUP', 
                                self.unpack_rava_msgdata(comm_data, 'B'))
         
        # RNG_PULSE_COUNTS
        elif comm_id == D_DEV_COMM['RNG_PULSE_COUNTS']:
            n_counts = self.unpack_rava_msgdata(comm_data, 'L')
            counts_bytes = self.read_serial(2 * n_counts)
            counts_bytes_a = counts_bytes[::2]
            counts_bytes_b = counts_bytes[1::2]
            self.put_queue_data('RNG_PULSE_COUNTS', 
                                (counts_bytes_a, counts_bytes_b))
       
        # RNG_BITS
        elif comm_id == D_DEV_COMM['RNG_BITS']:
            bit_type, bit_a, bit_b = self.unpack_rava_msgdata(comm_data, 'BBB')
            if bit_type == D_RNG_BIT_SRC['AB']:
                self.put_queue_data('RNG_BITS', (bit_type, bit_a, bit_b))
            else:
                self.put_queue_data('RNG_BITS', (bit_type, bit_a))

        # RNG_BYTES
        elif comm_id == D_DEV_COMM['RNG_BYTES']:
            n_bytes, request_id = self.unpack_rava_msgdata(comm_data, 'LB')
            rng_bytes = self.read_serial(n_bytes * 2)
            rng_bytes_a = rng_bytes[::2]
            rng_bytes_b = rng_bytes[1::2]
            self.put_queue_data('RNG_BYTES', (rng_bytes_a, rng_bytes_b), 
                                comm_ext_id=request_id)
       
        # RNG_STREAM_BYTES
        elif comm_id == D_DEV_COMM['RNG_STREAM_BYTES']:
            if self.rng_streaming:
                n_bytes = self.unpack_rava_msgdata(comm_data, 'L')
                rng_bytes = self.read_serial(n_bytes * 2)
                rng_bytes_a = rng_bytes[::2]
                rng_bytes_b = rng_bytes[1::2]
                self.put_queue_data('RNG_STREAM_BYTES', 
                                    (rng_bytes_a, rng_bytes_b))
   
        # RNG_STREAM_STATUS
        elif comm_id == D_DEV_COMM['RNG_STREAM_STATUS']:
            # stream_status
            stream_status = self.unpack_rava_msgdata(comm_data, 'B')
            self.put_queue_data('RNG_STREAM_STATUS', bool(stream_status))
    
        # RNG_INT8S
        elif comm_id == D_DEV_COMM['RNG_INT8S']:
            n_ints = self.unpack_rava_msgdata(comm_data, 'L')
            ints_bytes = self.read_serial(n_ints)
            self.put_queue_data('RNG_INT8S', ints_bytes)

        # RNG_INT16S
        elif comm_id == D_DEV_COMM['RNG_INT16S']:
            n_ints = self.unpack_rava_msgdata(comm_data, 'L')
            ints_bytes = self.read_serial(n_ints * 2)
            self.put_queue_data('RNG_INT16S', ints_bytes)

        # HEALTH_STARTUP_RESULTS  
        elif comm_id == D_DEV_COMM['HEALTH_STARTUP_RESULTS']:
            success, pc_avg_n_bytes, bias_bit_n_bytes, bias_byte_n_bytes = \
                self.unpack_rava_msgdata(comm_data, 'BBBB')

            # pc_avg_a, pc_avg_b, pc_avg_dif_a, pc_avg_dif_b,
            # pc_avg_min, pc_avg_diff_min, pc_result
            pc_avg_bytes = self.read_serial(pc_avg_n_bytes)
            pc_avg_vars = struct.unpack('<ffffffB', pc_avg_bytes)
            
            # bias_a, bias_b, bias_abs_treshold, bias_result
            bias_bit_bytes = self.read_serial(bias_bit_n_bytes)
            bias_bit_vars = struct.unpack('<fffB', bias_bit_bytes)

            # chisq_a, chisq_b, chisq_max_treshold, chisq_result
            bias_byte_bytes = self.read_serial(bias_byte_n_bytes)
            bias_byte_vars = struct.unpack('<fffB', bias_byte_bytes)

            self.put_queue_data('HEALTH_STARTUP_RESULTS', 
                (success, pc_avg_vars, bias_bit_vars, bias_byte_vars))

        # HEALTH_CONTINUOUS_ERRORS
        elif comm_id == D_DEV_COMM['HEALTH_CONTINUOUS_ERRORS']:
            n_extra_bytes = self.unpack_rava_msgdata(comm_data, 'B')
            health_extra_bytes = self.read_serial(n_extra_bytes)
            errors = struct.unpack('<HHHH', health_extra_bytes) 
            self.put_queue_data('HEALTH_CONTINUOUS_ERRORS', errors)

        # PERIPH_READ
        elif comm_id == D_DEV_COMM['PERIPH_READ']:
            # periph_id, digi_state
            self.put_queue_data('PERIPH_READ', 
                                self.unpack_rava_msgdata(comm_data, 'BB'))
      
        # PERIPH_D2_TIMER3_INPUT_CAPTURE
        elif comm_id == D_DEV_COMM['PERIPH_D2_TIMER3_INPUT_CAPTURE']:
            input_capture_count, input_capture_1s_n = \
                self.unpack_rava_msgdata(comm_data, 'HH')
            self.put_queue_data('PERIPH_D2_TIMER3_INPUT_CAPTURE', 
                                (input_capture_count, input_capture_1s_n))            
            lg.debug('> INCAPT count={}, ovflw={}, s={:.3f}'
                    .format(input_capture_count, input_capture_1s_n, 
                            input_capture_count*0.000016 + input_capture_1s_n))

        # PERIPH_D5_ADC
        elif comm_id == D_DEV_COMM['PERIPH_D5_ADC']:
            # adc_read_mv
            self.put_queue_data('PERIPH_D5_ADC', 
                                self.unpack_rava_msgdata(comm_data, 'f'))
        
        # INTERFACE_DS18B20
        elif comm_id == D_DEV_COMM['INTERFACE_DS18B20']:
            # temperature
            self.put_queue_data('INTERFACE_DS18B20', 
                                self.unpack_rava_msgdata(comm_data, 'f'))


    #####################
    ## RAVA COMM

    def pack_rava_msg(self, comm_str, data_user=[], data_user_fmt=''):
        # Transform comm and variables into a 8-byte RAVA message

        # Get comm id
        if not(comm_str in D_DEV_COMM):
            lg.error('{} MSG Pack: Unknown command {}'
                     .format(self.dev_name, comm_str))
            return None
        comm_id = D_DEV_COMM[comm_str]

        # Check if data and data_fmt have the same size
        if len(data_user) != len(data_user_fmt):
            lg.error('{} MSG Pack: Data and data_fmt must have the same size'
                     .format(self.dev_name))
            return None

        # Msg data contains (COMM_MSG_LEN - 2) bytes
        # (as the first 2 are always $ and the command id)
        data_usr_n_bytes = struct.calcsize('<' + data_user_fmt)
        data_n_bytes = COMM_MSG_LEN - 2
        if  data_usr_n_bytes > data_n_bytes:
            lg.error('{} MSG Pack: Data contains {} bytes - the maximum is {}'
                     .format(self.dev_name, data_usr_n_bytes, data_n_bytes))
            return None
        
        # Fill remaining data bytes with 0
        data_fmt = data_user_fmt + (data_n_bytes - data_usr_n_bytes) * 'B'
        data = data_user + (data_n_bytes - data_usr_n_bytes) * [0]

        # Pack rava msg
        return struct.pack('<cB' + data_fmt, COMM_MSG_START, comm_id, *data)
    

    def snd_rava_msg(self, comm_str, data_user=[], data_user_fmt=''):
        # Pack rava msg
        comm_bytes = self.pack_rava_msg(comm_str=comm_str, data_user=data_user, 
                                         data_user_fmt=data_user_fmt)
        if comm_bytes is None:
            return False

        # Send command        
        write_success = self.write_serial(comm_bytes)

        # Debug
        if write_success:
            comm_dbg = [c for c in comm_bytes][1:]
            comm_dbg[0] = D_DEV_COMM_INV[comm_dbg[0]]
            lg.debug('> COMM SND {}'.format(comm_dbg))

        return write_success
    
    
    def unpack_rava_msgdata(self, data, data_get_format):        
        # Transform RAVA 6-byte message data into variables

        # Msg data contains (COMM_MSG_LEN - 2) bytes
        data_n_bytes = COMM_MSG_LEN - 2
        if  len(data) != data_n_bytes:
            lg.error('{} MSG Unpack: Data contains {} bytes - expected {}'
                     .format(self.dev_name, len(data), data_n_bytes))
            return None
        
        # Check data_get_fmt 
        dataget_n_bytes = struct.calcsize('<' + data_get_format)
        if (dataget_n_bytes == 0) or (dataget_n_bytes > data_n_bytes):
            lg.error('{} MSG Unpack: Data format asks for {} bytes - expected'
                     ' 0 < size <= {}'
                     .format(self.dev_name, dataget_n_bytes, data_n_bytes))
            return None

        # Fill remaining data fmt bytes
        data_format = data_get_format + (data_n_bytes - dataget_n_bytes) * 'B'

        # Unpack and return data
        vars_n = len(data_get_format)
        vars = struct.unpack('<' + data_format, data)
        if vars_n == 1:
            return vars[:vars_n][0]
        else:
            return vars[:vars_n]
        

    #####################
    ## DEVICE

    def get_device_serial_number(self, timeout=GET_TIMEOUT_S):
        comm = 'DEVICE_SERIAL_NUMBER'
        if self.snd_rava_msg(comm):
            return self.get_queue_data(comm, timeout=timeout)
    

    def get_device_temperature(self, timeout=GET_TIMEOUT_S):
        comm = 'DEVICE_TEMPERATURE'
        if self.snd_rava_msg(comm):
            return self.get_queue_data(comm, timeout=timeout)
    

    def get_device_free_ram(self, timeout=GET_TIMEOUT_S):
        comm = 'DEVICE_FREE_RAM'
        if self.snd_rava_msg(comm):
            return self.get_queue_data(comm, timeout=timeout)


    def snd_device_reboot(self):
        comm = 'DEVICE_REBOOT'
        return self.snd_rava_msg(comm)
    

    #####################
    ## EEPROM

    def snd_eeprom_reset_to_default(self):
        comm = 'EEPROM_RESET_TO_DEFAULT'
        return self.snd_rava_msg(comm)


    def snd_eeprom_device(self, temp_calib_slope, temp_calib_intercept):
        comm = 'EEPROM_DEVICE'
        rava_send = False
        data = [rava_send, temp_calib_slope, temp_calib_intercept]
        return self.snd_rava_msg(comm, data, 'BHh')


    def get_eeprom_device(self, timeout=GET_TIMEOUT_S):
        comm = 'EEPROM_DEVICE'
        rava_send = True
        if self.snd_rava_msg(comm, [rava_send], 'B'):
            data_vars = self.get_queue_data(comm, timeout=timeout)
            data_names = ['temp_calib_slope', 'temp_calib_intercept']
            return dict(zip(data_names, data_vars))
        

    def get_eeprom_firmware(self, timeout=GET_TIMEOUT_S):
        comm = 'EEPROM_FIRMWARE'
        if self.snd_rava_msg(comm):
            version_hi, version_lo, modules = \
                self.get_queue_data(comm, timeout=timeout)
            
            version = float('{}.{}'.format(version_hi, version_lo))
            health_startup_enabled = modules & 1 << 0 != 0
            health_continuous_enabled = modules & 1 << 1 != 0
            led_enabled = modules & 1 << 2 != 0
            lamp_enabled = modules & 1 << 3 != 0
            peripherals_enabled = modules & 1 << 4 != 0
            serial1_enabled = modules & 1 << 5 != 0
            return {'version':version,                 
                    'health_startup_enabled':health_startup_enabled, 
                    'health_continuous_enabled':health_continuous_enabled,
                    'led_enabled':led_enabled, 
                    'lamp_enabled':lamp_enabled,
                    'peripherals_enabled':peripherals_enabled,
                    'serial1_enabled':serial1_enabled
                    }
    

    def snd_eeprom_pwm(self, freq_id, duty):        
        if not freq_id in D_PWM_FREQ_INV:
            lg.error('{} EEPROM PWM: Unknown freq_id {}'
                     .format(self.dev_name, freq_id))
            return False
        if duty == 0:
            lg.error('{} EEPROM PWM: Provide a duty > 0'.format(self.dev_name))
            return False
        
        comm = 'EEPROM_PWM'
        rava_send = False
        return self.snd_rava_msg(comm, [rava_send, freq_id, duty], 'BBB')


    def get_eeprom_pwm(self, timeout=GET_TIMEOUT_S):        
        comm = 'EEPROM_PWM'
        rava_send = True
        if self.snd_rava_msg(comm, [rava_send], 'B'):
            freq_id, duty = self.get_queue_data(comm, timeout=timeout)
            return {'freq_id':freq_id,
                    'freq_str':D_PWM_FREQ_INV[freq_id],
                    'duty':duty}


    def snd_eeprom_rng(self, sampling_interval_us):
        if sampling_interval_us == 0:
            lg.error('{} EEPROM RNG: Provide a sampling_interval_us > 0'
                     .format(self.dev_name))
            return False
        
        comm = 'EEPROM_RNG'
        rava_send = False
        return self.snd_rava_msg(comm, [rava_send, sampling_interval_us], 'BB')


    def get_eeprom_rng(self, timeout=GET_TIMEOUT_S):
        comm = 'EEPROM_RNG'
        rava_send = True
        if self.snd_rava_msg(comm, [rava_send], 'B'):
            sampling_interval_us = self.get_queue_data(comm, timeout=timeout)
            return {'sampling_interval_us':sampling_interval_us}


    def snd_eeprom_led(self, led_attached):
        comm = 'EEPROM_LED'
        rava_send = False
        return self.snd_rava_msg(comm, [rava_send, led_attached], 'BB')


    def get_eeprom_led(self, timeout=GET_TIMEOUT_S):
        comm = 'EEPROM_LED'
        rava_send = True
        if self.snd_rava_msg(comm, [rava_send], 'B'):
            led_attached = self.get_queue_data(comm, timeout=timeout)
            return {'led_attached':led_attached}
    

    def snd_eeprom_lamp(self, exp_dur_max_ms, exp_z_significant, 
                        exp_mag_smooth_n_trials):
        if exp_dur_max_ms < 60000:
            lg.error('{} EEPROM LAMP: Provide an exp_dur_max_ms >= 60000'
                     .format(self.dev_name))
            return False
        if exp_z_significant < 1.0:
            lg.error('{} EEPROM LAMP: Provide an exp_z_significant >= 1.0'
                     .format(self.dev_name))
            return False
        if exp_mag_smooth_n_trials == 0:
            lg.error('{} EEPROM LAMP: Provide an exp_mag_smooth_n_trials > 0'
                     .format(self.dev_name))
            return False
        
        comm = 'EEPROM_LAMP'
        rava_send = False
        if self.snd_rava_msg(comm, 
                             [rava_send, exp_mag_smooth_n_trials, 8], 'BBB'):
            comm_extra = struct.pack('<Lf', exp_dur_max_ms, exp_z_significant)
            return self.write_serial(comm_extra)
        else:
            return False


    def get_eeprom_lamp(self, timeout=GET_TIMEOUT_S):
        comm = 'EEPROM_LAMP'
        rava_send = True
        if self.snd_rava_msg(comm, [rava_send], 'B'):
            data_vars = self.get_queue_data(comm, timeout=timeout)
            data_names = ['exp_dur_max_ms', 'exp_z_significant', 
                          'exp_mag_smooth_n_trials']
            return dict(zip(data_names, data_vars))
        

    #####################
    ## PWM

    def snd_pwm_setup(self, freq_id, duty):        
        if not freq_id in D_PWM_FREQ_INV:
            lg.error('{} PWM: Unknown freq_id {}'
                     .format(self.dev_name, freq_id))
            return False
        if duty == 0:
            lg.error('{} PWM: Provide a duty > 0'.format(self.dev_name))
            return False
        
        comm = 'PWM_SETUP'
        rava_send = False
        return self.snd_rava_msg(comm, [rava_send, freq_id, duty], 'BBB')


    def get_pwm_setup(self, timeout=GET_TIMEOUT_S):
        rava_send = True
        comm = 'PWM_SETUP'
        if self.snd_rava_msg(comm, [rava_send], 'B'):
            freq_id, duty = self.get_queue_data(comm, timeout=timeout)
            return {'freq_id':freq_id,
                    'freq_str':D_PWM_FREQ_INV[freq_id],
                    'duty':duty}


    #####################
    ## RNG

    def snd_rng_setup(self, sampling_interval_us):
        if sampling_interval_us == 0:
            lg.error('{} RNG: Provide a sampling_interval_us > 0'.
                     format(self.dev_name))
            return False
        
        comm = 'RNG_SETUP'
        rava_send = False
        return self.snd_rava_msg(comm, [rava_send, sampling_interval_us], 'BB')


    def get_rng_setup(self, timeout=GET_TIMEOUT_S):
        comm = 'RNG_SETUP'
        rava_send = True
        if self.snd_rava_msg(comm, [rava_send], 'B'):
            sampling_interval_us = self.get_queue_data(comm, timeout=timeout)
            return {'sampling_interval_us':sampling_interval_us}
 

    def snd_rng_timing_debug_d1(self, on=True):
        comm = 'RNG_TIMING_DEBUG_D1'
        return self.snd_rava_msg(comm, [on], 'B')


    def get_rng_pulse_counts(self, n_counts, timeout=GET_TIMEOUT_S):
        comm = 'RNG_PULSE_COUNTS'
        if self.snd_rava_msg(comm, [n_counts], 'L'):
            counts_bytes_a, counts_bytes_b = \
                self.get_queue_data(comm, timeout=timeout)

            counts_a = process_bytes(counts_bytes_a, 
                                     out_type=D_RNG_BYTE_OUT['NUMPY_ARRAY'])
            counts_b = process_bytes(counts_bytes_b, 
                                     out_type=D_RNG_BYTE_OUT['NUMPY_ARRAY'])
            return counts_a, counts_b


    def get_rng_bits(self, bit_type_id, timeout=GET_TIMEOUT_S):
        if not bit_type_id in D_RNG_BIT_SRC_INV:
            lg.error('{} RNG Bits: Unknown bit_type_id {}'
                     .format(self.dev_name, bit_type_id))
            return None

        comm = 'RNG_BITS'
        if self.snd_rava_msg(comm, [bit_type_id], 'B'):
            bit_type_id_recv, *bits = self.get_queue_data(comm, timeout=timeout)

            if bit_type_id == D_RNG_BIT_SRC['AB_RND']:
                bit_type_str = D_RNG_BIT_SRC_INV[bit_type_id_recv]
                return bit_type_str, bits[0]
            elif bit_type_id == D_RNG_BIT_SRC['AB']:
                return tuple(bits)
            else:
                return bits[0]


    def get_rng_bytes(self, n_bytes, postproc_id=D_RNG_POSTPROC['NONE'], 
                      request_id=0, out_type=D_RNG_BYTE_OUT['NUMPY_ARRAY'], 
                      timeout=GET_TIMEOUT_S):
        if not postproc_id in D_RNG_POSTPROC_INV:
            lg.error('{} RNG Bytes: Unknown postproc_id {}'
                     .format(self.dev_name, postproc_id))
            return None
        
        comm = 'RNG_BYTES'
        if self.snd_rava_msg(comm, [n_bytes, postproc_id, request_id], 'LBB'):
            bytes_data = self.get_queue_data(comm, comm_ext_id=request_id, 
                                      timeout=timeout)
            
            if not (bytes_data is None):
                rng_bytes_a, rng_bytes_b = bytes_data
                rng_a = process_bytes(rng_bytes_a, out_type)
                rng_b = process_bytes(rng_bytes_b, out_type)
                return rng_a, rng_b
            else:
                return None, None


    def get_rng_int8s(self, n_ints, int_max, timeout=GET_TIMEOUT_S):
        if n_ints >= 2**32:
            lg.error('{} RNG Ints: Provide n_ints as a 32-bit integer'
                     .format(self.dev_name))
            return None
        if int_max >= 2**8:
            lg.error('{} RNG Ints: Provide int_max as a 8-bit integer'
                     .format(self.dev_name))
            return None

        comm = 'RNG_INT8S'
        if self.snd_rava_msg(comm, [n_ints, int_max], 'LB'):
            ints_bytes = self.get_queue_data(comm, timeout=timeout)
            ints_list = struct.unpack('<{}B'.format(n_ints), ints_bytes)
            return np.array(ints_list, dtype=np.uint8)


    def get_rng_int16s(self, n_ints, int_max, timeout=GET_TIMEOUT_S):
        if n_ints >= 2**32:
            lg.error('{} RNG Ints: Provide n_ints as a 32-bit integer'
                     .format(self.dev_name))
            return None
        if int_max >= 2**16:
            lg.error('{} RNG Ints: Provide int_max as a 16-bit integer'
                     .format(self.dev_name))
            return None

        comm = 'RNG_INT16S'
        if self.snd_rava_msg(comm, [n_ints, int_max], 'LH'):
            ints_bytes = self.get_queue_data(comm, timeout=timeout)
            ints_list = struct.unpack('<{}H'.format(n_ints), ints_bytes)
            return np.array(ints_list, dtype=np.uint16)


    def get_rng_floats(self, n_floats):
        if n_floats >= (2**32) // 4:
            lg.error('{} RNG Floats: Maximum n_floats is {}'
                     .format(self.dev_name, (2**32) // 4))
            return None

        # 32 bits floating point number
        bytes_res = self.get_rng_bytes(n_bytes=n_floats*4, timeout=None)
        if bytes_res is None:
            return 
        rnd_bytes_a, rnd_bytes_b = bytes_res
        
        # XOR them
        int_a = int.from_bytes(rnd_bytes_a, 'little')
        int_b = int.from_bytes(rnd_bytes_b, 'little')
        rnd_bytes = (int_a ^ int_b).to_bytes(len(rnd_bytes_a), 'little')
        # Convert bytes to ints
        rnd_lists = struct.unpack('<{}I'.format(n_floats), rnd_bytes)
        rnd_ints = np.array(rnd_lists, dtype=np.uint32)
        
        # IEEE754 bit pattern for single precision floating point value in the 
        # range of 1.0 - 2.0. Uses the first 23 bytes and fixes the float 
        # exponent to 127
        rnd_ints_tmp = (rnd_ints & 0x007FFFFF) | 0x3F800000
        rnd_bytes_filtered = rnd_ints_tmp.tobytes()
        rnd_lists_filtered = struct.unpack('<{}f'.format(n_floats), 
                                           rnd_bytes_filtered)
        rnd_floats = np.array(rnd_lists_filtered, dtype=np.float32)
        return rnd_floats - 1


    def get_rng_doubles(self, n_doubles):
        if n_doubles >= (2**32) // 8:
            lg.error('{} RNG Doubles: Maximum n_doubles is {}'
                     .format(self.dev_name, (2**32) // 8))
            return None

        # 64 bits floating point number
        bytes_res = self.get_rng_bytes(n_bytes=n_doubles*8, timeout=None)
        if bytes_res is None:
            return 
        rnd_bytes_a, rnd_bytes_b = bytes_res
        
        # XOR them
        int_a = int.from_bytes(rnd_bytes_a, 'little')
        int_b = int.from_bytes(rnd_bytes_b, 'little')
        rnd_bytes = (int_a ^ int_b).to_bytes(len(rnd_bytes_a), 'little')
        # Convert bytes to ints
        rnd_lists = struct.unpack('<{}Q'.format(n_doubles), rnd_bytes)
        rnd_ints = np.array(rnd_lists, dtype=np.uint64)
        
        # IEEE754 bit pattern for single precision floating point value in the 
        # range of 1.0 - 2.0. Uses the first 52 bytes and fixes the float 
        # exponent to 1023
        rnd_ints_tmp = (rnd_ints & 0xFFFFFFFFFFFFF) | 0x3FF0000000000000
        rnd_bytes_filtered = rnd_ints_tmp.tobytes()
        rnd_lists_filtered = struct.unpack('<{}d'.format(n_doubles), 
                                           rnd_bytes_filtered)
        rnd_doubles = np.array(rnd_lists_filtered, dtype=np.float64)
        return rnd_doubles - 1
    

    def snd_rng_byte_stream_start(self, n_bytes, stream_delay_ms, 
                                  postproc_id=D_RNG_POSTPROC['NONE']):
        if not postproc_id in D_RNG_POSTPROC_INV:
            lg.error('{} RNG Stream: Unknown postproc_id {}'
                     .format(self.dev_name, postproc_id))
            return None
        if n_bytes >= 2**16:
            lg.error('{} RNG Stream: Provide n_bytes as a 16-bit integer'
                     .format(self.dev_name))
            return None
        if stream_delay_ms > RNG_BYTE_STREAM_MAX_DELAY_MS:
            lg.error('{} RNG Stream: Provide a stream_delay_ms <= {}ms.'
                     .format(self.dev_name, RNG_BYTE_STREAM_MAX_DELAY_MS))
            return None

        comm = 'RNG_STREAM_START'
        msg_success = self.snd_rava_msg(comm, 
                                 [n_bytes, postproc_id, stream_delay_ms], 'HBH')
        if msg_success: 
            self.rng_streaming = True

        return msg_success


    def snd_rng_byte_stream_stop(self):
        comm = 'RNG_STREAM_STOP'
        msg_success = self.snd_rava_msg(comm)

        if msg_success: 
            self.rng_streaming = False

        # Read remaining stream bytes        
        if 'RNG_STREAM_BYTES' in self.serial_data:
            while not self.serial_data['RNG_STREAM_BYTES'].empty():
                self.serial_data['RNG_STREAM_BYTES'].get_nowait()
        
        return msg_success


    def get_rng_byte_stream_data(self, out_type=D_RNG_BYTE_OUT['NUMPY_ARRAY'], 
                                 timeout=GET_TIMEOUT_S):
        if not self.rng_streaming:
            lg.error('{} RNG Stream: Streaming is disabled'.
                    format(self.dev_name))
            return None, None

        comm = 'RNG_STREAM_BYTES'
        byte_data = self.get_queue_data(comm, timeout=timeout)
        
        # Timeout?
        if byte_data is None:
            return None, None
        
        rng_bytes_a, rng_bytes_b = byte_data
        rng_a = process_bytes(rng_bytes_a, out_type)
        rng_b = process_bytes(rng_bytes_b, out_type)
        return rng_a, rng_b
    

    def get_rng_byte_stream_status(self, timeout=GET_TIMEOUT_S):
        comm = 'RNG_STREAM_STATUS'
        if self.snd_rava_msg(comm):
            return self.get_queue_data(comm, timeout=timeout)


    #####################
    ## HEALTH

    def snd_health_startup_run(self):
        comm = 'HEALTH_STARTUP_RUN'
        return self.snd_rava_msg(comm)


    def get_health_startup_results(self, timeout=GET_TIMEOUT_S):
        comm = 'HEALTH_STARTUP_RESULTS'
        if self.snd_rava_msg(comm):
            success, pc_avg_vars, bias_bit_vars, bias_byte_vars = \
                self.get_queue_data(comm, timeout=timeout)
            data_vars = [pc_avg_vars, bias_bit_vars, bias_byte_vars]
            data_names = ['pulse_count', 'bit_bias', 'byte_bias']
            return bool(success), dict(zip(data_names, data_vars))


    def get_health_continuous_errors(self, timeout=GET_TIMEOUT_S):
        comm = 'HEALTH_CONTINUOUS_ERRORS'
        if self.snd_rava_msg(comm):
            data_vars = self.get_queue_data(comm, timeout=timeout)
            n_errors = sum(data_vars)
            data_names = ['repetitive_count_a', 'repetitive_count_b', 
                          'adaptative_proportion_a', 'adaptative_proportion_b']
            return n_errors, dict(zip(data_names, data_vars))


    #####################
    ## PERIPHERALS

    def snd_periph_digi_mode(self, periph_id, mode_id):
        if periph_id == 0 or periph_id > 5:
            lg.error('{} Periph: Provide a periph_id between 1 and 5'
                     .format(self.dev_name))
            return None
        if not mode_id in D_PERIPH_MODES_INV:
            lg.error('{} Periph: Unknown mode_id {}'
                     .format(self.dev_name, mode_id))
            return None
        
        comm = 'PERIPH_MODE'
        return self.snd_rava_msg(comm, [periph_id, mode_id], 'BB')
  

    def get_periph_digi_state(self, periph_id=1, timeout=GET_TIMEOUT_S):
        if periph_id == 0 or periph_id > 5:
            lg.error('{} Periph: Provide a periph_id between 1 and 5'
                     .format(self.dev_name))
            return None
        
        comm = 'PERIPH_READ'
        if self.snd_rava_msg(comm, [periph_id], 'B'):
            return self.get_queue_data(comm, timeout=timeout)


    def snd_periph_digi_state(self, periph_id, digi_state):
        if periph_id == 0 or periph_id > 5:
            lg.error('{} Periph: Provide a periph_id between 1 and 5'
                     .format(self.dev_name))
            return None
        
        comm = 'PERIPH_WRITE'
        rava_send = False
        return self.snd_rava_msg(comm, [periph_id, digi_state], 'BB')
  

    def snd_periph_digi_pulse(self, periph_id=1, pulse_duration_us=100):
        if periph_id == 0 or periph_id > 5:
            lg.error('{} Periph: Provide a periph_id between 1 and 5'
                     .format(self.dev_name))
            return None
        if pulse_duration_us == 0:
            lg.error('{} Periph: Provide a pulse_duration_us > 0'
                     .format(self.dev_name))
            return None
        
        comm = 'PERIPH_PULSE'
        return self.snd_rava_msg(comm, [periph_id, pulse_duration_us], 'BH')
   

    def snd_periph_d1_trigger_input(self, on=True):
        comm = 'PERIPH_D1_TRIGGER_INPUT'
        return self.snd_rava_msg(comm, [on], 'B')
 

    def snd_periph_d1_comparator(self, neg_to_adc12=False, on=True):
        comm = 'PERIPH_D1_COMPARATOR'
        return self.snd_rava_msg(comm, [on, neg_to_adc12], 'BB')
    

    def snd_periph_d1_delay_us_test(self, delay_us):
        if delay_us == 0:
            lg.error('{} Periph: Provide a delay_us > 0'
                     .format(self.dev_name))
            return None
        
        comm = 'PERIPH_D1_DELAY_US_TEST'
        return self.snd_rava_msg(comm, [delay_us], 'B')


    def snd_periph_d2_input_capture(self, on=True):
        comm = 'PERIPH_D2_TIMER3_INPUT_CAPTURE'
        send_res = self.snd_rava_msg(comm, [on], 'B')
        
        # Read remaining stream bytes
        if not on:
            time.sleep(.1)
            while not self.serial_data[comm].empty():
                self.self.serial_data[comm].get_nowait()
        return send_res


    def get_periph_d2_input_capture(self, timeout=GET_TIMEOUT_S):
        comm = 'PERIPH_D2_TIMER3_INPUT_CAPTURE'
        return self.get_queue_data(comm, timeout=timeout)
    

    def snd_periph_d3_timer3_trigger_output(self, delay_ms=1, on=True):
        if delay_ms == 0:
            lg.error('{} Periph: Provide a delay_ms > 0'
                     .format(self.dev_name))
            return None
        
        comm = 'PERIPH_D3_TIMER3_TRIGGER_OUTPUT'
        return self.snd_rava_msg(comm, [on, delay_ms], 'BH')

    
    def snd_periph_d3_timer3_pwm(self, freq_prescaler=1, top=2**8-1, duty=10, 
                                 on=True):
        if freq_prescaler == 0 or freq_prescaler > 5:
            lg.error('{} Periph D3: Provide a freq_prescaler between 1 and 5'
                     .format(self.dev_name))
            return None
        if top == 0:
            lg.error('{} Periph D3: Provide a top > 0'
                     .format(self.dev_name))
            return None
        if duty == 0:
            lg.error('{} Periph D3: Provide a duty > 0'
                     .format(self.dev_name))
            return None

        comm = 'PERIPH_D3_TIMER3_PWM'
        return self.snd_rava_msg(comm, [on, freq_prescaler, top, duty], 'BBHH')


    def snd_periph_d4_pin_change(self, on=True):
        comm = 'PERIPH_D4_PIN_CHANGE'
        return self.snd_rava_msg(comm, [on], 'B')


    def get_periph_d5_adc_read(self, ref_5v=1, clk_prescaler=0, 
                               oversampling_n_bits=0, on=True, 
                               timeout=GET_TIMEOUT_S):
        if clk_prescaler == 0 or clk_prescaler > 7:
            lg.error('{} Periph D5: Provide a clk_prescaler between 1 and 7'
                     .format(self.dev_name))
            return None
        if oversampling_n_bits > 6:
            lg.error('{} Periph D5: Provide a oversampling_n_bits <= 6'
                     .format(self.dev_name))
            return None
        
        comm = 'PERIPH_D5_ADC'
        if self.snd_rava_msg(comm, 
                             [on, ref_5v, clk_prescaler, oversampling_n_bits], 
                             'BBBB'):
            if on:
                return self.get_queue_data(comm, timeout=timeout)


    #####################
    ## INTERFACES

    def get_interface_ds18bs0(self, timeout=GET_TIMEOUT_S):
        comm = 'INTERFACE_DS18B20'
        if self.snd_rava_msg(comm):
            return self.get_queue_data(comm, timeout=timeout)