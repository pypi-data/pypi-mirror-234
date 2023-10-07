from cobs import cobs
from crccheck.crc import *
from crccheck.checksum import *
import ctypes
from enum import Enum
import serial
import numpy as np

EOF = b"\0"
USER_SPACE_SIZE = 256


class MessageIds(Enum):
    MESSAGE_MODE_STOP = 3
    MESSAGE_MODE_FREE_RUNNING = 5
    MESSAGE_MODE_TRIGGER_INPUT = 6
    MESSAGE_MODE_TRIGGER_OUTPUT = 7
    MESSAGE_MODE_SIMULATION = 8
    MESSAGE_PROCESSING_NONE = 9
    MESSAGE_PROCESSING_SIMPLE_AVERAGE = 10
    MESSAGE_PROCESSING_SAMPLE_IIR = 11
    MESSAGE_PROCESSING_BUFFER_IIR = 12
    MESSAGE_PROCESSING_OVERSAMPLING = 13
    MESSAGE_PROCESSING_PEAK_PEAK = 14
    MESSAGE_PROCESSING_BUFFER_DECIMATION = 15
    MESSAGE_CONFIGURE_INTERFACES = 50
    MESSAGE_CONFIGURE_SAMPLING = 51
    MESSAGE_CONFIGURE_DETECTOR_TEMPERATURE = 52
    MESSAGE_CONFIGURE_USER_SPACE = 53
    MESSAGE_CONFIG_SAVE = 55
    MESSAGE_CONFIG_READ = 56
    MESSAGE_OUTPUT_DATA = 90
    MESSAGE_MODE_READ = 100
    MESSAGE_PROCESSING_READ = 105
    MESSAGE_STATUS = 120
    MESSAGE_REBOOT = 124
    MESSAGE_CLEAR_RESET_FLAG = 125

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class SampleSize(Enum):
    SAMPLE_SIZE_8b = 1
    SAMPLE_SIZE_16b = 2
    SAMPLE_SIZE_32b = 4

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class ComparableStruct(ctypes.Structure):
    def __eq__(self, other):
        for fld in self._fields_:
            if getattr(self, fld[0]) != getattr(other, fld[0]):
                return False
        return True

    def __ne__(self, other):
        for fld in self._fields_:
            if getattr(self, fld[0]) != getattr(other, fld[0]):
                print("difference in ", fld[0])
                return True
        return False


class Header(ComparableStruct, ctypes.Structure):
    _pack_ = 1
    CRC_FIELD_TYPE = ctypes.c_uint32
    _fields_ = [
        ("crc", CRC_FIELD_TYPE),
        ("messageId", ctypes.c_ubyte),
    ]


class AutoCastMessage:
    pass


class AbstractMessage(ComparableStruct):
    _pack_ = 1

    def calculate_crc(self):
        crcinst = Crc32Cksum()
        crcinst.process(bytearray(self)[ctypes.sizeof(self.header.CRC_FIELD_TYPE) :])
        crcint = crcinst.final()
        return crcint

    def fill_crc(self):
        self.header.crc = self.calculate_crc()

    def check_crc(self):
        return self.header.crc == self.calculate_crc()

    def encoded(self):
        self.fill_crc()
        return cobs.encode(bytearray(self))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header.messageId = self._messageId.value
        self.fill_crc()

    def __repr__(self):
        return f"{self.__class__.__name__}"


