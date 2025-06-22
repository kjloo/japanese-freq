from abc import ABC, abstractmethod


class BaseModel(ABC):
    def __init__(self, data: dict[str]):
        """
        Initialize the model with a dictionary.
        :param dict: A dictionary containing the model data.
        """
        self.from_dict(data)

    @abstractmethod
    def to_dict(self) -> dict[str]:
        """
        Convert the form data to a dictionary.
        """
        pass

    @abstractmethod
    def from_dict(self, data: dict[str]):
        """
        Populate the form data from a dictionary.
        :param data: The dictionary containing form data.
        """
        pass

    @abstractmethod
    def get_key(self) -> dict[str]:
        """
        Get the key for the form data.
        """
        pass
