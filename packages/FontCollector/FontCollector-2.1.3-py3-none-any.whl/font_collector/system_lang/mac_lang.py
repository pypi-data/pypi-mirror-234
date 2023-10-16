from ..exceptions import OSNotSupported
from ..font.name import Name, PlatformID
from .system_lang import SystemLang
from ctypes import cdll, c_uint32, c_void_p, util
from find_system_fonts_filename.mac_fonts import MacVersionHelpers


class MacLang(SystemLang):
    __core_foundation = None

    def get_lang() -> str:
        if not MacVersionHelpers.is_mac_version_or_greater(10, 6):
            raise OSNotSupported("get_lang() only works on mac 10.6 or more")

        if MacLang.__core_foundation is None:
            MacLang.__load__core_foundation()

        locale = MacLang.__core_foundation.CFLocaleCopyCurrent()
        identifier = MacLang.__core_foundation.CFLocaleGetIdentifier(locale)
        lang_id = MacLang.__core_foundation.CFLocaleGetWindowsLocaleCodeFromLocaleIdentifier(identifier)

        return Name.get_lang_code_from_platform_lang_id(PlatformID.MICROSOFT, lang_id)


    @staticmethod
    def __load__core_foundation():
        core_foundation_library_name = util.find_library("CoreFoundation")
        # Hack for compatibility with macOS greater or equals to 11.0.
        # From: https://github.com/pyglet/pyglet/blob/a44e83a265e7df8ece793de865bcf3690f66adbd/pyglet/libs/darwin/cocoapy/cocoalibs.py#L10-L14
        if core_foundation_library_name is None:
            core_foundation_library_name = "/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation"
        MacLang.__core_foundation = cdll.LoadLibrary(core_foundation_library_name)

        # https://developer.apple.com/documentation/corefoundation/1542508-cflocalecopycurrent?language=objc
        MacLang.__core_foundation.CFLocaleCopyCurrent.restype = c_void_p
        MacLang.__core_foundation.CFLocaleCopyCurrent.argtypes = []

        # https://developer.apple.com/documentation/corefoundation/1543634-cflocalegetidentifier?language=objc
        MacLang.__core_foundation.CFLocaleGetIdentifier.restype = c_void_p
        MacLang.__core_foundation.CFLocaleGetIdentifier.argtypes = [c_void_p]

        # https://developer.apple.com/documentation/corefoundation/1542147-cflocalegetwindowslocalecodefrom?language=objc
        MacLang.__core_foundation.CFLocaleGetWindowsLocaleCodeFromLocaleIdentifier.restype = c_uint32
        MacLang.__core_foundation.CFLocaleGetWindowsLocaleCodeFromLocaleIdentifier.argtypes = [c_void_p]