def decode_to_specific_message(header, bytes, reference_voltage):
    if header.messageId == MessageIds.MESSAGE_OUTPUT_DATA.value:
        msg = MessageOutputData.from_buffer_and_fill_data(
            bytes, reference_voltage=reference_voltage
        )
        return msg
    elif header.messageId == MessageIds.MESSAGE_MODE_SIMULATION.value:
        temp_class = message_simulation_class(1, SampleSize.SAMPLE_SIZE_8b.value)
        msg = temp_class.from_buffer(bytes[: ctypes.sizeof(temp_class)])
        if msg.sample_size == SampleSize.SAMPLE_SIZE_8b.value:
            pass
        elif msg.sample_size == SampleSize.SAMPLE_SIZE_16b.value:
            msg = message_simulation_class(
                msg.samples_count, SampleSize.SAMPLE_SIZE_16b.value
            ).from_buffer(bytes)
        elif msg.sample_size == SampleSize.SAMPLE_SIZE_32b.value:
            msg = message_simulation_class(
                msg.samples_count, SampleSize.SAMPLE_SIZE_32b.value
            ).from_buffer(bytes)
        else:
            raise Exception("Unknow sample size = " + str(msg.sample_size))
        return msg

    target_classes = []
    for cls in AutoCastMessage.__subclasses__():
        if cls._messageId.value == header.messageId:
            target_classes.append(cls)
    if not target_classes:
        raise Exception("Unknown message id " + str(header.messageId))
    return target_classes[0].from_buffer_copy(bytes)


def generic_message_class(*args, total_length):
    if total_length < ctypes.sizeof(Header):
        return None

    class GenericMessage(AbstractMessage, ctypes.Structure):
        _fields_ = [
            ("header", Header),
            ("payload", ctypes.c_ubyte * (total_length - ctypes.sizeof(Header))),
        ]

    return GenericMessage


def decode_cobs(bytes):
    try:
        return cobs.decode(bytes)
    except cobs.DecodeError as e:
        return None


def convert_to_generic_message(decoded):
    ret = generic_message_class(total_length=len(decoded))
    if ret is None:
        return None, "Unknown message"
    ret = ret.from_buffer_copy(decoded)
    if not ret.check_crc():
        return None, "CRC error"
    return ret, None


class MessageProcessingNone(AbstractMessage, AutoCastMessage, ctypes.Structure):
    _messageId = MessageIds.MESSAGE_PROCESSING_NONE
    _fields_ = [
        ("header", Header),
        ("slotId", ctypes.c_ubyte),
    ]


class MessageProcessingSimpleAverage(
    AbstractMessage, AutoCastMessage, ctypes.Structure
):
    _messageId = MessageIds.MESSAGE_PROCESSING_SIMPLE_AVERAGE
    _fields_ = [
        ("header", Header),
        ("slotId", ctypes.c_ubyte),
    ]


class MessageProcessingSampleIIR(AbstractMessage, AutoCastMessage, ctypes.Structure):
    _messageId = MessageIds.MESSAGE_PROCESSING_SAMPLE_IIR
    _fields_ = [
        ("header", Header),
        ("slotId", ctypes.c_ubyte),
        ("weight", ctypes.c_float),
    ]


class MessageProcessingBufferIIR(AbstractMessage, AutoCastMessage, ctypes.Structure):
    _messageId = MessageIds.MESSAGE_PROCESSING_BUFFER_IIR
    _fields_ = [
        ("header", Header),
        ("slotId", ctypes.c_ubyte),
        ("weight", ctypes.c_float),
    ]


class MessageProcessingOversampling(AbstractMessage, AutoCastMessage, ctypes.Structure):
    _messageId = MessageIds.MESSAGE_PROCESSING_OVERSAMPLING
    _fields_ = [
        ("header", Header),
        ("slotId", ctypes.c_ubyte),
        ("ratio", ctypes.c_uint32),
        ("output_samples", ctypes.c_uint32),
    ]


class MessageProcessingPeakPeak(AbstractMessage, AutoCastMessage, ctypes.Structure):
    _messageId = MessageIds.MESSAGE_PROCESSING_PEAK_PEAK
    _fields_ = [
        ("header", Header),
        ("slotId", ctypes.c_ubyte),
    ]


class MessageProcessingBufferDecimation(
    AbstractMessage, AutoCastMessage, ctypes.Structure
):
    _messageId = MessageIds.MESSAGE_PROCESSING_BUFFER_DECIMATION
    _fields_ = [
        ("header", Header),
        ("slotId", ctypes.c_ubyte),
        ("ratio", ctypes.c_uint32),
    ]


