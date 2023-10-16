""" module:: socketcan_uds.common
    :platform: Posix
    :synopsis: An abstraction of ISO 14229 UDS protocol
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""

import struct
from collections import OrderedDict
from enum import IntEnum, unique, IntFlag

import logging
from io import BytesIO
from typing import Optional, List, Union, Tuple

LOGGER = logging.getLogger(__name__)


class DiagnosticSession(IntEnum):
    """
    Diagnostic session enum
    """
    DefaultSession = 1
    ProgrammingSession = 2
    ExtendedDiagnosticSession = 3
    SafetySystemDiagnosticSession = 4


class ResetType(IntEnum):
    """
    Reset type enum
    """
    HardReset = 1
    KeyOffOnReset = 2
    SoftReset = 3
    EnableRapidPowerShutdown = 4
    DisableRapidPowerShutdown = 5


class ComCtrlType(IntEnum):
    """
    Control types used in Communication Control service.
    """
    EnableRxTx = 0
    EnableRxDisableTx = 1
    DisableRxEnableTx = 2
    DisableRxTx = 3
    EnableRxDisableTxEnhancedAddressInfo = 4
    EnableRxTxEnhancedAddressInfo = 5


class ComType(IntEnum):
    """
    Com Type used in Communication Control Service.
    Defines the scope of messages.
    """
    NormalCommunicationMessages = 1


class DtcSettingType(IntEnum):
    """
    Type used in socketcan_uds service control dtc settings.
    """
    On = 1
    Off = 2


@unique
class DtcReportType(IntEnum):
    """
    Type used in socketcan_uds service read dtc information
    """
    ReportNumberOfDtcByStatusMask = 1
    ReportDtcByStatusMask = 2
    ReportDtcSnapshotIdentification = 3
    ReportDtcSnapshotByDtcNumber = 4
    ReportDtcStoredDataByRecordNumber = 5
    ReportDtcExtDataRecordByDtcNumber = 6
    ReportNumberOfDtcBySeverityMaskRecord = 7
    ReportDtcBySeverityMaskRecord = 8
    ReportSeverityInformationOfDtc = 9
    ReportSupportedDtc = 0xA
    ReportFirstTestFailedDtc = 0xB
    ReportFirstConfirmedDtc = 0xC
    ReportMostRecentTestFailedDtc = 0xD
    ReportMostRecentConfirmedDtc = 0xE
    ReportDtcFaultDetectionCounter = 0x14
    ReportDtcWithPermanentStatus = 0x15
    ReportDtcExtDataRecordByRecordNumber = 0x16
    ReportUserDefMemoryDtcByStatusMask = 0x17
    ReportUserDefMemoryDtcSnapshotRecordByDtcNumber = 0x18
    ReportUserDefMemoryDtcExtDataRecordByDtcNumber = 0x19
    ReportSupportedDtcExtDataRecord = 0x1A
    ReportWwhobdDtcByMaskRecord = 0x42
    ReportWwhobdDtcWithPermanentStatus = 0x55
    ReportDtcInformationByDtcReadinessGroupIdentifier = 0x56


class CompressionMethod(IntEnum):
    """
    Enum for compression method.
    """
    NO_COMPRESSION = 0
    LZMA = 0xA


class EncryptionMethod(IntEnum):
    """
    Enum for encryption method.
    """
    NO_ENCRYPTION = 0
    AES128CBC = 0xA


class ServiceId(IntEnum):
    """
    Enum for UDS Services
    """
    # Diagnostic and Communication Management
    DiagnosticSessionControl = 0x10
    EcuReset = 0x11
    SecurityAccess = 0x27
    CommunicationControl = 0x28
    TesterPresent = 0x3E
    AccessTimingParameter = 0x83  # <-- obsolete ?!
    SecuredDataTransmission = 0x84
    ControlDtcSettings = 0x85
    ResponseOnEvent = 0x86
    LinkControl = 0x87

    # Data Transmission
    ReadDataByIdentifier = 0x22
    ReadMemoryByAddress = 0x23
    ReadScalingDataByIdentifier = 0x24
    ReadDataByPeriodicIdentifier = 0x2A
    DynamicallyDefineDataIdentifier = 0x2C
    WriteDataByIdentifier = 0x2E
    WriteMemoryByAddress = 0x3D

    # Stored Data Transmission
    ClearDiagnosticInformation = 0x14
    ReadDtcInformation = 0x19

    # Input / Output Control
    InputOutputByIdentifier = 0x2F

    # Remote Activation of Routine
    RoutineControl = 0x31

    # Upload / Download
    RequestDownload = 0x34
    RequestUpload = 0x35
    TransferData = 0x36
    RequestTransferExit = 0x37


class ResponseCode(IntEnum):
    """
    UDS Negative Response Codes

    Some Explanation, when ISO14229 (UDS) was made,
    it had to be compatible with the preceding ISO14230 (KWP2000)
    so everything up to the 0x40 range is nearly identical.
    BTW: See how BOSCH managed to fake the ISO numbering?
    There are some unofficial ranges for different topics
    0x10-0x1F, 0x20-0x2F and so on.
    """
    # tester side error
    GeneralReject = 0x10
    ServiceNotSupported = 0x11
    SubFunctionNotSupported = 0x12
    IncorrectMessageLengthOrInvalidFormat = 0x13
    ResponseTooLong = 0x14

    # device side error
    BusyRepeatRequest = 0x21
    ConditionsNotCorrect = 0x22
    RequestSequenceError = 0x24
    NoResponseFromSubnetComponent = 0x25
    FaultPreventsExecutionOfRequestedAction = 0x26

    # function side error
    RequestOutOfRange = 0x31
    SecurityAccessDenied = 0x33
    InvalidKey = 0x35
    ExceededNumberOfAttempts = 0x36
    RequiredTimeDelayNotExpired = 0x37

    # 0x38-0x4F Reserved by Extended Data Link Security Document

    UploadDownloadNotAccepted = 0x70
    TransferDataSuspended = 0x71
    GeneralProgrammingFailure = 0x72
    WrongBlockSequenceCounter = 0x73

    RequestCorrectlyReceivedButResponsePending = 0x78
    # This is essentially not an Error, it is just a delay information.
    # This Response Code is due to the fact that standard autosar modules do not necessarily run on the same time disc
    # and no IPC method has every been defined for Autosar.

    SubFunctionNotSupportedInActiveSession = 0x7E
    ServiceNotSupportedInActiveSession = 0x7F


class RoutineControlType(IntEnum):
    """
    Enum for Routine Control Type.

    The first byte of Routine Control Request
    that determines what should be done with the routine.
    """
    StartRoutine = 1
    StopRoutine = 2
    RequestRoutineResults = 3


class DtcStatus(IntFlag):
    """
    Flags for DTC Status
    """
    TestFailed = 1
    TestFailedThisOperationCycle = 2
    Pending = 4
    Confirmed = 8
    TestNotCompleteSinceLastClear = 0x10
    TestFailedSinceLastClear = 0x20
    TestNotCompletedThisOperationCycle = 0x40
    WarningIndicatorRequested = 0x80


class DtcSeverety(IntFlag):
    """
    Flags for DTC Severity
    """
    DtcClass0 = 1
    DtcClass1 = 2
    DtcClass2 = 4
    DtcClass3 = 8
    DtcClass4 = 0x10
    MaintenanceOnly = 0x20
    CheckAtNextHalt = 0x40
    CheckImmediately = 0x80


class DtcReadinessGroup(IntEnum):
    """
    Enum for DTC Readiness Group (WWHOBD)
    """
    ComprehensiveComponentsMonitoring = 1


class DtcSystemGroup(IntEnum):
    """
    The "original" groups of DTCs before standardized by WWHOBD.
    24 bit unsigned integer, relates to KWP500, KWP1281, KWP2000 trouble codes.
    """
    EmissionsRelated = 0xFFFF33
    All = 0xFFFFFF


class DtcFunctionalGroup(IntEnum):
    """
    Enum for DTC Functional Group (WWHOBD)
    """
    VOBD = 0xFE
    SafetySystem = 0xD0
    EmissionSystem = 0x33


class DtcFormatIdentifier(IntEnum):
    """
    Enum for DTC Format
    """
    SAE_J2012_DA_DTCFormat_00 = 0
    ISO_14229_1_DTCFORMAT = 1
    SAE_J1939_73_DTCFORMAT = 2
    SAE_11992_4_DTCFORMAT = 3
    SAE_J2012_DA_DTCFormat_04 = 4


class IOCtlCommand(IntEnum):
    """
    Enum for Input Output Control Command
    """
    ReturnCtlToEcu = 0
    ResetToDefault = 1
    FreezeCurrentState = 2
    ShortTermAdjustment = 3


class LinkControlType(IntEnum):
    """
    Enum for Link Control Type
    """
    VerifyModeTransitionWithFixedParameter = 1
    VerifyModeTransitionWithSpecificParameter = 2
    TransitionMode = 3
    # 40-5F Vehicle Manufacturer Specific
    # 60-7E System Supplier Specific


class LinkControlModeIdentifier(IntEnum):
    PC9600Baud = 1
    PC19200Baud = 2
    PC38400Baud = 3
    PC57600Baud = 4
    PC115200Baud = 5
    CAN125kBaud = 0x10
    CAN250kBaud = 0x11
    CAN500kBaud = 0x12
    CAN1MBaud = 0x13
    ProgrammingSetup = 0x20


class ScalingDataType(IntEnum):
    """
    Enum for Scaling Data Type
    """
    UnsignedInt = 0  # Int can be 1,2,4 bytes
    SignedInt = 1  # Int can be 1,2,4 bytes
    Bits = 2
    BitsWithMask = 3
    BinaryCodedDecimal = 4
    State = 5  # 1 byte of Statemachine ENUM
    Ascii = 6
    SignedFloat = 7
    Packet = 8
    Formula = 9
    Unit = 0xA
    StateWithType = 0xB  # 1 byte


class ScalingByteUnit(IntEnum):
    """
    Enum for Scaling Byte Extension "Unit"

    Note: The variety of units basically proofs that the author had no clue about the topic.
          Having >10 different time and date formats is just stupid, there is ISO FORMAT established world wide.
          Supporting Imperial Units in a time where ISO units have been adapted world wide ?!
          This whole list can be reduced to <25% of what is defined here.
          Best thing is the Radioactivity and the Jet Engine Thrust at Sea Level!
          Truly the Batmobile has UDS support!
    """
    NoUnit = 0
    Metre = 1
    Foot = 2
    Inch = 3
    Yard = 4
    Mile = 5
    Gram = 6
    Ton = 7
    Second = 8
    Minute = 9
    Hour = 0xA
    Day = 0xB
    Year = 0xC
    Ampere = 0xD
    Volt = 0xE
    Coulomb = 0xF
    Ohm = 0x10
    Farad = 0x11
    Henry = 0x12
    Siemens = 0x13
    Weber = 0x14
    Tesla = 0x15
    Kelvin = 0x16
    Celsius = 0x17
    Fahrenheit = 0x18
    Candela = 0x19
    Radian = 0x1A
    Degree = 0x1B
    Hertz = 0x1C
    Joule = 0x1D
    Newton = 0x1E
    Kilopond = 0x1F  # seriously, a unit for jet engine thrust at sea level?!
    PoundForce = 0x20
    Watt = 0x21
    HorsePowerMetric = 0x22
    HorsePowerImperial = 0x23
    Pascal = 0x24
    Bar = 0x25
    Atmosphere = 0x26
    PoundForcePerSquareInch = 0x27
    Becqerel = 0x28  # seriously, a unit for radioactivity ?!
    Lumen = 0x29
    Lux = 0x2A
    Litre = 0x2B
    GallonUK = 0x2C
    GallonUS = 0x2D
    CubicInch = 0x2E
    MeterPerSecond = 0x2F
    KilometerPerHour = 0x30
    MilePerHour = 0x31
    RevolutionsPerSecond = 0x32
    RevolutionsPerMinute = 0x33
    Counts = 0x34
    Percent = 0x35
    MilligramPerStroke = 0x36
    MetrePerSquareSecond = 0x37
    NewtonMeter = 0x38
    LitrePerMinute = 0x39
    WattPerSquareMetre = 0x3A
    BarPerSecond = 0x3B
    RadiansPerSecond = 0x3C
    RadiansPerSquareSecond = 0x3D
    KilogramPerSquareMetre = 0x3E

    # Scaling
    Exa = 0x40  # 10**18
    Peta = 0x41  # 10*15
    Tera = 0x42  # 10**12
    Giga = 0x43  # 10**9
    Mega = 0x44  # 10**6
    Kilo = 0x45  # 10**3
    Hecto = 0x46  # 10**2
    Deca = 0x47  # 10**1
    Deci = 0x48  # 10**-1
    Centi = 0x49  # 10**-2
    Milli = 0x4A  # 10**-3
    Micro = 0x4B  # 10**-6
    Nano = 0x4C  # 10**-9
    Pico = 0x4D  # 10**-12
    Femto = 0x4E  # 10**-15
    Atto = 0x4F  # 10**-18

    # time and date - seriously ?! and were is ISO FORMAT ?!
    Date1 = 0x50  # y-m-d
    Date2 = 0x51  # d/m/y
    Date3 = 0x52  # m/d/y
    Week = 0x53  # calendar week
    Time1 = 0x54  # UTC H/M/S
    Time2 = 0x55  # H/M/S
    TimeAndDate1 = 0x56  # S/M/H/d/m/y
    TimeAndDate2 = 0x57  # S/M/H/d/m/y/minute_offset/hour_offset
    TimeAndDate3 = 0x58  # S/M/H/m/d/y
    TimeAndDate4 = 0x59  # S/M/H/m/d/y/minute_offset/hour_offset


class LogicState(IntEnum):
    NotActive = 0
    Active = 1
    Error = 2
    NotAvailable = 3
    Function2 = 4


class SignalState(IntEnum):
    Low = 0
    Middle = 1
    High = 2


class SignalDirection(IntEnum):
    Input = 0
    Output = 1


class SignalDrive(IntEnum):
    Internal = 0
    PullDown = 1
    PullUp = 2
    Strong = 3  # Pull-Up and PullDown


class EventStorageState(IntEnum):
    NoStorage = 0
    StoreEvent = 1


class EventCommand(IntEnum):
    Stop = 0
    OnDtcStatusChange = 1
    OnDidChange = 3
    ReportActiveEvents = 4
    Start = 5
    Clear = 6
    OnValueCompare = 7
    ReportMostRecentDtcStatusChange = 8
    ReportDtcRecordInformationOnDtcStatusChange = 9


class EventWindow(IntEnum):
    Infinite = 2
    Short = 3
    Medium = 4
    Long = 5
    PowerCycle = 6
    IgnitionCycle = 7
    Manufacturer = 8


# helper functions

def int_to_dtc_bytes(dtc_as_integer: int,
                     ) -> bytes:
    """
    A helper to cast an integer into a 3 byte big endian representation.

    :param dtc_as_integer: The number.
    :return: The number as 3 bytes.
    """
    assert 0 <= dtc_as_integer < 0x1000000
    return struct.pack(">I", dtc_as_integer)[1:]


def dtc_bytes_to_int(dtc_as_bytes: bytes,
                     ) -> int:
    """
    A helper to cast a 3 byte big endian number to integer.

    :param dtc_as_bytes: The 3 bytes big endian value.
    :return: The number as integer.
    """
    assert len(dtc_as_bytes) == 3
    return struct.unpack(">I", dtc_as_bytes.rjust(4, b"\x00"))[0]


# parser and concat functions for services

def concat_diagnostic_session_control_request(session: DiagnosticSession) -> bytes:
    """
    Concat diagnostic session control request.

    :param session: The requested diagnostic session.
    :return: The request as bytes.
    """
    assert session in DiagnosticSession
    return struct.pack("BB", ServiceId.DiagnosticSessionControl, session)


def parse_diagnostic_session_control_response(resp: bytes) -> dict:
    """
    Parse diagnostic session control response.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    values = list(struct.unpack(">BBHH", resp))
    # scale both values to seconds
    values[1] = DiagnosticSession(values[1])
    values[2] = values[2] / 1000
    values[3] = values[3] / 100
    return dict(zip(["response_sid", "session", "p2_server_max", "p2*_server_max"], values))


