import re
from typing import Optional, Sequence
from xml.etree import ElementTree as ET


def generate_short_name_from_long_name(long_name: str) -> str:
    short_name = re.sub(pattern=r"\W+",
                        repl=r" ",
                        string=long_name)
    result = []
    for tag in short_name.split():
        if tag.startswith("_"):
            result.append("_{0}".format(tag[1:5].capitalize()))
        else:
            result.append(tag[:5].capitalize())
    return "".join(result)


class OdxElement:
    __TAG__ = "TO_BE_DEFINED_BY_SUBCLASS"
    __NAME_PREFIX__ = "TO_BE_DEFINED_BY_SUBCLASS"

    def __init__(self,
                 id_: Optional[str] = None,
                 short_name: Optional[str] = None,
                 long_name: Optional[str] = None,
                 ):
        """
        Constructor
        According to ISO 22901
        Allowed characters are alphanumeric and "_"
        :param id_: A unique ID string, typically identical to short name
        :param short_name: A short name, up to 127 chars
        :param long_name: A long name, up to 256 chars
        """
        self.id = None
        self.short_name = None
        self.long_name = long_name
        if long_name is not None:
            if id_ is not None:
                self.id = id_
            else:
                self.id = self.generate_short_name_from_long_name_with_prefix(long_name)

            if short_name is not None:
                self.short_name = short_name
            else:
                self.short_name = self.generate_short_name_from_long_name_with_prefix(long_name)

    @classmethod
    def from_element(cls, tree: ET.Element):
        id_ = tree.attrib.get("ID")
        short_name = None
        short_name_node = tree.find(".//SHORT-NAME")
        if short_name_node is not None:
            short_name = short_name_node.text
        long_name = None
        long_name_node = tree.find(".//LONG-NAME")
        if long_name_node is not None:
            long_name = long_name_node.text
        return cls(id_=id_,
                   short_name=short_name,
                   long_name=long_name)

    def to_element(self) -> ET.Element:
        root_node = ET.Element(self.__TAG__)
        if self.id is not None:
            root_node.set("ID", self.id)
        if self.short_name is not None:
            ET.SubElement(root_node, "SHORT-NAME").text = self.short_name
        if self.long_name is not None:
            ET.SubElement(root_node, "LONG-NAME").text = self.long_name
        return root_node

    def generate_short_name_from_long_name_with_prefix(self, long_name):
        return "{0}_{1}".format(self.__NAME_PREFIX__, generate_short_name_from_long_name(long_name))


class FlashDataElement(OdxElement):
    __TAG__ = "FLASHDATA"
    __NAME_PREFIX__ = "FD"

    def __init__(self,
                 long_name: str,
                 id_: Optional[str] = None,
                 short_name: Optional[str] = None,
                 encrypt_compress_method: bytes = bytes.fromhex("00"),
                 data: Optional[bytes] = None,
                 datafile: Optional[str] = None,
                 dataformat: str = "BINARY",
                 datafile_type: str = "false",
                 ):
        super().__init__(id_=id_,
                         short_name=short_name,
                         long_name=long_name)
        self.dataformat = dataformat
        self.encrypt_compress_method = encrypt_compress_method
        self.data = data
        self.datafile = datafile
        self.datafile_type = datafile_type

    @classmethod
    def from_element(cls, tree: ET.Element):
        assert tree.tag == cls.__TAG__
        id_ = tree.attrib.get("ID")
        short_name = tree.find(".//SHORT-NAME").text
        long_name = tree.find(".//LONG-NAME").text
        dataformat = tree.find(".//DATAFORMAT").get("SELECTION")
        encrypt_compress_method = tree.find(".//ENCRYPT-COMPRESS-METHOD").text
        data_node = tree.find("./DATA")
        datafile_node = tree.find("./DATAFILE")
        data = None
        datafile = None
        datafile_type = None
        if data_node is not None:
            data = bytes.fromhex(data_node.text)
        elif datafile_node is not None:
            datafile = datafile_node.text
            datafile_type = datafile_node.get("LATEBOUND-DATAFILE")
        return cls(id_=id_,
                   short_name=short_name,
                   long_name=long_name,
                   dataformat=dataformat,
                   encrypt_compress_method=bytes.fromhex(encrypt_compress_method),
                   data=data,
                   datafile=datafile,
                   datafile_type=datafile_type
                   )

    def to_element(self) -> ET.Element:
        root_node = super(FlashDataElement, self).to_element()
        root_node.set("xsi:type", "INTERN-FLASHDATA")
        ET.SubElement(root_node, "DATAFORMAT", {"SELECTION": self.dataformat})
        ET.SubElement(root_node, "ENCRYPT-COMPRESS-METHOD",
                      {"TYPE": "A_BYTEFIELD"}).text = self.encrypt_compress_method.hex()
        if self.data is not None:
            ET.SubElement(root_node, "DATA").text = self.data.hex()
        if self.datafile is not None:
            ET.SubElement(root_node, "DATAFILE", attrib={"LATEBOUND-DATAFILE": self.datafile_type}).text = self.datafile
        return root_node


