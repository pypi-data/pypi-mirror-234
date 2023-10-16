from __future__ import annotations
import logging
import os
import pickle
from ..exceptions import InvalidFontException
from .abc_font import ABCFont
from .factory_abc_font import FactoryABCFont
from find_system_fonts_filename import get_system_fonts_filename
from pathlib import Path
from tempfile import gettempdir
from typing import List, Set

_logger = logging.getLogger(__name__)

class FontLoader:

    @staticmethod
    def load_additional_fonts(additional_fonts_path: List[Path]) -> Set[ABCFont]:
        """
        Parameters:
            additional_fonts_path (List[Path]): A list that can contains: .ttf, .otf, .ttc or .otc file AND/OR an directory.
                If you need to use woff font, you will need to decompress them.
                See fontTools documentation to know how to do it: https://fonttools.readthedocs.io/en/latest/ttLib/woff2.html#fontTools.ttLib.woff2.decompress
        Returns:
            An Set of the loaded font
        """
        additional_fonts: Set[ABCFont] = set()

        for font_path in additional_fonts_path:
            if os.path.isfile(font_path):
                try:
                    additional_fonts.update(FactoryABCFont.from_font_path(font_path))
                except InvalidFontException as e:
                    _logger.info(f"{e}. The font {font_path} will be ignored.")
                continue

            elif os.path.isdir(font_path):
                for file in os.listdir(font_path):
                    if Path(file).suffix.lstrip(".").strip().lower() in ["ttf", "otf", "ttc", "otc"]:
                        try:
                            additional_fonts.update(FactoryABCFont.from_font_path(os.path.join(font_path, file)))
                        except InvalidFontException as e:
                            _logger.info(f"{e}. The font {font_path} will be ignored.")
                        continue
            else:
                raise FileNotFoundError(f"The file {font_path} is not reachable")
        return additional_fonts


    @staticmethod
    def load_system_fonts() -> Set[ABCFont]:
        system_fonts: Set[ABCFont] = set()
        fonts_paths: Set[str] = get_system_fonts_filename()
        system_font_cache_file = FontLoader.get_system_font_cache_file_path()

        if os.path.exists(system_font_cache_file):

            with open(system_font_cache_file, "rb") as file:
                cached_fonts: Set[ABCFont] = pickle.load(file)

            cached_paths = set(map(lambda font: font.filename, cached_fonts))

            # Remove font that aren't anymore installed
            removed = cached_paths.difference(fonts_paths)
            system_fonts = set(
                filter(lambda font: font.filename not in removed, cached_fonts)
            )

            # Add font that have been installed since last execution
            added = fonts_paths.difference(cached_paths)
            for font_path in added:
                try:
                    system_fonts.update(FactoryABCFont.from_font_path(font_path))
                except InvalidFontException as e:
                    _logger.info(f"{e}. The font {font_path} will be ignored.")
                continue


            # If there is a change, update the cache file
            if len(added) > 0 or len(removed) > 0:
                with open(system_font_cache_file, "wb") as file:
                    pickle.dump(system_fonts, file)

        else:
            # Since there is no cache file, load the font
            for font_path in fonts_paths:
                try:
                    system_fonts.update(FactoryABCFont.from_font_path(font_path))
                except InvalidFontException as e:
                    _logger.info(f"{e}. The font {font_path} will be ignored.")
                continue

            # Save the font into the cache file
            with open(system_font_cache_file, "wb") as file:
                pickle.dump(system_fonts, file)

        return system_fonts


    @staticmethod
    def load_generated_fonts() -> Set[ABCFont]:
        generated_fonts: Set[ABCFont] = set()
        generated_font_cache_file = FontLoader.get_generated_font_cache_file_path()

        if os.path.exists(generated_font_cache_file):
            with open(generated_font_cache_file, "rb") as file:
                cached_fonts: Set[ABCFont] = pickle.load(file)

            generated_fonts = set(filter(lambda font: os.path.exists(font.filename), cached_fonts))
        
        return generated_fonts


    @staticmethod
    def __save_generated_fonts(generated_fonts: Set[ABCFont]):
        generated_font_cache_file = FontLoader.get_generated_font_cache_file_path()
        with open(generated_font_cache_file, "wb") as file:
            pickle.dump(generated_fonts, file)


    @staticmethod
    def add_generated_font(font: ABCFont):
        """
        Parameters:
            font (Font): Generated font by Helpers.variable_font_to_collection
            It will be cached. 
        """
        generated_fonts = FontLoader.load_generated_fonts()
        generated_fonts.add(font)
        FontLoader.__save_generated_fonts(generated_fonts)


    @staticmethod
    def discard_system_font_cache():
        system_font_cache = FontLoader.get_system_font_cache_file_path()
        if os.path.isfile(system_font_cache):
            os.remove(system_font_cache)


    @staticmethod
    def discard_generated_font_cache():
        generated_font_cache = FontLoader.get_generated_font_cache_file_path()
        if os.path.isfile(generated_font_cache):
            os.remove(generated_font_cache)


    @staticmethod
    def get_system_font_cache_file_path() -> Path:
        tempDir = gettempdir()
        return Path(os.path.join(tempDir, "FontCollector_SystemFont.bin"))


    @staticmethod
    def get_generated_font_cache_file_path() -> Path:
        tempDir = gettempdir()
        return Path(os.path.join(tempDir, "FontCollector_GeneratedFont.bin"))