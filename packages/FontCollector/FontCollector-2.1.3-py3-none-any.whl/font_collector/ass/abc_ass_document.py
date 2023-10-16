from __future__ import annotations
from .ass_style import AssStyle
from .usage_data import UsageData
from abc import ABC, abstractmethod
from ass_tag_analyzer import (
    AssDraw,
    AssInvalidTagBold,
    AssInvalidTagFontName,
    AssInvalidTagItalic,
    AssInvalidTagResetStyle,
    AssInvalidTagWrapStyle,
    AssItem,
    AssTagBold,
    AssTagFontName,
    AssTagItalic,
    AssTagResetStyle,
    AssTagWrapStyle,
    AssText,
    AssValidTagAnimation,
    AssValidTagBold,
    AssValidTagFontName,
    AssValidTagItalic,
    AssValidTagResetStyle,
    AssValidTagWrapStyle,
    parse_line,
    WrapStyle,
)
from typing import Dict, List, Optional, Tuple


class ABCAssDocument(ABC):
    """
    You can extend this class.
    You can inspire yourself from ass_document.
    """

    @abstractmethod
    def _get_sub_wrap_style(self: ABCAssDocument) -> Optional[WrapStyle]:
        """
        Returns:
            The subtitle WrapStyle.
            If the subtitle doesn't contain an WrapStyle, it return None
        """
        pass

    def get_sub_wrap_style(self: ABCAssDocument) -> WrapStyle:
        """
        Returns:
            The subtitle WrapStyle.
        """

        sub_wrap_style = self._get_sub_wrap_style()
        if sub_wrap_style is None:
            sub_wrap_style = WrapStyle.SMART_TOP
        return sub_wrap_style


    @abstractmethod
    def get_nbr_style(self: ABCAssDocument) -> int:
        """
        Returns:
            The number of styles.
        """
        pass


    def __verify_if_style_exist(self: ABCAssDocument, i: int) -> None:
        if i >= self.get_nbr_style():
            raise ValueError(f"There isn't any style at the index {i}. There is only {self.get_nbr_style()} style(s)")


    @abstractmethod
    def _get_style(self: ABCAssDocument, i: int) -> Tuple[str, str, bool, bool]:
        pass

    def get_style(self: ABCAssDocument, i: int) -> Tuple[str, str, bool, bool]:
        """
        Parameters:
            i (int): Index of the line.
        Returns:
            An Tuple formatted like this: style_name, font_name, is_bold, is_italic
        """
        self.__verify_if_style_exist(i)
        return self._get_style(i)


    def get_sub_styles(self: ABCAssDocument) -> Dict[str, AssStyle]:
        """
        Returns:
            An Dict:
                Key: The style name.
                Value: An AssStyle corresponding to the style name.
        """
        sub_styles: Dict[str, AssStyle] = {}

        for i in range(self.get_nbr_style()):
            style_name, font_name, is_bold, is_italic = self.get_style(i)

            # VSFilter trim:
            #   - "*": https://sourceforge.net/p/guliverkli2/code/HEAD/tree/src/subtitles/STS.cpp#l1447
            #   - tabulation and space : https://sourceforge.net/p/guliverkli2/code/HEAD/tree/src/subtitles/STS.cpp#l1172
            style_name = style_name.lstrip("\t ").lstrip("*")
            font_name = font_name.lstrip("\t ")
            weight = 700 if is_bold else 400

            ass_style = AssStyle(font_name, weight, is_italic)
            sub_styles[style_name] = ass_style

        return sub_styles
    

    @abstractmethod
    def get_nbr_line(self: ABCAssDocument) -> int:
        """
        Returns:
            The number of lines.
        """
        pass


    def __verify_if_line_exist(self: ABCAssDocument, i: int) -> None:
        if i >= self.get_nbr_line():
            raise ValueError(f"There isn't any line at the index {i}. There is only {self.get_nbr_line()} line(s)")


    @abstractmethod
    def _get_line_style_name(self: ABCAssDocument, i: int) -> str:
        pass

    def get_line_style_name(self: ABCAssDocument, i: int) -> str:
        """
        Parameters:
            i (int): Index of the line.
        Returns:
            The style name of the line.
        """
        self.__verify_if_line_exist(i)
        return self._get_line_style_name(i)


    @abstractmethod
    def _get_line_text(self: ABCAssDocument, i: int) -> str:
        pass

    def get_line_text(self: ABCAssDocument, i: int) -> str:
        """
        Parameters:
            i (int): Index of the line.
        Returns:
            The text of the line.
        """
        self.__verify_if_line_exist(i)
        return self._get_line_text(i)
    

    @abstractmethod
    def _is_line_dialogue(self: ABCAssDocument, i: int) -> bool:
        pass

    def is_line_dialogue(self: ABCAssDocument, i: int) -> bool:
        """
        Parameters:
            i (int): Index of the line.
        Returns:
            True if the line is an Dialogue. Else, return false.
        """
        self.__verify_if_line_exist(i)
        return self._is_line_dialogue(i)
    

    def __set_used_styles(
        self: ABCAssDocument,
        used_styles: Dict[AssStyle, UsageData],
        tags: List[AssItem],
        line_index: int,
        sub_styles: Dict[str, AssStyle],
        original_line_style: AssStyle,
        line_style: AssStyle,
        current_style: AssStyle,
        current_wrap_style: WrapStyle,
        collect_draw_fonts: bool
    ) -> None:
        """
        Parameters:
            used_styles (Dict[AssStyle, UsageData]): This variable will be modified
            tags (List[AssItem]): List of all tags
            line_index (int): Position of the line in the subtitle
            sub_styles (Dict[str, AssStyle]): Dict of the [V4+ Styles] sections
            original_line_style (AssStyle): Style of the line
            line_style (AssStyle): Style of the line. In general, it will be equal to original_line_style except it there is an \rXXX
            current_style (AssStyle): Real style of the text. It exist since \fn, \b, \i can override the line_style.
            current_wrap_style (WrapStyle): Since \q can override the subtitle WrapStyle, we need it.
            collect_draw_fonts (bool): If true, then it will also collect the draw style, if false, it will ignore it.
        """

        for tag in tags:
            if isinstance(tag, AssTagResetStyle):
                if isinstance(tag, AssValidTagResetStyle):
                    style = sub_styles.get(tag.style, original_line_style)

                    # Copy the style
                    line_style = AssStyle(style.fontname, style.weight, style.italic)
                    current_style = AssStyle(style.fontname, style.weight, style.italic)
                elif isinstance(tag, AssInvalidTagResetStyle):
                    # Copy the original_line_style
                    line_style = AssStyle(
                        original_line_style.fontname,
                        original_line_style.weight,
                        original_line_style.italic,
                    )
                    current_style = AssStyle(
                        original_line_style.fontname,
                        original_line_style.weight,
                        original_line_style.italic,
                    )

            elif isinstance(tag, AssTagBold):
                if isinstance(tag, AssValidTagBold):
                    current_style.weight = tag.weight
                elif isinstance(tag, AssInvalidTagBold):
                    current_style.weight = line_style.weight

            elif isinstance(tag, AssTagItalic):
                if isinstance(tag, AssValidTagItalic):
                    current_style.italic = tag.enabled
                elif isinstance(tag, AssInvalidTagItalic):
                    current_style.italic = line_style.italic

            elif isinstance(tag, AssTagFontName):
                if isinstance(tag, AssValidTagFontName):
                    current_style.fontname = tag.name

                elif isinstance(tag, AssInvalidTagFontName):
                    current_style.fontname = line_style.fontname

            elif isinstance(tag, AssTagWrapStyle):
                if isinstance(tag, AssValidTagWrapStyle):
                    current_wrap_style = tag.style
                elif isinstance(tag, AssInvalidTagWrapStyle):
                    current_wrap_style = WrapStyle(self.get_sub_wrap_style())

            elif isinstance(tag, AssValidTagAnimation):
                self.__set_used_styles(
                    used_styles,
                    tag.tags,
                    line_index,
                    sub_styles,
                    original_line_style,
                    line_style,
                    current_style,
                    current_wrap_style,
                    collect_draw_fonts
                )

            elif isinstance(tag, AssText) and len(tag.text) > 0:
                # Inspired by
                #     - https://github.com/libass/libass/blob/a2b39cde4ecb74d5e6fccab4a5f7d8ad52b2b1a4/libass/ass_parse.c#L1039-L1075
                #     - Aegisub FontCollector ignore \n: https://github.com/arch1t3cht/Aegisub/blob/fad362ec2e2975d8e37893c6dfb3a39452e71d23/src/font_file_lister.cpp#L118-L120
                text = tag.text.replace("\t", " ")
                if current_wrap_style == WrapStyle.NO_WORD:
                    text = text.replace("\\n", "")
                else:
                    text = text.replace("\\n", " ")
                text = text.replace("\\N", "")
                # Libass use latin space to render NBSP: https://github.com/libass/libass/blob/a2b39cde4ecb74d5e6fccab4a5f7d8ad52b2b1a4/libass/ass_font.c#L573-L574
                text = text.replace("\\h", " ")
                text = text.replace("\u00A0", " ")

                # Update or create the usage_data
                usage_data = used_styles.get(current_style, None)
                if usage_data is None:
                    usage_data = UsageData(set(text), set([line_index]))
                    used_styles[current_style] = usage_data
                else:
                    usage_data.characters_used.update(set(text))
                    usage_data.lines.add(line_index)

                # We need to make an copy of the style since current_style can be modified
                current_style = AssStyle(current_style.fontname, current_style.weight, current_style.italic)
            elif collect_draw_fonts and isinstance(tag, AssDraw) and len(tag.text) > 0:
                usage_data = used_styles.get(current_style, None)
                if usage_data is None:
                    usage_data = UsageData(set(), set([line_index]))
                    used_styles[current_style] = usage_data
                else:
                    usage_data.lines.add(line_index)

                # We need to make an copy of the style since current_style can be modified
                current_style = AssStyle(current_style.fontname, current_style.weight, current_style.italic)


    def get_used_style(self: ABCAssDocument, collect_draw_fonts: bool = False) -> Dict[AssStyle, UsageData]:
        """
        Parameters:
            collect_draw_fonts (bool): If true, then it will also collect the draw style, if false, it will ignore it.
        Returns:
            An dictionnary which contain all the used AssStyle and it's UsageData.
        """
        used_styles: Dict[AssStyle, UsageData] = {}
        sub_styles: Dict[str, AssStyle] = self.get_sub_styles()
        sub_wrap_style = self.get_sub_wrap_style()

        for i in range(self.get_nbr_line()):
            if self.is_line_dialogue(i):
                
                original_line_style = sub_styles.get(self.get_line_style_name(i), None)

                if original_line_style is None:
                    tags = parse_line(self.get_line_text(i))

                    # If the line is empty, we won't raise an exception
                    for tag in tags:
                        if isinstance(tag, (AssDraw, AssText)) and len(tag.text) > 0:
                            raise ValueError(f'Error: Unknown style "{self.get_line_style_name(i)}" on line {i+1}. You need to correct the .ass file.')
                    continue

                tags = parse_line(self.get_line_text(i))

                # Copy the original_line_style
                line_style = AssStyle(
                    original_line_style.fontname,
                    original_line_style.weight,
                    original_line_style.italic,
                )
                current_style = AssStyle(
                    original_line_style.fontname,
                    original_line_style.weight,
                    original_line_style.italic,
                )


                self.__set_used_styles(
                    used_styles,
                    tags,
                    i + 1,
                    sub_styles,
                    original_line_style,
                    line_style,
                    current_style,
                    sub_wrap_style,
                    collect_draw_fonts
                )

        return used_styles