class SegmentElement(OdxElement):
    __TAG__ = "SEGMENT"
    __NAME_PREFIX__ = "SEG"

    def __init__(self,
                 long_name: str,
                 source_start_address: int,
                 compressed_size: int,
                 uncompressed_size: int,
                 id_: Optional[str] = None,
                 short_name: Optional[str] = None,
                 ):
        super().__init__(id_=id_,
                         short_name=short_name,
                         long_name=long_name)
        self.source_start_address = source_start_address
        self.compressed_size = compressed_size
        self.uncompressed_size = uncompressed_size

    @classmethod
    def from_element(cls, tree: ET.Element):
        assert tree.tag == cls.__TAG__
        id_ = tree.attrib.get("ID")
        short_name = tree.find("./SHORT-NAME").text
        long_name = tree.find("./LONG-NAME").text
        source_start_address = int(tree.find("./SOURCE-START-ADDRESS").text, 16)

        compressed_size = None
        compressed_size_node = tree.find("./COMPRESSED-SIZE")
        if compressed_size_node is not None:
            compressed_size = int(compressed_size_node.text)

        uncompressed_size = None
        uncompressed_size_node = tree.find("./UNCOMPRESSED-SIZE")
        if uncompressed_size_node is not None:
            uncompressed_size = int(uncompressed_size_node.text)

        return cls(id_=id_,
                   short_name=short_name,
                   long_name=long_name,
                   source_start_address=source_start_address,
                   compressed_size=compressed_size,
                   uncompressed_size=uncompressed_size,
                   )

    def to_element(self) -> ET.Element:
        root_node = super(SegmentElement, self).to_element()
        ET.SubElement(root_node, "SOURCE-START-ADDRESS").text = "{0:X}".format(self.source_start_address)
        if self.compressed_size is not None:
            ET.SubElement(root_node, "COMPRESSED-SIZE").text = str(self.compressed_size)
        if self.uncompressed_size is not None:
            ET.SubElement(root_node, "UNCOMPRESSED-SIZE").text = str(self.uncompressed_size)
        return root_node


class SecurityElement(OdxElement):
    __TAG__ = "SECURITY"
    __NAME_PREFIX__ = "SEC"

    def __init__(self,
                 security_method: str,
                 fw_signature: Optional[bytes] = None,
                 fw_checksum: Optional[bytes] = None,
                 validity_for: Optional[str] = None,
                 ):
        super().__init__()
        self.security_method = security_method
        self.fw_signature = fw_signature
        self.fw_checksum = fw_checksum
        self.validity_for = validity_for

    @classmethod
    def from_element(cls, tree: ET.Element):
        assert tree.tag == cls.__TAG__
        security_method = tree.find("./SECURITY-METHOD").text

        fw_signature_node = tree.find("./FW-SIGNATURE")
        fw_signature = None
        if fw_signature_node is not None:
            # print(fw_signature_node.text, fw_signature_node.attrib)
            fw_signature = bytes.fromhex(fw_signature_node.text)

        fw_checksum = None
        fw_checksum_node = tree.find("./FW-CHECKSUM")
        if fw_checksum_node is not None:
            fw_checksum = bytes.fromhex(fw_checksum_node.text)

        validity_for = None
        validity_for_node = tree.find("./VALIDITY-FOR")
        if validity_for_node is not None:
            validity_for = validity_for_node.text

        return cls(security_method=security_method,
                   fw_signature=fw_signature,
                   fw_checksum=fw_checksum,
                   validity_for=validity_for
                   )

    def to_element(self) -> ET.Element:
        root_node = super(SecurityElement, self).to_element()
        ET.SubElement(root_node, "SECURITY-METHOD", {"TYPE": "A_ASCIISTRING"}).text = self.security_method
        ET.SubElement(root_node, "FW-SIGNATURE", {"TYPE": "A_BYTEFIELD"}).text = self.fw_signature.hex()
        if self.fw_checksum is not None:
            ET.SubElement(root_node, "FW-CHECKSUM", {"TYPE": "A_BYTEFIELD"}).text = self.fw_checksum.hex()
        if self.validity_for is not None:
            ET.SubElement(root_node, "VALIDITY-FOR", {"TYPE": "A_ASCIISTRING"}).text = self.validity_for
        return root_node


