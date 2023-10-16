"""Simplifies interacting with an ActivityPub server / instance.

This is a minimal implementation only implementing some API calls. API
calls supported will likely be expanded over time. However, do not
expect a full or complete implementation of the ActivityPub API.
"""
import asyncio
import json
import logging
import random
import uuid
from typing import Any
from typing import BinaryIO
from typing import Dict
from typing import Final
from typing import List
from typing import Optional
from typing import Tuple
from typing import TypeVar
from typing import Union
from urllib.parse import parse_qs
from urllib.parse import urlencode
from urllib.parse import urlparse

import aiohttp
import arrow
from aiohttp.client_exceptions import ClientError as aiohttp_ClientError

from . import USER_AGENT
from . import Status
from . import __display_name__
from . import __version__

logger = logging.getLogger(__display_name__)


ActivityPubClass = TypeVar("ActivityPubClass", bound="ActivityPub")
REDIRECT_URI: Final[str] = "urn:ietf:wg:oauth:2.0:oob"

# HTTP status codes of interest (more detail at https://en.wikipedia.org/wiki/List_of_HTTP_status_codes)
STATUS_BAD_REQUEST: Final[int] = 400
STATUS_UNAUTHORIZED: Final[int] = 401
STATUS_FORBIDDEN: Final[int] = 403
STATUS_NOT_FOUND: Final[int] = 404
STATUS_CONFLICT: Final[int] = 409
STATUS_GONE: Final[int] = 410
STATUS_UNPROCESSABLE_ENTITY: Final[int] = 422
STATUS_TOO_MANY_REQUESTS: Final[int] = 429
STATUS_INTERNAL_SERVER_ERROR: Final[int] = 500

INSTANCE_TYPE_MASTODON: Final[str] = "Mastodon"
INSTANCE_TYPE_PLEROMA: Final[str] = "Pleroma"
INSTANCE_TYPE_TAKAHE: Final[str] = "takahe"


