from __future__ import annotations
from ..ass.ass_style import AssStyle
from .abc_font import ABCFont
from .font import Font
from .font_loader import FontLoader
from .font_result import FontResult
from typing import Any, Optional, Set


class FontCollection:
    """Contains fonts. This class allows to query fonts.

    Attributes:
        use_system_font (bool): If true, then the collection will contains the system font.
        reload_system_font (bool): If true, then each time you will try to access the system_fonts,
            it will reload it to see if any new font(s) have been installed or uninstalled. This can reduce performance.
            If false, it will only load the system font 1 time and never reload it.
        use_generated_fonts (bool): Use the cached font collection (.ttc file) that were been generated from an variable font.
        system_fonts (Set[ABCFont]): If use_system_font is set to True, it will contain the system font. 
            If false, it will be empty.
        generated_fonts (Set[ABCFont]): It use_generated_fonts is set to True, it will contain the font collection (.ttc file) that were been generated from an variable font. 
            If false, it will be empty.
            Warning: All the FontCollection use the same generated_fonts.
        additional_fonts (Set[ABCFont]): It contain the font you specified.
        fonts (Set[ABCFont]): It contain the font(s) from system_fonts, generated_fonts and additional_fonts.
    """


    def __init__(
        self: FontCollection, 
        use_system_font: bool = True,
        reload_system_font: bool = False,
        use_generated_fonts: bool = True,
        additional_fonts: Set[ABCFont] = set(), 
    ) -> FontCollection:
        self.use_system_font = use_system_font
        self.reload_system_font = reload_system_font
        self.use_generated_fonts = use_generated_fonts
        self.additional_fonts = additional_fonts

    
    def __iter__(self: FontCollection) -> ABCFont:
        for font in self.fonts:
            yield font


    @property
    def system_fonts(self: FontCollection) -> Set[ABCFont]:
        if self.use_system_font:
            if self.reload_system_font:
                return FontLoader.load_system_fonts()

            if hasattr(self, '__system_fonts'):
                return self.__system_fonts
            self.__system_fonts = FontLoader.load_system_fonts()
            return self.__system_fonts
        return set()

    @system_fonts.setter
    def system_fonts(self: FontCollection, value: Any):
        raise AttributeError("You cannot set system_fonts, but you can set use_system_font")


    @property
    def generated_fonts(self: FontCollection) -> Set[ABCFont]:
        if self.use_generated_fonts:
            return FontLoader.load_generated_fonts()
        return set()

    @generated_fonts.setter
    def generated_fonts(self: FontCollection, value: Any):
        raise AttributeError("You cannot set generated_fonts, but you can set use_generated_fonts")


    @property
    def fonts(self: FontCollection) -> Set[ABCFont]:
        return self.system_fonts.union(self.generated_fonts).union(self.additional_fonts)

    @fonts.setter
    def fonts(self: FontCollection, value: Any):
        raise AttributeError("You cannot set the fonts. If you want to add font, set additional_fonts")


    def get_used_font_by_style(self: FontCollection, style: AssStyle) -> Optional[FontResult]:
        """
        Parameters:
            style (AssStyle): An AssStyle
        Returns:
            Ordered list of the font that match the best to the AssStyle
        """

        score_min = float('inf')
        selected_font = None
        for font in self.fonts:
            score = float('inf')

            family_name_match = any(style.fontname.lower() == family_name.value.lower() for family_name in font.family_names)

            if family_name_match:
                score = font.get_similarity_score(style)
            else:
                exact_name_match = any(style.fontname.lower() == exact_name.value.lower() for exact_name in font.exact_names)
                if exact_name_match:
                    score = font.get_similarity_score(style)
            
            if score < score_min:
                score_min = score
                selected_font = font

            if family_name_match and score == 0 and isinstance(selected_font, Font):
                break

        if selected_font is None:
            return None

        mismatch_bold = abs(selected_font.weight - style.weight) >= 150
        mismatch_italic = selected_font.is_italic != style.italic

        font_result = FontResult(selected_font, mismatch_bold, mismatch_italic)
        return font_result
    

    def __eq__(self: FontCollection, other: FontCollection) -> bool:
        return (self.fonts, self.reload_system_font, self.use_generated_fonts, self.additional_fonts) == (
            other.use_system_font, other.reload_system_font, other.use_generated_fonts, other.fonts
        )

    def __hash__(self: FontCollection) -> int:
        return hash(
            (
                self.use_system_font,
                self.reload_system_font,
                self.use_generated_fonts,
                frozenset(self.additional_fonts),
            )
        )

    def __repr__(self: FontCollection) -> str:
        return f'FontCollection(Use system font="{self.use_system_font}", Reload system font="{self.reload_system_font}", Use generated fonts="{self.use_generated_fonts}", Additional fonts="{self.additional_fonts}")'
