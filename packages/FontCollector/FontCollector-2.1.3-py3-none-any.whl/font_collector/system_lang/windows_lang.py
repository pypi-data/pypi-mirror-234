from ..exceptions import OSNotSupported
from ..font.name import Name, PlatformID
from .system_lang import SystemLang
from ctypes import windll, wintypes
from find_system_fonts_filename.windows_fonts import WindowsVersionHelpers
from sys import getwindowsversion


class WindowsLang(SystemLang):
    __kernel32 = None

    def get_lang() -> str:
        windows_version = getwindowsversion()

        if not WindowsVersionHelpers.is_windows_version_or_greater(windows_version, 5, 0, 0):
            raise OSNotSupported("get_lang() only works on Windows 2000 or more")

        if WindowsLang.__kernel32 is None:
            WindowsLang.__load_kernel32()

        lang_id = WindowsLang.__kernel32.GetUserDefaultLangID()
        return Name.get_lang_code_from_platform_lang_id(PlatformID.MICROSOFT, lang_id)


    @staticmethod
    def __load_kernel32():
        WindowsLang.__kernel32 = windll.kernel32

        # https://learn.microsoft.com/en-us/windows/win32/api/winnls/nf-winnls-getuserdefaultlangid
        WindowsLang.__kernel32.GetUserDefaultLangID.restype = wintypes.LANGID
        WindowsLang.__kernel32.GetUserDefaultLangID.argtypes = []