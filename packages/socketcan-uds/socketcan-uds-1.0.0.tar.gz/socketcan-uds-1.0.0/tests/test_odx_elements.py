""" module:: test.tests_odx_elements
    :platform: Posix
    :synopsis: Tests for module socketcan_uds.common
    author:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
from collections.abc import Sequence

import pytest

from socketcan_uds.odx_elements import OdxElement, FlashDataElement, SegmentElement, SecurityElement, DataBlockElement, \
    SessionElement, MemElement, EcuMemElement, generate_short_name_from_long_name, ExpectedIdentElement, OwnIdentElement
from xml.etree import ElementTree as ET


@pytest.fixture()
def flashdata_mock() -> FlashDataElement:
    yield FlashDataElement(id_="some.path.some_name",
                           short_name="SOME_FICTIONAL_NAME",
                           long_name="some fictional long name",
                           dataformat="BINARY",
                           encrypt_compress_method=b"00",
                           data=bytes(range(64)),
                           )


@pytest.fixture()
def flashdatas_mock(flashdata_mock) -> Sequence[FlashDataElement]:
    size = 5
    yield [flashdata_mock for x in range(size)]


@pytest.fixture()
def segment_mock() -> SegmentElement:
    yield SegmentElement(id_="some.path.some_name",
                         short_name="SOME_FICTIONAL_NAME",
                         long_name="some fictional long name",
                         source_start_address=0x12345678,
                         compressed_size=12345678,
                         uncompressed_size=12345678,
                         )


@pytest.fixture()
def segments_mock(segment_mock) -> Sequence[SegmentElement]:
    size = 5
    yield [segment_mock for x in range(size)]

@pytest.fixture()
def own_ident_mock() -> OwnIdentElement:
    yield OwnIdentElement(long_name="SomeName", value="SomeValue")

@pytest.fixture()
def own_idents_mock(own_ident_mock) -> Sequence[OwnIdentElement]:
    size = 5
    yield [own_ident_mock for x in range(size)]

@pytest.fixture()
def datablock_mock(segments_mock) -> DataBlockElement:
    yield DataBlockElement(id_="some.path.some_name",
                           short_name="SOME_FICTIONAL_NAME",
                           long_name="some fictional long name",
                           flashdata_ref="some_ref",
                           segments=segments_mock,
                           block_type="FLASH_DATA")


@pytest.fixture()
def datablocks_mock(datablock_mock) -> Sequence[DataBlockElement]:
    size = 5
    yield [datablock_mock for x in range(size)]


@pytest.fixture()
def security_mock() -> SecurityElement:
    yield SecurityElement(security_method="ALFID",
                          fw_signature=bytes.fromhex("01412004"))


@pytest.fixture()
def securitys_mock(security_mock) -> Sequence[SecurityElement]:
    size = 5
    yield [security_mock for x in range(size)]


@pytest.fixture()
def expected_ident_mock() -> ExpectedIdentElement:
    yield ExpectedIdentElement(long_name="SomeName", values=["SomeValue"])


@pytest.fixture()
def expected_idents_mock(expected_ident_mock) -> Sequence[ExpectedIdentElement]:
    size = 5
    yield [expected_ident_mock for x in range(size)]


@pytest.fixture()
def session_mock(securitys_mock, datablockrefs_mock, expected_idents_mock) -> SessionElement:
    yield SessionElement(id_="some.path.some_name",
                         short_name="SOME_FICTIONAL_NAME",
                         long_name="some fictional long name",
                         securitys=securitys_mock,
                         datablockrefs=datablockrefs_mock,
                         expected_idents=expected_idents_mock,
                         )


@pytest.fixture()
def datablockrefs_mock() -> dict:
    yield {"ID-REF": "some.path.some_name"}


@pytest.fixture()
def mem_mock(session_mock, flashdatas_mock, datablocks_mock) -> MemElement:
    yield MemElement(session=session_mock,
                     flashdatas=flashdatas_mock,
                     datablocks=datablocks_mock)


class TestOdxElements:
    def test_odx_element(self):
        e = OdxElement(id_="some.path.some_name",
                       short_name="SOME_FICTIONAL_NAME",
                       long_name="some fictional long name")
        elem = e.to_element()
        e_str_repr = ET.tostring(element=elem)
        # print(e_str_repr)
        new_e = OdxElement.from_element(elem)
        assert new_e.id == e.id
        assert new_e.short_name == e.short_name
        assert new_e.long_name == e.long_name

    def test_flashdata_element(self):
        data = bytes(range(64))
        e = FlashDataElement(id_="some.path.some_name",
                             short_name="SOME_FICTIONAL_NAME",
                             long_name="some fictional long name",
                             dataformat="BINARY",
                             encrypt_compress_method=b"00",
                             data=data,
                             )
        elem = e.to_element()
        e_str_repr = ET.tostring(element=elem)
        # print(e_str_repr)
        new_e = FlashDataElement.from_element(elem)
        assert new_e.id == e.id
        assert new_e.short_name == e.short_name
        assert new_e.long_name == e.long_name
        assert new_e.dataformat == e.dataformat
        assert new_e.encrypt_compress_method == e.encrypt_compress_method
        assert new_e.data == e.data

    def test_flashdata_datafile_element(self):
        datafile = "SOME_FILE"
        e = FlashDataElement(id_="some.path.some_name",
                             short_name="SOME_FICTIONAL_NAME",
                             long_name="some fictional long name",
                             dataformat="BINARY",
                             encrypt_compress_method=b"00",
                             datafile=datafile,
                             )
        elem = e.to_element()
        e_str_repr = ET.tostring(element=elem)
        # print(e_str_repr)
        new_e = FlashDataElement.from_element(elem)
        assert new_e.id == e.id
        assert new_e.short_name == e.short_name
        assert new_e.long_name == e.long_name
        assert new_e.dataformat == e.dataformat
        assert new_e.encrypt_compress_method == e.encrypt_compress_method
        assert new_e.datafile == e.datafile

    def test_datablock_element(self, segments_mock, own_idents_mock):
        e = DataBlockElement(id_="some.path.some_name",
                             short_name="SOME_FICTIONAL_NAME",
                             long_name="some fictional long name",
                             flashdata_ref="some_ref",
                             block_type="FLASH_DATA",
                             segments=segments_mock,
                             own_idents=own_idents_mock,
                             )
        elem = e.to_element()
        e_str_repr = ET.tostring(element=elem)
        print(e_str_repr)
        new_e = DataBlockElement.from_element(elem)
        assert new_e.id == e.id
        assert new_e.short_name == e.short_name
        assert new_e.long_name == e.long_name
        assert len(new_e.segments) == len(segments_mock)
        assert len(new_e.own_idents) == len(own_idents_mock)

    def test_datablock_with_security_element(self, segments_mock, securitys_mock):
        e = DataBlockElement(id_="some.path.some_name",
                             short_name="SOME_FICTIONAL_NAME",
                             long_name="some fictional long name",
                             flashdata_ref="some_ref",
                             block_type="FLASH_DATA",
                             segments=segments_mock,
                             securitys=securitys_mock)
        elem = e.to_element()
        e_str_repr = ET.tostring(element=elem)
        # print(e_str_repr)
        new_e = DataBlockElement.from_element(elem)
        assert new_e.id == e.id
        assert new_e.short_name == e.short_name
        assert new_e.long_name == e.long_name
        assert len(new_e.segments) == len(segments_mock)
        assert len(new_e.securitys) == len(securitys_mock)

    def test_segment_element(self):
        e = SegmentElement(id_="some.path.some_name",
                           short_name="SOME_FICTIONAL_NAME",
                           long_name="some fictional long name",
                           source_start_address=0x12345678,
                           compressed_size=12345678,
                           uncompressed_size=12345678,
                           )
        elem = e.to_element()
        e_str_repr = ET.tostring(element=elem)
        # print(e_str_repr)
        new_e = SegmentElement.from_element(elem)
        assert new_e.id == e.id
        assert new_e.short_name == e.short_name
        assert new_e.long_name == e.long_name
        assert new_e.source_start_address == e.source_start_address
        assert new_e.compressed_size == e.compressed_size
        assert new_e.uncompressed_size == e.uncompressed_size

    def test_security_element(self):
        e = SecurityElement(security_method="SOME_METHOD",
                            fw_signature=bytes(range(128)),
                            fw_checksum=bytes(range(4)),
                            validity_for="SOME_BLOCK"
                            )
        elem = e.to_element()
        e_str_repr = ET.tostring(element=elem)
        # print(e_str_repr)
        new_e = SecurityElement.from_element(elem)
        assert new_e.security_method == e.security_method
        assert new_e.fw_signature == e.fw_signature
        assert new_e.fw_checksum == e.fw_checksum
        assert new_e.validity_for == e.validity_for

    def test_expected_ident_element(self):
        e = ExpectedIdentElement(long_name="Some Name", values=["Some Value"])
        elem = e.to_element()
        e_str_repr = ET.tostring(element=elem)
        # print(e_str_repr)
        new_e = ExpectedIdentElement.from_element(elem)
        assert new_e.values == e.values

    def test_own_ident_element(self):
        e = OwnIdentElement(long_name="Some Name", value="Some Value")
        elem = e.to_element()
        e_str_repr = ET.tostring(element=elem)
        # print(e_str_repr)
        new_e = OwnIdentElement.from_element(elem)
        assert new_e.value == e.value

    def test_mem_element(self, datablocks_mock, flashdatas_mock, session_mock):
        e = MemElement(datablocks=datablocks_mock, flashdatas=flashdatas_mock, session=session_mock)
        elem = e.to_element()
        e_str_repr = ET.tostring(element=elem)
        # print(e_str_repr)
        new_e = MemElement.from_element(elem)
        assert new_e.id == e.id
        assert new_e.short_name == e.short_name
        assert new_e.long_name == e.long_name
        assert len(new_e.datablocks) == len(datablocks_mock)

    def test_ecu_mem_element(self, mem_mock):
        e = EcuMemElement(id_="some.path.some_name",
                          short_name="SOME_FICTIONAL_NAME",
                          long_name="some fictional long name",
                          mem=mem_mock,
                          desc="Some description of whatever sense",
                          )

        elem = e.to_element()
        e_str_repr = ET.tostring(element=elem)
        # print(e_str_repr)
        new_e = EcuMemElement.from_element(elem)
        assert new_e.id == e.id
        assert new_e.short_name == e.short_name
        assert new_e.long_name == e.long_name


class TestUtils:

    @pytest.mark.parametrize("value, expected", [
        ("hello world", "HelloWorld"),
        ("hello 12345", "Hello12345"),
        ("hello _12345", "Hello_1234"),
        ("some very loooong name", "SomeVeryLooooName"),
        ("hello _World", "Hello_Worl"),
    ])
    def test_generate_short_name_from_long_name(self,
                                                value: str,
                                                expected: str):
        assert generate_short_name_from_long_name(value) == expected
