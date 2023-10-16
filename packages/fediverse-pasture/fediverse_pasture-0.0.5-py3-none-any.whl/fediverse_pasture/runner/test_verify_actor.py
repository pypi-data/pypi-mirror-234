from .verify_actor import VerifyActorRunner, format_verify_actor_result


async def test_verify_actor():
    runner = VerifyActorRunner(applications=[])

    result = await runner.run()

    assert result == []


def test_format():
    entry_data = {
        "alice": {"get_actor": False, "post_inbox": False},
        "bob": {"get_actor": True, "post_inbox": True},
        "claire": {"get_actor": True, "post_inbox": True},
        "dean": {"get_actor": False, "post_inbox": False},
        "emily": {"get_actor": True, "post_inbox": True},
        "frank": {"get_actor": True, "post_inbox": True},
    }

    result = [
        {
            "application_name": "test",
            "verify_actor_table": entry_data,
            "messages": "bla",
        }
    ]

    markdown = format_verify_actor_result(result)

    print()
    print()
    print(markdown)
