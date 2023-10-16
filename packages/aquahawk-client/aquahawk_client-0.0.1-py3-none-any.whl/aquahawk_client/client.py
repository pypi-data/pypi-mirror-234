"""Define a base client for interacting with AquaHawk."""
import datetime
import json
import time
import urllib.parse
from typing import Dict, Optional

import aiohttp
import pytz
from yarl import URL

from .types import Interval, Usage


class AquaHawkClient:
    def __init__(
        self,
        account_number,
        hostname,
        username,
        password,
        session: Optional[aiohttp.ClientSession] = None,
        http_schema: str = "https",
    ):
        self.account_number = account_number
        self.hostname = hostname
        self.username = username
        self.password = password
        self.http_schema = http_schema

        self._session = session or aiohttp.ClientSession()
        self._session._base_url = URL(f"{self.http_schema}://{self.hostname}")

    async def http_get_request(self, uri: str, headers: Dict[str, str]) -> str:
        """
        Sends an HTTP GET request to the specified URI with the given headers.

        Args:
            uri (str): The URI to send the request to.
            headers (Dict[str, str]): The headers to include in the request.

        Returns:
            str: The response text from the server.

        Raises:
            HTTPError: If the response status code is not in the 200-299 range.
        """
        async with self._session.get(uri, headers=headers) as response:
            response.raise_for_status()
            return await response.text()

    async def http_post_request(self, uri, headers, data):
        """
        Sends an HTTP POST request.

        Args:
            uri (str): The URI to send the request to.
            headers (dict): The headers to include in the request.
            data (bytes): The data to include in the request body.

        Returns:
            The response object from the server.
        """
        async with self._session.post(uri, headers=headers, data=data) as response:
            response.raise_for_status()
            return await response.json()

    async def get_usage(
        self,
        startTime: datetime.datetime,
        endTime: datetime.datetime,
        interval: Interval = Interval.ONE_DAY,
    ):
        """
        Retrieves water usage data for a specified time range and interval.

        Args:
            startTime (datetime.datetime): The start time of the time range.
            endTime (datetime.datetime): The end time of the time range.
            interval (aquahawk_types.Interval, optional):
                The interval at which to retrieve data.
                Defaults to aquahawk_types.Interval.ONE_DAY.
                The interval at which to retrieve data.
                Defaults to aquahawk_types.Interval.ONE_DAY.

        Returns:
            aquahawk_types.Usage: The water usage data for the specified time
                range and interval.
        """
        await self.authenticate()

        metrics = {
            "waterUse": True,
            "waterUseReading": True,
            "temperature": True,
            "rainfall": True,
        }

        params = {
            "_dc": int(time.time()),
            "districtName": self.hostname.split(".")[0],
            "accountNumber": self.account_number,
            "startTime": startTime.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "endTime": endTime.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "interval": interval.value,
            "extraStartTime": "true",
            "extraEndTime": "true",
            "metrics": json.dumps(metrics),
        }

        query_string = urllib.parse.urlencode(params)

        jsonText = await self.http_get_request(
            "/timeseries?" + query_string, headers={"accept": "application/json"}
        )
        return Usage.from_json(jsonText)  # pyright: ignore [reportGeneralTypeIssues]

    async def get_usage_today(self) -> Usage:
        """
        Gets the water usage for the current day.

        Creates a start time and end time for the current day, and calls the
        get_usage method with these times. The start time is set to 24 hours
        before the current time, and the end time is set to the current time.

        Returns:
            aquahawk_types.Usage: The water usage for the current day.

        """
        now = datetime.datetime.now(tz=pytz.timezone("UTC"))
        startTime = now - datetime.timedelta(days=1)
        endTime = now

        return await self.get_usage(startTime, endTime)

    async def get_usage_this_year(self) -> Usage:
        """
        Gets the water usage for the current year.

        Creates a start time and end time for the current year, and calls the
        get_usage method with these times and a "1 year" interval.

        Returns:
            aquahawk_types.Usage: The water usage for the current year.

        """
        startTime = datetime.datetime(datetime.date.today().year, 1, 1)
        endTime = datetime.datetime(datetime.date.today().year, 12, 31)

        return await self.get_usage(startTime, endTime, Interval.ONE_YEAR)

    async def authenticate(self):
        """
        Authenticates the client with the server.

        Raises:
            AuthenticationError: If authentication fails.

        Returns:
            None
        """
        headers = {"accept": "application/json"}
        payload = {"username": self.username, "password": self.password}
        json = await self.http_post_request("/login", data=payload, headers=headers)
        if json.get("success") is not True:
            raise AuthenticationError("Authentication failed")


class AuthenticationError(Exception):
    """Raised when authentication fails.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Authentication failed."):
        self.message = message
        super().__init__(self.message)
