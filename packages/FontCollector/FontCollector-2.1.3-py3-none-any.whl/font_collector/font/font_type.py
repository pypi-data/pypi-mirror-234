from __future__ import annotations
from enum import auto, Enum
from fontTools.ttLib.ttFont import TTFont


class FontType(Enum):
    UNKNOWN = auto()
    TRUETYPE = auto()
    OPENTYPE = auto()

    @classmethod
    def from_font(cls: FontType, font: TTFont) -> FontType:
        """
        Parameters:
            font (TTFont): An fontTools object
        """

        if 'glyf' in font:
            return cls.TRUETYPE
        elif 'CFF ' in font or 'CFF2' in font:
            return cls.OPENTYPE
        else:
            return cls.UNKNOWN