class OwnIdentElement(OdxElement):
    __TAG__ = "OWN-IDENT"
    __NAME_PREFIX__ = "OI"

    def __init__(self,
                 long_name: str,
                 value: str,
                 id_: Optional[str] = None,
                 short_name: Optional[str] = None,
                 ):
        super().__init__(id_=id_,
                         short_name=short_name,
                         long_name=long_name)
        self.value = value

    @classmethod
    def from_element(cls, tree: ET.Element):
        assert tree.tag == cls.__TAG__
        id_ = tree.attrib.get("ID")
        short_name = tree.find("./SHORT-NAME").text
        long_name = tree.find("./LONG-NAME").text
        value = tree.find("./IDENT-VALUE").text

        return cls(id_=id_,
                   short_name=short_name,
                   long_name=long_name,
                   value=value
                   )

    def to_element(self) -> ET.Element:
        root_node = super(OwnIdentElement, self).to_element()
        ET.SubElement(root_node, "IDENT-VALUE", {"TYPE": "A_ASCIISTRING"}).text = self.value
        return root_node


class DataBlockElement(OdxElement):
    __TAG__ = "DATABLOCK"
    __NAME_PREFIX__ = "DB"

    def __init__(self,
                 long_name: str,
                 flashdata_ref: str,
                 block_type: str,
                 segments: Optional[Sequence[SegmentElement]] = None,
                 own_idents: Optional[Sequence[OwnIdentElement]] = None,
                 securitys: Optional[Sequence[SecurityElement]] = None,
                 id_: Optional[str] = None,
                 short_name: Optional[str] = None,
                 ):
        super().__init__(id_=id_,
                         short_name=short_name,
                         long_name=long_name)
        self.flashdata_ref = flashdata_ref
        self.segments = segments
        self.own_idents = list()
        if own_idents is not None:
            self.own_idents = own_idents
        self.block_type = block_type
        self.securitys = list()
        if securitys is not None:
            self.securitys = securitys

    @classmethod
    def from_element(cls, tree: ET.Element):
        assert tree.tag == cls.__TAG__
        id_ = tree.attrib.get("ID")
        block_type = tree.attrib.get("TYPE")
        short_name = tree.find("./SHORT-NAME").text
        long_name = tree.find("./LONG-NAME").text
        flashdata_ref = tree.find("./FLASHDATA-REF").get("ID-REF")
        segments = [SegmentElement.from_element(elem) for elem in tree.findall("./SEGMENTS/SEGMENT")]
        own_idents = [OwnIdentElement.from_element(elem) for elem in tree.findall("./OWN-IDENTS/OWN-IDENT")]
        securitys = [SecurityElement.from_element(elem) for elem in tree.findall("./SECURITYS/SECURITY")]
        return cls(id_=id_,
                   short_name=short_name,
                   long_name=long_name,
                   flashdata_ref=flashdata_ref,
                   segments=segments,
                   own_idents=own_idents,
                   block_type=block_type,
                   securitys=securitys,
                   )

    def to_element(self) -> ET.Element:
        root_node = super(DataBlockElement, self).to_element()
        root_node.set("TYPE", self.block_type)
        ET.SubElement(root_node, "FLASHDATA-REF", {"ID-REF": self.flashdata_ref})
        securitys_node = ET.Element("SECURITYS")
        for security in self.securitys:
            securitys_node.append(security.to_element())
        root_node.append(securitys_node)
        segments_node = ET.Element("SEGMENTS")
        for segment in self.segments:
            segments_node.append(segment.to_element())
        root_node.append(segments_node)
        own_idents_node = ET.Element("OWN-IDENTS")
        for own_ident in self.own_idents:
            own_idents_node.append(own_ident.to_element())
        root_node.append(own_idents_node)
        return root_node