def concat_ecu_reset_request(rtype: ResetType) -> bytes:
    """
    Concat ecu reset request.

    :param rtype: The requested ResetType.
    :return: The request as bytes.
    """
    assert rtype in ResetType
    return struct.pack("BB", ServiceId.EcuReset, rtype)


def parse_ecu_reset_response(resp: bytes) -> dict:
    """
    Parse ecu reset response.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    return dict(zip(["response_sid", "rtype", "power_down_time"], resp))


def concat_security_access_request(security_level: int,
                                   key: Optional[bytes]
                                   ) -> bytes:
    """
    Concat security access request.

    :param security_level: The security level. Uneven=SeedRequest, Even=KeyPost
    :param key: The key bytes.
    :return: The request as bytes.
    """
    if security_level not in range(0x100):
        raise ValueError("Value {0} is not in range 0-0xFF".format(security_level))

    if (security_level & 0x1) == 0:
        if key is None:
            raise ValueError(
                "Security Access to an even security_level ({0}) must provide a key {1}".format(security_level, key))
        req = struct.pack("BB{0}s".format(len(key)), ServiceId.SecurityAccess, security_level, key)
    else:
        req = struct.pack("BB", ServiceId.SecurityAccess, security_level)
    return req


def parse_security_access_response(resp: bytes) -> dict:
    """
    Parse security access response.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    if resp[1] & 0x1:
        # response to seed request, so extract seed, otherwise not
        fmt = "BB{0}s".format(len(resp) - 2)
    else:
        fmt = "BB"
    values = list(struct.unpack(fmt, resp))
    keys = ["response_sid", "security_level", "seed"]
    return dict(zip(keys, values))


