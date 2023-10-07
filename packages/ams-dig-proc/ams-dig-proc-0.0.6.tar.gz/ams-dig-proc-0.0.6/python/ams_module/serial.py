"""
Implementation of serial communication and methods to send/read data to/from the AMS module.
"""

import serial
from ams_messages.messages import *
import logging
import time
import threading, queue

logger = logging.getLogger("AMSModule")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


class ReaderThread(threading.Thread):
    total_correct_messages_count = 0
    total_incorrect_messages_count = 0

    def __init__(
        self,
        *args,
        output_messages_queue,
        port,
        read_timeout=0.1,
        baudrate,
        reference_voltage,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.output_messages_queue = output_messages_queue
        self.read_timeout = read_timeout
        self.port = port
        self.baudrate = baudrate
        self._stop_event = threading.Event()
        self._read_lock = threading.Lock()
        self._write_lock = threading.Lock()
        self.reference_voltage = reference_voltage
        self._open_port()

    def flush_input(self):
        self._read_lock.acquire()
        self.ser.flushInput()
        self.ser.read(self.ser.inWaiting())  # Just in case flush would not work
        self.stream = b""
        self._read_lock.release()

    def flush_output(self):
        self._write_lock.acquire()
        self.ser.flushOutput()
        self._write_lock.release()

    def stop(self):
        self._stop_event.set()

    def write(self, content):
        # self._lock.acquire()
        # print("Writing")
        self._write_lock.acquire()
        self.ser.write(content)
        self.ser.write(EOF)
        # self._lock.release()
        # self.flush_output()
        self._write_lock.release()
        time.sleep(0.1)

    def _open_port(self):
        self._write_lock.acquire()
        self._read_lock.acquire()
        self.ser = serial.Serial(timeout=self.read_timeout)
        self.ser.port = self.port
        self.ser.baudrate = self.baudrate
        self.ser.bitrate = self.baudrate
        self.ser.timeout = self.read_timeout
        self.ser.setDTR(0)
        self.ser.rtscts = 0
        self.ser.rts = 0
        self.ser.set_buffer_size(rx_size=1_000_000, tx_size=100_000)
        try:
            self.ser.open()
        except Exception as e:
            logger.error("Problem with opening port")
            raise e
        self.ser.flushInput()
        self.ser.read(self.ser.inWaiting())  # Just in case flush would not work
        self.stream = b""
        if self.ser.isOpen():
            logger.debug("AMS module opened at " + str(self.port))
        else:
            logger.error("AMS module NOT opened at " + str(self.port))
            self.output_messages_queue.put(None)

        self._read_lock.release()
        self._write_lock.release()

    def run(self):
        while not self._stop_event.is_set():
            self._read_lock.acquire()
            msgs = self._read_list_of_messages()
            self._read_lock.release()
            for msg in msgs:
                # print("Adding msg to queue")
                try:
                    self.output_messages_queue.put(msg, block=False)
                except queue.Full:
                    pass

    def _read_list_of_messages(self):
        count = self.ser.inWaiting()
        if count <= 0:
            count = 1
        new_bytes = self.ser.read(min(1_000, count))
        if not new_bytes:
            # print("no new bytes")
            logger.debug("Nothing received")
            return []
        # print("Got new bytes")
        self.stream += new_bytes
        frames = self.stream.split(EOF)
        ret = []
        if frames[-1]:
            self.stream = frames[-1]
        else:
            self.stream = b""

        frames = frames[:-1]
        for frame in frames:
            decoded = decode_cobs(frame)
            if not decoded:
                logger.warning(f"COBS decoding error. Frame length = {len(frame)}")
                continue
            message, error_msg = convert_to_generic_message(decoded)
            if message:
                if MessageIds.has_value(message.header.messageId):
                    ret.append(
                        decode_to_specific_message(
                            message.header,
                            decoded,
                            reference_voltage=self.reference_voltage,
                        )
                    )
                    self.total_correct_messages_count += 1
                    logger.debug(
                        f"Got message id {message.header.messageId}, len {len(message.payload)}"
                    )
                else:
                    logloggering.error("Unknown msgId " + str(message.header.messageId))
                    self.total_incorrect_messages_count += 1
            else:
                self.total_incorrect_messages_count += 1
                logger.error(
                    f"Incorrect frame received: {error_msg}. Frame len: {len(frame)}"
                )
        return ret


class AMSSerialModule:
    """
    Represents serial AMS-DIG-PROC board.
    """

    processing_slots = 4
    """Number of available processing slots"""
    reference_voltage = 3.3
    """ Reference voltage for built-in ADC"""

    def __init__(
        self,
        *args,
        port="COM1",
        baudrate: int = 1000_000,
        read_timeout=0.1,
        rx_max_queue_len=0,
        **kwargs
    ):
        """

        Args:
            :port (str, optional): String representing serial device. Defaults to "COM1".
            :baudrate (int, optional): Baudrate. Defaults to 1000_000.
            :read_timeout (float, optional): Timeout for reading in seconds. Defaults to 0.1.
            :rx_max_queue_len (int, optional): Maximal length of rx queue. Zero means that rx queue is unlimited. Defaults to 0.
        """
        super().__init__(*args, **kwargs)
        self.read_timeout = read_timeout
        self.msg_queue = queue.Queue(maxsize=rx_max_queue_len)
        self.reader_thread = ReaderThread(
            output_messages_queue=self.msg_queue,
            port=port,
            baudrate=baudrate,
            read_timeout=read_timeout,
            daemon=True,
            reference_voltage=self.reference_voltage,
        )
        self.reader_thread.start()

    def flush_input(self):
        """Drops all not yet read messages from rx queue and clears input buffers."""
        self.reader_thread.flush_input()
        with self.msg_queue.mutex:
            self.msg_queue.queue.clear()

    def flush_output(self):
        """Sends all not yet sent messages and buffers to the serial device."""
        self.reader_thread.flush_output()

    def read_one_message(self, msgClasses=None, block=True, timeout=0.1, latest=False):
        """Reads one message from rx queue. If msgClasses are provided, all non matching messages will be dropped.

        Args:
            :msgClasses (list or single class from ams_messages): If set it will filter only specified messages.
            :block (bool, optional): Set to False to return immadietly when there is no message in rx queue.
                Defaults to True
            :timeout (float, optional): Timeout in seconds. Defaults to 0.1.
            :latest (bool, optional): By default oldest message from rx queue will be returned.
                Set this argument to True to obtain only latest message and clear queue. Defaults to False.

        Returns:
            :AbstractMessage subclass: Subclass of AbstractMessage with received message or None.

                List of subclasses:
                    - MessageOutputData
                    - MessageStatus
                    - MessageConfig*
                    - MessageProcessing*
                    - MessageWorkmode*

        """
        ret = None
        try:
            some_object_iterator = iter(msgClasses)
        except TypeError as te:
            if msgClasses is not None:
                msgClasses = [
                    msgClasses,
                ]
        if latest:
            try:
                while True:
                    ret = self.msg_queue.queue[-1]
                    if not msgClasses:
                        break
                    gotIt = False
                    for msgClass in msgClasses:
                        if issubclass(msg.__class__, msgClass):
                            gotIt = True
                            break
                    if gotIt:
                        break
                self.msg_queue.queue.clear()
            except IndexError:
                ret = None
            return ret

        try:
            while True:
                ret = self.msg_queue.get(block=block, timeout=timeout)
                if msgClasses is None:
                    break
                gotIt = False
                for msgClass in msgClasses:
                    if issubclass(ret.__class__, msgClass):
                        gotIt = True
                        break
                if gotIt:
                    break
        except queue.Empty:
            return None
        if ret is None:
            raise Exception("Port not opened!")
        return ret

    def _write_msg(self, msg):
        self.reader_thread.write(msg.encoded())

    def __del__(self):
        if hasattr(self, "reader_thread"):
            self.reader_thread.stop()

    def workmode_stop(self):
        """Enters STOP workmode. Stops data acquisition."""
        msg = MessageWorkmodeStop()
        self._write_msg(msg)

    def workmode_freerunning(self, samples_count=0):
        """Starts FREERUNNING workmode.

        Args:
            :samples_count (int, optional): Total number of samples to acquire. Has to be a muptiple of 2048. The module will enter STOP mode after collecting all samples. If zero, the module will stay in FREERUNNING mode. Defaults to 0.
        """
        logger.debug(f"Setting mode: freerunning with samples_count={samples_count}")
        freerunning_msg = MessageWorkmodeFreerunning()
        freerunning_msg.samples_count = samples_count
        self._write_msg(freerunning_msg)

    def workmode_trigger_input(self, samples_count, delay):
        """Starts TRIGGER_INPUT workmode.
        The module will start sampling after trigger event with defined delay. After collecting defined number of samples and sending them to the host, it will wait for next trigger event.

        Args:
            :samples_count (int): Total number of samples to acquire after single trigger event. Has to be a multiple of 2048.
            :delay (float): Delay between trigger event and start of sampling [in seconds].
        """
        logger.debug(
            f"Setting mode: trigger input with samples_count={samples_count} and delay={delay}"
        )
        msg = MessageWorkmodeTriggerInput()
        msg.samples_count = samples_count
        msg.delay = int(delay * 1000000)
        msg.edge = 1
        self._write_msg(msg)

    def workmode_trigger_output(self, samples_count, period, delay):
        """Starts TRIGGER_OUTPUT workmode.
        The module will start sampling and generate trigger event after defined delay. After collecting defined number of samples and sending them to the host, it will generate next trigger with defined period.

        Args:
            :samples_count (int): Number of samples to acquire after single trigger output event. Has to be a multiple of 2048.
            :period (float): Period of trigger events in seconds. Keep in mind that real period can be longer due to limitations of UART interface.
            :delay (float): Delay between starting of data acquisition and trigger event [in seconds]
        """
        logger.debug(
            f"Setting mode: trigger output with samples_count={samples_count}, delay={delay}, period={period}"
        )
        msg = MessageWorkmodeTriggerOutput()
        msg.samples_count = samples_count
        msg.delay = int(delay * 1000000)
        msg.period = int(period * 1000000)
        msg.edge = 1
        self._write_msg(msg)

    def processing_disable(self):
        """Disables all processing slots"""
        msg = MessageProcessingNone()
        for slotId in range(self.processing_slots):
            logger.debug(f"Disabling processing slot {slotId}")
            msg.slotId = slotId
            self._write_msg(msg)

    def processing_read(self, slotID: int):
        """Reads processing parameters for given slotID

        Args:
            :slotID (int): Number of slot, starting from 0.
        """
        assert slotID >= 0
        assert slotID < self.processing_slots
        msg = MessageProcessingRead()
        msg.slotID = slotID
        self._write_msg(msg)

    def processing_sample_iir(self, slotId: int, weight: float):
        """Configures slot for sample-wise infinite impulse response algorithm.
        Each sample will be calculated based on the following formula:

        .. math::
            X = X_{previous} * weight + X_{new} * (1 - weight)

        Args:
            :slotID (int): Number of slot, starting from 0.
            :weight (float): weight for IIR filter.
        """
        assert slotId >= 0
        assert slotId < self.processing_slots
        logger.debug(f"Configuring sample IIR processing with weight={weight}")
        msg = MessageProcessingSampleIIR()
        msg.weight = weight
        msg.slotId = slotId
        self._write_msg(msg)

    def processing_simple_average(self, slotId: int):
        """Configures slot for simple average. Whole input buffer will be averaged and stored as single sample in the output buffer.

        Args:
            :slotID (int): Number of slot, starting from 0.
        """
        assert slotId >= 0
        assert slotId < self.processing_slots
        logger.debug(f"Configuring simple average processing")
        msg = MessageProcessingSimpleAverage()
        msg.slotId = slotId
        self._write_msg(msg)

    def processing_buffer_iir(self, slotId: int, weight: float):
        """Configures slot for buffer-wise infinite impulse response filter. Every n'th sample from input buffer will be averaged with every n'th sample from previous output buffer.

        Args:
            :slotID (int): Number of slot, starting from 0.
            :weight (float): Weight for the IIR filter.
        """
        assert slotId >= 0
        assert slotId < self.processing_slots
        logger.debug(f"Configuring buffer IIR processing with weight={weight}")
        msg = MessageProcessingBufferIIR()
        msg.weight = weight
        msg.slotId = slotId
        self._write_msg(msg)

    def workmode_simulation(
        self, samples: list, sample_size: SampleSize, noise_rms: float, period: int
    ):
        """Enters SIMULATION workmode. In this mode preconfigured set of samples will be sent periodically. Additional noise can be added to the samples.

        Args:
            :samples (list): List of samples that will be sent by the module.
            :sample_size (SampleSize): Size of the samples.
            :noise_rms (float): RMS of noise that will be added to the output samples.
            :period (int): Period in seconds
        """

        logger.debug(
            f"Setting mode: simulation with sample_size={sample_size} and noise_rms={noise_rms}"
        )
        if sample_size == SampleSize.SAMPLE_SIZE_8b:
            sample_type = ctypes.c_uint8
        elif sample_size == SampleSize.SAMPLE_SIZE_16b:
            sample_type = ctypes.c_uint16
        elif sample_size == SampleSize.SAMPLE_SIZE_32b:
            sample_type = ctypes.c_uint32
        else:
            raise ValueError(f"Unknown sample_size={sample_size}")
        c_samples = (sample_type * len(samples))(*samples)
        msg = message_simulation_class(len(samples), sample_size)()
        msg.samples = c_samples
        msg.noise_rms = noise_rms
        msg.period_in_ms = period * 1000
        self._write_msg(msg)

    def set_samplerate(self, physicalSampleRate: int):
        """Configures physical sample rate.
        Use it only if you know what you are doing, since lowering sample rate decreases signal to noise ratio

        Args:
            :physicalSampleRate (int): Physical sample rate. Has to be greater or equal 300_000 and lower or equal 7_000_000
        """
        assert physicalSampleRate >= 300_000
        assert physicalSampleRate <= 7_000_000
        logger.debug("Setting sample rate to " + str(physicalSampleRate))
        sampling_msg = MessageConfigSampling()
        sampling_msg.physicalSampleRate = physicalSampleRate
        sampling_msg.physicalResolution = 1
        sampling_msg.processingDataResolution = 1
        self._write_msg(sampling_msg)

    def reset(self):
        """Resets the board. Reset flag will be set to one."""
        logger.debug("Resetting device")
        msg = MessageReboot()
        self._write_msg(msg)

    def clear_reset_flag(self):
        """Clears reset flag."""
        logger.debug("Clearing reset flag")
        msg = MessageClearResetFlag()
        self._write_msg(msg)

    def processing_oversampling(self, slot_id: int, ratio: int, output_samples: int):
        """Configures slot for oversampling, including averaging. Usefull if full sample rate is not desired, i.e. when working with mechanical choppers
        or pulsing heaters.

        CAUTION: ratio * output_samples has to be multiple of input buffer length

        Args:
            :slot_id (int): Number of slot, starting from 0.
            :ratio (int): Ratio of oversampling. Has to be power of 2. For example value 4 means that there will be 4 times less samples in the output buffer.
            :output_samples (int): Number of samples in the output buffer. Has to be lower or equal 2048
        """
        assert slot_id >= 0
        assert slot_id < self.processing_slots
        assert output_samples >= 1
        assert ratio > 1
        logger.debug("Setting oversampling to ratio = " + str(ratio))
        msg = MessageProcessingOversampling()
        msg.ratio = ratio
        msg.output_samples = output_samples
        msg.slotId = slot_id
        self._write_msg(msg)

    def processing_buffer_decimation(self, slot_id: int, ratio: int):
        """Configures slot for buffer decimation.

        Args:
            :slot_id (int): Number of slot, starting from 0
            :ratio (int): Defines how many buffers will be skipped. For example value 4 means that every 4th buffer will be passed to the output.
        """
        assert slot_id >= 0
        assert slot_id < self.processing_slots
        assert ratio > 1
        logger.debug("Setting oversampling to ratio = " + str(ratio))
        msg = MessageProcessingBufferDecimation()
        msg.ratio = ratio
        msg.slotId = slot_id
        self._write_msg(msg)

    def processing_peak_peak(self, slot_id: int):
        """Configures slot for peak-peak measurement

        Args:
            :slot_id (int): Number of slot, starting from 0
        """
        assert slot_id >= 0
        assert slot_id < self.processing_slots
        logger.debug("Configuring peak-peak processing")
        msg = MessageProcessingPeakPeak()
        msg.slotId = slot_id
        self._write_msg(msg)

    def read_config(self, msgId: MessageIds):
        """Reads config for specified msgId.
        Can be used with MessageIds.MESSAGE_CONFIGURE_* values

        Args:
            :msgId (MessageIds): One of MessageIds.MESSAGE_CONFIGURE*
        """
        logger.debug(f"Reading config {msgId}")
        msg = MessageConfigRead()
        msg.configID = msgId.value
        self._write_msg(msg)

    def read_workmode(self):
        """Reads currently configures workmode and it's settings.
        The board will answer with one of the MessageIds.MESSAGE_MODE_* message.
        """
        logger.debug(f"Reading workmode")
        msg = MessageWorkModeRead()
        self._write_msg(msg)

    def set_detector_temperature(self, temperature: int):
        """Sets expected temperature of the IR detector.

        Args:
            :temperature (int): Expected temperature of the IR detector, in Kelvins. Set to zero to disable temperature controller.
        """
        assert temperature >= 0
        logger.debug(f"Settings temperature {temperature}")
        msg = MessageConfigDetectorTemperature()
        msg.temperature = temperature
        self._write_msg(msg)

    def save_config(self):
        """Saves configuration to non-volatile memory. This includes only MessageIds.MESSAGE_CONFIGURE* settings."""
        logger.debug("Saving configuration to non-volatile memory")
        msg = MessageConfigSave()
        self._write_msg(msg)