class MessageProcessingBufferIIR(AbstractMessage, AutoCastMessage, ctypes.Structure):
    _pack_ = 1
    _messageId = MessageIds.MESSAGE_PROCESSING_BUFFER_IIR
    _fields_ = [
        ("header", Header),
        ("slotId", ctypes.c_ubyte),
        ("weight", ctypes.c_float),
    ]


class MessageOutputData(AbstractMessage, ctypes.Structure):
    """Message with samples measured by the ADC."""

    _pack_ = 1
    _messageId = MessageIds.MESSAGE_OUTPUT_DATA
    _fields_ = [
        ("header", Header),
        ("counter", ctypes.c_ubyte),
        ("sample_size", ctypes.c_byte),
        (
            "_data",  # data attribute will be set dynamically since it has variable size
            ctypes.c_ubyte * 0,
        ),
    ]

    data: [list, None] = None
    """Will contain list of raw samples"""

    voltages: [list, None] = None
    """Will contain numpy array of measured voltages"""

    @classmethod
    def from_buffer_and_fill_data(cls, source, reference_voltage, offset=0):
        ret = MessageOutputData.from_buffer_copy(source, offset)
        assert ret.header.messageId == MessageIds.MESSAGE_OUTPUT_DATA.value
        if ret.sample_size == SampleSize.SAMPLE_SIZE_16b.value:
            assert ((len(source) - MessageOutputData._data.offset) % 2) == 0
            count = (len(source) - MessageOutputData._data.offset) // 2
            ret.data = (ctypes.c_uint16 * count).from_buffer_copy(
                source, MessageOutputData._data.offset
            )
            max_val = 65535
        elif ret.sample_size == SampleSize.SAMPLE_SIZE_8b.value:
            count = len(source) - MessageOutputData._data.offset
            ret.data = (ctypes.c_uint8 * count).from_buffer_copy(
                source, MessageOutputData._data.offset
            )
            max_val = 255
        elif ret.sample_size == SampleSize.SAMPLE_SIZE_32b.value:
            assert ((len(source) - MessageOutputData._data.offset) % 4) == 0
            count = (len(source) - MessageOutputData._data.offset) // 4
            ret.data = (ctypes.c_uint32 * count).from_buffer_copy(
                source, MessageOutputData._data.offset
            )
            max_val = ( 2 ** 32 ) - 1
        else:
            raise Exception(f"Unknown sample_size = {ret.sample_size}")
        ret.voltages = (
            np.array(ret.data, dtype=np.float64) * 2 / max_val - 1
        ) * reference_voltage
        return ret

    def __repr__(self):
        return (
            super().__repr__()
            + " : "
            + str(len(self.data))
            + " samples. Cnt: "
            + str(self.counter)
            + ". SampleSize: "
            + str(self.sample_size)
        )


class MessageConfigUserSpace(AbstractMessage, AutoCastMessage, ctypes.Structure):
    _messageId = MessageIds.MESSAGE_CONFIGURE_USER_SPACE
    _fields_ = [
        ("header", Header),
        ("data", ctypes.c_byte * USER_SPACE_SIZE),
    ]


class MessageConfigSampling(AbstractMessage, AutoCastMessage, ctypes.Structure):
    _messageId = MessageIds.MESSAGE_CONFIGURE_SAMPLING
    _fields_ = [
        ("header", Header),
        ("physicalSampleRate", ctypes.c_uint32),
        ("physicalResolution", ctypes.c_byte),
        ("processingResolution", ctypes.c_byte),
    ]

    def __repr__(self):
        return f"MessageConfigSampling: physicalSampleRate={self.physicalSampleRate}, physicalResolution={self.physicalResolution}, processingResolution={self.processingResolution}"


class MessageConfigInterfaces(AbstractMessage, AutoCastMessage, ctypes.Structure):
    _messageId = MessageIds.MESSAGE_CONFIGURE_INTERFACES
    _fields_ = [
        ("header", Header),
        ("uartBaud", ctypes.c_uint32),
    ]

    def __repr__(self):
        return f"MessageConfigInterfaces: uartBaud={self.uartBaud}"