def concat_read_data_by_id_request(did: int) -> bytes:
    """
    Concat read data by id request.

    :param did: The diagnostic identifier to be read.
    :return: The request as bytes.
    """
    if did not in range(0x10000):
        raise ValueError("Value {0} is not in range 0-0xFFFF".format(did))
    return struct.pack(">BH", ServiceId.ReadDataByIdentifier, did)


def parse_read_data_by_id_response(resp: bytes) -> dict:
    """
    Parse read data by id response.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    return dict(zip(["response_sid", "did", "data"], struct.unpack(">BH{0}s".format(len(resp) - 3), resp)))


def concat_communication_control_request(ctrl_type: ComCtrlType,
                                         com_type: ComType = ComType.NormalCommunicationMessages,
                                         node_id: Optional[int] = None,
                                         suppress_response: bool = False,
                                         ) -> bytes:
    """
    Concat communication control request.

    :param ctrl_type: The control type.
    :param com_type: The communication type. The scope of messages.
    :param node_id: The Node identification number. Used with enhanced address info.
    :param suppress_response: Suppress the the positive response.
    :return: The request as bytes.
    """
    assert ctrl_type in ComCtrlType
    if suppress_response:
        ctrl_type_byte = ctrl_type | 0x80
    else:
        ctrl_type_byte = ctrl_type
    if ctrl_type in [ComCtrlType.EnableRxDisableTxEnhancedAddressInfo, ComCtrlType.EnableRxTxEnhancedAddressInfo]:
        if node_id is None:
            raise ValueError("ctrl_type {0} requires node_id".format(ctrl_type.name))
        return struct.pack(">BBBH", ServiceId.CommunicationControl, ctrl_type_byte, com_type, node_id)
    else:
        if node_id is not None:
            raise ValueError("ctrl_type {0} may not have node_id".format(ctrl_type.name))
        return struct.pack("BBB", ServiceId.CommunicationControl, ctrl_type_byte, com_type)


def parse_communication_control_response(resp: bytes) -> dict:
    """
    Parse communication control response.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    values = list(struct.unpack("BB", resp))
    if values[1] & 0x80:
        raise ValueError("The suppress positive response bit is set, this is impossible")
    values[1] = ComCtrlType(values[1] & 0x7F)
    return dict(zip(["response_sid", "ctrl_type"], values))


def concat_tester_present_request(suppress_response: bool = True,
                                  ) -> bytes:
    """
    Concat tester present request.

    :param suppress_response: Suppress the the positive response. Default on.
    :return: The request as bytes.
    """
    zero_sub_function = 0
    if suppress_response:
        zero_sub_function = 0x80
    return struct.pack("BB", ServiceId.TesterPresent, zero_sub_function)


def parse_tester_present_response(resp: bytes) -> dict:
    """
    Parse tester present response.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    # second byte zerosubfunction is always 0
    return dict(zip(["response_sid", "zerosubfunction"], resp))


def concat_control_dtc_setting_request(stype: DtcSettingType,
                                       dtcs: Optional[List[int]] = None,
                                       suppress_response: bool = False):
    """
    Concat control dtc setting request.

    :param stype: The DtcSettingType On or Off
    :param dtcs: A list of dtc numbers in range 0-0xFFFFFF
    :param suppress_response: Suppress the the positive response.
    :return: The request as bytes.
    """
    stype_byte = stype
    if suppress_response:
        stype_byte = stype_byte | 0x80
    ret = bytearray(struct.pack("BB", ServiceId.ControlDtcSettings, stype_byte))
    if dtcs is not None:
        for dtc in dtcs:
            ret.extend(int_to_dtc_bytes(dtc))
    return bytes(ret)


def parse_control_dtc_setting_response(resp: bytes) -> dict:
    """
    Parse control dtc setting response.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    # second byte zerosubfunction is always 0
    values = list(resp)
    values[1] = DtcSettingType(values[1])
    return dict(zip(["response_sid", "stype"], values))


def concat_write_data_by_id_request(did: int,
                                    data: bytes) -> bytes:
    """
    Concat write data by id request.

    :param did: The diagnostic identifier to be read.
    :param data: The data bytes to be written.
    :return: The request as bytes.
    """
    if did not in range(0x10000):
        raise ValueError("Value {0} is not in range 0-0xFFFF".format(did))
    if len(data) == 0:
        raise ValueError("Invalid length of data {0}".format(len(data)))
    return struct.pack(">BH{0}s".format(len(data)), ServiceId.WriteDataByIdentifier, did, data)


def parse_write_data_by_id_response(resp: bytes) -> dict:
    """
    Parse write data by id response.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    return dict(zip(["response_sid", "did"], struct.unpack(">BH", resp)))


def concat_clear_diagnostic_information_request(group_filter: DtcSystemGroup,
                                                memory_select: Optional[int] = None) -> bytes:
    """
    Concat clear diagnostic information request.

    :param group_filter: The Dtc Mask, actually a DTC group, e.g. 0xFFFF33 is emissions-related systems.
    :param memory_select: An optional byte to select a specific error memory, e.g. a secondary error memory mirror.
    :return: The request as bytes.
    """
    if memory_select is not None:
        return struct.pack(">B3sB", ServiceId.ClearDiagnosticInformation, int_to_dtc_bytes(group_filter), memory_select)
    else:
        return struct.pack(">B3s", ServiceId.ClearDiagnosticInformation, int_to_dtc_bytes(group_filter))


def parse_clear_diagnostic_information_response(resp: bytes) -> dict:
    """
    Parse clear diagnostic information response.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    return dict(zip(["response_sid", ], struct.unpack("B", resp)))


def concat_read_dtc_information_request(
        subfunction: DtcReportType,
        status_filter: Optional[Union[DtcStatus, DtcSeverety, DtcReadinessGroup]] = None,
        group_filter: Optional[Union[DtcSystemGroup, DtcFunctionalGroup]] = None,
        record_filter: Optional[int] = None,
        memory_select: Optional[int] = None) -> bytearray:
    """
    Concat clear diagnostic information request.

    :param subfunction: The subfunction of this service.
    :param status_filter: A bitmask to filter by status flags.
    :param group_filter: The Dtc Mask. A DTC Mask is a group of dtcs, e.g. 0xFFFF33 is emissions-related systems.
    :param record_filter: The Record number / Index in Error Memory.
    :param memory_select: An optional byte to select a specific error memory, e.g. a secondary error memory mirror.

    :return: The request as bytes.
    :raises ValueError: In case not all inputs are provided correctly.
    """
    ret = bytearray((ServiceId.ReadDtcInformation, subfunction))

    if subfunction in [DtcReportType.ReportSeverityInformationOfDtc,
                       DtcReportType.ReportDtcSnapshotIdentification,
                       DtcReportType.ReportDtcSnapshotByDtcNumber,
                       DtcReportType.ReportDtcExtDataRecordByDtcNumber,
                       DtcReportType.ReportUserDefMemoryDtcSnapshotRecordByDtcNumber,
                       DtcReportType.ReportUserDefMemoryDtcExtDataRecordByDtcNumber
                       ]:
        ret.extend(int_to_dtc_bytes(group_filter))
    elif subfunction in [DtcReportType.ReportDtcInformationByDtcReadinessGroupIdentifier,
                         DtcReportType.ReportWwhobdDtcWithPermanentStatus,
                         DtcReportType.ReportWwhobdDtcByMaskRecord,
                         ]:
        ret.append(group_filter)

    if subfunction in [DtcReportType.ReportDtcStoredDataByRecordNumber,
                       DtcReportType.ReportDtcExtDataRecordByRecordNumber,
                       DtcReportType.ReportSupportedDtcExtDataRecord,
                       DtcReportType.ReportDtcSnapshotIdentification,
                       DtcReportType.ReportDtcSnapshotByDtcNumber,
                       DtcReportType.ReportDtcExtDataRecordByDtcNumber,
                       DtcReportType.ReportUserDefMemoryDtcSnapshotRecordByDtcNumber,
                       DtcReportType.ReportUserDefMemoryDtcExtDataRecordByDtcNumber
                       ]:
        ret.append(record_filter)

    elif subfunction in [DtcReportType.ReportNumberOfDtcByStatusMask,
                         DtcReportType.ReportDtcByStatusMask,
                         DtcReportType.ReportNumberOfDtcBySeverityMaskRecord,
                         DtcReportType.ReportDtcBySeverityMaskRecord,
                         DtcReportType.ReportUserDefMemoryDtcByStatusMask,
                         DtcReportType.ReportWwhobdDtcByMaskRecord,
                         DtcReportType.ReportDtcInformationByDtcReadinessGroupIdentifier
                         ]:
        ret.append(status_filter)

    if subfunction in [DtcReportType.ReportUserDefMemoryDtcSnapshotRecordByDtcNumber,
                       DtcReportType.ReportUserDefMemoryDtcExtDataRecordByDtcNumber,
                       DtcReportType.ReportUserDefMemoryDtcByStatusMask,
                       ]:
        ret.append(memory_select)

    return ret


