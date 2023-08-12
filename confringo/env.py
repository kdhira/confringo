import os
import logging
from . import config

logger: logging.Logger = logging.getLogger(__name__)

def resolve_env_context() -> dict[str, dict[str, str]]:
    env_context: dict[str, dict[str, str]] = {}
    for k, v in os.environ.items():
        if not k.startswith(config.ENV_PREFIX):
            logger.debug("Ignoring %s, as it doesn't start with env prefix %s", k, config.ENV_PREFIX)
            continue

        k = k.removeprefix(config.ENV_PREFIX)

        cfg_name, _, cfg_attribute = k.partition("_")
        if cfg_name not in env_context:
            logger.info("Detected new configuration: %s", cfg_name)
            env_context[cfg_name] = {}

        logger.info("Setting attribute %s for %s", cfg_attribute, cfg_name)
        env_context[cfg_name][cfg_attribute] = v

    return env_context
