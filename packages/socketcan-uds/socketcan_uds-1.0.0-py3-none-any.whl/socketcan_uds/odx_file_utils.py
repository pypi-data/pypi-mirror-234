""" module:: socketcan_uds.odx_file_parser
    :platform: Posix
    :synopsis: A class files for odx file parsers
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
from pathlib import Path
from typing import Optional, BinaryIO, OrderedDict
from xml.etree import ElementTree as ET

from socketcan_uds.odx_elements import DataBlockElement, SessionElement, EcuMemElement, FlashElement


def parse_index_xml(index_file: Path) -> dict:
    """
    Parse a catalog index file
    This concept likely comes from java, yet it is useless
    because these formats all come as zip files and zip files do
    the catalog themselves and likely better than this format does!

    BTW: The namespace feature used here is just a joke because there
         are no tags using namespaces in the file.

    :param index_file: An open file object.
    :type index_file: BinaryIO
    :return: A dictionary.
    :rtype: dict
    """
    with index_file.open("rb") as fp:
        root = ET.parse(fp).getroot()
    assert root.tag == "CATALOG"
    version = root.get("F-DTD-VERSION")
    short_name = root.find("./SHORT-NAME").text
    index_dict = {"version": version,
                  "short_name": short_name,
                  }
    ablocks = {}
    for ablock in root.findall("./ABLOCKS/ABLOCK"):
        short_name = ablock.find("./SHORT-NAME").text
        category = ablock.find("./CATEGORY").text
        files = [file_.text for file_ in ablock.findall("./FILES/FILE")]
        ablocks.update({short_name: {"category": category,
                                     "files": files}})
    index_dict.update({"ablocks": ablocks})
    return index_dict


def create_index_xml(index_file: Path,
                     short_name: str,
                     data_files: OrderedDict,
                     version: str = "ODX-2.2.0") -> None:
    root = ET.Element("CATALOG", {"F-DTD-VERSION": version,
                                  "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                                  "xsi:noNamespaceSchemaLocation": "odx-cc.xsd",
                                  })
    ET.SubElement(root, "SHORT-NAME").text = short_name
    ablocks_node = ET.SubElement(root, "ABLOCKS")
    for short_name, data_dict in data_files.items():
        category = data_dict.get("category")
        files = data_dict.get("files")
        ablock_node = ET.SubElement(ablocks_node, "ABLOCK")
        ET.SubElement(ablock_node, "SHORT-NAME").text = short_name
        ET.SubElement(ablock_node, "CATEGORY").text = category
        files_node = ET.SubElement(ablock_node, "FILES")
        for file in files:
            ET.SubElement(files_node, "FILE").text = file

    tree = ET.ElementTree(element=root)
    with index_file.open("wb") as fp:
        tree.write(file_or_filename=fp,
                   encoding="UTF-8",
                   xml_declaration=True,
                   )


def parse_odx(odx_file: BinaryIO) -> dict:
    tree = ET.parse(odx_file)
    root = tree.getroot()
    assert root.tag == "ODX"
    model_version = root.get("MODEL-VERSION")
    flash_elem = FlashElement.from_element(root.find("./FLASH"))
    return {
        "model_version": model_version,
        "flash": flash_elem
    }


def write_odx(odx_file: BinaryIO,
              flash: FlashElement,
              model_version: str = "2.0.2"):
    root = ET.Element("ODX", {"MODEL-VERSION": model_version,
                              "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                              "xsi:noNamespaceSchemaLocation": "odx.xsd",
                              })
    root.append(flash.to_element())
    tree = ET.ElementTree(element=root)
    tree.write(file_or_filename=odx_file,
               encoding="UTF-8",
               xml_declaration=True,
               )


def find_security_methods(ecu_mem: EcuMemElement) -> dict:
    return {sec.security_method: dict(fw_signature=sec.fw_signature, valid_for=sec.validity_for) for sec in
            ecu_mem.mem.session.securitys}


def find_block_security_methods(data_block: DataBlockElement) -> dict:
    return {sec.security_method: dict(fw_signature=sec.fw_signature, valid_for=sec.validity_for) for sec in
            data_block.securitys}


def find_uds_address_length_format_identifier(ecu_mem: EcuMemElement) -> dict:
    uds_address_length_format_identifier = None
    for sec in ecu_mem.mem.session.securitys:
        if sec.security_method == "ALFID":
            alfid_bytes = sec.fw_signature
            uds_address_length_format_identifier = {
                "routine_control": ((alfid_bytes[0] & 0xF), (alfid_bytes[0] >> 4)),
                "routine_control_erase_memory": ((alfid_bytes[0] & 0xF), (alfid_bytes[0] >> 4)),
                "request_download": ((alfid_bytes[1] & 0xF), (alfid_bytes[1] >> 4)),
                "routine_control_verify_partial_software_checksum": None,
            }
            if len(alfid_bytes) > 2:
                uds_address_length_format_identifier.update(
                    {"routine_control_verify_partial_software_checksum": (
                        (alfid_bytes[2] & 0xF), (alfid_bytes[2] >> 4))})
    return uds_address_length_format_identifier


def alfid_dict_to_alfid_bytes(alfid: dict) -> bytes:
    keys = ["routine_control",
            "request_download",
            "routine_control_verify_partial_software_checksum",
            ]
    b = bytearray()
    for key in keys:
        addr_size_len = alfid.get(key)
        if addr_size_len:
            addr_length, size_length = addr_size_len
            b.append((addr_length | (size_length << 4)))
    return bytes(b)


def find_sa2(ecu_mem: EcuMemElement) -> bytes:
    sa2 = None
    for sec in ecu_mem.mem.session.securitys:
        if sec.security_method == "SA2":
            sa2 = sec.fw_signature
            break
    return sa2


def find_checksum_for_block(datablock: DataBlockElement, session: SessionElement) -> Optional[bytes]:
    checksum = None
    if datablock.securitys:
        checksum = datablock.securitys[0].fw_checksum
    elif (session_securitys := [sec for sec in session.securitys if
                                (sec.validity_for is not None and datablock.id.endswith(
                                    sec.validity_for))]):
        checksum = session_securitys[0].fw_checksum
    return checksum


def find_signature_for_block(datablock: DataBlockElement, session: SessionElement) -> Optional[bytes]:
    signature = None
    if datablock.securitys:
        signature = datablock.securitys[0].fw_signature
    elif (session_securitys := [sec for sec in session.securitys if
                                (sec.validity_for is not None and datablock.id.endswith(
                                    sec.validity_for))]):
        signature = session_securitys[0].fw_signature
    return signature


def find_expected_idents(ecu_mem: EcuMemElement) -> dict:
    session = ecu_mem.mem.session
    expected_idents = {ei.short_name: ei.values for ei in session.expected_idents}
    return expected_idents


def find_own_idents_for_datablock(datablock: DataBlockElement) -> dict:
    own_idents = {oi.short_name: oi.value for oi in datablock.own_idents}
    return own_idents