class ActivityPub:
    """Simplifies interacting with an ActivityPub server / instance.

    This is a minimal implementation only implementing methods needed
    for the function of MastodonAmnesia
    """

    def __init__(
        self: ActivityPubClass,
        instance: str,
        session: aiohttp.ClientSession,
        access_token: str,
    ) -> None:
        """Initialise ActivityPub instance with reasonable default values.

        :param instance: domain name or url to instance to connect to
        :param session: session to use for communicating with instance
        :param access_token: authentication token

        """
        self.instance = instance
        self.authorization = f"Bearer {access_token}"
        self.session = session
        self.pagination: Dict[str, Dict[str, Optional[str]]] = {
            "next": {"max_id": None, "min_id": None},
            "prev": {"max_id": None, "min_id": None},
        }
        self.instance_type = INSTANCE_TYPE_MASTODON  # default until determined otherwise with determine_instance_type()
        self.ratelimit_limit = 300
        self.ratelimit_remaining = 300
        self.ratelimit_reset = arrow.now()
        logger.debug(
            "client_2_server.ActivityPub(instance=%s, session=%s, access_token=<redacted>)",
            instance,
            session,
        )
        logger.debug("client_2_server.ActivityPub() ... version=%s", __version__)

    async def verify_credentials(self: ActivityPubClass) -> Any:
        """Verify the credentials of the user.

        :returns: The response is a JSON object containing the account's information.

        """
        headers = {"Authorization": self.authorization}
        url = f"{self.instance}/api/v1/accounts/verify_credentials"
        try:
            async with self.session.get(url=url, headers=headers) as response:
                logger.debug(
                    "ActivityPub.verify_credentials - response: \n%s",
                    response,
                )
                self.__update_ratelimit(response.headers)
                await ActivityPub.__check_exception(response=response)
                self.__parse_next_prev(links=response.headers.get("Link"))
                json_response = await response.json()
        except aiohttp_ClientError as error:
            raise NetworkError from error

        logger.debug(
            "ActivityPub.verify_credentials -> json_response: \n%s",
            json.dumps(json_response, indent=4),
        )
        return json_response

    async def determine_instance_type(self: ActivityPubClass) -> None:
        """Check if the instance is a Pleroma instance or not."""
        instance = self.instance
        if "http" not in self.instance:
            instance = f"https://{self.instance}"

        try:
            async with self.session.get(url=f"{instance}/api/v1/instance") as response:
                await ActivityPub.__check_exception(response=response)
                response_dict = await response.json()
        except aiohttp_ClientError as error:
            raise NetworkError from error

        logger.debug(
            "ActivityPub.determine_instance_type -> response.dict:\n%s",
            json.dumps(response_dict, indent=4),
        )
        self.instance = instance
        if INSTANCE_TYPE_TAKAHE in response_dict.get("version"):
            self.instance_type = INSTANCE_TYPE_TAKAHE
        elif INSTANCE_TYPE_PLEROMA in response_dict.get("version"):
            self.instance_type = INSTANCE_TYPE_PLEROMA
        logger.debug(
            "ActivityPub.determine_instance_type() ... instance_type=%s",
            self.instance_type,
        )

    async def get_account_statuses(
        self: ActivityPubClass,
        account_id: str,
        max_id: Optional[str] = None,
        min_id: Optional[str] = None,
    ) -> Any:
        """Get statuses of a given account.

        :param account_id: The account ID of the account you want to get the statuses of
        :param max_id: The ID of the last status you want to get
        :param min_id: The ID of the oldest status you want to retrieve

        :returns: A list of statuses.

        """
        logger.debug(
            "ActivityPub.get_account_statuses(account_id=%s, max_id=%s, min_id=%s)",
            account_id,
            max_id,
            min_id,
        )

        await self.__pre_call_checks()

        headers = {"Authorization": self.authorization}
        paging = "?"
        url = f"{self.instance}/api/v1/accounts/{account_id}/statuses"
        if max_id:
            paging += f"max_id={max_id}"
        if min_id:
            if len(paging) > 1:
                paging += "&"
            paging += f"min_id={min_id}"
        if max_id or min_id:
            url += paging
        logger.debug("ActivityPub.get_account_statuses - url = %s", url)
        try:
            async with self.session.get(url=url, headers=headers) as response:
                self.__update_ratelimit(response.headers)
                await ActivityPub.__check_exception(response=response)
                self.__parse_next_prev(links=response.headers.get("Link"))
                result = await response.json()
        except aiohttp_ClientError as error:
            raise NetworkError from error

        logger.debug(
            "ActivityPub.get_account_statuses -> result:\n%s",
            json.dumps(result, indent=4),
        )
        return result

    async def delete_status(
        self: ActivityPubClass,
        status: Union[str, Dict[Any, Any]],
    ) -> Status:
        """Delete a status.

        :param status: The ID of the status you want to delete or a dict containing the status details

        :returns: Status that has just been deleted
        """
        # add random delay of up to 3 seconds in case we are deleting many
        # statuses in a batch
        sleep_for = random.SystemRandom().random() * 3
        logger.debug(
            "ActivityPub.delete_status - status_id = %s - sleep_for = %s",
            status if isinstance(status, str) else status["id"],
            sleep_for,
        )
        await asyncio.sleep(delay=sleep_for)

        if isinstance(status, str):
            status_id = status
        elif isinstance(status, dict):
            status_id = status["id"]
            if self.instance_type == INSTANCE_TYPE_PLEROMA and status["reblogged"]:
                undo_reblog_response = await self.undo_reblog(status=status)
                return undo_reblog_response
            if self.instance_type == INSTANCE_TYPE_PLEROMA and status["favourited"]:
                undo_favourite_response = await self.undo_favourite(status=status)
                return undo_favourite_response

        await self.__pre_call_checks()

        headers = {"Authorization": self.authorization}
        url = f"{self.instance}/api/v1/statuses/{status_id}"
        try:
            async with self.session.delete(url=url, headers=headers) as response:
                self.__update_ratelimit(response.headers)
                await ActivityPub.__check_exception(response=response)
                self.__parse_next_prev(links=response.headers.get("Link"))
                result: Status = await response.json()
        except aiohttp_ClientError as error:
            raise NetworkError from error

        logger.debug(
            "ActivityPub.delete_status -> result:\n%s",
            json.dumps(result, indent=4),
        )
        return result

    async def undo_reblog(
        self: ActivityPubClass, status: Union[str, Dict[Any, Any]]
    ) -> Status:
        """Remove a reblog.

        :param status: The ID of the status you want to delete or a dict containing the status details

        :returns: The response from the server.
        """
        logger.debug(
            "ActivityPub.undo_reblog(status=%s",
            status,
        )

        if isinstance(status, str):
            status_id = status
        elif isinstance(status, dict):
            status_id = status["reblog"]["id"]

        await self.__pre_call_checks()
        headers = {"Authorization": self.authorization}
        url = f"{self.instance}/api/v1/statuses/{status_id}/unreblog"
        try:
            async with self.session.post(url=url, headers=headers) as response:
                self.__update_ratelimit(response.headers)
                await ActivityPub.__check_exception(response=response)
                self.__parse_next_prev(links=response.headers.get("Link"))
                result: Status = await response.json()
        except aiohttp_ClientError as error:
            raise NetworkError from error

        logger.debug(
            "ActivityPub.undo_reblog -> result:\n%s",
            json.dumps(result, indent=4),
        )
        return result

    async def undo_favourite(
        self: ActivityPubClass,
        status: Union[str, Dict[Any, Any]],
    ) -> Status:
        """Remove a favourite.

        :param status: The ID of the status you want to delete or a dict containing the status details

        :returns: The Status that has just been un-favourited.
        """
        logger.debug(
            "ActivityPub.undo_favourite(status=%s)",
            status,
        )

        if isinstance(status, str):
            status_id = status
        elif isinstance(status, dict):
            status_id = status["id"]

        await self.__pre_call_checks()
        headers = {"Authorization": self.authorization}
        url = f"{self.instance}/api/v1/statuses/{status_id}/unfavourite"
        try:
            async with self.session.post(url=url, headers=headers) as response:
                self.__update_ratelimit(response.headers)
                await ActivityPub.__check_exception(response=response)
                self.__parse_next_prev(links=response.headers.get("Link"))
                result: Status = await response.json()
        except aiohttp_ClientError as error:
            raise NetworkError from error

        logger.debug(
            "ActivityPub.undo_favourite -> result:\n%s",
            json.dumps(result, indent=4),
        )
        return result

    @staticmethod
    async def generate_authorization_url(
        instance_url: str,
        client_id: str,
        user_agent: str = USER_AGENT,
    ) -> str:
        """Create URL to get access token interactively from website.

        :param instance_url: The URL of the Mastodon instance you want to connect to
        :param client_id: Client id of app as generated by create_app method
        :param user_agent: User agent identifier to use. Defaults to minimal_activitypub related one.

        :returns: String containing URL to visit to get access token interactively from instance.
        """
        logger.debug(
            "ActivityPub.get_auth_token_interactive(instance_url=%s, session=...,client_id=%s, user_agent=%s)",
            instance_url,
            client_id,
            user_agent,
        )
        if "http" not in instance_url:
            instance_url = f"https://{instance_url}"

        url_params = urlencode(
            {
                "response_type": "code",
                "client_id": client_id,
                "redirect_uri": REDIRECT_URI,
                "scope": "read write",
            }
        )
        auth_url = f"{instance_url}/oauth/authorize?{url_params}"
        logger.debug(
            "ActivityPub.get_auth_token_interactive(...) -> %s",
            auth_url,
        )

        return auth_url

    @staticmethod
    async def validate_authorization_code(
        session: aiohttp.ClientSession,
        instance_url: str,
        authorization_code: str,
        client_id: str,
        client_secret: str,
    ) -> str:
        """Validate an authorization code and get access token needed for API access.

        :param session: aiohttp.ClientSession
        :param instance_url: The URL of the Mastodon instance you want to connect to
        :param authorization_code: authorization code
        :param client_id: client id as returned by create_app method
        :param client_secret: client secret as returned by create_app method

        :returns: access token
        """
        logger.debug(
            "ActivityPub.validate_authorization_code(authorization_code=%s, client_id=%s, client_secret=<redacted>)",
            authorization_code,
            client_id,
        )
        if "http" not in instance_url:
            instance_url = f"https://{instance_url}"

        form_data = aiohttp.FormData()
        form_data.add_field("client_id", client_id)
        form_data.add_field("client_secret", client_secret)
        form_data.add_field("scope", "read write")
        form_data.add_field("redirect_uri", REDIRECT_URI)
        form_data.add_field("grant_type", "authorization_code")
        form_data.add_field("code", authorization_code)
        try:
            async with session.post(
                url=f"{instance_url}/oauth/token",
                data=form_data,
            ) as response:
                logger.debug(
                    "ActivityPub.validate_authorization_code - response:\n%s",
                    response,
                )
                await ActivityPub.__check_exception(response)
                response_dict = await response.json()
        except aiohttp_ClientError as error:
            raise NetworkError from error

        logger.debug(
            "ActivityPub.validate_authorization_code - response.json: \n%s",
            json.dumps(response_dict, indent=4),
        )
        return str(response_dict["access_token"])

    @staticmethod
    async def get_auth_token(  # noqa: PLR0913  - No way around needing all this parameters
        instance_url: str,
        username: str,
        password: str,
        session: aiohttp.ClientSession,
        user_agent: str = USER_AGENT,
        client_website: str = "https://pypi.org/project/minimal-activitypub/",
    ) -> str:
        """Create an app and use it to get an access token.

        :param instance_url: The URL of the Mastodon instance you want to connect to
        :param username: The username of the account you want to get an auth_token for
        :param password: The password of the account you want to get an auth_token for
        :param session: aiohttp.ClientSession
        :param user_agent: User agent identifier to use. Defaults to minimal_activitypub related one.
        :param client_website: Link to site for user_agent. Defaults to link to minimal_activitypub on Pypi.org

        :returns: The access token is being returned.
        """
        logger.debug(
            "ActivityPub.get_auth_token(instance_url=%s, username=%s, password=<redacted>, session=..., "
            "user_agent=%s, client_website=%s)",
            instance_url,
            username,
            user_agent,
            client_website,
        )
        if "http" not in instance_url:
            instance_url = f"https://{instance_url}"

        client_id, client_secret = await ActivityPub.create_app(
            client_website=client_website,
            instance_url=instance_url,
            session=session,
            user_agent=user_agent,
        )

        form_data = aiohttp.FormData()
        form_data.add_field("client_id", client_id)
        form_data.add_field("client_secret", client_secret)
        form_data.add_field("scope", "read write")
        form_data.add_field("redirect_uris", REDIRECT_URI)
        form_data.add_field("grant_type", "password")
        form_data.add_field("username", username)
        form_data.add_field("password", password)
        try:
            async with session.post(
                url=f"{instance_url}/oauth/token",
                data=form_data,
            ) as response:
                logger.debug(
                    "ActivityPub.get_auth_token - response:\n%s",
                    response,
                )
                await ActivityPub.__check_exception(response)
                response_dict = await response.json()
        except aiohttp_ClientError as error:
            raise NetworkError from error

        logger.debug(
            "ActivityPub.get_auth_token - response.json: \n%s",
            json.dumps(response_dict, indent=4),
        )
        return str(response_dict["access_token"])

    @staticmethod
    async def create_app(
        instance_url: str,
        session: aiohttp.ClientSession,
        user_agent: str = USER_AGENT,
        client_website: str = "https://pypi.org/project/minimal-activitypub/",
    ) -> Tuple[str, str]:
        """Create an app.

        :param instance_url: The URL of the Mastodon instance you want to connect to
        :param session: aiohttp.ClientSession
        :param user_agent: User agent identifier to use. Defaults to minimal_activitypub related one.
        :param client_website: Link to site for user_agent. Defaults to link to minimal_activitypub on Pypi.org

        :returns: tuple(client_id, client_secret)
        """
        logger.debug(
            "ActivityPub.create_app(instance_url=%s, session=..., user_agent=%s, client_website=%s)",
            instance_url,
            user_agent,
            client_website,
        )

        if "http" not in instance_url:
            instance_url = f"https://{instance_url}"

        form_data = aiohttp.FormData()
        form_data.add_field("client_name", user_agent)
        form_data.add_field("client_website", client_website)
        form_data.add_field("scopes", "read write")
        form_data.add_field("redirect_uris", REDIRECT_URI)
        try:
            async with session.post(
                url=f"{instance_url}/api/v1/apps",
                data=form_data,
            ) as response:
                logger.debug(
                    "ActivityPub.create_app response: \n%s",
                    response,
                )
                await ActivityPub.__check_exception(response)
                response_dict = await response.json()
        except aiohttp_ClientError as error:
            raise NetworkError from error

        logger.debug(
            "ActivityPub.create_app response.json: \n%s",
            json.dumps(response_dict, indent=4),
        )
        return (response_dict["client_id"]), (response_dict["client_secret"])

    async def post_status(  # noqa: PLR0913  - No way around needing all this parameters
        self: ActivityPubClass,
        status: str,
        visibility: str = "public",
        media_ids: Optional[List[str]] = None,
        sensitive: bool = False,
        spoiler_text: Optional[str] = None,
    ) -> Status:
        """Post a status to the fediverse.

        :param status: The text to be posted on the timeline.
        :param visibility: Visibility of the posted status. Enumerable one of `public`, `unlisted`,
            `private`, or `direct`. Defaults to `public`
        :param media_ids: List of ids for media (pictures, videos, etc) to be attached to this post.
            Can be `None` if no media is to be attached. Defaults to `None`
        :param sensitive: Set to true the post is of a sensitive nature and should be marked as such.
            For example overly political or explicit material is often marked as sensitive.
            Applies particularly to attached media. Defaults to `False`
        :param spoiler_text: Text to be shown as a warning or subject before the actual content.
            Statuses are generally collapsed behind this field. Defaults to `None`

        :return: Dict of the status just posted.
        """
        logger.debug(
            "ActivityPub.post_status(status=%s, visibility=%s, media_ids=%s, sensitive=%s, spoiler_text=%s)",
            status,
            visibility,
            media_ids,
            sensitive,
            spoiler_text,
        )
        await self.__pre_call_checks()

        url = f"{self.instance}/api/v1/statuses"
        headers = {
            "Authorization": self.authorization,
            "Idempotency-Key": uuid.uuid4().hex,
        }

        logger.debug("ActivityPub.post_status(...) - using URL=%s", url)

        form_data = aiohttp.FormData()
        form_data.add_field(name="status", value=status)
        form_data.add_field(name="visibility", value=visibility)
        if sensitive:
            form_data.add_field(name="sensitive", value="true")
        if media_ids:
            form_data.add_field(name="media_ids[]", value=media_ids)
        if spoiler_text:
            form_data.add_field(name="spoiler_text", value=spoiler_text)

        try:
            async with self.session.post(
                url=url,
                headers=headers,
                data=form_data,
            ) as response:
                self.__update_ratelimit(headers=response.headers)
                await ActivityPub.__check_exception(response=response)
                result: Status = await response.json()
                logger.debug(
                    "ActivityPub.post_status - request_info:\n%s",
                    response.request_info,
                )
        except aiohttp_ClientError as error:
            raise NetworkError from error

        logger.debug(
            "ActivityPub.post_status -> result:\n%s",
            json.dumps(result, indent=4),
        )
        return result

    async def post_media(
        self: ActivityPubClass,
        file: BinaryIO,
        mime_type: str,
        description: Optional[str] = None,
        focus: Optional[Tuple[float, float]] = None,
    ) -> Any:
        """Post a media file (image or video).

        :param file: The file to be uploaded
        :param mime_type: Mime type
        :param description: A plain-text description of the media, for accessibility purposes
        :param focus: Two floating points (x,y), comma-delimited, ranging from -1.0 to 1.0
            (see “Focal points <https://docs.joinmastodon.org/methods/statuses/media/#focal-points>”_)

        :returns: Dict containing details for this media on server, such a `id`, `url` etc
        """
        logger.debug(
            "ActivityPub.post_media(file=..., mime_type=%s, description=%s, focus=%s)",
            mime_type,
            description,
            focus,
        )

        await self.__pre_call_checks()

        headers = {"Authorization": self.authorization}
        url = f"{self.instance}/api/v1/media"
        data = aiohttp.FormData()
        data.add_field(
            name="file",
            value=file,
            filename=uuid.uuid4().hex,
            content_type=mime_type,
        )
        if description:
            data.add_field(name="description", value=description)
        if focus and len(focus) >= 2:  # noqa: PLR2004
            data.add_field(name="focus", value=f"{focus[0]},{focus[1]}")

        try:
            async with self.session.post(
                url=url,
                headers=headers,
                data=data,
            ) as response:
                self.__update_ratelimit(headers=response.headers)
                await ActivityPub.__check_exception(response=response)
                result = await response.json()
        except aiohttp_ClientError as error:
            raise NetworkError from error

        logger.debug(
            "ActivityPub.post_media -> result:\n%s",
            json.dumps(result, indent=4),
        )
        return result

    async def __pre_call_checks(self: ActivityPubClass) -> None:
        """Do checks contacting the instance server.

        For now just looking at rate limits by checking if the rate
        limit is 0 and the rate limit reset time is in the future, raise
        a RatelimitError
        """
        logger.debug(
            "ActivityPub.__pre_call_checks "
            "- Limit remaining: %s "
            "- Limit resetting at %s",
            self.ratelimit_remaining,
            self.ratelimit_reset,
        )
        if self.ratelimit_remaining == 0 and self.ratelimit_reset > arrow.now():
            raise RatelimitError(429, None, "Rate limited")

    def __parse_next_prev(self: ActivityPubClass, links: Optional[str]) -> None:
        """Extract min_id and max_id from a string like `https://example.com/api/v1/timelines/
        home?min_id=12345&max_id=67890` and store them in the instance attributes
        pagination_min_id and pagination_max_id.

        :param links: The links header from the response
        """
        logger.debug("ActivityPub.__parse_next_prev - links = %s", links)

        if links:
            self.pagination = {
                "next": {"max_id": None, "min_id": None},
                "prev": {"max_id": None, "min_id": None},
            }

            for comma_links in links.split(sep=", "):
                pagination_rel: Optional[str] = None
                if 'rel="next"' in comma_links:
                    pagination_rel = "next"
                elif 'rel="prev"' in comma_links:
                    pagination_rel = "prev"

                if pagination_rel:
                    urls = comma_links.split(sep="; ")

                    logger.debug(
                        "ActivityPub.__parse_next_prev - rel = %s - urls = %s",
                        pagination_rel,
                        urls,
                    )

                    for url in urls:
                        parsed_url = urlparse(url=url.lstrip("<").rstrip(">"))
                        queries_dict = parse_qs(str(parsed_url.query))
                        logger.debug(
                            "ActivityPub.__parse_next_prev - queries_dict = %s",
                            queries_dict,
                        )
                        min_id = queries_dict.get("min_id")
                        max_id = queries_dict.get("max_id")
                        if min_id:
                            self.pagination[pagination_rel]["min_id"] = min_id[0]
                        if max_id:
                            self.pagination[pagination_rel]["max_id"] = max_id[0]

        logger.debug("ActivityPub.__parse_next_prev - pagination = %s", self.pagination)

    def __update_ratelimit(self: ActivityPubClass, headers: Any) -> None:
        """If the instance is not Pleroma, update the ratelimit variables.

        :param headers: The headers of the response
        """
        temp_ratelimit_limit = temp_ratelimit_remaining = temp_ratelimit_reset = None

        if self.instance_type in (INSTANCE_TYPE_TAKAHE, INSTANCE_TYPE_PLEROMA):
            # Takahe and Pleroma do not seem to return rate limit headers.
            # Default to 5 minute rate limit reset time
            temp_ratelimit_reset = arrow.now().shift(minutes=+5)

        else:
            temp_ratelimit_limit = headers.get("X-RateLimit-Limit")
            temp_ratelimit_remaining = headers.get("X-RateLimit-Remaining")
            temp_ratelimit_reset = headers.get("X-RateLimit-Reset")

        if temp_ratelimit_limit:
            self.ratelimit_limit = int(temp_ratelimit_limit)
        if temp_ratelimit_remaining:
            self.ratelimit_remaining = int(temp_ratelimit_remaining)
        if temp_ratelimit_reset:
            self.ratelimit_reset = arrow.get(temp_ratelimit_reset)

        logger.debug(
            "ActivityPub.__update_ratelimit "
            "- Pleroma Instance: %s "
            "- RateLimit Limit %s",
            self.instance_type == INSTANCE_TYPE_PLEROMA,
            self.ratelimit_limit,
        )
        logger.debug(
            "ActivityPub.__update_ratelimit "
            "- Limit remaining: %s "
            "- Limit resetting at %s",
            self.ratelimit_remaining,
            self.ratelimit_reset,
        )

    @staticmethod
    async def __check_exception(response: aiohttp.ClientResponse) -> None:
        """If the response status is greater than or equal to 400, then raise
        an appropriate exception.

        :param response: aiohttp.ClientResponse
        """
        logger.debug(
            "ActivityPub.__check_exception - response.headers = %s", response.headers
        )
        logger.debug(
            "ActivityPub.__check_exception - response.status = %s", response.status
        )
        if response.status >= STATUS_BAD_REQUEST:
            error_message = await ActivityPub.__determine_error_message(response)

            if response.status == STATUS_UNAUTHORIZED:
                raise UnauthorizedError(response.status, response.reason, error_message)
            if response.status == STATUS_FORBIDDEN:
                raise ForbiddenError(response.status, response.reason, error_message)
            if response.status == STATUS_NOT_FOUND:
                raise NotFoundError(response.status, response.reason, error_message)
            if response.status == STATUS_CONFLICT:
                raise ConflictError(response.status, response.reason, error_message)
            if response.status == STATUS_GONE:
                raise GoneError(response.status, response.reason, error_message)
            if response.status == STATUS_UNPROCESSABLE_ENTITY:
                raise UnprocessedError(response.status, response.reason, error_message)
            if response.status == STATUS_TOO_MANY_REQUESTS:
                raise RatelimitError(response.status, response.reason, error_message)
            if response.status < STATUS_INTERNAL_SERVER_ERROR:
                raise ClientError(response.status, response.reason, error_message)

            raise ServerError(response.status, response.reason, error_message)

    @staticmethod
    async def __determine_error_message(response: aiohttp.ClientResponse) -> str:
        """If the response is JSON, return the error message from the JSON,
        otherwise return the response text.

        :param response: aiohttp.ClientResponse
        :returns: The error message as string.
        """
        error_message = "Exception has occurred"
        try:
            content = await response.json()
            error_message = content["error"]
        except (aiohttp.ClientError, KeyError):
            try:
                error_message = await response.text()
            except (aiohttp.ClientError, LookupError) as lookup_error:
                logger.debug(
                    "ActivityPub.__determine_error_message - Error when determining response.text  = %s",
                    lookup_error,
                )
        logger.debug(
            "ActivityPub.__determine_error_message - error_message = %s", error_message
        )
        return error_message


