# python3 -m confringo.main

__version = "v0.1.0-experimental"
__banner = rf'''
                  __      _
  ___ ___  _ __  / _|_ __(_)_ __   __ _  ___
 / __/ _ \| '_ \| |_| '__| | '_ \ / _` |/ _ \
| (_| (_) | | | |  _| |  | | | | | (_| | (_) |
 \___\___/|_| |_|_| |_|  |_|_| |_|\__, |\___/
  Kevin Hira                      |___/ {__version}
'''

import os
import logging

from . import config
from . import env
from . import injectors

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=os.environ.get("LOG_LEVEL", "INFO")
)
logging.getLogger("botocore").setLevel(os.environ.get("BOTOCORE_LOG_LEVEL", "INFO"))

logger: logging.Logger = logging.getLogger(__name__)

def initialise() -> None:
    print(__banner)

def main():
    initialise()

    logger.info("Parsing environment variables (ENV) for configurations with prefix \"%s\"", config.ENV_PREFIX)
    configurations: dict[str, dict[str, str]] = env.resolve_env_context()
    if not configurations:
        logger.warning("No configuration found to resolve and inject...")
        return

    logger.info("%d configurations found: %s", len(configurations), ", ".join(configurations.keys()))

    some_errors: bool = False

    for name, cfg in configurations.items():
        logger.info("Processing %s", name)
        injector: injectors.Injector | None = injectors.from_cfg(name, cfg)
        if not injector:
            some_errors = True
            continue
        logger.info("Resolving %s", name)
        if not injector.resolve():
            some_errors = True
            continue
        logger.info("Injecting %s", name)
        injector.inject()

    if some_errors:
        logger.error("Done, with errors...")
    else:
        logger.info("Done!")

if __name__ == "__main__": main()
