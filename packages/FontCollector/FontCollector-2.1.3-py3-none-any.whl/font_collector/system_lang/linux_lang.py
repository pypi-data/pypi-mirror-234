from .system_lang import SystemLang
from locale import getdefaultlocale
from typing import Optional

class LinuxLang(SystemLang):

    def get_lang() -> Optional[str]:
        lang, = getdefaultlocale()
        return lang
