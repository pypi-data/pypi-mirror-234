from __future__ import annotations
from ..exceptions import InvalidNameRecord
from enum import IntEnum
from typing import Optional
from fontTools.ttLib.tables._n_a_m_e import NameRecord, _MAC_LANGUAGES, _MAC_LANGUAGE_CODES, _WINDOWS_LANGUAGES, _WINDOWS_LANGUAGE_CODES
from langcodes import Language


class PlatformID(IntEnum):
    # From https://learn.microsoft.com/en-us/typography/opentype/spec/name#platform-ids
    UNICODE = 0
    MACINTOSH = 1
    MICROSOFT = 3


class NameID(IntEnum):
    # From: https://learn.microsoft.com/en-us/typography/opentype/spec/name#name-ids
    COPYRIGHT = 0
    FAMILY_NAME = 1
    SUBFAMILY_NAME = 2
    UNIQUE_ID = 3
    FULL_NAME = 4
    VERSION_STRING = 5
    POSTSCRIPT_NAME = 6
    TRADEMARK = 7
    MANUFACTURER = 8
    DESIGNER = 9
    DESCRIPTION = 10
    VENDOR_URL = 11
    DESIGNER_URL = 12
    LICENSE_DESCRIPTION = 13
    LICENSE_URL = 14
    TYPOGRAPHIC_FAMILY_NAME = 16
    TYPOGRAPHIC_SUBFAMILY_NAME = 17
    MAC_FULL_NAME = 18
    SAMPLE_TEXT = 19
    POSTSCRIPT_CID_FINDFONT_NAME = 20
    WWS_FAMILY_NAME = 21
    WWS_SUBFAMILY_NAME = 22
    LIGHT_BACKGROUND = 23
    DARK_BACKGROUND = 24
    VARIATIONS_PREFIX_NAME = 25


class Name:
    value: str
    lang_code: Language

    def __init__(
        self: Name,
        value: str,
        lang_code: Language
    ) -> Name:
        self.value = value
        self.lang_code = lang_code


    @classmethod
    def from_name_record(cls: Name, name_record: NameRecord) -> Name:
        """
        Parameters:
            name_record (NameRecord): Name record from the naming table
        Returns:
            An Name instance.
        """
        value = Name.get_decoded_name_record(name_record)
        lang_code = Language.get(Name.get_lang_code_of_namerecord(name_record))

        return cls(value, lang_code)


    @staticmethod
    def get_name_record_encoding(name: NameRecord) -> Optional[str]:
        """
        Parameters:
            names (NameRecord): Name record from the naming record
        Returns:
            The NameRecord encoding name.
            If GDI does not support the NameRecord, it return None.
        """
        # From: https://github.com/MicrosoftDocs/typography-issues/issues/956#issuecomment-1205678068
        if name.platformID == PlatformID.MICROSOFT:
            if name.platEncID == 3:
                return "cp936"
            elif name.platEncID == 4:
                if name.nameID == NameID.SUBFAMILY_NAME:
                    return "utf_16_be"
                else:
                    return "cp950"
            elif name.platEncID == 5:
                if name.nameID == NameID.SUBFAMILY_NAME:
                    return "utf_16_be"
                else:
                    return "cp949"
            else:
                return "utf_16_be"
        elif name.platformID == PlatformID.MACINTOSH and name.platEncID == 0:
            # From: https://github.com/libass/libass/issues/679#issuecomment-1442262479
            return "iso-8859-1"

        return None

    
    @staticmethod
    def get_decoded_name_record(name: NameRecord) -> str:
        """
        Parameters:
            names (NameRecord): Name record from the naming table
        Returns:
            The decoded name
        """
        encoding = Name.get_name_record_encoding(name)

        if encoding is None:
            raise InvalidNameRecord(f"The NameRecord you provided isn't supported by GDI: NameRecord(PlatformID={name.platformID}, PlatEncID={name.platEncID}, LangID={name.langID}, String={name.string}, NameID={name.nameID})")

        if name.platformID == PlatformID.MICROSOFT and encoding != "utf_16_be":
            # I spoke with a Microsoft employee and he told me that GDI performed this processing:
            name_to_decode = name.string.replace(b"\x00", b"")
        else:
            name_to_decode = name.string

        # GDI ignore any decoding error. See tests\font tests\Test #1\Test #1.py
        return name_to_decode.decode(encoding, "ignore")


    @staticmethod
    def get_lang_code_of_namerecord(name: NameRecord) -> str:
        """
        Parameters:
            names (NameRecord): Name record from the naming table
        Returns:
            The IETF BCP-47 code of the NameRecord. If the lang code isn't found, it return "und".
        """
        return Name.get_lang_code_from_platform_lang_id(name.platformID, name.langID)


    @staticmethod
    def get_lang_code_from_platform_lang_id(platform_id: PlatformID, lang_id: int) -> str:
        """
        Parameters:
            platform_id (PlatformID): An platform id.
            lang_id (int): An language id of an platform. See: https://learn.microsoft.com/en-us/typography/opentype/spec/name
        Returns:
            The IETF BCP-47 code corresponding to the language id. If the lang code isn't found, it return "und".
        """
        if platform_id == PlatformID.MICROSOFT:
            return _WINDOWS_LANGUAGES.get(lang_id, "und")
        elif platform_id == PlatformID.MACINTOSH:
            return _MAC_LANGUAGES.get(lang_id, "und")
        else:
            return "und"


    def get_lang_code_platform_code(self: Name, platform_id: PlatformID) -> int:
        """
        Parameters:
            platform_id (PlatformID): The platform id of which you wanna retrieve the lang_code
        Returns:
            The language code corresponding to the platform:
                - https://learn.microsoft.com/en-us/typography/opentype/spec/name#macintosh-language-ids
                - https://learn.microsoft.com/en-us/typography/opentype/spec/name#windows-language-ids
        """
        str_lang_code = str(self.lang_code)
        if platform_id == PlatformID.MICROSOFT:
            if str_lang_code not in _WINDOWS_LANGUAGE_CODES:
                raise ValueError(f'The lang_code "{str_lang_code}" isn\'t supported by the microsoft platform')
            return _WINDOWS_LANGUAGE_CODES[str_lang_code]

        elif platform_id == PlatformID.MACINTOSH:
            if str_lang_code not in _MAC_LANGUAGE_CODES:
                raise ValueError(f'The lang_code "{str_lang_code}" isn\'t supported by the macintosh platform')
            return _MAC_LANGUAGE_CODES[str_lang_code]
        raise ValueError(f"You cannot specify the platform id {platform_id}. You can only specify the microsoft or the macintosh id")


    def __eq__(self: Name, other: Name) -> bool:
        return (self.value, self.lang_code) == (other.value, other.lang_code)


    def __hash__(self: Name) -> int:
        return hash((self.value, self.lang_code))


    def __repr__(self: Name) -> str:
        return f'Name(value="{self.value}", lang_code="{self.lang_code}")'