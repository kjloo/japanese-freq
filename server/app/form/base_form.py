from abc import ABC, abstractmethod


class BaseForm(ABC):
    def __init__(self):
        self._validate()

    @abstractmethod
    def _validate(self):
        """
        Validate the form data.
        """
        pass
