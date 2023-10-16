""" module:: socketcan_uds.program_file
    :platform: Posix
    :synopsis: A class file for a program file / flash container
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
import logging
import pickle
import zipfile
from abc import ABC, abstractmethod
from collections import OrderedDict
from hashlib import sha256
from pathlib import Path
from typing import Optional, Dict
from copy import deepcopy

from socketcan_uds.common import EncryptionMethod, CompressionMethod
from socketcan_uds.odx_elements import EcuMemElement, SessionElement, FlashDataElement, SegmentElement, \
    DataBlockElement, SecurityElement, MemElement, FlashElement, ExpectedIdentElement, OwnIdentElement
from socketcan_uds.odx_file_utils import parse_odx, find_uds_address_length_format_identifier, \
    find_checksum_for_block, find_signature_for_block, parse_index_xml, write_odx, create_index_xml, \
    find_expected_idents, find_own_idents_for_datablock, find_security_methods, find_block_security_methods


class ProgrammingFileABC(ABC):

    def __init__(self, filepath: Optional[Path] = None):
        self._filepath = None
        self._dictionary = None
        self._logger = logging.getLogger(__name__)

        if filepath is not None:
            self._load_file(filepath=filepath)

    def get_blocks(self):
        return self._dictionary.get("blocks")

    def get_address_and_length_format_identifier(self):
        """
        A method that returns the address and length format identifier defined in the programming file.
        :return: A dictionary with values for various services.
        """
        return self._dictionary.get("uds_address_and_length_format_identifier")

    @abstractmethod
    def _load_file(self, filepath: Path):
        """
        A method to load the ProgrammingFile
        :param filepath: The Filepath
        :type filepath Path
        :return: Nothing
        """

    def copy(self):
        """
        Return a copy of self.
        :return: The Copy.
        """
        new_copy = self.__class__()
        new_copy._dictionary = deepcopy(self._dictionary)
        new_copy._filepath = self._filepath
        return new_copy

    def __copy__(self):
        """
        Standardized Interface for copy.copy().
        There is NO DIFFERENCE between copy and deepcopy
        here because it makes no sense for this object.
        :return: A deep copy of self.
        """
        return self.__deepcopy__()

    def __deepcopy__(self):
        """
        Standardized Interface for copy.deepcopy().
        :return: A deep copy of self.
        """
        return self.copy()


class ExampleProgrammingFile(ProgrammingFileABC):

    def _load_file(self, filepath):
        """
        Load Blocks from pickle file (Testdata)
        :param filepath: The Filepath
        :return: Nothing
        """
        with open(filepath, "rb") as f:
            self._dictionary = pickle.load(f)
        self._filepath = filepath


class UpdateContainerOdxFile(ProgrammingFileABC):
    """
    A xml based update container based on Odx Elements.
    """

    def __init__(self, filepath: Optional[Path] = None):
        self._container_name = "CONTAINER_NAME"
        super().__init__(filepath)

    def _load_file(self, filepath: Path):
        """
        Load a Odx file
        :param filepath: The Filepath
        :type filepath: Path
        :return: Nothing
        """

        with filepath.open("rb") as fp:
            odx = parse_odx(odx_file=fp)

        flash_elem: FlashElement = odx.get("flash")
        ecu_mem = flash_elem.ecu_mem
        self._dictionary = {}

        uds_address_length_format_identifier = find_uds_address_length_format_identifier(ecu_mem)
        security_methods = find_security_methods(ecu_mem)
        expected_idents = find_expected_idents(ecu_mem)

        blocks = OrderedDict()
        for datablockref in ecu_mem.mem.session.datablockrefs:
            datablock = [x for x in ecu_mem.mem.datablocks if x.id == datablockref][0]

            assert len(datablock.segments), "Datablocks with more then one segment are not handled yet."
            segment = datablock.segments[0]
            addr = segment.source_start_address
            uncompressed_size = segment.uncompressed_size
            compressed_size = segment.compressed_size
            flashdata_ref = datablock.flashdata_ref

            flashdata = [x for x in ecu_mem.mem.flashdatas if x.id == flashdata_ref][0]
            data = flashdata.data
            datafile = flashdata.datafile
            compression_method = CompressionMethod((flashdata.encrypt_compress_method[0] & 0xF0) >> 4)
            encryption_method = EncryptionMethod(flashdata.encrypt_compress_method[0] & 0xF)
            transfer_request_parameters = None

            erase_block = (datablock.block_type in ["FLASH_DATA", ])

            checksum = find_checksum_for_block(datablock=datablock,
                                               session=ecu_mem.mem.session)
            signature = find_signature_for_block(datablock=datablock,
                                                 session=ecu_mem.mem.session)
            own_idents = find_own_idents_for_datablock(datablock=datablock)

            blocks.update({datablock.long_name: {"addr": addr,
                                                 "data": data,
                                                 "datafile": datafile,
                                                 "own_idents": own_idents,
                                                 "erase_block": erase_block,
                                                 "compression_method": compression_method,
                                                 "encryption_method": encryption_method,
                                                 "transfer_request_parameters": transfer_request_parameters,
                                                 "uncompressed_size": uncompressed_size,
                                                 "compressed_size": compressed_size,
                                                 "security_methods": find_block_security_methods(datablock),
                                                 "checksum": checksum,  # obsolete
                                                 "signature": signature,  # obsolete
                                                 }})
        self._dictionary.update({"uds_address_and_length_format_identifier": uds_address_length_format_identifier,
                                 "security_methods": security_methods,
                                 "expected_idents": expected_idents,
                                 "blocks": blocks})
        # emem name can be extracted from datablock_id left most string of "."
        self._container_name = flash_elem.long_name
        self._filepath = filepath

    def _write_file(self, filepath: Path, format_flash_pdx: bool = False):
        """
        Write an odx file
        :param filepath: The Filepath
        :type filepath: Path
        :param format_flash_pdx: Format the odx as a flash pdx
        :type format_flash_pdx bool
        :return: Nothing
        """

        datablockrefs = []
        flashdatas = []
        datablocks = []
        session_securitys = []

        flash = FlashElement(long_name=self._container_name,
                             )

        ecu_mem = EcuMemElement(long_name=flash.long_name,
                                desc="""SOME FANCY DESCRIPTION
                                OVER MULTIPLE LINES.
                                 """)
        flash.ecu_mem = ecu_mem

        mem = MemElement(datablocks=datablocks,
                         flashdatas=flashdatas,
                         )
        ecu_mem.mem = mem

        expected_idents = [ExpectedIdentElement(long_name=long_name, values=values) for
                           long_name, values in self.get_expected_idents().items()]
        # print(expected_idents)
        session = SessionElement(securitys=session_securitys,
                                 long_name=ecu_mem.long_name,
                                 datablockrefs=datablockrefs,
                                 expected_idents=expected_idents,
                                 )
        session.id = ".".join([ecu_mem.short_name, session.short_name])
        mem.session = session

        session_securitys.extend([SecurityElement(security_method=security_method_name,
                                                  fw_signature=security_method_data.get("fw_signature"),
                                                  validity_for=security_method_data.get("valid_for"))
                                  for security_method_name, security_method_data in self.security_methods.items()])

        for index, (datablock_name, block_data) in enumerate(self.get_blocks().items()):
            if not datablock_name.split()[0].isnumeric():
                datablock_long_name = "{0:02X} {1}".format(index + 1, datablock_name)
            else:
                datablock_long_name = datablock_name

            self._logger.info("Using {0}".format(datablock_long_name))

            encrypt_compress_method = bytes(
                ((block_data.get("compression_method") << 4) | block_data.get("encryption_method"),))
            flash_data = FlashDataElement(datafile=block_data.get("datafile"),
                                          datafile_type="false",
                                          long_name=datablock_long_name,
                                          data=block_data.get("data"),
                                          encrypt_compress_method=encrypt_compress_method,
                                          dataformat="BINARY",
                                          )
            flash_data.id = ".".join([ecu_mem.short_name, flash_data.short_name])
            flashdatas.append(flash_data)

            block_securitys = [SecurityElement(security_method=security_method_name,
                                               fw_signature=security_method_data.get("fw_signature"),
                                               validity_for=security_method_data.get("valid_for"))
                               for security_method_name, security_method_data in
                               block_data.get("security_methods").items()]

            own_idents = [OwnIdentElement(long_name=long_name, value=value) for
                          long_name, value in block_data.get("own_idents").items()]
            datablock = DataBlockElement(long_name=datablock_long_name,
                                         securitys=block_securitys,
                                         block_type="FLASH-DATA",
                                         flashdata_ref=flash_data.id,
                                         own_idents=own_idents,
                                         )

            datablock.id = ".".join([ecu_mem.short_name, datablock.short_name])
            for own_ident in datablock.own_idents:
                own_ident.id = ".".join([datablock.id, own_ident.short_name])

            segment_long_name = "{0:X}".format(block_data.get("addr"))
            segment = SegmentElement(
                long_name=segment_long_name,
                compressed_size=block_data.get("compressed_size"),
                uncompressed_size=block_data.get("uncompressed_size"),
                source_start_address=block_data.get("addr"),
            )
            segment.id = ".".join([datablock.id, segment.short_name])
            datablock.segments = [segment, ]

            datablocks.append(datablock)
            datablockrefs.append(datablock.id)

        with filepath.open("wb") as fp:  # Note: The filename defaults to the id of the flash block
            write_odx(odx_file=fp,
                      flash=flash)

    def get_expected_idents(self) -> Dict[str, str]:
        """
        Get the EXPECTED-IDENT fields
        :return: A Dictionary of expected identifications
        """
        return self._dictionary.get("expected_idents")

    def get_own_idents(self) -> Dict[str, dict]:
        """
        Get the OWN-IDENT fields
        :return: A collection of Key,Value Tuples, tbd.
        """
        return {block_data.get("addr"): block_data.get("own_idents") for block_name, block_data in
                self.get_blocks().items()}

    @property
    def security_methods(self) -> Optional[dict]:
        """
        Get the SECURITY-METHODS
        :return: A collection of Security Methods
        """
        return self._dictionary.get("security_methods")

    def copy(self):
        """
        Return a copy of self.
        :return: The Copy.
        """
        new_copy = super(UpdateContainerOdxFile, self).copy()
        new_copy.__class__ = self.__class__
        new_copy._container_name = self._container_name
        return new_copy


class PackedUpdateContainer(UpdateContainerOdxFile):
    """
    A packed Update Container aka packed Odx or Pdx

    In essence, it is a Zip file, that contains an
    index.xml file catalog,
    an Odx Update Container,
    a number of .bin files.
    """

    def _load_file(self, filepath: Path):
        """
        Load a Pdx file
        :param filepath: The Filepath
        :type filepath: Path
        :return: Nothing
        """
        index_file_name = "index.xml"
        if not zipfile.is_zipfile(filename=filepath) or (filepath.suffix != ".pdx"):
            raise ValueError("Not a PdxFile {0}".format(filepath))
        with zipfile.ZipFile(file=filepath) as zfp:
            filenames_in_zip = [info.filename for info in zfp.infolist()]
            self._logger.info("Files inside: {0}".format(", ".join(filenames_in_zip)))
            index_file_dict = parse_index_xml(zipfile.Path(zfp, index_file_name))
            self._logger.info("Reading {short_name} Format {version}".format_map(index_file_dict))
            ablocks = index_file_dict.get("ablocks")
            odx_file_name = None
            programming_data_files = []
            for block_name, block_data in ablocks.items():
                if block_data.get("category") == "ODX-DATA":
                    odx_file_list = block_data.get("files")
                    assert odx_file_list is not None
                    assert len(odx_file_list) == 1
                    odx_file_name = odx_file_list[0]
                elif block_data.get("category") == "PROGRAMMING-DATA":
                    programming_data_files.extend(block_data.get("files"))
            self._logger.info("ODX File from Indedx {0}".format(odx_file_name))
            self._logger.info("Programming Files from Index {0}".format(", ".join(programming_data_files)))
            super(PackedUpdateContainer, self)._load_file(zipfile.Path(zfp, odx_file_name))

            for block, block_data in self._dictionary.get("blocks").items():
                bin_file_name = block_data.get("datafile")
                self._logger.info("reading data file {0} into dictionary".format(bin_file_name))
                assert bin_file_name is not None
                with zfp.open(bin_file_name) as bfp:
                    data = bfp.read()
                    block_data.update({"data": data})
        self._logger.info("packed {0}".format(self._container_name))
        self._filepath = filepath

    def _write_file(self, filepath: Path, **kwargs):
        """
        Write an Pdx file
        :param **kwargs: Unused Parameters, to match Parent Class signature.
        :param filepath: The Filepath
        :type filepath: Path
        :return: Nothing
        """
        self._logger.info("write packed {0}".format(self._container_name))
        blocks = self.get_blocks()
        with zipfile.ZipFile(file=filepath, mode="w") as zfp:
            for datablock_id, block_data in blocks.items():
                data = block_data.pop("data")
                h = sha256()
                h.update(data)
                bin_file_name = "{0}00.bin".format(h.hexdigest())
                with zipfile.Path(zfp, bin_file_name).open("wb") as bfp:
                    bfp.write(data)
                block_data.update({"datafile": bin_file_name})

            odx_file_name = "{0}.odx-f".format(self._container_name)
            super()._write_file(zipfile.Path(zfp, odx_file_name))

            index_file_name = "index.xml"
            data_files = OrderedDict()
            data_files.update(
                {
                    odx_file_name: {"category": "ODX-DATA",
                                    "files": [odx_file_name, ],
                                    }
                }
            )
            for datablock_id, block_data in blocks.items():
                data_file_short_name = datablock_id.rsplit(".", maxsplit=1)[-1]
                data_files.update(
                    {
                        data_file_short_name: {"category": "PROGRAMMING-DATA",
                                               "files": [block_data.get("datafile"), ],
                                               },
                    }
                )
            create_index_xml(zipfile.Path(zfp, index_file_name),
                             short_name=self._container_name,
                             data_files=data_files
                             )


def read_programming_file(filepath: Path) -> ProgrammingFileABC:
    """
    Read a programming file and return a suitable class object.
    This function is mainly for testing purposes.

    :param filepath: The Path to the file.
    :type filepath: Path
    :return: A programming file object.
    :rtype: ProgrammingFileABC
    :raise ValueError: If not successful.
    """

    FILE_EXT_TO_PROGRAMMING_FILE_MAPPING = {".pkl": ExampleProgrammingFile,
                                            ".odx": UpdateContainerOdxFile,
                                            ".pdx": PackedUpdateContainer,
                                            }

    if not filepath.exists():
        raise ValueError("Filepath does not exist. {0}".format(filepath))
    if filepath.suffix not in FILE_EXT_TO_PROGRAMMING_FILE_MAPPING:
        raise ValueError("No suitable programming file class for extention {0}".format(filepath.suffix))
    programming_file_class = FILE_EXT_TO_PROGRAMMING_FILE_MAPPING.get(filepath.suffix)
    return programming_file_class(filepath=filepath)


def read_odx_update_container(filepath: Path) -> UpdateContainerOdxFile:
    """
    Read an odx-based programming file and return a suitable class object.
    This is the actual function to be used when loading a file into the programmer.

    :param filepath: The Path to the file.
    :type filepath: Path
    :return: A programming file object.
    :rtype: ProgrammingFileABC
    :raise ValueError: If not successful.
    """

    FILE_EXT_TO_PROGRAMMING_FILE_MAPPING = {".odx": UpdateContainerOdxFile,
                                            ".pdx": PackedUpdateContainer,
                                            }

    if not filepath.exists():
        raise ValueError("Filepath does not exist. {0}".format(filepath))
    if filepath.suffix not in FILE_EXT_TO_PROGRAMMING_FILE_MAPPING:
        raise ValueError("No suitable programming file class for extention {0}".format(filepath.suffix))
    programming_file_class = FILE_EXT_TO_PROGRAMMING_FILE_MAPPING.get(filepath.suffix)
    return programming_file_class(filepath=filepath)
