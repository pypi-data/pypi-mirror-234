from __future__ import annotations
import json
from aiohttp.client import ClientSession
from math import ceil
from pathlib import Path
from pydantic.decorator import validate_arguments
from typing import Optional, Union, Dict, List, Any

import asyncio
import datetime as dt
import sys


try:
    from ._base import APIKeyClient, AsyncAPIKeyClient, JSONResponse
    from ._schemas import certronic as cert_schema
except ImportError:
    from _base import APIKeyClient, AsyncAPIKeyClient, JSONResponse
    from _schemas import certronic as cert_schema

if (sys.platform.startswith('win')
        and sys.version_info[0] == 3
        and sys.version_info[1] >= 8):
    policy = asyncio.WindowsSelectorEventLoopPolicy()
    asyncio.set_event_loop_policy(policy)


class Client(APIKeyClient):

    __name__ = "Certronic"

    def __enter__(self, *args, **kwargs) -> Client:
        return super().__enter__(*args, **kwargs)

    @validate_arguments
    def get_employees(
        self,
        page: Optional[int] = 1,
        pageSize: Optional[int] = 50,
        updatedFrom: Optional[dt.datetime] = None,
        includeDocuments: Optional[bool] = None,
        customFields: Optional[List[str]] = None,
        inactive: Optional[bool] = None,
        dni: Optional[Union[int, str]] = None,
        **kwargs
    ) -> Union[Dict, List]:
        """ Get employees from Certronic API with client.get()

        Args:
            page (Optional[int], optional): Page number. Defaults to 1.
            pageSize (Optional[int], optional):
                Max results per page.
                Defaults to 50.
            updatedFrom (Optional[Union[dt.datetime, str]], optional):
                Datetime to apply as start filter of employees.
                Defaults to None.
            includeDocuments (bool, optional):
                Boolean to get documents detail.
                Defaults to None.
            customFields (Optional[List[Union[int, str]]], optional):
                List of Custom fields to get from employe.
                Defaults to None.

        Returns:
            Union[Dict, List]: List of JSON employees obtained from Certronic
        """

        # datetime to str
        if isinstance(updatedFrom, dt.datetime):
            updatedFrom = updatedFrom.strftime("%Y-%m-%d %H:%M:%S")

        # foce None if is False
        if not includeDocuments:
            includeDocuments = None
        if not inactive:
            inactive = None

        # parameters prepare
        params = {
            "updatedFrom": updatedFrom,
            "includeDocuments": includeDocuments,
            "customFields": customFields,
            "inactive": inactive,
            "pageSize": pageSize,
            "page": page,
            "dni": dni
        }

        # request.get -> json
        return self.get(path='employees.php', params=params, **kwargs)

    @validate_arguments
    def post_clockings(
        self,
        clockings: cert_schema.ClockingList,
        **kwargs
    ) -> Union[Dict, List]:
        """ Send clockings to Certronic API

        Args:
            clockings (cert_schema.ClockingList):
                List of clockings cert_schema.Clocking

        Returns:
            Union[Dict, List]: JSON Certronic API response.
        """

        # return response
        return self.post(
            path='clocking.php',
            json={"clockings": json.loads(clockings.json())},
            **kwargs
        )


class AsyncClient(AsyncAPIKeyClient):

    __name__ = "Certronic"

    async def __aenter__(self, *args, **kwargs) -> AsyncClient:
        return await super().__aenter__(*args, **kwargs)

    @validate_arguments
    async def get_employees(
        self,
        page: Optional[int] = 1,
        pageSize: Optional[int] = None,
        updatedFrom: Optional[Union[dt.datetime, str]] = None,
        includeDocuments: Optional[bool] = None,
        customFields: Optional[List[str]] = None,
        inactive: Optional[bool] = None,
        dni: Optional[Union[int, str]] = None,
        all_pages: Optional[bool] = None,
        **kwargs
    ) -> JSONResponse:

        if isinstance(updatedFrom, dt.datetime):
            updatedFrom = updatedFrom.strftime("%Y-%m-%d %H:%M:%S")

        # foce None if is False
        if not includeDocuments: includeDocuments = None
        if not inactive: inactive = None

        # parameters prepare
        params = {
            "updatedFrom": updatedFrom,
            "includeDocuments": includeDocuments,
            "customFields": customFields,
            "inactive": inactive,
            "pageSize": pageSize or self.defaults.PAGE_SIZE,
            "page": page,
            "dni": dni
        }

        # request.get -> json
        employees = await self.get(
            path='employees.php',
            params=params,
            **kwargs
        )

        if not all_pages:
            return employees

        _count = employees.get('count', 0)
        _pageSize = int(employees.get('pageSize', self.defaults.PAGE_SIZE))

        # calculate pages number
        _pages = ceil(_count / _pageSize) if _count else 1

        if _pages > 1:
            # remove page of params
            params.pop('page', None)

            coroutines = [self.get(
                path='employees.php',
                params={**params, 'page': i},
                **kwargs
            ) for i in range(2, _pages + 1)]

            tasks = self.get_async_tasks(*coroutines)
            responses = await asyncio.gather(*tasks)

            for child_response in responses:
                employees['employees'].extend(child_response.get('employees'))

        return employees

    @validate_arguments
    async def post_clockings(
        self,
        clockings: cert_schema.ClockingList,
        **kwargs
    ) -> Union[Dict, List]:

        # return response
        return await self.post(
            path='clocking.php',
            json={"clockings": json.loads(clockings.json())},
            **kwargs
        )