class MessageConfigDetectorTemperature(
    AbstractMessage, AutoCastMessage, ctypes.Structure
):
    _messageId = MessageIds.MESSAGE_CONFIGURE_DETECTOR_TEMPERATURE
    _fields_ = [
        ("header", Header),
        ("temperature", ctypes.c_uint16),
    ]

    def __repr__(self):
        return f"MessageConfigDetectorTemperature: temperature={self.temperature}"


class MessageConfigRead(AbstractMessage, AutoCastMessage, ctypes.Structure):
    _messageId = MessageIds.MESSAGE_CONFIG_READ
    _fields_ = [
        ("header", Header),
        ("configID", ctypes.c_uint8),
    ]


class MessageConfigSave(AbstractMessage, AutoCastMessage, ctypes.Structure):
    _messageId = MessageIds.MESSAGE_CONFIG_SAVE
    _fields_ = [
        ("header", Header),
    ]


class MessageProcessingRead(AbstractMessage, AutoCastMessage, ctypes.Structure):
    _messageId = MessageIds.MESSAGE_PROCESSING_READ
    _fields_ = [
        ("header", Header),
        ("slotID", ctypes.c_uint8),
    ]

    def __repr__(self):
        return f"MessageProcessingRead: slotId={self.slotID}"


class AbstractWorkmode:
    """Usefull to pass to read_one_message method to filter only messages with workmode settings."""

    pass


class MessageWorkModeRead(AbstractMessage, AutoCastMessage, ctypes.Structure):
    _messageId = MessageIds.MESSAGE_MODE_READ
    _fields_ = [
        ("header", Header),
    ]


class MessageWorkmodeFreerunning(
    AbstractMessage, AbstractWorkmode, AutoCastMessage, ctypes.Structure
):
    """Describes freerunning workmode.

    Attributes:
        :samples_count: Number of samples to acquire. If zero - acquisition will never stop.
    """

    _messageId = MessageIds.MESSAGE_MODE_FREE_RUNNING
    _fields_ = [
        ("header", Header),
        ("samples_count", ctypes.c_uint32),
    ]


class MessageWorkmodeStop(
    AbstractMessage, AbstractWorkmode, AutoCastMessage, ctypes.Structure
):
    """Describes stop workmode"""

    _messageId = MessageIds.MESSAGE_MODE_STOP
    _fields_ = [
        ("header", Header),
    ]


class MessageWorkmodeTriggerInput(
    AbstractMessage, AbstractWorkmode, AutoCastMessage, ctypes.Structure
):
    """Describes trigger input workmode.

    Attributes:
        :samples_count: Number of samples to acquire with single trigger event.
        :delay: Delay between trigger event and start of acquisition, in microseconds.
        :edge: Edge of the event. Only rising edge (=1) is supported.
    """

    _messageId = MessageIds.MESSAGE_MODE_TRIGGER_INPUT
    _fields_ = [
        ("header", Header),
        ("samples_count", ctypes.c_uint32),
        ("delay", ctypes.c_uint32),
        ("edge", ctypes.c_uint8),
    ]

    def __repr__(self):
        return f"MessageWorkmodeTriggerInput: samples_count={self.samples_count}, delay={self.delay}, edge={self.edge}"


class MessageWorkmodeTriggerOutput(
    AbstractMessage, AbstractWorkmode, AutoCastMessage, ctypes.Structure
):
    """Describes trigger output workmode.

    Attributes:
        :samples_count: Number of samples to acquire with single trigger event.
        :delay: Delay between start of acquisition and trigger event, in microseconds.
        :period: Period of the trigger event, in microseconds.
        :edge: Edge of the event. Only rising edge (=1) is supported.
    """

    _messageId = MessageIds.MESSAGE_MODE_TRIGGER_OUTPUT
    _fields_ = [
        ("header", Header),
        ("samples_count", ctypes.c_uint32),
        ("delay", ctypes.c_uint32),
        ("period", ctypes.c_uint32),
        ("edge", ctypes.c_uint8),
    ]

    def __repr__(self):
        return f"MessageWorkmodeTriggerOutput: samples_count={self.samples_count}, delay={self.delay}, period={self.period}, edge={self.edge}"


