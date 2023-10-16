import aiohttp
import logging
import secrets
import json
from typing import List

from dataclasses import dataclass

from bovine.clients import lookup_uri_with_webfinger

from fediverse_pasture.data_provider import bovine_actor_for_actor_data
from fediverse_pasture.data_provider.models import ActorData
from fediverse_pasture.types import Message

logger = logging.getLogger(__name__)


def can_be_resolved(uri):
    if uri.startswith("http://"):
        return True

    if uri.startswith("https://"):
        return True

    return False


@dataclass
class ActorVerifier:
    """Class implementing the logic to verify a remote actor"""

    actor_list: List[ActorData]
    remote_uri: str
    domain: str
    message: Message

    remote_actor_uri: str | None = None

    async def verify(self):
        """Public interface, this method loops over the actors in `actor_list`
        and verifies using them if the remote_uri is accessible.

        Returns a dictionary with actor.actor_name as key and the
        result as value"""
        async with aiohttp.ClientSession() as session:
            await self.determine_remote_actor_uri(session)
            return {
                actor.actor_name: await self.verify_for_actor(session, actor)
                for actor in self.actor_list
                if actor.actor_name != "actor"
            }

    async def verify_for_actor(self, session, actor):
        actor_id = f"http://{self.domain}/{actor.actor_name}"
        bovine_actor, _ = bovine_actor_for_actor_data(actor_id, actor)
        await bovine_actor.init(session=session)

        self.message.add(f"Running verification for {actor.actor_name}")

        if actor.requires_signed_post_for_inbox:
            return await self.fetch_remote_and_post_using_actor(bovine_actor)
        else:
            return await self.fetch_remote_and_post_using_session(session)

    async def fetch_remote_and_post_using_actor(self, bovine_actor):
        result = {"get_actor": False, "post_inbox": False}

        try:
            actor = await bovine_actor.get(self.remote_actor_uri)
            inbox = actor.get("inbox")

            self.message.add(f"Got inbox {inbox}")

            if inbox:
                result["get_actor"] = True
                try:
                    response = await bovine_actor.post(
                        inbox,
                        data={
                            "@context": "https://www.w3.org/ns/activitystreams",
                            "type": "Like",
                            "actor": bovine_actor.actor_id,
                            "id": bovine_actor.actor_id + secrets.token_urlsafe(8),
                        },
                    )
                    self.message.add("Successfully posted to inbox with result")
                    self.message.add(response.status)
                    self.message.add((await response.text()))
                    result["post_inbox"] = True
                except Exception as e:
                    self.message.add("Failed to post to inbox")
                    self.message.add(repr(e))

        except Exception as e:
            self.message.add("Something went wrong")
            self.message.add(repr(e))

        return result

    async def fetch_remote_and_post_using_session(self, session):
        result = {"get_actor": False, "post_inbox": False}

        try:
            async with session.get(
                self.remote_actor_uri, headers={"accept": "application/activity+json"}
            ) as response:
                actor = json.loads(await response.text())
        except Exception as e:
            self.message.add("Something went wrong when fetching actor")
            self.message.add(repr(e))
            return result

        inbox = actor.get("inbox")

        self.message.add(f"Got inbox {inbox}")

        if inbox:
            result["get_actor"] = True
            try:
                async with session.post(
                    inbox,
                    data=json.dumps(
                        {
                            "@context": "https://www.w3.org/ns/activitystreams",
                            "type": "EchoRequest",
                        }
                    ),
                    headers={"content-type": "application/activity+json"},
                ) as response:
                    self.message.add(f"Got {response.status} for unsigned POST")

                    if response.status < 400 and response.status > 100:
                        result["post_inbox"] = True
            except Exception as e:
                self.message.add("Something went wrong when posting to inbox")
                self.message.add(repr(e))
                return result

        return result

    async def determine_remote_actor_uri(self, session) -> None:
        """Used to resolve an acct-URI into the corresponding http/https-URI
        using webfinger"""
        if can_be_resolved(self.remote_uri):
            self.remote_actor_uri = self.remote_uri
            self.message.add(f"Can fetch actor from {self.remote_uri}")
            return

        self.message.add(f"Need to resolve {self.remote_uri} to actor object id")

        if self.remote_uri.startswith("acct:"):
            acct_uri = self.remote_uri
        else:
            self.message.add("Not in account uri format")

            if self.remote_uri[0] == "@":
                acct_uri = "acct:" + self.remote_uri[1:]
            else:
                acct_uri = "acct:" + self.remote_uri

        domain = acct_uri.split("@")[1]

        self.message.add(f"Resolving {acct_uri} using webfinger")

        try:
            object_id, _ = await lookup_uri_with_webfinger(
                session, acct_uri, f"http://{domain}"
            )
        except Exception as e:
            logger.exception(e)
            return

        self.message.add(f"Resolved to {object_id}")
        self.remote_actor_uri = object_id