def split_by_number_of_elems(data: bytes) -> list[bytes]:
    """
    Split records by number of elements.

    A helper to split a record by its elem count.
    It relies on the approach that each element has the same length.

    :param data: The raw data of a dtc record.
    :return: A list of elements.
    """
    elem_cnt = data[0]
    assert len(data[1:]) % elem_cnt == 0
    elem_size = int(len(data[1:]) / elem_cnt)
    LOGGER.debug("elem_size {0} elem_cnt {1}".format(elem_size, elem_cnt))
    elems = []
    if elem_size > 0:
        elems = [data[idx: idx + elem_size] for idx in range(1, len(data[1:]) + 1, elem_size)]
    return elems


def split_records_by_index(data: bytes) -> list[bytes]:
    """
    Split records by index.

    A helper to split a record by its index's.
    An element starts with its index which is a single byte that is counted up over the index's.
    The idea is to look for the next byte that is equal to the next index, suspect this to be the element size and check
    if the overall size is a multiple of that element size.

    This function works on best effort basis. If no numbering scheme is found, it returns a list with one element.

    :param data: The raw data of a dtc record.
    :return: A list of elements.
    """

    try:
        LOGGER.info(data.hex())
        assert data[0] == 1
        elem_size = [index for index in range(int(len(data) / 2) + 1) if
                     ((data[index] == 2) and ((len(data) % index) == 0)
                      and data[(int(len(data) / index) - 1) * index] == int(len(data) / index)
                      )][-1]

    except (AssertionError, IndexError):
        elem_size = len(data)  # the default
    LOGGER.info("elem_size {0}".format(elem_size))
    elems = []
    if elem_size > 0:
        elems = [data[idx:idx + elem_size] for idx in range(0, len(data), elem_size)]
    return elems


def dtc_values_record_to_dict(data: bytes) -> dict:
    values = {}
    for chunk in split_by_number_of_elems(data):
        identifier = int.from_bytes(chunk[:2], "big")
        identifier_data = chunk[2:]
        values.update({identifier: identifier_data})
    return values


def parse_read_dtc_information_number_of_dtc_response(resp: bytes) -> dict:
    """
    Parse read dtc information response.

    Subtype to reduce complexity.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    status_availability = resp[2]
    format_identifier = DtcFormatIdentifier(resp[3])
    dtc_count = int.from_bytes(resp[4:6], "big")
    return dict(status_availablitiy=status_availability, format_idendifier=format_identifier, dtc_count=dtc_count)


def parse_read_dtc_information_list_response(resp: bytes) -> dict:
    """
    Parse read dtc information response.

    Subtype to reduce complexity.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    status_availability = resp[2]
    records = OrderedDict()
    for idx in range(3, len(resp), 4):
        dtc_number = dtc_bytes_to_int(resp[idx:idx + 3])
        status = DtcStatus(resp[idx + 3])
        records.update({dtc_number: status})
    return dict(status_availablitiy=status_availability, records=records)


def parse_read_dtc_information_snapshot_identification_response(resp: bytes) -> dict:
    """
    Parse read dtc information response.

    Subtype to reduce complexity.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    records = OrderedDict()
    for idx in range(2, len(resp), 4):
        records.update({dtc_bytes_to_int(resp[idx:idx + 3]): resp[idx + 3]})
    return dict(records=records)


def parse_read_dtc_information_snapshot_by_number_response(resp: bytes) -> dict:
    """
    Parse read dtc information response.

    Subtype to reduce complexity.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    dtc = dtc_bytes_to_int(resp[2:5])
    dtc_status = DtcStatus(resp[5])
    records = OrderedDict()
    for record in split_records_by_index(data=resp[6:]):
        # LOGGER.info("record {0}".format(record))
        record_number = record[0]
        # LOGGER.info("record_number {0}".format(record_number))
        values = dtc_values_record_to_dict(record[1:])
        records.update({record_number: values})
    return dict(dtc=dtc, dtc_status=dtc_status, records=records)


def parse_read_dtc_information_stored_data_by_record_number_response(resp: bytes) -> dict:
    """
    Parse read dtc information response.

    Subtype to reduce complexity.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    stored_dtcs = OrderedDict()
    for record in split_records_by_index(data=resp[2:]):
        # record_idx = record[0]  # useless, drop it
        dtc = dtc_bytes_to_int(record[1:4])
        # LOGGER.info("dtc {0:X}".format(dtc))
        dtc_status = DtcStatus(record[4])
        # LOGGER.info("dtc_status {0}".format(str(dtc_status)))
        values = dtc_values_record_to_dict(record[5:])
        stored_dtcs.update({dtc: dict(dtc_status=dtc_status, values=values)})
    return dict(records=stored_dtcs)


def parse_read_dtc_information_ext_data_record_by_dtc_number_response(resp: bytes) -> dict:
    """
    Parse read dtc information response.

    Subtype to reduce complexity.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    dtc = dtc_bytes_to_int(resp[2:5])
    dtc_status = DtcStatus(resp[5])
    ext_data = split_records_by_index(data=resp[6:])
    return dict(dtc=dtc, dtc_status=dtc_status, ext_data=ext_data)


def parse_read_dtc_information_severety_information_response(resp: bytes) -> dict:
    """
    Parse read dtc information response.

    Subtype to reduce complexity.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    records = OrderedDict()
    for idx in range(2, len(resp), 6):
        severety = DtcSeverety(resp[idx])
        functional_unit = resp[idx + 1]
        dtc = dtc_bytes_to_int(resp[idx + 2:idx + 5])
        dtc_status = DtcStatus(resp[idx + 5])
        records.update({dtc: dict(severety=severety, functional_unit=functional_unit, dtc_status=dtc_status)})
    return dict(records=records)


def parse_read_dtc_information_fault_detection_counter_response(resp: bytes) -> dict:
    """
    Parse read dtc information response.

    Subtype to reduce complexity.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    records = OrderedDict()
    for idx in range(2, len(resp), 4):
        dtc = dtc_bytes_to_int(resp[idx:idx + 3])
        dtc_cnt = resp[idx + 3]
        records.update({dtc: dtc_cnt})
    return dict(records=records)


def parse_read_dtc_information_ext_data_record_by_record_number_response(resp: bytes) -> dict:
    """
    Parse read dtc information response.

    Subtype to reduce complexity.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    records = OrderedDict()
    for record in split_by_number_of_elems(data=resp[2:]):
        dtc = dtc_bytes_to_int(record[:3])
        dtc_status = DtcStatus(record[3])
        ext_data = record[4:]
        records.update({dtc: dict(dtc_status=dtc_status, ext_data=ext_data)})
    return dict(records=records)


def parse_read_dtc_information_user_def_memory_status_mask_response(resp: bytes) -> dict:
    """
    Parse read dtc information response.

    Subtype to reduce complexity.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    memory_select = resp[2]
    status_availability = resp[3]

    records = OrderedDict()
    for idx in range(4, len(resp), 4):
        dtc = dtc_bytes_to_int(resp[idx:idx + 3])
        dtc_status = DtcStatus(resp[idx + 3])
        records.update({dtc: dtc_status})
    return dict(records=records, memory_select=memory_select, status_availability=status_availability)