class ActivityPubError(Exception):
    """Base class for all mastodon exceptions."""


class NetworkError(ActivityPubError):
    """`NetworkError` is a subclass of `ActivityPubError` that is raised when
    there is a network error.
    """

    pass


class ApiError(ActivityPubError):
    """`ApiError` is a subclass of `ActivityPubError` that is raised when there
    is an API error.
    """

    pass


class ClientError(ActivityPubError):
    """`ClientError` is a subclass of `ActivityPubError` that is raised when
    there is a client error.
    """

    pass


class UnauthorizedError(ClientError):
    """`UnauthorizedError` is a subclass of `ClientError` that is raised when
    the user represented by the auth_token is not authorized to perform a
    certain action.
    """

    pass


class ForbiddenError(ClientError):
    """`ForbiddenError` is a subclass of `ClientError` that is raised when the
    user represented by the auth_token is forbidden to perform a certain
    action.
    """

    pass


class NotFoundError(ClientError):
    """`NotFoundError` is a subclass of `ClientError` that is raised when an
    object for an action cannot be found.
    """

    pass


class ConflictError(ClientError):
    """`ConflictError` is a subclass of `ClientError` that is raised when there
    is a conflict with performing an action.
    """

    pass


class GoneError(ClientError):
    """`GoneError` is a subclass of `ClientError` that is raised when an object
    for an action has gone / been deleted.
    """

    pass


class UnprocessedError(ClientError):
    """`UnprocessedError` is a subclass of `ClientError` that is raised when an
    action cannot be processed.
    """

    pass


class RatelimitError(ClientError):
    """`RatelimitError` is a subclass of `ClientError` that is raised when
    we've reached a limit of number of actions performed quickly.
    """

    pass


class ServerError(ActivityPubError):
    """`ServerError` is a subclass of `ActivityPubError` that is raised when
    the server / instance encountered an error.
    """

    pass
