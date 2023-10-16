from __future__ import annotations
from .abc_font import ABCFont


class FontResult:

    font: ABCFont
    mismatch_bold: bool
    mismatch_italic: bool

    def __init__(
        self: FontResult,
        font: ABCFont,
        mismatch_bold: bool,
        mismatch_italic: bool,
    ) -> None:
        self.font = font
        self.mismatch_bold = mismatch_bold
        self.mismatch_italic = mismatch_italic


    def __repr__(self):
        return f'FontResult(Font="{self.font}", Mismatch bold="{self.mismatch_bold}", Mismatch italic="{self.mismatch_italic}")'