def parse_read_dtc_information_user_def_memory_by_snapshot_response(resp: bytes) -> dict:
    """
    Parse read dtc information response.

    Subtype to reduce complexity.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    memory_select = resp[2]
    dtc = dtc_bytes_to_int(resp[3:6])
    records = OrderedDict()
    for record in split_records_by_index(data=resp[6:]):
        record_number = record[0]
        values = dtc_values_record_to_dict(record[1:])
        records.update({record_number: values})
    return dict(dtc=dtc, memory_select=memory_select, records=records)


def parse_read_dtc_information_user_def_memory_by_dtc_number_response(resp: bytes) -> dict:
    """
    Parse read dtc information response.

    Subtype to reduce complexity.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    memory_select = resp[2]
    dtc = dtc_bytes_to_int(resp[3:6])
    dtc_status = DtcStatus(resp[6])
    ext_data = split_records_by_index(data=resp[7:])
    return dict(dtc=dtc, dtc_status=dtc_status, ext_data=ext_data, memory_select=memory_select)


def parse_read_dtc_information_supported_dtc_ext_data_response(resp: bytes) -> dict:
    """
    Parse read dtc information response.

    Subtype to reduce complexity.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    status_availability = resp[2]
    records = OrderedDict()
    for record in split_by_number_of_elems(data=resp[3:]):
        dtc = dtc_bytes_to_int(record[:3])
        dtc_status = DtcStatus(record[3])
        records.update({dtc: dtc_status})
    return dict(records=records, status_availability=status_availability)


def parse_read_dtc_information_wwhobdc_by_mask_response(resp: bytes) -> dict:
    """
    Parse read dtc information response.

    Subtype to reduce complexity.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    functional_group = DtcFunctionalGroup(resp[2])
    status_availability = resp[3]
    severity_availability = resp[4]
    dtc_format_identifier = DtcFormatIdentifier(resp[5])
    records = OrderedDict()
    for idx in range(6, len(resp), 5):
        severity = DtcSeverety(resp[idx])
        dtc = dtc_bytes_to_int(resp[idx + 1:idx + 4])
        dtc_status = DtcStatus(resp[idx + 4])
        # LOGGER.info("INDEX {0} LEN {1}".format(idx, len(resp[6:])))
        records.update({dtc: dict(dtc_status=dtc_status, severity=severity)})
    return dict(records=records, status_availability=status_availability, dtc_format_identifier=dtc_format_identifier,
                severity_availability=severity_availability, functional_group=functional_group)


def parse_read_dtc_information_wwhobdc_with_permanent_status_response(resp: bytes) -> dict:
    """
    Parse read dtc information response.

    Subtype to reduce complexity.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    functional_group = DtcFunctionalGroup(resp[2])
    status_availability = resp[3]
    dtc_format_identifier = DtcFormatIdentifier(resp[4])
    records = OrderedDict()
    for idx in range(5, len(resp), 4):
        dtc = dtc_bytes_to_int(resp[idx:idx + 3])
        dtc_status = DtcStatus(resp[idx + 3])
        records.update({dtc: dtc_status})
    return dict(records=records, status_availability=status_availability, dtc_format_identifier=dtc_format_identifier,
                functional_group=functional_group)


def parse_read_dtc_information_wwhobdc_dtc_by_readiness_group_response(resp: bytes) -> dict:
    """
    Parse read dtc information response.

    Subtype to reduce complexity.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    functional_group = DtcFunctionalGroup(resp[2])
    status_availability = resp[3]
    dtc_format_identifier = DtcFormatIdentifier(resp[4])
    readiness_group_identifier = DtcReadinessGroup(resp[5])
    records = OrderedDict()
    for idx in range(6, len(resp), 4):
        dtc = dtc_bytes_to_int(resp[idx:idx + 3])
        dtc_status = DtcStatus(resp[idx + 3])
        records.update({dtc: dtc_status})
    return dict(records=records, status_availability=status_availability, dtc_format_identifier=dtc_format_identifier,
                functional_group=functional_group, readiness_group_identifier=readiness_group_identifier)


def parse_read_dtc_information_response(resp: bytes) -> dict:
    """
    Parse read dtc information response.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """

    dtc_report_to_parser_mapping = {
        DtcReportType.ReportNumberOfDtcBySeverityMaskRecord: parse_read_dtc_information_number_of_dtc_response,
        DtcReportType.ReportNumberOfDtcByStatusMask: parse_read_dtc_information_number_of_dtc_response,
        DtcReportType.ReportDtcByStatusMask: parse_read_dtc_information_list_response,
        DtcReportType.ReportSupportedDtc: parse_read_dtc_information_list_response,
        DtcReportType.ReportFirstTestFailedDtc: parse_read_dtc_information_list_response,
        DtcReportType.ReportFirstConfirmedDtc: parse_read_dtc_information_list_response,
        DtcReportType.ReportMostRecentTestFailedDtc: parse_read_dtc_information_list_response,
        DtcReportType.ReportMostRecentConfirmedDtc: parse_read_dtc_information_list_response,
        DtcReportType.ReportDtcWithPermanentStatus: parse_read_dtc_information_list_response,
        DtcReportType.ReportDtcSnapshotIdentification: parse_read_dtc_information_snapshot_identification_response,
        DtcReportType.ReportDtcSnapshotByDtcNumber: parse_read_dtc_information_snapshot_by_number_response,
        DtcReportType.ReportDtcStoredDataByRecordNumber:
            parse_read_dtc_information_stored_data_by_record_number_response,
        DtcReportType.ReportDtcExtDataRecordByDtcNumber:
            parse_read_dtc_information_ext_data_record_by_dtc_number_response,
        DtcReportType.ReportSeverityInformationOfDtc: parse_read_dtc_information_severety_information_response,
        DtcReportType.ReportDtcBySeverityMaskRecord: parse_read_dtc_information_severety_information_response,
        DtcReportType.ReportDtcFaultDetectionCounter: parse_read_dtc_information_fault_detection_counter_response,
        DtcReportType.ReportDtcExtDataRecordByRecordNumber:
            parse_read_dtc_information_ext_data_record_by_record_number_response,
        DtcReportType.ReportUserDefMemoryDtcByStatusMask:
            parse_read_dtc_information_user_def_memory_status_mask_response,
        DtcReportType.ReportUserDefMemoryDtcSnapshotRecordByDtcNumber:
            parse_read_dtc_information_user_def_memory_by_snapshot_response,
        DtcReportType.ReportUserDefMemoryDtcExtDataRecordByDtcNumber:
            parse_read_dtc_information_user_def_memory_by_dtc_number_response,
        DtcReportType.ReportSupportedDtcExtDataRecord: parse_read_dtc_information_supported_dtc_ext_data_response,
        DtcReportType.ReportWwhobdDtcByMaskRecord: parse_read_dtc_information_wwhobdc_by_mask_response,
        DtcReportType.ReportWwhobdDtcWithPermanentStatus:
            parse_read_dtc_information_wwhobdc_with_permanent_status_response,
        DtcReportType.ReportDtcInformationByDtcReadinessGroupIdentifier:
            parse_read_dtc_information_wwhobdc_dtc_by_readiness_group_response,
    }

    response_sid = resp[0]
    subfunction = DtcReportType(resp[1])
    ret = dict(response_sid=response_sid,
               subfunction=subfunction)

    parser = dtc_report_to_parser_mapping.get(subfunction)

    if parser is not None and callable(parser):
        ret.update(parser(resp=resp))

    return ret


def concat_alfid_size_addr(size: int,
                           addr: int,
                           addr_size_len: Union[str, Tuple[int, int]] = "auto"
                           ) -> bytearray:
    """
    Concat the address and length format identifier together with address and size field.

    This is a commonly used pattern, so it became a separate function.
    Instead of using fixed sizes or at least one size indicator for both, the protocol defines an overly complicated
    format just to save a few bytes.
    In reality ECUs have fixed sizes for different services, so you need to know what size they accept.
    The most common practice is to deliver this information in a zipped xml file,
    together with dataset binaries to be downloaded. The file extension for those is ".pdx".

    :param addr: The address of the download/upload.
    :type addr: int
    :param size: The size of the download/upload.
    :type size: int
    :param addr_size_len: Byte length used to represent addr and size. Default is "auto".
    :type addr_size_len: Union[str, Tuple[int, int]]
    :return: The address length format identifier.
    :rtype: bytearray
    """
    ret = bytearray()
    if addr_size_len == "auto":
        addr_length = int(len("{0:02X}".format(addr)) / 2)
        size_length = int(len("{0:02X}".format(size)) / 2)
    else:
        addr_length, size_length = addr_size_len
        assert int(len("{0:02X}".format(addr)) / 2) <= addr_length
        assert int(len("{0:02X}".format(size)) / 2) <= size_length

    LOGGER.debug("addr {0} len {1}, size {2} len {3}".format(addr, addr_length, size, size_length))
    address_and_length_format_identifier = (size_length << 4) | addr_length

    ret.append(address_and_length_format_identifier)
    ret.extend(addr.to_bytes(length=addr_length, byteorder="big"))
    ret.extend(size.to_bytes(length=size_length, byteorder="big"))
    return ret


