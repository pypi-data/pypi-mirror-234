from .request import APIRequest
from .mixins import user, media_post, search


__all__ = [
    "Client",
]


class Client(
    APIRequest,
    user.UserMixin,
    media_post.MediaPostMixin,
    search.SearchMixin,
):
    """ Base class for receiving API data """
    def __init__(
            self,
            token: str
    ) -> None:
        """
        :param token: RAPID api token
        """
        APIRequest.__init__(
            self,
            token=token
        )
