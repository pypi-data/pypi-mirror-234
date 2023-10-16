import aiohttp
from datetime import datetime

class TastyIgniter:
    """Python library to interface with TastyIgniter order platform."""
    def __init__(
        self, 
        username:str,
        password:str,
        domain:str,
        session:aiohttp.ClientSession=None,
    ):
        """Initialize the API connection."""

        self.session = session if session else aiohttp.ClientSession()
        self.username = username
        self.password = password
        self.api_url = f"https://{domain}/api/"
        self.api_key = None

    async def authenticate_user(self):
        """Authenticate user and save API Key."""
        REQUEST_URL = self.api_url + "admin/token"
        params = {
            "username": self.username,
            "password": self.password,
            "device_name": "call_alert",
        }

        try:
            async with self.session.post(
                REQUEST_URL,
                data=params,
            ) as resp:
                response = await resp.json()
        except aiohttp.ClientConnectionError as error:
            raise ConnectionError(error)

        if response.get("status_code") != 201:
            raise AuthenticationError()

        self.api_key = response.get("token")

    async def get_response(self, request_url: str, params:dict=None):
        """Get and return JSON payload from TastyIgniter endpoint."""
        if not self.api_key:
            await self.authenticate_user()

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        try:
            async with self.session.get(
                request_url,
                headers=headers,
                params=params,
            ) as resp:
                response = await resp.json()
        except aiohttp.ClientConnectionError as error:
            raise ConnectionError(error)
        
        return response

    async def get_locations(self):
        """Retrieve a list of locations."""
        REQUEST_URL = self.api_url + "locations"
        params = {"pageLimit":1000}
        response = await self.get_response(REQUEST_URL, params)
        return response.get("data")

    async def get_enabled_locations(self):
        """Return only restaurants which are enabled."""
        locations = await self.get_locations()
        enabled_locations = []

        for location in locations:
            if location["location_status"]:
                enabled_locations.append(location)

        return enabled_locations

    async def get_orders(self):
        """Retrieve a list of orders."""
        REQUEST_URL = self.api_url + "orders"
        params = {
            "pageLimit": 10,
            "sort": "date_added desc",
        }
        response = await self.get_response(REQUEST_URL, params)
        return response.get("data")

    async def get_received_orders(self):
        """Return only orders in Received status (status_id=1)."""
        orders = await self.get_orders()
        r_orders = []

        for order in orders:
            if order["status_id"] == 1:
                r_orders.append(order)

        return r_orders
                
