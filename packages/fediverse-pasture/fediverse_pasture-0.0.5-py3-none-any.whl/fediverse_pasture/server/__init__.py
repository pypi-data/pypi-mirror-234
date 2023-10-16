import logging
import aiohttp

from dataclasses import dataclass
from typing import List, Callable, Awaitable

from quart import Blueprint, request, send_from_directory
from bovine.utils import webfinger_response_json
from bovine.crypto import build_validate_http_signature

from fediverse_pasture.data_provider.models import ActorData
from fediverse_pasture.data_provider import bovine_actor_for_actor_data
from .utils import actor_object_to_public_key


logger = logging.getLogger(__name__)


def assets_blueprint_for_directory(directory: str) -> Blueprint:
    blueprint = Blueprint("assets", __name__)

    @blueprint.get("/assets/<filename>")
    async def assets(filename):
        return await send_from_directory(directory, filename)

    return blueprint


@dataclass
class BlueprintForActors:
    """Creates a blueprint to expose actors. This blueprint handles
    exposing the Actor objects and their Inboxes

    If `application_actor` is not set, it is set to the actor
    with name `actor` from the list `actors`."""

    actors: List[ActorData]
    application_actor: ActorData | None = None
    on_inbox: Callable[dict, Awaitable] | None = None

    def __post_init__(self):
        if self.application_actor is None:
            self.application_actor = self.actor_for_name("actor")

    def actor_for_name(self, name: str) -> ActorData | None:
        for actor in self.actors:
            if actor.actor_name == name:
                return actor
        return None

    def actor_for_user(self, user: str) -> ActorData | None:
        for actor in self.actors:
            if actor.user_part == user:
                return actor
        return None

    async def validate_request(self, request):
        logger.info("Validating request")
        application_actor_id = f"{request.scheme}://{request.host}/actor"
        application, _ = bovine_actor_for_actor_data(
            application_actor_id, self.application_actor
        )
        async with aiohttp.ClientSession() as session:
            await application.init(session=session)

            async def key_retriever(key_id):
                result = await application.get(key_id)
                return actor_object_to_public_key(result, key_id)

            return await build_validate_http_signature(key_retriever)(request)

    @property
    def blueprint(self):
        """The Quart blueprint. Provides the endpoints

        ```plaintext
            - GET /.well-known/webfinger
            - GET /<actor_name
            - POST /<actor_name>/inbox
        ```
        """
        actor_blueprint = Blueprint("actors", __name__)

        @actor_blueprint.get("/.well-known/webfinger")
        async def webfinger():
            resource = request.args.get("resource")
            if not resource or not resource.startswith("acct:") or "@" not in resource:
                return "", 404

            acct = resource.removeprefix("acct:")
            user, domain = acct.split("@", 1)

            if domain != request.host:
                return "", 404

            actor = self.actor_for_user(user)
            if not actor:
                return "", 404
            actor_id = f"{request.scheme}://{request.host}/{actor.actor_name}"
            return webfinger_response_json(resource, actor_id)

        @actor_blueprint.get("/<actor_name>")
        async def actor_get(actor_name):
            actor = self.actor_for_name(actor_name)
            if not actor:
                return "not found", 404
            if actor.requires_signed_get_for_actor:
                if not await self.validate_request(request):
                    return "unauthorized", 401
            actor_id = f"{request.scheme}://{request.host}/{actor.actor_name}"
            _, data = bovine_actor_for_actor_data(actor_id, actor)
            return data.build(), 200, {"content-type": "application/activity+json"}

        @actor_blueprint.post("/<actor_name>/inbox")
        async def inbox_post(actor_name):
            actor = self.actor_for_name(actor_name)
            if not actor:
                return "not found", 404
            if actor.requires_signed_post_for_inbox:
                if not await self.validate_request(request):
                    return "unauthorized", 401

            if self.on_inbox:
                try:
                    data = await request.get_json()
                    await self.on_inbox(data)
                except Exception as e:
                    logger.warning("Something went wrong in inbox parsing")
                    logger.warning(repr(e))

            return "", 202

        return actor_blueprint
