""" module:: tests.test_client
    :platform: Posix
    :synopsis: Tests for module socketcan_uds.client
    author:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
import struct

import pytest

from socketcan_uds.client import UdsClient

from tests.mocks import MockSocket
from socketcan_uds.common import UdsProtocolViolation, DtcFormatIdentifier, ScalingByteUnit, ScalingDataType, \
    LinkControlModeIdentifier, UdsTimeoutError, DiagnosticSession, ResetType, ComCtrlType, DtcSettingType, \
    DtcReportType, DtcStatus, RoutineControlType, LinkControlType, IOCtlCommand

import logging

LOGGER = logging.getLogger()


@pytest.fixture
def mock_client() -> UdsClient:
    # noinspection PyTypeChecker
    client = UdsClient(socket=MockSocket())
    yield client


@pytest.fixture
def mock_client_with_fixed_timing() -> UdsClient:
    fixed_session_parameters = \
        {
            "p2_server_max": 1,
            "p2*_server_max": 1,
            "s3_client": 1,
        }
    # noinspection PyTypeChecker
    client = UdsClient(socket=MockSocket(),
                       fixed_timings=fixed_session_parameters,
                       )
    yield client


class TestClient:
    """
    A collection of tests for UdsClient
    """

    def test_obj_generation(self, mock_client, mock_client_with_fixed_timing):
        pass

    def test_service_timeout(self, mock_client):
        with pytest.raises(UdsTimeoutError):
            # there is no answer set in mock for this specific request, so this results in a timeout.
            mock_client.security_access(security_level=0x21)

    def test_diagnostic_session_control(self, mock_client):
        resp = mock_client.diagnostic_session_control(session=DiagnosticSession.ExtendedDiagnosticSession)
        assert resp == {"response_sid": 0x50,
                        "session": DiagnosticSession.ExtendedDiagnosticSession,
                        "p2_server_max": 0.05,
                        "p2*_server_max": 5,
                        "raw": bytes.fromhex("50 03 00 32 01 F4")
                        }

    def test_ecu_reset(self, mock_client):
        mock_client.rx_queue.put(bytes.fromhex("51 01"))  # for coverage only
        resp = mock_client.ecu_reset(rtype=ResetType.HardReset)
        assert resp == {"response_sid": 0x51,
                        "rtype": ResetType.HardReset,
                        "raw": bytes.fromhex("51 01")
                        }

    def test_security_access(self, mock_client):
        resp = mock_client.security_access(security_level=1)
        assert resp == {"response_sid": 0x67,
                        "security_level": 1,
                        "seed": bytes.fromhex("11 22 33 44"),
                        "raw": bytes.fromhex("67 01 11 22 33 44")
                        }
        seed_int = struct.unpack(">I", resp.get("seed"))[0]
        key_bytes = struct.pack(">I", seed_int + 1)
        resp = mock_client.security_access(security_level=2,
                                           key=key_bytes)
        assert resp == {"response_sid": 0x67,
                        "security_level": 2,
                        "raw": bytes.fromhex("67 02")
                        }

        with pytest.raises(ValueError):
            mock_client.security_access(security_level=0xFE)

        with pytest.raises(ValueError):
            mock_client.security_access(security_level=0x100)

        with pytest.raises(ValueError):
            mock_client.security_access(security_level=-1)

    def test_communication_control(self, mock_client):
        resp = mock_client.communication_control(ctrl_type=ComCtrlType.EnableRxDisableTx,
                                                 suppress_response=False)
        assert resp == {"response_sid": 0x68,
                        "ctrl_type": ComCtrlType.EnableRxDisableTx,
                        "raw": bytes.fromhex("68 01"),
                        }

        with pytest.raises(ValueError):
            mock_client.communication_control(ctrl_type=ComCtrlType.EnableRxDisableTx,
                                              node_id=0x4242,
                                              suppress_response=True)

        mock_client.communication_control(ctrl_type=ComCtrlType.EnableRxDisableTx,
                                          com_type=1,
                                          suppress_response=True)

        with pytest.raises(ValueError):
            mock_client.communication_control(ctrl_type=ComCtrlType.EnableRxTxEnhancedAddressInfo,
                                              com_type=1,
                                              suppress_response=True)

        mock_client.communication_control(ctrl_type=ComCtrlType.EnableRxTxEnhancedAddressInfo,
                                          node_id=0x4242,
                                          suppress_response=True)

        mock_client.communication_control(ctrl_type=ComCtrlType.EnableRxTxEnhancedAddressInfo,
                                          com_type=1,
                                          node_id=0x4242,
                                          suppress_response=True)

    def test_tester_present(self, mock_client):
        resp = mock_client.tester_present(suppress_response=False)

        assert resp == {"response_sid": 0x7E,
                        "zerosubfunction": 0,
                        "raw": bytes.fromhex("7E 00"),
                        }

        mock_client.tester_present(suppress_response=True)

    def test_control_dtc_setting(self, mock_client):
        resp = mock_client.control_dtc_setting(stype=DtcSettingType.Off, dtcs=[0, 0xFFFFFF])

        assert resp == {"response_sid": 0xC5,
                        "stype": DtcSettingType.Off,
                        "raw": bytes.fromhex("C5 02"),
                        }

        resp = mock_client.control_dtc_setting(stype=DtcSettingType.On)

        assert resp == {"response_sid": 0xC5,
                        "stype": DtcSettingType.On,
                        "raw": bytes.fromhex("C5 01"),
                        }

        mock_client.control_dtc_setting(stype=DtcSettingType.On, suppress_response=True)

    def test_read_data_by_id(self, mock_client):
        with pytest.raises(ValueError):
            mock_client.read_data_by_id(did=-1)

        with pytest.raises(ValueError):
            mock_client.read_data_by_id(did=0x10000)

        resp = mock_client.read_data_by_id(did=0x4242)
        assert resp == {"response_sid": 0x62,
                        "did": 0x4242,
                        "data": bytes.fromhex("11 22 33 44"),
                        "raw": bytes.fromhex("62 42 42 11 22 33 44"),
                        }

    def test_read_data_by_id_w_delayed_response(self, mock_client):
        resp = mock_client.read_data_by_id(did=0xDEAD)
        assert resp == {"response_sid": 0x62,
                        "did": 0xDEAD,
                        "data": bytes.fromhex("11 22 33 44"),
                        "raw": bytes.fromhex("62 DE AD 11 22 33 44"),
                        }

    def test_read_data_by_id_w_delayed_response_auto_timeout(self, mock_client):
        resp = mock_client.read_data_by_id(did=0xDEAD)
        assert resp == {"response_sid": 0x62,
                        "did": 0xDEAD,
                        "data": bytes.fromhex("11 22 33 44"),
                        "raw": bytes.fromhex("62 DE AD 11 22 33 44"),
                        }

    def test_write_data_by_id(self, mock_client):
        with pytest.raises(ValueError):
            mock_client.write_data_by_id(did=-1,
                                         data=bytes.fromhex("11 22 33 44"))

        with pytest.raises(ValueError):
            mock_client.write_data_by_id(did=0x10000,
                                         data=bytes.fromhex("11 22 33 44"))

        with pytest.raises(ValueError):
            mock_client.write_data_by_id(did=0x4242,
                                         data=bytes(0))

        resp = mock_client.write_data_by_id(did=0x4242,
                                            data=bytes.fromhex("11 22 33 44"))
        assert resp == {"response_sid": 0x6E,
                        "did": 0x4242,
                        "raw": bytes.fromhex("6E 42 42"),
                        }

    def test_request_download(self, mock_client):
        with pytest.raises(ValueError):
            mock_client.request_download(addr=0x11223344,
                                         size=0x12345688,
                                         )

        resp = mock_client.request_download(addr=0x11223344,
                                            size=0x12345678,
                                            )
        assert resp == {"response_sid": 0x74,
                        "max_block_length": 0x87654321,
                        "raw": bytes.fromhex("74 40 87 65 43 21"),
                        }

        resp = mock_client.request_download(addr=0x1122,
                                            size=0x1234,
                                            addr_size_len=(2, 2),
                                            )

    def test_request_upload(self, mock_client):
        resp = mock_client.request_upload(addr=0x11223344,
                                          size=0x12345678,
                                          )
        assert resp == {"response_sid": 0x75,
                        "max_block_length": 0x87654321,
                        "raw": bytes.fromhex("75 40 87 65 43 21"),
                        }

    def test_transfer_data(self, mock_client):
        resp = mock_client.transfer_data(block_sequence_counter=1,
                                         data=bytes.fromhex("11 22 33 44 55 66 77 88"))
        assert resp == {"response_sid": 0x76,
                        "block_sequence_counter": 1,
                        "data": bytes(),
                        "raw": bytes.fromhex("76 01"),
                        }

        resp = mock_client.transfer_data(block_sequence_counter=1,
                                         data=bytes())
        assert resp == {"response_sid": 0x76,
                        "block_sequence_counter": 1,
                        "data": bytes.fromhex("11 22 33 44 55 66 77 88"),
                        "raw": bytes.fromhex("76 01 11 22 33 44 55 66 77 88"),
                        }

    def test_request_transfer_exit(self, mock_client):
        resp = mock_client.request_transfer_exit()
        assert resp == {"response_sid": 0x77,
                        "transfer_request_parameters": bytes(),
                        "raw": bytes.fromhex("77"),
                        }

    def test_clear_diagnostic_information(self, mock_client):
        resp = mock_client.clear_diagnostic_information(dtc_mask=0xFFFF33)
        assert resp == {"response_sid": 0x54,
                        "raw": bytes.fromhex("54"),
                        }

        resp = mock_client.clear_diagnostic_information(dtc_mask=0xFFFF33,
                                                        memory_select=1)
        assert resp == {"response_sid": 0x54,
                        "raw": bytes.fromhex("54"),
                        }

    def test_read_dtc_information(self, mock_client):
        resp = mock_client.read_dtc_information(subfunction=DtcReportType.ReportNumberOfDtcByStatusMask,
                                                status_filter=DtcStatus.TestFailed,
                                                )
        assert resp == {"response_sid": 0x59,
                        "raw": bytes.fromhex("59 01 FF 01 12 34"),
                        "subfunction": DtcReportType.ReportNumberOfDtcByStatusMask,
                        "status_availablitiy": 0xFF,
                        "format_idendifier": DtcFormatIdentifier.ISO_14229_1_DTCFORMAT,
                        "dtc_count": 0x1234
                        }

    def test_routine_control(self, mock_client):
        resp = mock_client.routine_control(routine_control_type=RoutineControlType.StartRoutine,
                                           routine_id=0x1234,
                                           data=bytes.fromhex("11 22 33 44 55 66 77 88"))
        assert resp == {'raw': bytes.fromhex("71 01 12 34 01"),
                        'response_sid': 0x71,
                        'routine_control_type': RoutineControlType.StartRoutine,
                        'routine_id': 0x1234,
                        'routine_info': 1,
                        'routine_status_record': None}

        mock_client.routine_control(routine_control_type=RoutineControlType.StartRoutine,
                                    routine_id=0x1235)

        with pytest.raises(UdsProtocolViolation):
            mock_client.routine_control(routine_control_type=RoutineControlType.StartRoutine,
                                        routine_id=0x1122)

        data = bytes.fromhex("00 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF"
                             " 00 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF")
        mock_client.routine_control(routine_control_type=RoutineControlType.StartRoutine,
                                    routine_id=0x1236, data=data)

    def test_read_memory_by_address(self, mock_client):
        resp = mock_client.read_memory_by_address(addr=0x11223344, size=8, addr_size_len=(4, 2))
        assert resp.get("data") == bytes.fromhex("11 22 33 44 55 66 77 88")

    def test_write_memory_by_address(self, mock_client):
        addr = 0x11223344
        data = bytes.fromhex("11 22 33 44 55 66 77 88")
        resp = mock_client.write_memory_by_address(addr=addr, data=data, addr_size_len=(4, 2))
        assert resp.get("addr") == addr
        assert resp.get("size") == len(data)

    def test_input_output_control(self, mock_client):
        did = 0x9B00  # Air Inlet Position
        control_option = IOCtlCommand.ShortTermAdjustment
        control_state = bytes((60,))
        resp = mock_client.input_output_control(did=did,
                                                control_option=control_option,
                                                control_state=control_state)
        assert resp.get("did") == did
        assert resp.get("control_option") == control_option
        assert resp.get("control_state") == control_state

    def test_link_control(self, mock_client):
        link_control_command = LinkControlType.VerifyModeTransitionWithSpecificParameter
        link_control_parameter = 0x112233
        resp = mock_client.link_control(link_control_command=link_control_command,
                                        link_control_parameter=link_control_parameter,
                                        suppress_response=False)
        assert resp.get("link_control_command") == link_control_command

        mock_client.link_control(link_control_command=LinkControlType.TransitionMode,
                                 suppress_response=True)

        mock_client.link_control(link_control_command=LinkControlType.VerifyModeTransitionWithFixedParameter,
                                 link_control_parameter=LinkControlModeIdentifier.CAN500kBaud,
                                 suppress_response=False)

    def test_read_scaling_data_by_identifier(self, mock_client):
        did = 0x9B00  # Air Inlet Position
        resp = mock_client.read_scaling_data_by_identifier(did=did)
        assert resp == {'did': 0x9B00,
                        'raw': b'd\x9b\x00\xa15',
                        'response_sid': 0x64,
                        'scaling': {'records': [{'unit': [ScalingByteUnit.Percent]}],
                                    'size': 1,
                                    'type': ScalingDataType.Unit}}
