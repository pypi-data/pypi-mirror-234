"""
Copyright (c) 2023 Gabriel Guerrer

Distributed under the MIT license - See LICENSE for details
"""

"""
The RAVA_RNG_AIO class offers the same functionality as RAVA_RNG but within an 
asynchronous framework.
"""

import asyncio

from rng_rava.rava_defs import *
from rng_rava.rava_rng import *


class RAVA_RNG_AIO(RAVA_RNG):

    def __init__(self):
        super().__init__(dev_name='RAVA_RNG_AIO')
        self.queue_type = asyncio.Queue

        # Variables
        self.serial_listen_task = None
    

    async def connect(self, serial_number):
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
        self.serial_listen_task = asyncio.create_task(self.loop_serial_listen())

        # Stop any active RNG byte stream
        self.snd_rng_byte_stream_stop()

        # Request firmware info
        firmw_info = await self.get_eeprom_firmware()
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
            test_success, test_vars = await self.get_health_startup_results()

            # Print test info
            print_health_startup_results(test_success, test_vars)

            # Error? Users have then a limited command variety (see Firmware)
            if not test_success: 
                lg.warning('{} Connect: Startup tests failed'
                           .format(self.dev_name))

        return True
        

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
            self.serial_data[comm_ext].put_nowait(value)
            return True
        
        except asyncio.QueueFull:
            lg.error('{} Data: {} Queue full'.format(self.dev_name, comm_ext))
            return False
        

    async def get_queue_data(self, comm, comm_ext_id=0):
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
        
        # Read asyncio queue
        return await self.serial_data[comm_ext].get()


    async def loop_serial_listen(self):
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
                    await asyncio.sleep(SERIAL_LISTEN_LOOP_DELAY_S)

        except Exception as err:
            lg.error('{} Serial Listen Loop: Error'
                     '\n{}{} - {}'
                     .format(self.dev_name, 
                             LOG_FILL, type(err).__name__, err))
            # Close device
            self.close()
        

    #####################
    ## DEVICE

    async def get_device_serial_number(self):
        comm = 'DEVICE_SERIAL_NUMBER'
        if self.snd_rava_msg(comm):
            return await self.get_queue_data(comm)
        

    async def get_device_temperature(self):
        comm = 'DEVICE_TEMPERATURE'
        if self.snd_rava_msg(comm):
            return await self.get_queue_data(comm)
    

    async def get_device_free_ram(self):
        comm = 'DEVICE_FREE_RAM'
        if self.snd_rava_msg(comm):
            return await self.get_queue_data(comm)
        

    #####################
    ## EEPROM

    async def get_eeprom_device(self):
        comm = 'EEPROM_DEVICE'
        rava_send = True
        if self.snd_rava_msg(comm, [rava_send], 'B'):
            data_vars = await self.get_queue_data(comm)
            data_names = ['temp_calib_slope', 'temp_calib_intercept']
            return dict(zip(data_names, data_vars))


    async def get_eeprom_firmware(self):
        comm = 'EEPROM_FIRMWARE'
        if self.snd_rava_msg(comm):
            version_hi, version_lo, modules = await self.get_queue_data(comm)
            
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
        
        
    async def get_eeprom_pwm(self):        
        comm = 'EEPROM_PWM'
        rava_send = True
        if self.snd_rava_msg(comm, [rava_send], 'B'):
            freq_id, duty = await self.get_queue_data(comm)
            return {'freq_id':freq_id,
                    'freq_str':D_PWM_FREQ_INV[freq_id],
                    'duty':duty}
        

    async def get_eeprom_rng(self):
        comm = 'EEPROM_RNG'
        rava_send = True
        if self.snd_rava_msg(comm, [rava_send], 'B'):
            sampling_interval_us = await self.get_queue_data(comm)
            return {'sampling_interval_us':sampling_interval_us}
        

    async def get_eeprom_led(self):
        comm = 'EEPROM_LED'
        rava_send = True
        if self.snd_rava_msg(comm, [rava_send], 'B'):
            led_attached = await self.get_queue_data(comm)
            return {'led_attached':led_attached}


    async def get_eeprom_lamp(self):
        comm = 'EEPROM_LAMP'
        rava_send = True
        if self.snd_rava_msg(comm, [rava_send], 'B'):
            data_vars = await self.get_queue_data(comm)
            data_names = ['exp_dur_max_ms', 'exp_z_significant', 
                          'exp_mag_smooth_n_trials']
            return dict(zip(data_names, data_vars))
        

    #####################
    ## PWM

    async def get_pwm_setup(self):
        rava_send = True
        comm = 'PWM_SETUP'
        if self.snd_rava_msg(comm, [rava_send], 'B'):
            freq_id, duty = await self.get_queue_data(comm)
            return {'freq_id':freq_id,
                    'freq_str':D_PWM_FREQ_INV[freq_id],
                    'duty':duty}

        
    #####################
    ## RNG

    async def get_rng_setup(self):
        comm = 'RNG_SETUP'
        rava_send = True
        if self.snd_rava_msg(comm, [rava_send], 'B'):
            sampling_interval_us = await self.get_queue_data(comm)
            return {'sampling_interval_us':sampling_interval_us}
        

    async def get_rng_pulse_counts(self, n_counts):
        comm = 'RNG_PULSE_COUNTS'
        if self.snd_rava_msg(comm, [n_counts], 'L'):
            counts_bytes_a, counts_bytes_b = await self.get_queue_data(comm)

            counts_a = process_bytes(counts_bytes_a, 
                                     out_type=D_RNG_BYTE_OUT['NUMPY_ARRAY'])
            counts_b = process_bytes(counts_bytes_b, 
                                     out_type=D_RNG_BYTE_OUT['NUMPY_ARRAY'])
            return counts_a, counts_b


    async def get_rng_bits(self, bit_type_id):
        if not bit_type_id in D_RNG_BIT_SRC_INV:
            lg.error('{} RNG Bits: Unknown bit_type_id {}'
                     .format(self.dev_name, bit_type_id))
            return None

        comm = 'RNG_BITS'
        if self.snd_rava_msg(comm, [bit_type_id], 'B'):
            bit_type_id_recv, *bits = await self.get_queue_data(comm)

            if bit_type_id == D_RNG_BIT_SRC['AB_RND']:
                bit_type_str = D_RNG_BIT_SRC_INV[bit_type_id_recv]
                return bit_type_str, bits[0]
            elif bit_type_id == D_RNG_BIT_SRC['AB']:
                return tuple(bits)
            else:
                return bits[0]
            

    async def get_rng_bytes(self, n_bytes, postproc_id=D_RNG_POSTPROC['NONE'], 
                      out_type=D_RNG_BYTE_OUT['NUMPY_ARRAY']):
        if not postproc_id in D_RNG_POSTPROC_INV:
            lg.error('{} RNG Bytes: Unknown postproc_id {}'
                     .format(self.dev_name, postproc_id))
            return None
        
        comm = 'RNG_BYTES'
        if self.snd_rava_msg(comm, [n_bytes, postproc_id], 'LB'):
            bytes_data = await self.get_queue_data(comm)

            if not (bytes_data is None):
                rng_bytes_a, rng_bytes_b = bytes_data
                rng_a = process_bytes(rng_bytes_a, out_type)
                rng_b = process_bytes(rng_bytes_b, out_type)
                return rng_a, rng_b
            else:
                return None, None


    async def get_rng_int8s(self, n_ints, int_max):
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
            ints_bytes = await self.get_queue_data(comm)
            ints_list = struct.unpack('<{}B'.format(n_ints), ints_bytes)
            return np.array(ints_list, dtype=np.uint8)


    async def get_rng_int16s(self, n_ints, int_max):
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
            ints_bytes = await self.get_queue_data(comm)
            ints_list = struct.unpack('<{}H'.format(n_ints), ints_bytes)
            return np.array(ints_list, dtype=np.uint16)


    async def get_rng_floats(self, n_floats):
        if n_floats >= (2**32) // 4:
            lg.error('{} RNG Floats: Maximum n_floats is {}'
                     .format(self.dev_name, (2**32) // 4))
            return None
        
        # 32 bits floating point number
        bytes_res = await self.get_rng_bytes(n_bytes=n_floats*4)
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


    async def get_rng_doubles(self, n_doubles):
        if n_doubles >= (2**32) // 8:
            lg.error('{} RNG Doubles: Maximum n_doubles is {}'
                     .format(self.dev_name, (2**32) // 8))
            return None
        
        # 64 bits floating point number
        bytes_res = await self.get_rng_bytes(n_bytes=n_doubles*8)
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
    

    async def get_rng_byte_stream_data(self, 
                                       out_type=D_RNG_BYTE_OUT['NUMPY_ARRAY']):
        if not self.rng_streaming:
            lg.error('{} RNG Stream: Streaming is disabled'.
                    format(self.dev_name))
            return None, None

        comm = 'RNG_STREAM_BYTES'
        byte_data = await self.get_queue_data(comm)
        
        # Timeout?
        if byte_data is None:
            return None, None
        
        rng_bytes_a, rng_bytes_b = byte_data
        rng_a = process_bytes(rng_bytes_a, out_type)
        rng_b = process_bytes(rng_bytes_b, out_type)
        return rng_a, rng_b
    

    async def get_rng_byte_stream_status(self):
        comm = 'RNG_STREAM_STATUS'
        if self.snd_rava_msg(comm):
            return await self.get_queue_data(comm)


    #####################
    ## HEALTH

    async def get_health_startup_results(self):
        comm = 'HEALTH_STARTUP_RESULTS'
        if self.snd_rava_msg(comm):
            success, pc_avg_vars, bias_bit_vars, bias_byte_vars = \
                await self.get_queue_data(comm)
            data_vars = [pc_avg_vars, bias_bit_vars, bias_byte_vars]
            data_names = ['pulse_count', 'bit_bias', 'byte_bias']
            return bool(success), dict(zip(data_names, data_vars))
        

    async def get_health_continuous_errors(self):
        comm = 'HEALTH_CONTINUOUS_ERRORS'
        if self.snd_rava_msg(comm):
            data_vars = await self.get_queue_data(comm)
            n_errors = sum(data_vars)
            data_names = ['repetitive_count_a', 'repetitive_count_b', 
                          'adaptative_proportion_a', 'adaptative_proportion_b']
            return n_errors, dict(zip(data_names, data_vars))
    

    #####################
    ## PERIPHERALS

    async def get_periph_digi_state(self, periph_id=1):
        if periph_id == 0 or periph_id > 5:
            lg.error('{} Periph: Provide a periph_id between 1 and 5'
                     .format(self.dev_name))
            return None
        
        comm = 'PERIPH_READ'
        if self.snd_rava_msg(comm, [periph_id], 'B'):
            return await self.get_queue_data(comm)
        
        
    async def get_periph_d2_input_capture(self):
        comm = 'PERIPH_D2_TIMER3_INPUT_CAPTURE'
        return await self.get_queue_data(comm)
    

    async def get_periph_d5_adc_read(self, ref_5v=1, clk_prescaler=0, 
                               oversampling_n_bits=0, on=True):
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
                return await self.get_queue_data(comm)
            

    #####################
    ## INTERFACES

    async def get_interface_ds18bs0(self):
        comm = 'INTERFACE_DS18B20'
        if self.snd_rava_msg(comm):
            return await self.get_queue_data(comm)