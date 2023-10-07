import asyncio
from functools import wraps
from typing import Any, Callable

import click

from kelvin.publisher import Publisher, PublisherServer


def coro(f: Callable) -> Any:
    """
    Decorator to allow async click commands.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):  # type: ignore
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.command()
@coro
@click.option("--config", required=True, type=click.STRING, show_default=True, help="Path to the app config file")
@click.option(
    "--period", required=True, default=5, type=click.FLOAT, show_default=True, help="Publish period in seconds"
)
@click.option("--min", required=True, default=0, type=click.FLOAT, show_default=True, help="Minimum value to publish")
@click.option("--max", required=True, default=100, type=click.FLOAT, show_default=True, help="Maximum value to publish")
@click.option(
    "--random/--counter", "rand", default=True, show_default=True, help="Publish random values or incremental"
)
async def start(config: str, period: float, min: float, max: float, rand: bool) -> None:
    publisher = Publisher(app_yaml=config, rand_min=min, rand_max=max, random=rand)
    pubserver = PublisherServer(period, publisher)
    server = await asyncio.start_server(pubserver.new_client, "127.0.0.1", 8888)

    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"Serving on {addrs}")

    async with server:
        await server.serve_forever()


def main() -> None:
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print("Shutdown.")


if __name__ == "__main__":
    main()
