from ..exceptions import OSNotSupported
from platform import system


def get_lang() -> str:
    system_name = system()

    if system_name == "Windows":
        from .windows_lang import WindowsLang
        return WindowsLang.get_lang()

    elif system_name == "Linux":
        from .linux_lang import LinuxLang
        return LinuxLang.get_lang()

    elif system_name == "Darwin":
        from .mac_lang import MacLang
        return MacLang.get_lang()

    else:
        raise OSNotSupported("get_lang() only works on Windows, Mac and Linux.")