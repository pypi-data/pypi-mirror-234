from abc import ABC, abstractmethod
from typing import Optional, Set


class SystemLang(ABC):
    @staticmethod
    @abstractmethod
    def get_lang() -> Optional[str]:
        """
        Return an str of the system language. Ex: "en-US"
        If the system language couldn't be found, it return None
        """
        pass