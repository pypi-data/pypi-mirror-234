import logging
import click
from quart import Quart


from .server.http_signature import http_signature_blueprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option("--port", default=2909, help="port to run on")
def http_signature(port):
    app = Quart(__name__)
    app.register_blueprint(http_signature_blueprint)
    app.run(port=port, host="0.0.0.0", use_reloader=True)


if __name__ == "__main__":
    http_signature()
