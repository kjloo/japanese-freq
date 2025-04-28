from abc import ABC, abstractmethod


class BaseModel(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def to_dict(self) -> dict[str]:
        """
        Convert the form data to a dictionary.
        """
        pass

    @abstractmethod
    def get_key(self) -> dict[str]:
        """
        Get the key for the form data.
        """
        pass
