import pytest
import json
from datetime import datetime

from fediverse_pasture.data_provider import DataProvider, bovine_actor_for_actor_data

from . import ActivitySender


@pytest.fixture
def activity_sender():
    dp = DataProvider.generate(with_possible_actors=False)

    bovine_actor, actor_object = bovine_actor_for_actor_data(
        "http://localhost/actor", dp.one_actor
    )

    yield ActivitySender.for_actor(bovine_actor, actor_object)


def test_activity_sender(activity_sender):
    activity_sender.init_create_note(lambda x: {**x, "content": "text"})

    assert isinstance(activity_sender.published, datetime)
    assert isinstance(activity_sender.activity, dict)

    obj = activity_sender.activity.get("object")

    assert obj.get("content") == "text"

    text = json.dumps(activity_sender.activity)

    assert len(text) > 20
