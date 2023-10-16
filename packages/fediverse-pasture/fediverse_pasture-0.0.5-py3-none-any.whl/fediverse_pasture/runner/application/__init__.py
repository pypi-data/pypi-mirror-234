import aiohttp
from bovine.clients import lookup_uri_with_webfinger

from fediverse_pasture.types import ApplicationAdapterForActor


from .mastodon import MastodonApplication
from .firefish import FirefishApplication


async def actor_for_application(
    account_uri: str, application_name: str, session: aiohttp.ClientSession
) -> ApplicationAdapterForActor:
    """Creates a ApplicationAdapterForActor

    :param account_uri: The acct uri, e.g. `acct:user@domain`
    :param application_name: The name of the application
    :param session: the aiohttp ClientSession
    """

    domain = account_uri.split("@")[1]

    actor_uri = await lookup_uri_with_webfinger(
        session, account_uri, f"http://{domain}"
    )

    return ApplicationAdapterForActor(
        actor_uri=actor_uri, application_name=application_name
    )


async def activity_for_mastodon(
    domain: str, username: str, access_token: str, session: aiohttp.ClientSession
):
    """Creates a ApplicationAdapterForLastActivity object for connecting to
    mastodon. Example usage:

    ```python
    mastodon = await activity_for_mastodon("mastodon_web", "bob", "xxx", session)
    ```
    """
    mastodon = MastodonApplication(
        domain=domain, access_token=access_token, username=username
    )

    return mastodon.last_activity(session)


async def activity_for_firefish(
    domain: str, username: str, session: aiohttp.ClientSession
):
    """Creates a ApplicationAdapterForLastActivity object for connecting to
    firefish. Example usage:

    ```python
    firefish = await activity_for_firefish("firefish_web", "admin", session)
    ```
    """
    firefish = FirefishApplication(domain=domain, username=username)

    return await firefish.last_activity(session)
