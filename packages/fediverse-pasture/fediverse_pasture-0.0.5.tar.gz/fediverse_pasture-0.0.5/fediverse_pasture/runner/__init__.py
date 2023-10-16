import asyncio

from dataclasses import dataclass
from datetime import datetime
from typing import Callable, List
from secrets import token_urlsafe

from bovine import BovineActor
from bovine.activitystreams import (
    ActivityFactory,
    ObjectFactory,
    factories_for_actor_object,
)
from bovine.utils import now_isoformat

from fediverse_pasture.types import ApplicationAdapterForLastActivity


@dataclass
class ActivitySender:
    """The ActivitySender class serves as a way to coordinate the process
    of sending the same activity to multiple Fediverse applications.

    The basic process is

    * Create an Activity with a published timestamp stored in published
    * Send this activity to applications using `send`
    * Retrieve the result from said applications
    """

    activity_factory: ActivityFactory
    object_factory: ObjectFactory
    bovine_actor: BovineActor
    make_id: Callable

    published: datetime | None = None
    activity: dict | None = None

    def init_create_note(self, modifier: Callable[dict, dict]):
        """Sets activity to a Create for a Note. Here the Note is
        constructed from a skeleton by applying `modifier` to it.
        To successfully send the note to most applications, modifier
        should set the Note's content.

        This method can be used to create objects of other types
        by overriding "type".
        """
        published = now_isoformat()

        note = self.object_factory.note(
            id=self.make_id(),
            to={"as:Public"},
            published=published,
        ).build()
        del note["@context"]
        note = modifier(note)

        create = self.activity_factory.create(note, id=self.make_id()).build()

        create["@context"] = [
            create["@context"],
            {"Hashtag": "as:Hashtag", "sensitive": "as:sensitive"},
        ]

        self.activity = create
        self.published = datetime.fromisoformat(published.removesuffix("Z"))

    async def send(self, remote: str):
        """Sends the activity to the remote user

        :param remote: Actor URI of the remote user"""
        remote_inbox = (await self.bovine_actor.get(remote))["inbox"]

        return await self.bovine_actor.post(remote_inbox, self.activity)

    @staticmethod
    def for_actor(bovine_actor, actor_object):
        """Initializes the Activity Sender object for a given BovineActor
        and the corresponding actor object"""
        activity_factory, object_factory = factories_for_actor_object(
            actor_object.build()
        )

        def make_id():
            return actor_object.id + "/" + token_urlsafe(8)

        return ActivitySender(
            activity_factory=activity_factory,
            object_factory=object_factory,
            bovine_actor=bovine_actor,
            make_id=make_id,
        )


@dataclass
class ActivityRunner:
    """Coordinates sending an activity to many applications through an ActivitySender
    instances"""

    activity_sender: ActivitySender
    applications: List[ApplicationAdapterForLastActivity]

    async def run_for_modifier(
        self, modifier: Callable[dict, dict], wait_time: float = 2.0
    ):
        """modifier has the same format as for ActivitySender"""
        self.activity_sender.init_create_note(modifier)

        await asyncio.gather(
            *[
                self.activity_sender.send(application.actor_uri)
                for application in self.applications
            ]
        )

        await asyncio.sleep(wait_time)

        result = {"activity": self.activity_sender.activity}

        for application in self.applications:
            result[application.application_name] = await application.fetch_activity(
                self.activity_sender.published
            )

        return result