class ExpectedIdentElement(OdxElement):
    __TAG__ = "EXPECTED-IDENT"
    __NAME_PREFIX__ = "EI"

    def __init__(self,
                 long_name: str,
                 values: Sequence[str],
                 id_: Optional[str] = None,
                 short_name: Optional[str] = None,
                 ):
        super().__init__(id_=id_,
                         short_name=short_name,
                         long_name=long_name)
        self.values = values

    @classmethod
    def from_element(cls, tree: ET.Element):
        assert tree.tag == cls.__TAG__
        id_ = tree.attrib.get("ID")
        short_name = tree.find("./SHORT-NAME").text
        long_name = tree.find("./LONG-NAME").text
        values = [ident_values_node.text
                  for ident_values_node in tree.findall("./IDENT-VALUES/IDENT-VALUE")]

        return cls(id_=id_,
                   short_name=short_name,
                   long_name=long_name,
                   values=values
                   )

    def to_element(self) -> ET.Element:
        root_node = super(ExpectedIdentElement, self).to_element()
        ident_values_node = ET.Element("IDENT-VALUES")
        for value in self.values:
            ET.SubElement(ident_values_node, "IDENT-VALUE", {"TYPE": "A_ASCIISTRING"}).text = value
        root_node.append(ident_values_node)
        return root_node


class SessionElement(OdxElement):
    __TAG__ = "SESSION"
    __NAME_PREFIX__ = "SES"

    def __init__(self,
                 long_name: str,
                 expected_idents: Sequence[ExpectedIdentElement],
                 securitys: Sequence[SecurityElement],
                 datablockrefs: Sequence[str],
                 id_: Optional[str] = None,
                 short_name: Optional[str] = None,
                 ):
        super().__init__(id_=id_,
                         short_name=short_name,
                         long_name=long_name)
        self.expected_idents = expected_idents
        self.securitys = securitys
        self.datablockrefs = datablockrefs

    @classmethod
    def from_element(cls, tree: ET.Element):
        assert tree.tag == cls.__TAG__
        id_ = tree.attrib.get("ID")
        short_name = tree.find("./SHORT-NAME").text
        long_name = tree.find("./LONG-NAME").text
        securitys = [SecurityElement.from_element(elem) for elem in tree.findall("./SECURITYS/SECURITY")]
        expected_idents = [ExpectedIdentElement.from_element(elem) for elem in
                           tree.findall("./EXPECTED-IDENTS/EXPECTED-IDENT")]

        datablockrefs = [datablockref_node.get("ID-REF")
                         for datablockref_node in tree.findall("./DATABLOCK-REFS/DATABLOCK-REF")]

        return cls(id_=id_,
                   short_name=short_name,
                   long_name=long_name,
                   expected_idents=expected_idents,
                   securitys=securitys,
                   datablockrefs=datablockrefs
                   )

    def to_element(self) -> ET.Element:
        root_node = super(SessionElement, self).to_element()
        expected_idents_node = ET.Element("EXPECTED-IDENTS")
        for expected_ident in self.expected_idents:
            expected_idents_node.append(expected_ident.to_element())
        root_node.append(expected_idents_node)

        securitys_node = ET.Element("SECURITYS")
        for security in self.securitys:
            securitys_node.append(security.to_element())
        root_node.append(securitys_node)

        datablockrefs_node = ET.Element("DATABLOCK-REFS")
        for datablockref in self.datablockrefs:
            ET.SubElement(datablockrefs_node, "DATABLOCK-REF", {"ID-REF": datablockref})
        root_node.append(datablockrefs_node)

        return root_node


