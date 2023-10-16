import asyncio
import json

from quart import Quart, make_response
from urllib.parse import urljoin

from .data_provider import (
    DataProvider,
    bovine_actor_for_actor_data,
)
from .server import BlueprintForActors, assets_blueprint_for_directory

import click


def bovine_actor_and_actor_object(domain: str):
    """Returns the BovineActor and the Actor object corresponding to the
    actor being served by one_actor"""
    dp = DataProvider.load()

    actor_id = urljoin(domain, "/actor")

    return bovine_actor_for_actor_data(actor_id, dp.one_actor)


@click.command()
@click.option("--only_generate_config", default=False, is_flag=True)
@click.option(
    "--assets",
    default=None,
    help="Directory to serve assets from. Assets will be served under /assets/",
)
@click.option("--port", default=2909, help="port to run on")
def one_actor(only_generate_config, assets, port):
    dp = DataProvider.generate_and_load(only_generate_config)
    app = Quart(__name__)

    queue = asyncio.Queue()

    async def generator():
        yield """<html><body><h1>Inbox content</h1>"""
        while True:
            data = await queue.get()
            if data:
                yield f"""<p><pre>{json.dumps(data, indent=2)}</pre></p>"""

    async def on_inbox(data):
        await queue.put(data)

    if assets:
        app.register_blueprint(assets_blueprint_for_directory(assets))

    app.register_blueprint(
        BlueprintForActors(actors=[dp.one_actor], on_inbox=on_inbox).blueprint
    )

    @app.get("/")
    async def inbox_display():
        response = await make_response(generator())
        response.timeout = None
        return response

    app.run(port=port, host="0.0.0.0", use_reloader=False)


if __name__ == "__main__":
    one_actor()
