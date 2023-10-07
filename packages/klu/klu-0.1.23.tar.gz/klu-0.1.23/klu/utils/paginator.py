from typing import Optional

from klu.api.client import APIClient

DEFAULT_PAGE_SIZE = 100


class Paginator:
    def __init__(self, endpoint, limit=DEFAULT_PAGE_SIZE):
        self.endpoint = endpoint

        self.limit = limit
        self.current_page = 0
        self.total_count = None
        self.has_next_page = True

    async def _get_paginated_results(
        self,
        api_client: APIClient,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        **params,
    ):
        limit = limit if limit is not None else self.limit
        skip = skip if skip is not None else self.current_page * limit

        if offset is not None:
            skip = skip + offset

        # Make API request with skip, limit, and additional parameters
        response = await api_client.get(
            self.endpoint, {**params, "skip": skip, "limit": limit}
        )
        results = response.get("data", [])

        self.total_count = response.get("total_count", 0)
        self.has_next_page = response.get("has_next_page", False)

        return results

    async def fetch_all(self, api_client: APIClient, limit: Optional[int] = None):
        results = []
        self._reset_paginator()

        while self.has_next_page:
            results.extend(await self._get_paginated_results(api_client, limit=limit))
            self.current_page += 1

        self._reset_paginator()
        return results

    async def fetch_single_page(
        self, api_client: APIClient, page_number: int, limit: Optional[int] = None
    ):
        self._reset_paginator()

        limit = self.limit if limit is None else limit
        skip = (page_number - 1) * limit

        results = await self._get_paginated_results(api_client, skip=skip, limit=limit)

        self._reset_paginator()
        return results

    async def fetch_next_page(
        self,
        api_client: APIClient,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        if not self.has_next_page:
            return []

        curr_page_results = await self._get_paginated_results(
            api_client, limit=limit, offset=offset
        )
        self.current_page += 1

        return curr_page_results

    def _reset_paginator(self):
        self.current_page = 0
        self.total_count = None
        self.has_next_page = True
