""" module:: test.tests_program_file
    :platform: Posix
    :synopsis: Tests for module socketcan_uds.common
    author:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
import logging
from pathlib import Path
from copy import copy
import pytest

from socketcan_uds.program_file import UpdateContainerOdxFile, PackedUpdateContainer

LOGGER = logging.getLogger()


@pytest.fixture
def flash_odx() -> Path:
    yield list(Path(".").glob("**/data/example_flash_odx.odx"))[0]


@pytest.fixture
def flash_pdx_odx() -> Path:
    yield list(Path(".").glob("**/data/example_flash_pdx.odx"))[0]


@pytest.fixture
def packed_update_container_filepath_mock() -> Path:
    yield list(Path(".").glob("**/data/test_pdx.pdx"))[0]


class TestProgrammFiles:

    def test_flash_odx_file(self, flash_odx, tmp_path):
        odx = UpdateContainerOdxFile(flash_odx)
        alfid = odx.get_address_and_length_format_identifier()
        assert isinstance(alfid, dict)
        blocks = odx.get_blocks()
        assert blocks
        print(blocks)
        expected_idents = odx.get_expected_idents()
        assert expected_idents
        print(expected_idents)

        own_idents = odx.get_own_idents()
        assert own_idents
        print(own_idents)

        p = tmp_path / "test_write_flash_pdx.odx"
        odx._write_file(p)

        p = tmp_path / "test_write_flash_odx.odx"
        odx._write_file(filepath=p, format_flash_pdx=True)

    def test_flash_pdx_odx_file(self, flash_pdx_odx):
        odx = UpdateContainerOdxFile(flash_pdx_odx)
        alfid = odx.get_address_and_length_format_identifier()
        assert isinstance(alfid, dict)
        blocks = odx.get_blocks()
        assert blocks
        print(blocks)
        expected_idents = odx.get_expected_idents()
        assert expected_idents
        print(expected_idents)

        odx_copy = copy(odx)
        block_copy = odx_copy.get_blocks()
        first_block_copy = list(block_copy.keys())[0]
        first_block_copy_block_data = block_copy.get(first_block_copy)
        LOGGER.info("Changing Block {0} - Copy Data Prior to Change {1}".format(first_block_copy,
                                                                                first_block_copy_block_data.get(
                                                                                    "data")))
        first_block_copy_block_data.update({"data": None})
        LOGGER.info("Changing Block {0} - Copy Data after Change {1}".format(first_block_copy,
                                                                             first_block_copy_block_data.get("data")))
        original_odx_block_data = blocks.get(first_block_copy).get("data")

        LOGGER.info("Changing Block {0} - Original Data {1}".format(first_block_copy,
                                                                    original_odx_block_data))
        assert original_odx_block_data is not None

    def test_pdx_file(self, packed_update_container_filepath_mock, tmp_path):
        pdx_obj = PackedUpdateContainer(packed_update_container_filepath_mock)

        alfid = pdx_obj.get_address_and_length_format_identifier()
        assert isinstance(alfid, dict)
        # print(alfid)

        blocks = pdx_obj.get_blocks()
        assert blocks
        expected_idents = pdx_obj.get_expected_idents()
        assert expected_idents
        # print(expected_idents)

        own_idents = pdx_obj.get_own_idents()
        assert own_idents
        # print(own_idents)

        # print(pdx_obj.security_methods)

        p = tmp_path / "test_pdx.pdx"
        pdx_obj._write_file(p)

        with pytest.raises(ValueError):
            PackedUpdateContainer(Path("Some_None_Existing_Path"))
