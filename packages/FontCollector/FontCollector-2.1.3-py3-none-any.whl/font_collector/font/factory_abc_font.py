import logging
import os
from ..exceptions import InvalidFontException, InvalidVariableFontException
from .abc_font import ABCFont, FontType
from .font import Font
from .font_parser import FontParser
from .name import NameID, PlatformID
from .variable_font import VariableFont
from fontTools.ttLib.ttFont import TTFont
from typing import Any, Dict, List, Set, Tuple

_logger = logging.getLogger(__name__)


class FactoryABCFont:
    @staticmethod
    def from_font_path(font_path: str) -> List[ABCFont]:
        """
        Parameters:
            font_path (str): Font path. The font can be a .ttf, .otf, .ttc or .otc file
        Returns:
            An list of Font or VariableFont object that represent the file at the font_path
        """
        ttFonts: List[TTFont] = []

        font = TTFont(font_path, fontNumber=0)
        ttFonts.append(font)

        # Handle TTC font
        if hasattr(font.reader, "numFonts") and font.reader.numFonts > 1:
            for index in range(1, font.reader.numFonts):
                font = TTFont(font_path, fontNumber=index)
                ttFonts.append(font)

        fonts: List[ABCFont] = []
        try:
            for font_index, ttFont in enumerate(ttFonts):

                # If is Variable Font, else "normal" font
                is_var_font = FontParser.is_valid_variable_font(ttFont)
                if is_var_font:
                    try:
                        fonts.extend(FactoryABCFont.__get_variable_fonts(ttFont, font_path, font_index))
                    except InvalidVariableFontException:
                        is_var_font = False

                if not is_var_font:
                    font = FactoryABCFont.__get_font(ttFont, font_path, font_index)
                    fonts.append(font)
        except (InvalidFontException, InvalidVariableFontException):
            _logger.error(f'The font "{font_path}" is invalid.{os.linesep}If you think it is an error, please open an issue on github, share the font and the following error message:')
            raise

        except Exception:
            _logger.error(f'An unknown error occurred while reading the font "{font_path}"{os.linesep}Please open an issue on github, share the font and the following error message:')
            raise

        return fonts


    @staticmethod
    def __get_font(ttFont: TTFont, font_path: str, font_index: int) -> Font:
        """
        Parameters:
            ttFont (TTFont): An fontTools object
            font_path (str): Font path.
            font_index (int): Font index.
        Returns:
            An Font instance that represent the ttFont
        """

        cmaps = FontParser.get_supported_cmaps(ttFont["cmap"].tables)
        if len(cmaps) == 0:
             raise InvalidFontException(f"The font {font_path} doesn't contain any valid cmap.")
        
        cmap_platform_id = PlatformID(cmaps[0].platformID)
        family_names = FontParser.get_filtered_names(ttFont["name"].names, platformID=cmap_platform_id, nameID=NameID.FAMILY_NAME)
        
        # This is something like: https://github.com/libass/libass/blob/a2b39cde4ecb74d5e6fccab4a5f7d8ad52b2b1a4/libass/ass_fontselect.c#L303-L311
        if len(family_names) == 0:
                raise InvalidFontException("The font does not contain an valid family name")
        
        font_type = FontType.from_font(ttFont)
        if font_type == FontType.TRUETYPE:
            exact_names = FontParser.get_filtered_names(ttFont["name"].names, platformID=cmap_platform_id, nameID=NameID.FULL_NAME)
        elif font_type == FontType.OPENTYPE:
            exact_names = FontParser.get_filtered_names(ttFont["name"].names, platformID=cmap_platform_id, nameID=NameID.POSTSCRIPT_NAME)
        elif font_type == FontType.UNKNOWN:
            raise InvalidFontException(f"The font type is not recognized.")
        else:
            raise InvalidFontException(f"The font isn't an opentype or truetype. It is {font_type.name}")


        if cmap_platform_id == PlatformID.MICROSOFT:
            is_italic, is_glyphs_emboldened, weight = FontParser.get_font_italic_bold_property_microsoft_platform(ttFont, font_path, font_index)
        elif cmap_platform_id == PlatformID.MACINTOSH:
            is_italic, is_glyphs_emboldened, weight = FontParser.get_font_italic_bold_property_mac_platform(ttFont, font_path, font_index)
        else:
            # This should never happen
             raise InvalidFontException(f"The font {font_path} doesn't contain any valid cmap.")


        return Font(
            font_path,
            font_index,
            family_names,
            exact_names,
            weight,
            is_italic,
            is_glyphs_emboldened,
            font_type
        )


    def __get_variable_fonts(ttFont: TTFont, font_path: str, font_index: int) -> List[VariableFont]:
        """
        Parameters:
            ttFont (TTFont): An fontTools object
            font_path (str): Font path.
            font_index (int): Font index.
        Returns:
            An list of Font instance that represent the ttFont.
        """

        fonts: Set[VariableFont] = set()
        families_prefix = FontParser.get_var_font_family_prefix(ttFont["name"].names, PlatformID.MICROSOFT)

        if len(families_prefix) == 0:
                raise InvalidVariableFontException("The font does not contain an valid family name")

        font_type = FontType.from_font(ttFont)

        # Ex axis_values_coordinates: [([AxisValue], {"wght", 400.0})]
        axis_values_coordinates: List[Tuple[List[Any], Dict[str, float]]] = []

        for instance in ttFont["fvar"].instances:
            axis_value_table = FontParser.get_axis_value_from_coordinates(ttFont, instance.coordinates)

            # If we get exactly the same axis_value_table for 2 different fvar instance, then, we ignore the first fvar instance.
            named_instance_coordinates = instance.coordinates
            for axis_value_coordinates in axis_values_coordinates:
                if axis_value_coordinates[0] == axis_value_table:
                    named_instance_coordinates = axis_value_coordinates[1]
                    break
            axis_values_coordinates.append((axis_value_table, instance.coordinates))

            (
                families_suffix,
                exact_names_suffix,
                weight,
                is_italic,
            ) = FontParser.get_axis_value_table_property(
                ttFont, axis_value_table
            )


            font = VariableFont(
                font_path,
                font_index,
                families_prefix,
                families_suffix,
                exact_names_suffix,
                int(weight),
                is_italic,
                font_type,
                named_instance_coordinates,
            )
            fonts.add(font)

        return list(fonts)