class MemElement(OdxElement):
    __TAG__ = "MEM"
    __NAME_PREFIX__ = "MEM"

    def __init__(self,
                 datablocks: Sequence[DataBlockElement],
                 flashdatas: Sequence[FlashDataElement],
                 session: Optional[SessionElement] = None,
                 ):
        super().__init__()
        self.flashdatas = flashdatas
        self.datablocks = datablocks
        self.session = session

    @classmethod
    def from_element(cls, tree: ET.Element):
        assert tree.tag == cls.__TAG__
        datablocks = [DataBlockElement.from_element(elem) for elem in tree.findall("./DATABLOCKS/DATABLOCK")]
        flashdatas = [FlashDataElement.from_element(elem) for elem in tree.findall("./FLASHDATAS/FLASHDATA")]
        session = SessionElement.from_element(tree.find("./SESSIONS/SESSION"))
        return cls(datablocks=datablocks,
                   flashdatas=flashdatas,
                   session=session,
                   )

    def to_element(self) -> ET.Element:
        root_node = super(MemElement, self).to_element()
        sessions_node = ET.SubElement(root_node, "SESSIONS")
        sessions_node.append(self.session.to_element())

        datablocks_node = ET.Element("DATABLOCKS")
        for datablock in self.datablocks:
            datablocks_node.append(datablock.to_element())
        root_node.append(datablocks_node)

        flashdatas_node = ET.Element("FLASHDATAS")
        for flashdata in self.flashdatas:
            flashdatas_node.append(flashdata.to_element())
        root_node.append(flashdatas_node)

        return root_node


class EcuMemElement(OdxElement):
    __TAG__ = "ECU-MEM"
    __NAME_PREFIX__ = "EMEM"

    def __init__(self,
                 long_name: str,
                 mem: Optional[MemElement] = None,
                 desc: Optional[str] = None,
                 id_: Optional[str] = None,
                 short_name: Optional[str] = None,
                 ):
        super().__init__(id_=id_,
                         short_name=short_name,
                         long_name=long_name)
        self.mem = mem
        self.desc = desc

    @classmethod
    def from_element(cls, tree: ET.Element):
        assert tree.tag == cls.__TAG__
        id_ = tree.attrib.get("ID")
        short_name = tree.find("./SHORT-NAME").text
        long_name = tree.find("./LONG-NAME").text
        mem = MemElement.from_element(tree.find("./MEM"))
        desc_node = tree.find("./DESC/p")
        desc = None
        if desc_node is not None:
            desc = desc_node.text
        return cls(id_=id_,
                   short_name=short_name,
                   long_name=long_name,
                   mem=mem,
                   desc=desc,
                   )

    def to_element(self) -> ET.Element:
        root_node = super(EcuMemElement, self).to_element()
        if self.desc is not None:
            desc_node = ET.SubElement(root_node, "DESC")
            ET.SubElement(desc_node, "p").text = self.desc
        root_node.append(self.mem.to_element())
        return root_node


class FlashElement(OdxElement):
    __TAG__ = "FLASH"
    __NAME_PREFIX__ = "FL"

    def __init__(self,
                 long_name: str,
                 ecu_mem: Optional[EcuMemElement] = None,
                 id_: Optional[str] = None,
                 short_name: Optional[str] = None,
                 ):
        super().__init__(id_=id_,
                         short_name=short_name,
                         long_name=long_name)
        self.ecu_mem = ecu_mem

    @classmethod
    def from_element(cls, tree: ET.Element):
        assert tree.tag == cls.__TAG__
        id_ = tree.attrib.get("ID")
        short_name = tree.find("./SHORT-NAME").text
        long_name = tree.find("./LONG-NAME").text
        ecu_mem = EcuMemElement.from_element(tree.find("./ECU-MEMS/ECU-MEM"))
        return cls(id_=id_,
                   short_name=short_name,
                   long_name=long_name,
                   ecu_mem=ecu_mem,
                   )

    def to_element(self) -> ET.Element:
        root_node = super(FlashElement, self).to_element()
        node = ET.SubElement(root_node, "ECU-MEMS")
        node.append(self.ecu_mem.to_element())
        return root_node
