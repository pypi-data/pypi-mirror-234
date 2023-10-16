""" module:: test.tests_common
    :platform: Posix
    :synopsis: Tests for module socketcan_uds.common
    author:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
from collections import OrderedDict
from random import choice

import pytest

from socketcan_uds.common import concat_request_download_or_upload_request, RESPONSE_CODE_TO_EXCEPTION_MAPPING, ServiceId, \
    raise_for_exception, dtc_bytes_to_int, int_to_dtc_bytes, parse_diagnostic_session_control_response, \
    parse_communication_control_response, DiagnosticSession, parse_ecu_reset_response, parse_ecu_reset_response, \
    parse_security_access_response, ComCtrlType, parse_read_data_by_id_response, ResetType, parse_response, \
    CompressionMethod, EncryptionMethod, concat_read_dtc_information_request, DtcReportType, DtcReadinessGroup, \
    DtcStatus, \
    DtcSeverety, DtcFunctionalGroup, split_records_by_index, split_by_number_of_elems, dtc_values_record_to_dict, \
    parse_read_dtc_information_response, DtcFormatIdentifier, parse_formula_constant, parse_scaling_data_payload, \
    ScalingDataType, ScalingByteUnit, SignalDirection, SignalDrive, LogicState, SignalState

import logging

LOGGER = logging.getLogger()


class TestExceptions:
    """
    A collection of tests for exceptions.
    """

    def test_negative_responses(self):
        for code, e in RESPONSE_CODE_TO_EXCEPTION_MAPPING.items():
            with pytest.raises(e):
                raise_for_exception(resp=bytes((0x7F, ServiceId(choice([sid.value for sid in ServiceId])), code)))

    def test_positive_responses(self):
        for sid in ServiceId:
            raise_for_exception(resp=bytes(((sid | 0x40),)))


class TestHelpers:
    """
    A collection of tests for helper functions
    """

    def test_int_to_dtc_mask(self):
        x = 0xFFFFFF
        result = int_to_dtc_bytes(x)
        assert len(result) == 3
        assert result == bytes.fromhex("FF FF FF")

    def test_dtc_mask_to_int(self):
        x = bytes.fromhex("FF FF FF")
        result = dtc_bytes_to_int(x)
        assert 0 <= result < 0x1000000
        assert result == 0xFFFFFF


class TestParseResponses:
    """
    A collection of tests for parsing responses
    """

    def test_parse_diagnostic_session_control_response(self):
        resp = bytes.fromhex("50 03 00 32 01 F4")  # common answer from any ECU
        data = parse_diagnostic_session_control_response(resp=resp)
        assert data == {"response_sid": 0x50,
                        "session": DiagnosticSession.ExtendedDiagnosticSession,
                        "p2_server_max": 0.05,
                        "p2*_server_max": 5,
                        }

    def test_parse_ecu_reset_response(self):
        resp = bytes.fromhex("51 01")
        data = parse_ecu_reset_response(resp=resp)
        assert data == {"response_sid": 0x51,
                        "rtype": ResetType.HardReset,
                        }

    def test_parse_ecu_reset_response_w_shutdown(self):
        resp = bytes.fromhex("51 04 64")
        data = parse_ecu_reset_response(resp=resp)
        assert data == {"response_sid": 0x51,
                        "rtype": ResetType.EnableRapidPowerShutdown,
                        "power_down_time": 100,
                        }

    def test_parse_security_access_response_seed(self):
        resp = bytes.fromhex("67 01 11 22 33 44")
        data = parse_security_access_response(resp=resp)
        assert data == {"response_sid": 0x67,
                        "security_level": 1,
                        "seed": bytes.fromhex("11 22 33 44"),
                        }

    def test_parse_security_access_response_key(self):
        resp = bytes.fromhex("67 02")
        data = parse_security_access_response(resp=resp)
        assert data == {"response_sid": 0x67,
                        "security_level": 2,
                        }

    def test_parse_communication_control_response(self):
        resp = bytes.fromhex("68 01")
        data = parse_communication_control_response(resp=resp)
        assert data == {"response_sid": 0x68,
                        "ctrl_type": ComCtrlType.EnableRxDisableTx,
                        }

        resp = bytes.fromhex("68 81")
        with pytest.raises(ValueError):
            parse_communication_control_response(resp=resp)

    def test_parse_read_data_by_id_response(self):
        resp = bytes.fromhex("62 42 42 11 22 33 44")
        data = parse_read_data_by_id_response(resp=resp)
        assert data == {"response_sid": 0x62,
                        "did": 0x4242,
                        "data": bytes.fromhex("11 22 33 44"),
                        }

    def test_parse_response(self):
        raw_responses = [bytes.fromhex("50 03 00 32 01 F4"),
                         bytes.fromhex("51 01"),
                         bytes.fromhex("51 04 64"),
                         bytes.fromhex("67 01 11 22 33 44"),
                         bytes.fromhex("67 02"),
                         bytes.fromhex("62 42 42 11 22 33 44"),
                         bytes.fromhex("68 01"),
                         ]
        exp_responses = [{"response_sid": 0x50,
                          "session": DiagnosticSession.ExtendedDiagnosticSession,
                          "p2_server_max": 0.05,
                          "p2*_server_max": 5,
                          },
                         {"response_sid": 0x51,
                          "rtype": ResetType.HardReset,
                          },
                         {"response_sid": 0x51,
                          "rtype": ResetType.EnableRapidPowerShutdown,
                          "power_down_time": 100,
                          },
                         {"response_sid": 0x67,
                          "security_level": 1,
                          "seed": bytes.fromhex("11 22 33 44"),
                          },
                         {"response_sid": 0x67,
                          "security_level": 2,
                          },
                         {"response_sid": 0x62,
                          "did": 0x4242,
                          "data": bytes.fromhex("11 22 33 44"),
                          },
                         {"response_sid": 0x68,
                          "ctrl_type": ComCtrlType.EnableRxDisableTx,
                          },
                         ]
        for resp, data in zip(raw_responses, exp_responses):
            req = bytes((resp[0] & 0xBF,))
            LOGGER.debug(req)
            parsed = parse_response(resp=resp)
            raw = parsed.pop("raw")
            assert raw == resp
            assert data == parsed

    @pytest.mark.parametrize("addr,size,expected", [(0x1234, 0x1234, bytes.fromhex("34002212341234")),
                                                    (0x1234, 0x8, bytes.fromhex("340012123408")),
                                                    (0x11223344, 0x1234, bytes.fromhex("340024112233441234")),
                                                    ])
    def test_concat_request_download_or_upload_request(self, addr, size, expected):
        result = concat_request_download_or_upload_request(service_id=ServiceId.RequestDownload,
                                                           addr=addr,
                                                           size=size,
                                                           compression_method=CompressionMethod.NO_COMPRESSION,
                                                           encryption_method=EncryptionMethod.NO_ENCRYPTION)
        LOGGER.info(result.hex())
        assert result == expected

    @pytest.mark.parametrize("sub_fct,args,expected", [
        (DtcReportType.ReportDtcSnapshotIdentification,
         {"group_filter": 0xFFFFFF,
          "record_filter": 1},
         bytearray.fromhex("19 03 ff ff ff 01")),
        (DtcReportType.ReportWwhobdDtcByMaskRecord,
         {"group_filter": DtcFunctionalGroup.VOBD,
          "status_filter": DtcReadinessGroup.ComprehensiveComponentsMonitoring},
         bytearray.fromhex("19 42 fe 01")),
        (DtcReportType.ReportUserDefMemoryDtcByStatusMask,
         {"status_filter": DtcStatus.TestFailed,
          "memory_select": 1},
         bytearray.fromhex("19 17 01 01")),
        (DtcReportType.ReportDtcBySeverityMaskRecord,
         {"status_filter": DtcSeverety.DtcClass2},
         bytearray.fromhex("19 08 04")),
    ])
    def test_concat_read_dtc_information_request(self, sub_fct, args, expected):
        result = concat_read_dtc_information_request(subfunction=sub_fct, **args)
        LOGGER.info(result.hex())
        assert result == expected

    @pytest.mark.parametrize("data,expected",
                             [
                                 (bytes.fromhex("01 11 22 33 44 55 02 11 22 33 44 55"),
                                  [bytes.fromhex("01 11 22 33 44 55"),
                                   bytes.fromhex("02 11 22 33 44 55")]),
                                 (bytes.fromhex("01 11 02 22 03 44 04 55"),
                                  [bytes.fromhex("01 11"),
                                   bytes.fromhex("02 22"),
                                   bytes.fromhex("03 44"),
                                   bytes.fromhex("04 55")]),
                             ])
    def test_split_records_by_index(self, data, expected):
        result = split_records_by_index(data=data)
        assert result == expected

    @pytest.mark.parametrize("data,expected",
                             [
                                 (bytes.fromhex("02 11 22 33 44 55 11 22 33 44 55"),
                                  [bytes.fromhex("11 22 33 44 55"),
                                   bytes.fromhex("11 22 33 44 55")]),
                                 (bytes.fromhex("04 11 22 44 55"),
                                  [bytes.fromhex("11"),
                                   bytes.fromhex("22"),
                                   bytes.fromhex("44"),
                                   bytes.fromhex("55")]),
                             ])
    def test_split_by_number_of_elems(self, data, expected):
        result = split_by_number_of_elems(data=data)
        assert result == expected

    @pytest.mark.parametrize("data,expected",
                             [
                                 (bytes.fromhex("02 11 22 33 44 55 11 23 33 44 55"),
                                  {0x1122: bytes.fromhex("33 44 55"),
                                   0x1123: bytes.fromhex("33 44 55"),
                                   }),
                             ])
    def test_dtc_values_record_to_dict(self, data, expected):
        result = dtc_values_record_to_dict(data=data)
        assert result == expected

    @pytest.mark.parametrize("data,expected",
                             [
                                 (bytes.fromhex("59 01 FF 01 12 34"),
                                  {"response_sid": 0x59,
                                   "subfunction": DtcReportType.ReportNumberOfDtcByStatusMask,
                                   "status_availablitiy": 0xFF,
                                   "format_idendifier": DtcFormatIdentifier.ISO_14229_1_DTCFORMAT,
                                   "dtc_count": 0x1234
                                   }),
                                 (bytes.fromhex("59 02 FF 11 22 33 01"),
                                  {"response_sid": 0x59,
                                   "subfunction": DtcReportType.ReportDtcByStatusMask,
                                   "status_availablitiy": 0xFF,
                                   "records": {0x112233: 1}
                                   }),
                                 (bytes.fromhex("59 03 11 22 33 01"),
                                  {"response_sid": 0x59,
                                   "subfunction": DtcReportType.ReportDtcSnapshotIdentification,
                                   "records": {0x112233: 1}
                                   }),
                                 (bytes.fromhex("59 04 11 22 33 01 01 02 11 22 33 44 55 11 23 33 44 55"),
                                  {"response_sid": 0x59,
                                   "subfunction": DtcReportType.ReportDtcSnapshotByDtcNumber,
                                   "dtc": 0x112233,
                                   "dtc_status": DtcStatus.TestFailed,
                                   "records": OrderedDict({1: {0x1122: bytes.fromhex("33 44 55"),
                                                               0x1123: bytes.fromhex("33 44 55")
                                                               }})
                                   }),
                                 (bytes.fromhex("59 05 01 11 22 33 01 01 11 22 33 44"),
                                  {"response_sid": 0x59,
                                   "subfunction": DtcReportType.ReportDtcStoredDataByRecordNumber,
                                   "records": OrderedDict({0x112233: {"dtc_status": DtcStatus.TestFailed,
                                                                      "values": {0x1122: bytes.fromhex("33 44")}}
                                                           })
                                   }),
                                 (bytes.fromhex("59 06 11 22 33 01 01 11 22 33 44 02 55 66 77 88"),
                                  {"response_sid": 0x59,
                                   "subfunction": DtcReportType.ReportDtcExtDataRecordByDtcNumber,
                                   "dtc_status": DtcStatus.TestFailed,
                                   "dtc": 0x112233,
                                   "ext_data": [bytes.fromhex("01 11 22 33 44"),
                                                bytes.fromhex("02 55 66 77 88"),
                                                ],
                                   }),
                                 (bytes.fromhex("59 09 01 01 11 22 33 01"),
                                  {"response_sid": 0x59,
                                   "subfunction": DtcReportType.ReportSeverityInformationOfDtc,
                                   "records": {0x112233: {"dtc_status": DtcStatus.TestFailed,
                                                          "severety": 1,
                                                          "functional_unit": 1}
                                               }
                                   }),

                                 (bytes.fromhex("59 14 11 22 33 01"),
                                  {"response_sid": 0x59,
                                   "subfunction": DtcReportType.ReportDtcFaultDetectionCounter,
                                   "records": {0x112233: 1}
                                   }),

                                 (bytes.fromhex("59 16 02 11 22 33 01 11 22 33 11 22 34 01 44 55 66"),
                                  {"response_sid": 0x59,
                                   "subfunction": DtcReportType.ReportDtcExtDataRecordByRecordNumber,
                                   "records": {0x112233: {"dtc_status": 1,
                                                          "ext_data": bytes.fromhex("11 22 33")},
                                               0x112234: {"dtc_status": 1,
                                                          "ext_data": bytes.fromhex("44 55 66")},
                                               }
                                   }),

                                 (bytes.fromhex("59 17 01 01 11 22 33 01 11 22 34 01"),
                                  {"response_sid": 0x59,
                                   "memory_select": 1,
                                   "status_availability": 1,
                                   "subfunction": DtcReportType.ReportUserDefMemoryDtcByStatusMask,
                                   "records": OrderedDict({0x112233: DtcStatus.TestFailed,
                                                           0x112234: DtcStatus.TestFailed,
                                                           })
                                   }),
                                 (bytes.fromhex("59 18 01 11 22 33  01 02 11 22 33 44 55 66"),
                                  {"response_sid": 0x59,
                                   "memory_select": 1,
                                   "dtc": 0x112233,
                                   "subfunction": DtcReportType.ReportUserDefMemoryDtcSnapshotRecordByDtcNumber,
                                   "records": OrderedDict({1: {0x1122: b"\x33",
                                                               0x4455: b"\x66",
                                                               }})
                                   }),
                                 (bytes.fromhex("59 19 01 11 22 33 01 01 11 22 33 02 44 55 66"),
                                  {"response_sid": 0x59,
                                   "memory_select": 1,
                                   "dtc": 0x112233,
                                   "dtc_status": DtcStatus.TestFailed,
                                   "subfunction": DtcReportType.ReportUserDefMemoryDtcExtDataRecordByDtcNumber,
                                   "ext_data": [bytes.fromhex("01 11 22 33"),
                                                bytes.fromhex("02 44 55 66")]
                                   }),

                                 (bytes.fromhex("59 1A 01 02   11 22 33 01   11 22 34 01"),
                                  {"response_sid": 0x59,
                                   "status_availability": 1,
                                   "subfunction": DtcReportType.ReportSupportedDtcExtDataRecord,
                                   "records": OrderedDict({0x112233: DtcStatus.TestFailed,
                                                           0x112234: DtcStatus.TestFailed,
                                                           })
                                   }),
                                 (bytes.fromhex("59 42 FE 01 01 01   01 11 22 33 01   01 11 22 34 01"),
                                  {"response_sid": 0x59,
                                   "functional_group": DtcFunctionalGroup.VOBD,
                                   "severity_availability": 1,
                                   "dtc_format_identifier": DtcFormatIdentifier.ISO_14229_1_DTCFORMAT,
                                   "status_availability": 1,
                                   "subfunction": DtcReportType.ReportWwhobdDtcByMaskRecord,
                                   "records": OrderedDict({0x112233: {"dtc_status": DtcStatus.TestFailed,
                                                                      "severity": DtcSeverety.DtcClass0},
                                                           0x112234: {"dtc_status": DtcStatus.TestFailed,
                                                                      "severity": DtcSeverety.DtcClass0},
                                                           })
                                   }),

                                 (bytes.fromhex("59 55 FE 01 01   11 22 33 01   11 22 34 01"),
                                  {"response_sid": 0x59,
                                   "functional_group": DtcFunctionalGroup.VOBD,
                                   "dtc_format_identifier": DtcFormatIdentifier.ISO_14229_1_DTCFORMAT,
                                   "status_availability": 1,
                                   "subfunction": DtcReportType.ReportWwhobdDtcWithPermanentStatus,
                                   "records": OrderedDict({0x112233: DtcStatus.TestFailed,
                                                           0x112234: DtcStatus.TestFailed,
                                                           })
                                   }),

                                 (bytes.fromhex("59 56 FE 01 01 01  11 22 33 01   11 22 34 01"),
                                  {"response_sid": 0x59,
                                   "functional_group": DtcFunctionalGroup.VOBD,
                                   "dtc_format_identifier": DtcFormatIdentifier.ISO_14229_1_DTCFORMAT,
                                   "status_availability": 1,
                                   "readiness_group_identifier": DtcReadinessGroup.ComprehensiveComponentsMonitoring,
                                   "subfunction": DtcReportType.ReportDtcInformationByDtcReadinessGroupIdentifier,
                                   "records": OrderedDict({0x112233: DtcStatus.TestFailed,
                                                           0x112234: DtcStatus.TestFailed,
                                                           })
                                   }),

                             ])
    def test_parse_read_dtc_information_response(self, data, expected):
        result = parse_read_dtc_information_response(resp=data)
        assert result == expected

    @pytest.mark.parametrize("data,expected",
                             [(bytes.fromhex("00 01"), 1),
                              (bytes.fromhex("0F FF"), -1),
                              (bytes.fromhex("FF FF"), -0.1),
                              ])
    def test_parse_formula_constant(self, data, expected):
        assert parse_formula_constant(data) == expected

    def test_parse_scaling_data_payload_formula(self):
        data = bytes.fromhex("91 05 00 01 00 01 00 01")  # easiest function (x+1 / 1) + 1
        result = parse_scaling_data_payload(data=data)
        assert result.get("size") == 1
        assert result.get("type") == ScalingDataType.Formula
        func = result.get("records")[0].get("formula")
        assert callable(func)
        for i in range(100):  # proof that function results in this function
            assert func(i) == i + 2

    def test_parse_scaling_data_payload_bitmask(self):
        data = bytes.fromhex("22 FF FF")
        result = parse_scaling_data_payload(data=data)
        assert result == {'records': [{'validity_mask': 65535}],
                          'size': 2,
                          'type': ScalingDataType.Bits}

    def test_parse_scaling_data_payload_unit(self):
        data = bytes.fromhex("A2 4A 0E")  # 2 bytes mV
        result = parse_scaling_data_payload(data=data)
        assert result == {'records': [{'unit': [ScalingByteUnit.Milli,
                                                ScalingByteUnit.Volt]}],
                          'size': 2,
                          'type': ScalingDataType.Unit}

    def test_parse_scaling_data_payload_state(self):
        data = bytes.fromhex("51 20")
        result = parse_scaling_data_payload(data=data)
        assert result == {'records': [{'direction': SignalDirection.Output,
                                       'drive': SignalDrive.Internal,
                                       'logical': LogicState.NotActive,
                                       'signal': SignalState.Low}],
                          'size': 1,
                          'type': ScalingDataType.State}
