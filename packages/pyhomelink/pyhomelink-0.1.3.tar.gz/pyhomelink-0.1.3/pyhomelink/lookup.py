"""Python module for accessing HomeLINK Lookup."""
from .auth import AbstractAuth


class Lookup:
    """Lookup is the instantiation of a HomeLINK Lookup"""

    def __init__(self, raw_data: dict, auth: AbstractAuth):
        """Initialize the property."""
        self._raw_data = raw_data
        self._auth = auth

    @property
    def lookupid(self) -> str:
        """Return the id of the Lookup"""
        return self._raw_data["id"]

    @property
    def code(self) -> str:
        """Return the codet of the Lookup"""
        return self._raw_data["code"]

    @property
    def name(self) -> str:
        """Return the name of the Lookup"""
        return self._raw_data["name"]

    @property
    def description(self) -> str:
        """Return the descriptionof the Lookup"""
        return self._raw_data["description"]

    @property
    def active(self) -> bool:
        """Return the active of the Lookup"""
        return self._raw_data["active"]
