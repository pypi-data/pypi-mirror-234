from http import HTTPMethod

import requests

from scrapify_ig import types


__all__ = [
    "SearchMixin",
]


class SearchMixin(object):
    """
    Used to search hashtags, users or places.

    @DynamicAttrs
    """
    def search(self, search_query: str) -> types.SearchResult:
        """ Search Users, Hashtags and Places by query param. """
        response: requests.Response = self.api_request(
            url="/search",
            method=HTTPMethod.GET,
            params={
                "search_query": search_query
            }
        )
        return types.SearchResult(**response.json()["data"])
