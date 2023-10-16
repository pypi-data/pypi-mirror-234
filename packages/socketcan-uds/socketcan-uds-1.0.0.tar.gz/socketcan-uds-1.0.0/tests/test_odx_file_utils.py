""" module:: socketcan_uds.test_odx_file_parser
    :platform: Posix
    :synopsis: Tests for odx_file_parser content
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
from pathlib import Path

import pytest

from socketcan_uds.odx_elements import EcuMemElement, SecurityElement, SessionElement, MemElement
from socketcan_uds.odx_file_utils import parse_index_xml, parse_odx, create_index_xml, alfid_dict_to_alfid_bytes, find_sa2


@pytest.fixture
def index_xml():
    idx_file = list(Path(".").glob("**/data/index.xml"))[0]
    yield idx_file


@pytest.fixture
def flash_odx() -> Path:
    yield list(Path(".").glob("**/data/example_flash_odx.odx"))[0]


@pytest.fixture
def flash_pdx_odx() -> Path:
    yield list(Path(".").glob("**/data/example_flash_pdx.odx"))[0]


@pytest.fixture
def flash_odx_bytes(flash_odx):
    with flash_odx.open("rb") as fp:
        yield fp


@pytest.fixture
def pdx_file_mock() -> Path:
    yield list(Path(".").glob("**/data/*.pdx"))[0]


class TestBasicParsers:

    def test_index_file_parser(self, tmp_path, index_xml):
        index_dict = parse_index_xml(index_xml)
        print(index_dict)
        p = tmp_path / "test_write_index.xml"
        short_name = index_dict.get("short_name")
        version = index_dict.get("version")
        ablocks = index_dict.get("ablocks")
        create_index_xml(index_file=p,
                         data_files=ablocks,
                         version=version,
                         short_name=short_name
                         )

    def test_parse_odx(self, flash_odx_bytes):
        odx_obj = parse_odx(flash_odx_bytes)
        assert odx_obj.get("model_version")
        print(odx_obj)


class TestUtils:

    def test_alfid_dict_to_alfid_bytes(self):
        data = {"routine_control": (2, 4),
                }
        result = alfid_dict_to_alfid_bytes(data)
        assert result == bytes.fromhex("42")

    def test_find_sa2(self):
        security = SecurityElement(security_method="SA2",
                                   fw_signature=bytes.fromhex("01412004"))
        session = SessionElement(id_="some.path.some_name",
                                 short_name="SOME_FICTIONAL_NAME",
                                 long_name="some fictional long name",
                                 securitys=[security, ],
                                 datablockrefs=[],
                                 expected_idents=[],
                                 )
        mem = MemElement(session=session,
                         flashdatas=[],
                         datablocks=[])

        ecu_mem = EcuMemElement(id_="some.path.some_name",
                                short_name="SOME_FICTIONAL_NAME",
                                long_name="some fictional long name",
                                mem=mem,
                                desc="Some description of whatever sense",
                                )
        result = find_sa2(ecu_mem)
        assert result == bytes.fromhex("01412004")
