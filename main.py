import argparse
import logging
import os
from threading import Thread

from coloredlogs import install as install_coloredlogs
from sqlmodel.sql.expression import Select, SelectOfScalar
from uvicorn import run as uvicorn_run

from core.bot import ModularBot
from core.const import loglevels
from core.functions import generate_necessarry_files, is_in_virtualenv
from web import app

# Fix sqlalchemy caching with sqlmodel
SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

if __name__ == "__main__":
    # Command line interface handling
    parser = argparse.ArgumentParser(
        prog="Trinity", description="Economy discord bot made in python"
    )
    parser.add_argument(
        "-l",
        "--logging",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Choose level of logging",
    )
    parser.add_argument("-f", "--file", type=str, help="Filename for logging")
    parser.add_argument(
        "--token",
        default=os.environ.get("TRINITY"),
        type=str,
        help="Discord API token: Get yours at https://discord.com/developers/applications",
    )
    parser.add_argument(
        "--enable-rce",
        action="store_true",
        help="Enable remote code execution for owner for fast debugging",
    )
    parser.add_argument(
        "--disable-plugins", action="store_true", help="Disable plugins"
    )
    parser.add_argument(
        "--host", default="0.0.0.0", type=str, help="Host address to bind to"
    )
    parser.add_argument("--port", default=8080, type=int, help="Port to bind to")
    args = parser.parse_args()

    def run_web(host: str = "0.0.0.0", port: int = 8080) -> None:
        uvicorn_run(app, host=host, port=port)

    # Generate all necessary files and directories
    generate_necessarry_files()

    # Disable DEBUG logging of discord module
    discord_gateway_logger = logging.getLogger("discord.gateway")
    discord_gateway_logger.setLevel(logging.INFO)
    discord_client_logger = logging.getLogger("discord.client")
    discord_client_logger.setLevel(logging.INFO)
    discord_http_logger = logging.getLogger("discord.http")
    discord_http_logger.setLevel(logging.INFO)

    # Log into file if specified
    if args.file:
        logging.basicConfig(
            level=loglevels[args.logging],
            handlers=[logging.FileHandler(args.file, "w", "utf-8")],
            format="%(levelname)s | %(asctime)s | %(name)s |->| %(message)s",
            datefmt=r"%H:%M:%S",
        )

    # Coloring the logs
    install_coloredlogs(
        level=loglevels[args.logging],
        fmt="%(levelname)s | %(asctime)s | %(name)s |->| %(message)s",
        datefmt=r"%H:%M:%S",
        reconfigure=False,
    )

    logger = logging.getLogger()
    logger.name = "bot"

    # Quit if not in virtualenv
    if not is_in_virtualenv():
        logging.error(
            "For security and portability reasons, this bot should only be used in a virtualenv, please create one and run this script again"
        )
        exit(1)

    # Init bot and add necessary commands
    bot = ModularBot(enable_rce=args.enable_rce, disable_plugins=args.disable_plugins)

    web_thread = Thread(target=run_web, args=[args.host, args.port])
    web_thread.daemon = True

    web_thread.start()
    bot.run(args.token, reconnect=True)
