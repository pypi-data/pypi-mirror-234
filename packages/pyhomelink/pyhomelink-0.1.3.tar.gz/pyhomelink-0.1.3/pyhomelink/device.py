"""Python module for accessing HomeLINK Device."""
from datetime import datetime
from typing import List

from .alert import Alert
from .auth import AbstractAuth
from .const import ATTR_RESULTS
from .utils import check_status, parse_date


class Device:
    """Device is the instantiation of a HomeLINK Device"""

    def __init__(self, raw_data: dict, auth: AbstractAuth):
        """Initialize the property."""
        self._raw_data = raw_data
        self._auth = auth

    @property
    def serialnumber(self) -> str:
        """Return the serialnumber of the Device"""
        return self._raw_data["serialNumber"]

    @property
    def createdate(self) -> datetime:
        """Return the createdat of the Device"""
        return parse_date(self._raw_data["createdAt"])

    @property
    def updatedat(self) -> datetime:
        """Return the updatedat of the Device"""
        return parse_date(self._raw_data["updatedAt"])

    @property
    def model(self) -> str:
        """Return the model of the Device"""
        return self._raw_data["model"]

    @property
    def modeltype(self) -> str:
        """Return the modeltype of the Device"""
        return self._raw_data["modelType"]

    @property
    def location(self) -> str:
        """Return the location of the Device"""
        return self._raw_data["location"]

    @property
    def locationnickname(self) -> str:
        """Return the locationnickname of the Device"""
        return self._raw_data["locationNickname"]

    @property
    def manufacturer(self) -> str:
        """Return the manufacturer of the Device"""
        return self._raw_data["manufacturer"]

    @property
    def installationdate(self) -> datetime:
        """Return the installationdate of the Device"""
        return parse_date(self._raw_data["installationDate"])

    @property
    def installedby(self) -> str:
        """Return the installedby of the Device"""
        return self._raw_data["installedBy"]

    @property
    def replacedate(self) -> datetime:
        """Return the replacedate of the Device"""
        return parse_date(self._raw_data["replaceDate"])

    @property
    def metadata(self) -> any:
        """Return the metadata of the Device"""
        return self.Metadata(self._raw_data["metadata"])

    @property
    def status(self) -> any:
        """Return the tags of the Device"""
        return self.Status(self._raw_data["status"])

    @property
    def rel(self) -> any:
        """Return the tags of the Device"""
        return self.Rel(self._raw_data["_rel"])

    class Metadata:
        """Metadata for property."""

        def __init__(self, raw_data):
            """Initialise Metadata"""
            self._raw_data = raw_data

        @property
        def signalstrength(self) -> str:
            """Return the signalstrength of the Device"""
            return self._raw_data["signalStrength"]

        @property
        def lastseendate(self) -> datetime:
            """Return the lastseendate of the Device"""
            return parse_date(self._raw_data["lastSeenDate"])

        @property
        def connectivitytype(self) -> str:
            """Return the connectivitytype of the Device"""
            return self._raw_data["connectivityType"]

    class Status:
        """Status for property."""

        def __init__(self, raw_data):
            """Initialise Status"""
            self._raw_data = raw_data

        @property
        def operationalstatus(self) -> str:
            """Return the operationalstatus of the Device"""
            return self._raw_data["operationalStatus"]

        @property
        def lasttesteddate(self) -> datetime:
            """Return the lasttesteddate of the Device"""
            return parse_date(self._raw_data["lastTestedDate"])

        @property
        def datacollectionstatus(self) -> str:
            """Return the datacollectionstatus of the Device"""
            return self._raw_data["dataCollectionStatus"]

    class Rel:
        """Relative URLs for property."""

        def __init__(self, raw_data):
            """Initialise _Rel."""
            self._raw_data = raw_data

        @property
        def self(self) -> str:
            """Return the self url of the Device"""
            return self._raw_data["_self"]

        @property
        def hl_property(self) -> str:
            """Return the property url of the Device"""
            return self._raw_data["property"]

        @property
        def alerts(self) -> str:
            """Return the alerts url of the Device"""
            return self._raw_data["alerts"]

    async def async_get_alerts(self) -> List[Alert]:
        """Return the Alerts."""
        resp = await self._auth.request("get", f"{self.rel.alerts}")
        check_status(resp.status)
        return [
            Alert(alert_data, self._auth)
            for alert_data in (await resp.json())[ATTR_RESULTS]
        ]
