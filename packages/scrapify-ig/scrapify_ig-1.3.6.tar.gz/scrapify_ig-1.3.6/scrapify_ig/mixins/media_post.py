from http import HTTPMethod

import requests

from scrapify_ig import types


__all__ = [
    "MediaPostMixin",
]


class MediaPostMixin(object):
    """
    Used to process Instagram media posts

    @DynamicAttrs
    """

    def get_media_info(self, code_or_id_or_url: str) -> types.MediaPost:
        """
        Get post details for feed posts, reels, stories or tv posts.
        Posts accepted have URL with /p/ or /reel/ or /tv/ or /stories/ (e.g. instagram.com/p/CxYQJO8xuC6/).
        """
        response: requests.Response = self.api_request(
            url="/post_info",
            method=HTTPMethod.GET,
            params={
                "code_or_id_or_url": code_or_id_or_url
            }
        )
        return types.MediaPost(**response.json()["data"])

    def get_media_comments_chunk(
            self,
            code_or_id_or_url: str,
            pagination_token: str = None
    ) -> types.CommentsChunk:
        """
        Get list of comments of a post. Up to 15 comments at a time.
        This endpoint is paginated. Use the token from the previous request to retrieve the continuation of the list. Leave empty in the first request.
        """
        response: requests.Response = self.api_request(
            url="/comments",
            method=HTTPMethod.GET,
            params={
                "code_or_id_or_url": code_or_id_or_url,
                "pagination_token": pagination_token
            }
        )
        return types.CommentsChunk(
            **response.json(),
            client=self,
            media_identifier=code_or_id_or_url
        )

    def get_comment_thread_chunk(
            self,
            comment_id: str,
            pagination_token: str = None
    ) -> types.CommentsThreadChunk:
        """
        Get list of nested comments (also called child comments or comments thread). Up to 50 at a time.
        From the Comments endpoint, you will know if there are child comments
        based on the child_comment_count field in each comment.
        If child_comment_count == 0, this endpoint will raise HTTPNotFoundError.
        This endpoint is paginated. Use the token from the previous request to retrieve the continuation of the list.
        Leave empty in the first request.
        """
        response: requests.Response = self.api_request(
            url="/comments_thread",
            method=HTTPMethod.GET,
            params={
                "comment_id": comment_id,
                "pagination_token": pagination_token
            }
        )
        return types.CommentsThreadChunk(
            **response.json(),
            client=self,
            commend_id=comment_id
        )

    def get_medias_by_hashtag_chunk(
            self,
            hashtag: str,
            pagination_token: str = None
    ) -> types.MediaPostsHashtagChunk:
        response: requests.Response = self.api_request(
            url="/hashtag",
            method=HTTPMethod.GET,
            params={
                "hashtag": hashtag,
                "pagination_token": pagination_token
            }
        )
        return types.MediaPostsHashtagChunk(
            **response.json(),
            client=self,
            hashtag=hashtag
        )

    def get_tagged_medias_chunk(
            self,
            username_or_id_or_url: str,
            pagination_token: str = None
    ) -> types.TaggedMediaPostsChunk:
        """
        Get user tagged posts (posts where user was tagged). 12 posts at a time.
        This endpoint is paginated. Use the token from the previous request to retrieve the continuation of the list.
        Leave empty in the first request.
        """

        response: requests.Response = self.api_request(
            url="/tagged",
            method=HTTPMethod.GET,
            params={
                "username_or_id_or_url": username_or_id_or_url,
                "pagination_token": pagination_token
            }
        )
        return types.TaggedMediaPostsChunk(
            **response.json(),
            client=self,
            user_identifier=username_or_id_or_url
        )