def parse_alfid_content(data: Union[bytes, bytearray]) -> dict:
    """
    Parse the address and length format identifier and the tailing payload.

    Return the numbers for address and length.
    :param data: The data bytes.
    :type data: Union[bytes, bytearray]
    :return: A dictionary with addr and size.
    :rtype: dict
    """
    size_length = data[0] >> 4
    addr_length = data[0] & 0xF
    addr = int.from_bytes(data[1:1 + addr_length], "big")
    size = int.from_bytes(data[1 + addr_length:1 + addr_length + size_length], "big")
    return dict(addr=addr, size=size)


def concat_request_download_or_upload_request(service_id: ServiceId,
                                              addr: int,
                                              size: int,
                                              compression_method: CompressionMethod = CompressionMethod.NO_COMPRESSION,
                                              encryption_method: EncryptionMethod = EncryptionMethod.NO_ENCRYPTION,
                                              addr_size_len: Union[str, Tuple[int, int]] = "auto",
                                              ) -> bytes:
    """
    Concat request download/upload request.

    This method prevents double coding because the service and its response only differ by the service id.

    :param service_id: Select download/upload via service_id
    :param addr: The address of the download/upload.
    :param size: The size of the download/upload.
    :param compression_method: The method of compression.
    :param encryption_method: The method of encryption.
    :param addr_size_len: Byte length used to represent addr and size.
    :return: The request as bytes.
    """
    assert service_id in [ServiceId.RequestDownload, ServiceId.RequestUpload]
    assert 0 <= compression_method <= 0xF
    assert 0 <= encryption_method <= 0xF

    data_format_identifier = (compression_method << 4) | encryption_method
    ret = bytearray((service_id, data_format_identifier))
    ret.extend(concat_alfid_size_addr(size=size,
                                      addr=addr,
                                      addr_size_len=addr_size_len))
    return bytes(ret)


def concat_request_download_request(addr: int,
                                    size: int,
                                    compression_method: CompressionMethod = CompressionMethod.NO_COMPRESSION,
                                    encryption_method: EncryptionMethod = EncryptionMethod.NO_ENCRYPTION,
                                    addr_size_len: Union[str, Tuple[int, int]] = "auto",
                                    ) -> bytes:
    """
    Concat request download request.

    :param addr: The address of the download. Hardcoded to 32bit for now.
    :param size: The size of the download. Hardcoded to 32bit for now.
    :param compression_method: The method of compression.
    :param encryption_method: The method of encryption.
    :param addr_size_len: Byte length used to represent addr and size.
    :return: The request as bytes.
    """
    return concat_request_download_or_upload_request(service_id=ServiceId.RequestDownload,
                                                     addr=addr,
                                                     size=size,
                                                     compression_method=compression_method,
                                                     encryption_method=encryption_method,
                                                     addr_size_len=addr_size_len,
                                                     )


def concat_request_upload_request(addr: int,
                                  size: int,
                                  compression_method: CompressionMethod = CompressionMethod.NO_COMPRESSION,
                                  encryption_method: EncryptionMethod = EncryptionMethod.NO_ENCRYPTION,
                                  addr_size_len: Union[str, Tuple[int, int]] = "auto",
                                  ) -> bytes:
    """
    Concat request download request.

    :param addr: The address of the download. Hardcoded to 32bit for now.
    :param size: The size of the download. Hardcoded to 32bit for now.
    :param compression_method: The method of compression.
    :param encryption_method: The method of encryption.
    :param addr_size_len: Byte length used to represent addr and size.
    :return: The request as bytes.
    """
    return concat_request_download_or_upload_request(service_id=ServiceId.RequestUpload,
                                                     addr=addr,
                                                     size=size,
                                                     compression_method=compression_method,
                                                     encryption_method=encryption_method,
                                                     addr_size_len=addr_size_len,
                                                     )


def parse_request_download_or_upload_response(resp: bytes) -> dict:
    """
    Parse request download/upload response.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    response_sid = resp[0]
    length_format_identifier = resp[1] >> 4
    if length_format_identifier != len(resp[2:]):
        raise ValueError(
            "Mismatch length_format_identifier {0} != buffer length {1}".format(length_format_identifier,
                                                                                len(resp[2:])))
    max_block_length = int.from_bytes(resp[2:], byteorder="big")
    return dict(zip(["response_sid", "max_block_length"], [response_sid, max_block_length]))


def concat_transfer_data_request(block_sequence_counter: int,
                                 data: bytes,
                                 ) -> bytes:
    """
    Concat transfer data request.

    :param block_sequence_counter: The block counter for this transfer.
    :param data: The data to be transferred.
    :return: The request as bytes.
    """
    return struct.pack(">BB{0}s".format(len(data)), ServiceId.TransferData, (block_sequence_counter & 0xFF), data)


def parse_transfer_data_response(resp: bytes) -> dict:
    """
    Parse transfer data response

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    values = struct.unpack(">BB{0}s".format(len(resp) - 2), resp)
    return dict(zip(["response_sid", "block_sequence_counter", "data"], values))


def concat_request_transfer_exit_request(transfer_request_parameters: Optional[bytes] = None
                                         ) -> bytes:
    """
    Concat request transfer exit request.

    :param transfer_request_parameters: A never used manufacturer specific value.
    :return: The request as bytes.
    """
    ret = bytearray()
    ret.append(ServiceId.RequestTransferExit)
    if transfer_request_parameters is not None:
        ret.extend(transfer_request_parameters)
    return bytes(ret)


def parse_request_transfer_exit_response(resp: bytes) -> dict:
    """
    Parse request transfer exit response

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    values = struct.unpack(">B{0}s".format(len(resp) - 1), resp)
    return dict(zip(["response_sid", "transfer_request_parameters"], values))


def concat_routine_control_request(routine_control_type: RoutineControlType,
                                   routine_id: int,
                                   data: Optional[bytes] = None
                                   ) -> bytes:
    """
    Concat routine control request.

    :param routine_control_type: The control type, e.g. Start/Stop/Poll.
    :param routine_id: The Routine Id.
    :param data: The (optional) data that the routine consumes.
    :return: The request as bytes.
    """
    ret = bytearray(struct.pack(">BBH", ServiceId.RoutineControl, routine_control_type, routine_id))
    if data is not None and isinstance(data, bytes):
        ret.extend(data)
    return bytes(ret)


def parse_routine_control_response(resp: bytes) -> dict:
    """
    Parse routine control response.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    assert len(resp) >= 4
    values = list(struct.unpack(">BBH", resp[:4]))
    values[1] = RoutineControlType(values[1])

    # routines according to a defined scope of specs have to provide routine_info
    routine_info = None
    if len(resp) >= 5:
        routine_info = resp[4]
    values.append(routine_info)

    # routines may return data or not, this is the routine_status_record
    routine_status_record = None
    if len(resp) >= 6:
        routine_status_record = resp[5:]
    values.append(routine_status_record)

    return dict(
        zip(["response_sid", "routine_control_type", "routine_id", "routine_info", "routine_status_record"], values))


def concat_read_memory_by_address(addr: int,
                                  size: int,
                                  addr_size_len: Union[str, Tuple[int, int]] = "auto") -> bytes:
    """
    Concat the read memory by address request.

    :param addr: The address to read.
    :type addr int
    :param size: The size to read.
    :type size int
    :param addr_size_len: Byte length used to represent addr and size. Default is "auto".
    :type addr_size_len: Union[Tuple[int, int], str]
    :return: The request message.
    :rtype bytes
    """
    ret = bytearray((ServiceId.ReadMemoryByAddress,))
    ret.extend(concat_alfid_size_addr(addr=addr,
                                      size=size,
                                      addr_size_len=addr_size_len))
    return bytes(ret)


def parse_read_memory_by_address_response(resp: bytes) -> dict:
    """
    Parse read memory by address response.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    return dict(response_sid=resp[0], data=resp[1:])


def concat_write_memory_by_address(addr: int,
                                   data: Union[bytes, bytearray],
                                   size: Union[str, int] = "auto",
                                   addr_size_len: Union[str, Tuple[int, int]] = "auto") -> bytes:
    """
    Concat the write memory by address request.

    :param addr: The address.
    :type addr int
    :param data: The data to be transferred.
    :type data: Union[bytes, bytearray],
    :param size: The size. Default is "auto"
    :type size Union[str, int]
    :param addr_size_len: Byte length used to represent addr and size. Default is "auto".
    :type addr_size_len: Union[Tuple[int, int], str]
    :return: The request message.
    :rtype bytes
    """
    ret = bytearray((ServiceId.WriteMemoryByAddress,))
    if size == "auto":
        size = len(data)
    ret.extend(concat_alfid_size_addr(addr=addr,
                                      size=size,
                                      addr_size_len=addr_size_len))
    ret.extend(data)
    return bytes(ret)


def parse_write_memory_by_address_response(resp: bytes) -> dict:
    """
    Parse write memory by address response.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    ret = dict(response_sid=resp[0])
    ret.update(parse_alfid_content(resp[1:]))
    return ret


