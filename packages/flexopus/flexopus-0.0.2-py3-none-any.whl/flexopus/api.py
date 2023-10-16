import logging
from urllib.parse import urlparse, urlunparse

import aiohttp

_LOGGER = logging.getLogger(__name__)


class FlexopusApi:
    def __init__(self, tenant_url, access_token):
        if tenant_url is None:
            raise AttributeError('tenant_url is None')
        if access_token is None:
            raise AttributeError('access_token is None')
        self._base_url = self.normalize_url(tenant_url)
        self._access_token = access_token

    @property
    def _headers(self):
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self._access_token}",
        }

    async def fetch_location(self, location_id):
        url = f"{self._base_url}/locations/{location_id}/bookables/occupancy"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._headers) as response:
                response.raise_for_status()
                return await response.json()

    async def fetch_buildings(self):
        url = f"{self._base_url}/buildings"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._headers) as response:
                response.raise_for_status()
                return await response.json()

    async def get_locations(self):
        buildings = await self.fetch_buildings()
        return {
            str(l['id']): b['name'] + ' - ' + l['name']
                for b in buildings['data']
                    for l in b['locations']
        }

    def normalize_url(self, tenant_url):
        tenant_url = tenant_url.strip()
        parsed_url = urlparse(tenant_url)

        return urlunparse(
            (parsed_url.scheme, parsed_url.netloc, "/api/v1", None, None, None)
        )