def message_simulation_class(samples_count, sample_size):
    payload_bytes = (
        samples_count - ctypes.sizeof(Header) - ctypes.sizeof(ctypes.c_ubyte)
    )
    if (
        sample_size == SampleSize.SAMPLE_SIZE_8b.value
        or sample_size == SampleSize.SAMPLE_SIZE_8b
    ):
        sample_class = ctypes.c_ubyte
        sample_size_bytes = 1
    elif (
        sample_size == SampleSize.SAMPLE_SIZE_16b.value
        or sample_size == SampleSize.SAMPLE_SIZE_16b
    ):
        sample_class = ctypes.c_uint16
        sample_size_bytes = 2
    elif (
        sample_size == SampleSize.SAMPLE_SIZE_32b.value
        or sample_size == SampleSize.SAMPLE_SIZE_32b
    ):
        sample_class = ctypes.c_uint32
        sample_size_bytes = 4
    else:
        raise ValueError(f"Wrong sample_size {sample_size}")
    if samples_count * sample_size_bytes > 8192:
        raise ValueError(
            f"Buffer overflow with total {samples_count * sample_size.value} bytes"
        )

    class MessageWorkmodeSimulation(AbstractMessage, AutoCastMessage, ctypes.Structure):
        _messageId = MessageIds.MESSAGE_MODE_SIMULATION
        _fields_ = [
            ("header", Header),
            ("samples_count", ctypes.c_uint32),
            ("sample_size", ctypes.c_uint8),
            ("noise_rms", ctypes.c_float),
            ("period_in_ms", ctypes.c_uint32),
            ("samples", sample_class * samples_count),
        ]

        def __repr__(self):
            return (
                super().__repr__()
                + " : "
                + str(len(self.samples))
                + " samples, sample_size="
                + str(self.sample_size)
                + ", noise_rms="
                + str(self.noise_rms)
                + ", period="
                + str(self.period_in_ms)
            )

        def __init__(self, sample_size=sample_size, samples_count=samples_count):
            if sample_size in SampleSize:
                sample_size = sample_size.value
            super().__init__(sample_size=sample_size, samples_count=samples_count)

    return MessageWorkmodeSimulation


class MessageStatus(AbstractMessage, AutoCastMessage, ctypes.Structure):
    """Will be sent periodically by the board.

    Instances of this class will have the following members:

    :reset_flag: Indicates whether board was reset since last clearing of this flag.
    :configuration_changes: Indicates wheter some configuration was changed and is not written to non-volatile memory


    """

    _messageId = MessageIds.MESSAGE_STATUS
    _fields_ = [
        ("header", Header),
        ("reset_flag", ctypes.c_ubyte),
        ("configuration_changed", ctypes.c_ubyte),
        ("sampling_state", ctypes.c_ubyte),
        ("processing_state", ctypes.c_ubyte),
        ("data_overflow_counter", ctypes.c_uint32),
        ("messages_received_counter", ctypes.c_uint32),
        ("detector_temperature", ctypes.c_uint32),
        ("temperature_ok", ctypes.c_uint8),
    ]

    def __repr__(self):
        return f"Status: sampling={self.sampling_state}, det_temp={self.detector_temperature/1000}, temp_ok={self.temperature_ok}"


class MessageClearResetFlag(AbstractMessage, AutoCastMessage, ctypes.Structure):
    _messageId = MessageIds.MESSAGE_CLEAR_RESET_FLAG
    _fields_ = [
        ("header", Header),
    ]


class MessageReboot(AbstractMessage, AutoCastMessage, ctypes.Structure):
    _messageId = MessageIds.MESSAGE_REBOOT
    _fields_ = [
        ("header", Header),
    ]
