"""API in support of HomeLINK."""
from typing import List

from .alert import Alert
from .auth import AbstractAuth
from .const import ATTR_RESULTS, HomeLINKEndpoint
from .device import Device
from .lookup import Lookup
from .property import Property
from .utils import check_status


class HomeLINKApi:
    """HomeLINK API"""

    def __init__(self, auth: AbstractAuth) -> None:
        """Initialise the api."""
        self.auth = auth

    async def async_get_properties(self) -> List[Property]:
        """Return the Properties."""
        resp = await self.auth.request("get", HomeLINKEndpoint.PROPERTIES)
        check_status(resp.status)
        return [
            Property(property_data, self.auth)
            for property_data in (await resp.json())[ATTR_RESULTS]
        ]

    async def async_get_property(self, propertyreference) -> Property:
        """Return the Properties."""
        resp = await self.auth.request(
            "get",
            HomeLINKEndpoint.PROPERTY.format(propertyreference=propertyreference),
        )
        check_status(resp.status)
        return Property(await resp.json(), self.auth)

    async def async_get_property_devices(self, propertyreference) -> List[Device]:
        """Return the Property Devices."""
        resp = await self.auth.request(
            "get",
            HomeLINKEndpoint.PROPERTY_DEVICES.format(
                propertyreference=propertyreference
            ),
        )
        check_status(resp.status)
        return [
            Device(device_data, self.auth)
            for device_data in (await resp.json())[ATTR_RESULTS]
        ]

    async def async_get_property_alerts(self, propertyreference) -> List[Alert]:
        """Return the Property Alerts."""
        resp = await self.auth.request(
            "get",
            HomeLINKEndpoint.PROPERTY_ALERTS.format(
                propertyreference=propertyreference
            ),
        )
        check_status(resp.status)
        return [
            Alert(alert_data, self.auth)
            for alert_data in (await resp.json())[ATTR_RESULTS]
        ]

    async def async_add_property_tags(self, propertyreference, tags) -> List[str]:
        """Add tags to a property."""
        resp = await self.auth.request(
            "put",
            HomeLINKEndpoint.PROPERTY_TAGS.format(propertyreference=propertyreference),
            json={"tagIds": tags},
        )
        check_status(resp.status)
        return await resp.json()

    async def async_delete_property_tags(self, propertyreference, tags) -> List[str]:
        """Delete tags from a property."""
        resp = await self.auth.request(
            "delete",
            HomeLINKEndpoint.PROPERTY_TAGS.format(propertyreference=propertyreference),
            json={"tagIds": tags},
        )
        check_status(resp.status)
        return await resp.json()

    async def async_get_devices(self) -> List[Device]:
        """Return the Properties."""
        resp = await self.auth.request("get", HomeLINKEndpoint.DEVICES)
        check_status(resp.status)
        return [
            Device(device_data, self.auth)
            for device_data in (await resp.json())[ATTR_RESULTS]
        ]

    async def async_get_device(self, serialnumber) -> Device:
        """Return the Properties."""
        resp = await self.auth.request(
            "get", HomeLINKEndpoint.DEVICE.format(serialnumber=serialnumber)
        )
        check_status(resp.status)
        return Device(await resp.json(), self.auth)

    async def async_get_device_alerts(self, serialnumber) -> List[Alert]:
        """Return the Device Alerts."""
        resp = await self.auth.request(
            "get",
            HomeLINKEndpoint.DEVICES_ALERTS.format(serialnumber=serialnumber),
        )
        check_status(resp.status)
        return [
            Alert(alert_data, self.auth)
            for alert_data in (await resp.json())[ATTR_RESULTS]
        ]

    async def async_get_lookups(self, lookuptype) -> List[Lookup]:
        """Return the Lookups for lookuptype"""
        resp = await self.auth.request(
            "get", HomeLINKEndpoint.LOOKUPS.format(lookuptype=lookuptype)
        )
        check_status(resp.status)
        return [Lookup(lookup_data, self.auth) for lookup_data in await resp.json()]

    async def async_get_lookup(self, lookuptype, lookupid) -> Lookup:
        """Return the Lookups for lookuptype"""
        resp = await self.auth.request(
            "get",
            HomeLINKEndpoint.LOOKUP.format(lookuptype=lookuptype, lookupid=lookupid),
        )
        check_status(resp.status)
        return Lookup(await resp.json(), self.auth)
