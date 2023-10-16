import os

from .result_store import with_store


async def test_with_store():
    file = "test3.sqlite"

    async with with_store(db_url=f"sqlite://{file}") as store:
        await store.add_result("test", "app1", {})
        await store.add_result("test", "app1", {"a": "b"})
        await store.add_result("test", "app2", {})
        await store.add_result("other", "app1", {})

        result = await store.results_for_test("test")

        assert len(result) == 2

    os.unlink(file)
