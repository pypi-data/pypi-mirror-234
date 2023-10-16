from contextlib import asynccontextmanager

from tortoise import Tortoise

from .models import TestRecord


class ResultStore:
    async def add_result(self, test_name: str, application_name: str, data: dict):
        """Adds a result to the database. The pairs (test_name, application_name)
        are assumed to be unique"""
        await TestRecord.update_or_create(
            test_name=test_name,
            application_name=application_name,
            defaults={"data": data},
        )

    async def results_for_test(self, test_name: str) -> list:
        """Retrieves the results for a given test_name"""
        result = await TestRecord.filter(test_name=test_name).all()

        return [{"application_name": x.application_name, **x.data} for x in result]


@asynccontextmanager
async def with_store(db_url="sqlite://test_results.sqlite") -> ResultStore:
    """Initializes the database and returns a ResultStore. Usage:

    ```python
    async with with_store() as store:
        await store.add_result(...)
        ...
        await store.results_for_test(...)
    ```
    """
    await Tortoise.init(
        config={
            "connections": {"default": db_url},
            "apps": {
                "models": {
                    "models": [
                        "fediverse_pasture.runner.models",
                    ],
                    "default_connection": "default",
                },
            },
        },
    )
    await Tortoise.generate_schemas()

    yield ResultStore()

    await Tortoise.close_connections()
