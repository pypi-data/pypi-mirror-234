"""base.py."""
from abc import ABC, abstractmethod
from typing import Optional


class ConfigSource(ABC):
    """Base class for configuration source classes.

    Methods
    -------
    get(key: str, profile: Optional[str])
        retrieves the value for the given configuration parameter
    set(profile: str, overwrite: bool, **params)
        updates existing configuration with the key-value pairs from `**params`.
    """

    @abstractmethod
    def get(self, key: str, profile: Optional[str]) -> Optional[str]:
        pass

    @abstractmethod
    def set(self, profile: str = "default", overwrite: bool = False, **params):
        pass