def concat_input_output_control(did: int,
                                control_option: IOCtlCommand,
                                control_state: Optional[bytes] = None,
                                enable_mask: Optional[bytes] = None) -> bytes:
    """
    Concat the input output control request.

    :param did: The identifier of the output.
    :type did: int
    :param control_option
    :type control_option: IOCtlCommand
    :param control_state: The control state depending on control_option. Byte Size is also variable. May also be None.
    :type control_state: Optional[bytes]
    :param enable_mask: Some special behaviour which likely nobody uses. Byte Size is also variable. May also be None.
    :type enable_mask: Optional[bytes].
    :return: The request message.
    :rtype bytes
    """
    ret = bytearray((ServiceId.InputOutputByIdentifier,))
    ret.extend(did.to_bytes(2, "big"))
    ret.append(control_option)
    control_state is None or ret.extend(control_state)
    enable_mask is None or ret.extend(enable_mask)
    return bytes(ret)


def parse_input_output_control_response(resp: bytes) -> dict:
    """
    Parse input output control response.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    return dict(response_sid=resp[0], did=int.from_bytes(resp[1:3], "big"),
                control_option=IOCtlCommand(resp[3]),
                control_state=resp[4:])


def concat_link_control(link_control_command: LinkControlType,
                        link_control_parameter: Optional[Union[int, LinkControlModeIdentifier]] = None,
                        suppress_response: bool = False,
                        ) -> bytes:
    """
    Concat the link control request.

    :param link_control_command: The command.
    :type link_control_command LinkControlType
    :param link_control_parameter: An control parameter used in VerifyModeTransitionWithSpecificParameter.
    :type link_control_parameter: int, LinkControlModeIdentifier
    :param suppress_response: Suppress the the positive response.
    :type suppress_response: bool
    :return: The request message.
    :rtype bytes
    """
    stype_byte = link_control_command
    if suppress_response:
        stype_byte = stype_byte | 0x80
    ret = bytearray((ServiceId.LinkControl, stype_byte))
    assert link_control_command != LinkControlType.VerifyModeTransitionWithSpecificParameter \
           or link_control_parameter is not None
    if link_control_command == LinkControlType.VerifyModeTransitionWithSpecificParameter:
        assert link_control_parameter is not None
        ret.extend(link_control_parameter.to_bytes(3, "big"))
    elif link_control_command == LinkControlType.VerifyModeTransitionWithFixedParameter:
        assert isinstance(link_control_parameter, LinkControlModeIdentifier)
        ret.extend(link_control_parameter.to_bytes(1, "big"))

    return bytes(ret)


def parse_link_control_response(resp: bytes) -> dict:
    """
    Parse link control response.

    :param resp: The response message in bytes.
    :return: A dictionary with response specific values.
    """
    return dict(response_sid=resp[0], link_control_command=LinkControlType(resp[1]))


def concat_read_scaling_data_by_identifier(did: int) -> bytes:
    """
    Concat the read scaling data by identifier.

    :param did: The identifier of the output.
    :type did: int
    :return: The request message.
    :rtype bytes
    """
    ret = bytearray((ServiceId.ReadScalingDataByIdentifier,))
    ret.extend(did.to_bytes(2, "big"))
    return bytes(ret)


def parse_formula_constant(data: bytes) -> float:
    """
    Parse a scaling formula constant

    The scaling data is a float squashed into 2 bytes,
    highest 4 bits are the exponent, lower 12 bits are the
    base value mantissa.

    :note: This format is pure trouble for conversion.

    :param data: The byte representation of the constant
    :type data: bytes
    :return: The numeric value.
    :rtype: float
    """
    assert len(data) == 2
    base = int.from_bytes(data, "big")
    mantisse_uint = (base & 0xFFF)
    if mantisse_uint & 0x800:
        mantisse_uint |= 0xF000
    mantisse = int.from_bytes(mantisse_uint.to_bytes(2, "big"), "big", signed=True)

    exp_uint = (base & 0xF000) >> 12
    if exp_uint & 0x8:
        exp_uint |= 0xF0
    exp = int.from_bytes(exp_uint.to_bytes(1, "big"), "big", signed=True)

    return mantisse * 10 ** exp


def parse_state_and_connection(data: bytes) -> dict:
    """
    Parse state and connection scaling extention byte.

    :param data: The scaling data payload.
    :type data: bytes
    :return: A dictionary with response specific values.
    :rtype: dict
    """

    return dict(logical=LogicState(data[0] & 0x7),
                signal=SignalState((data[0] & 0x18) >> 3),
                direction=SignalDirection((data[0] & 0x20) >> 5),
                drive=SignalDrive((data[0] & 0xC0) >> 6),
                )


def parse_scaling_data_payload(data: bytes) -> dict:
    """
    Parse scaling data payload.

    :param data: The scaling data payload.
    :type data: bytes
    :return: A dictionary with response specific values.
    :rtype: dict
    """
    formula_identifier_to_func_mapping = {0: lambda x, c0, c1: (c0 * x) + c1,
                                          1: lambda x, c0, c1: c0 * (x + c1),
                                          2: lambda x, c0, c1, c2: (c0 / (x + c1)) + c2,
                                          3: lambda x, c0, c1: (x / c0) + c1,
                                          4: lambda x, c0, c1: (x + c0) / c1,
                                          5: lambda x, c0, c1, c2: ((x + c0) / c1) + c2,
                                          6: lambda x, c0, c1: c0 * x,
                                          7: lambda x, c0, c1: x / c0,
                                          8: lambda x, c0, c1: x + c0,
                                          9: lambda x, c0, c1: c0 * x / c1,
                                          }

    ret = dict()
    buf = BytesIO(data)
    while scaling_byte := int.from_bytes(buf.read(1), "big"):
        type_ = ScalingDataType(scaling_byte >> 4)
        size_ = scaling_byte & 0xF
        ret.update(dict(type=type_, size=size_, records=list()))
        records = ret.get("records")
        if type_ == ScalingDataType.Formula:
            formula_identifier = int.from_bytes(buf.read(1), "big")
            formula_func = formula_identifier_to_func_mapping.get(formula_identifier)
            constants = dict()
            constants.update({"c0": parse_formula_constant(buf.read(2))})
            constants.update({"c1": parse_formula_constant(buf.read(2))})
            if formula_identifier in [2, 5]:
                constants.update({"c2": parse_formula_constant(buf.read(2))})
            records.append(dict(formula=lambda x: formula_func(x, **constants)))

        elif type_ == ScalingDataType.Bits:
            records.append(dict(validity_mask=int.from_bytes(buf.read(size_), "big")))
        elif type_ == ScalingDataType.Unit:
            unit_ = [ScalingByteUnit(int.from_bytes(buf.read(1), "big"))]
            if 0x40 <= unit_[0] <= 0x4F:
                unit_.append(ScalingByteUnit(int.from_bytes(buf.read(1), "big")))
            records.append(dict(unit=unit_))
        elif type_ == ScalingDataType.State:
            records.append(parse_state_and_connection(buf.read(1)))
    return ret


def parse_read_scaling_data_by_identifier_response(resp: bytes) -> dict:
    """
    Parse read scaling data by identifier response.

    :param resp: The response message in bytes.
    :type resp: bytes
    :return: A dictionary with response specific values.
    :rtype: dict
    """

    return dict(response_sid=resp[0], did=int.from_bytes(resp[1:3], "big"),
                scaling=parse_scaling_data_payload(resp[3:]))


def parse_response(resp: bytes) -> dict:
    """
    A generic function to parse a service response.

    In case of negative response, it raises the appropriate protocol exceptions.
    Otherwise it calls a service specific parser and returns a dictionary with the contents.
    The UDS protocol was not designed properly, so the request is also needed to process the response.
    :param resp: The response bytes.
    :return: A dictionary with response specific values.
    """

    service_to_parser_mapping = {ServiceId.DiagnosticSessionControl: parse_diagnostic_session_control_response,
                                 ServiceId.EcuReset: parse_ecu_reset_response,
                                 ServiceId.ReadDataByIdentifier: parse_read_data_by_id_response,
                                 ServiceId.SecurityAccess: parse_security_access_response,
                                 ServiceId.CommunicationControl: parse_communication_control_response,
                                 ServiceId.TesterPresent: parse_tester_present_response,
                                 ServiceId.ControlDtcSettings: parse_control_dtc_setting_response,
                                 ServiceId.WriteDataByIdentifier: parse_write_data_by_id_response,
                                 ServiceId.RequestDownload: parse_request_download_or_upload_response,
                                 ServiceId.RequestUpload: parse_request_download_or_upload_response,
                                 ServiceId.TransferData: parse_transfer_data_response,
                                 ServiceId.RequestTransferExit: parse_request_transfer_exit_response,
                                 ServiceId.ClearDiagnosticInformation: parse_clear_diagnostic_information_response,
                                 ServiceId.RoutineControl: parse_routine_control_response,
                                 ServiceId.ReadDtcInformation: parse_read_dtc_information_response,
                                 ServiceId.ReadMemoryByAddress: parse_read_memory_by_address_response,
                                 ServiceId.WriteMemoryByAddress: parse_write_memory_by_address_response,
                                 ServiceId.InputOutputByIdentifier: parse_input_output_control_response,
                                 ServiceId.LinkControl: parse_link_control_response,
                                 ServiceId.ReadScalingDataByIdentifier: parse_read_scaling_data_by_identifier_response,
                                 }

    raise_for_exception(resp=resp)
    sid = ServiceId(resp[0] & 0xBF)
    parser_function = service_to_parser_mapping.get(sid)
    ret = {"raw": resp}
    if parser_function is not None and callable(parser_function):
        try:
            ret.update(parser_function(resp))
        except (IndexError, struct.error, AssertionError):
            raise UdsProtocolViolation(
                "Check response for protocol violation {0}".format(resp.hex()))
    return ret


def raise_for_exception(resp: bytes) -> None:
    """
    Raise an exception in case of negative response.

    The exception is mapped to the error code.
    :param resp: The response bytes.
    :return: Nothing.
    """

    if resp[0] == 0x7F:
        assert len(resp) >= 3
        assert resp[0] == 0x7F
        sid = ServiceId(resp[1])
        response_code = ResponseCode(resp[2])
        if response_code != ResponseCode.RequestCorrectlyReceivedButResponsePending:
            LOGGER.error("Service {0} Exception {1}".format(sid.name, response_code.name))
        raise RESPONSE_CODE_TO_EXCEPTION_MAPPING.get(response_code)


# Exceptions from client perspective

class UdsProtocolException(Exception):
    """
    The base exception for UDS
    """
    pass


class UdsProtocolViolation(UdsProtocolException):
    """
    A violation of the UDS protocol. This may be related to invalid length and format of a UDS response.
    It is deployed as a means to raise an error while parsing a response without misleading to the assumption
    that the request was wrong.
    """
    pass


class UdsTimeoutError(UdsProtocolException):
    """
    A (socket/message/protocol) timeout
    """
    pass


class NegativeResponse(UdsProtocolException):
    """
    The base negative response exception
    """
    pass


class GeneralReject(NegativeResponse):
    """
    A default exception.
    """
    pass


class ServiceNotSupported(NegativeResponse):
    """
    An exception that the service is not valid.
    """
    pass


class SubfunctionNotSupported(NegativeResponse):
    """
    An exception that the subfunction byte is not valid.
    """
    pass


class IncorrectMessageLengthOrInvalidFormat(NegativeResponse):
    """
    An exception about wrong data format,
    e.g. The length check in UDS server failed or the Address-Length-Format-Id (ALFID) value is wrong.
    """
    pass


class ResponseTooLong(NegativeResponse):
    """
    An exception about the data length of the response from client to server.
    """
    pass


class BusyRepeatRequest(NegativeResponse):
    """
    An exception that the UDS server is busy with another task.
    """
    pass


class ConditionsNotCorrect(NegativeResponse):
    """
    An exception that conditions in the UDS server are not correct,

    E.g. You try to switch to bootloader while the car is driving.
    The crazy thing is, some ECUs actually do that!
    """
    pass


class RequestSequenceError(NegativeResponse):
    """
    An exception that hints onto some violated logical sequence by the UDS client.

    Typical example would be a request download service and the memory at this location was not erased before.
    You can argue that this is just a stupid excuse for not implementing smart applications but this is common.
    """
    pass


class NoResponseFromSubnetComponent(NegativeResponse):
    """
    An exception that links to routing of diagnostic information,

    e.g. this is reported by a gateway ECU when the subnet service timeouts.
    """
    pass


class FaultPreventsExecutionOfRequestedAction(NegativeResponse):
    """
    An exception that a service is locked / inhibited due to a DTC.

    Typical example is a routine that requires some electrical/functional action and in this case there would be some
    problem with it.
    """
    pass


class RequestOutOfRange(NegativeResponse):
    """
    An exception that hints onto a failed value check inside a service.

    Typical example is read data by id on an invalid / not implemented id.
    """
    pass


class SecurityAccessDenied(NegativeResponse):
    """
    An exception that is raised by any service that requires privileged access.

    Typically write operations require a successful security access prior to execution.
    """
    pass


class InvalidKey(NegativeResponse):
    """
    An exception that is raised by security access service if failed.
    """
    pass


class ExceededNumberOfAttempts(NegativeResponse):
    """
    An exception that a blocking counter has not elapsed.

    Typically happens on failed authentication after 3 (typical) attempts failed.
    This then starts a blocking counter.
    """
    pass


class RequiredTimeDelayNotExpired(NegativeResponse):
    """
    An exception that a blocking counter has not elapsed.

    Typically happens on failed authentication to stretch the time needed for
    brute-forcing a device. The standard time for blocking counter is 5 minutes.
    """
    pass


class UploadDownloadNotAccepted(NegativeResponse):
    """
    An exception that something in the data stream is wrong.
    """
    pass


class TransferDataSuspended(NegativeResponse):
    """
    A server side abort of data block transfer.

    Typically happens on power cycling an ECU.
    """
    pass


class GeneralProgrammingFailure(NegativeResponse):
    """
    Default exception

    in almost every ECU if no specific Exception was set for the error.
    """
    pass


class WrongBlockSequenceCounter(NegativeResponse):
    """
    An exception during data transfer.

    The block number consecutively sent data blocks is out of sync.
    """
    pass


class RequestCorrectlyReceivedButResponsePending(NegativeResponse):
    """
    Request Correctly Received But Response Pending

    UDS protocol abuses this Error Code to change program flow in the socketcan_uds client.
    The Error Code 0x78 basically says, "Reset the timer, I'm still working on it".
    There is no guarantee that there will be an answer at all because this can run forever.
    """
    pass


class SubFunctionNotSupportedInActiveSession(NegativeResponse):
    """
    A subfunction of a service is not supported in the active diagnostic session.
    """
    pass


class ServiceNotSupportedInActiveSession(NegativeResponse):
    """
    A service is not supported in the active diagnostic session.
    """
    pass


RESPONSE_CODE_TO_EXCEPTION_MAPPING = {
    ResponseCode.GeneralReject: GeneralReject,
    ResponseCode.ServiceNotSupported: ServiceNotSupported,
    ResponseCode.SubFunctionNotSupported: SubfunctionNotSupported,
    ResponseCode.IncorrectMessageLengthOrInvalidFormat: IncorrectMessageLengthOrInvalidFormat,
    ResponseCode.ResponseTooLong: ResponseTooLong,
    ResponseCode.BusyRepeatRequest: BusyRepeatRequest,
    ResponseCode.ConditionsNotCorrect: ConditionsNotCorrect,
    ResponseCode.RequestSequenceError: RequestSequenceError,
    ResponseCode.NoResponseFromSubnetComponent: NoResponseFromSubnetComponent,
    ResponseCode.FaultPreventsExecutionOfRequestedAction: FaultPreventsExecutionOfRequestedAction,
    ResponseCode.RequestOutOfRange: RequestOutOfRange,
    ResponseCode.SecurityAccessDenied: SecurityAccessDenied,
    ResponseCode.InvalidKey: InvalidKey,
    ResponseCode.ExceededNumberOfAttempts: ExceededNumberOfAttempts,
    ResponseCode.RequiredTimeDelayNotExpired: RequiredTimeDelayNotExpired,
    ResponseCode.UploadDownloadNotAccepted: UploadDownloadNotAccepted,
    ResponseCode.TransferDataSuspended: TransferDataSuspended,
    ResponseCode.GeneralProgrammingFailure: GeneralProgrammingFailure,
    ResponseCode.WrongBlockSequenceCounter: WrongBlockSequenceCounter,
    ResponseCode.RequestCorrectlyReceivedButResponsePending: RequestCorrectlyReceivedButResponsePending,
    ResponseCode.SubFunctionNotSupportedInActiveSession: SubFunctionNotSupportedInActiveSession,
    ResponseCode.ServiceNotSupportedInActiveSession: ServiceNotSupportedInActiveSession,
}
