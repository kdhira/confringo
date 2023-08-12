import functools
from .. import resolvers

import logging

logger: logging.Logger = logging.getLogger(__name__)

class BaseInjector:
    name: str
    payload: dict[str, str]
    configuration: dict[str, str]

    def __init__(self, name: str, configuration: dict[str, str]) -> None:
        self.name = name
        self.payload = {}
        self.configuration = configuration


    def resolve(self) -> bool:
        if "DATA" in self.configuration:
            logger.info("Resolving payload from DATA attribute only for configuration %s", self.name)
            if not self.resolve_payload(self.configuration["DATA"], "DATA"):
                logger.error("DATA did not resolve due to an error (or empty output), configuration %s will not be injected...", self.name)
                return False
            return True

        ok_to_progress: bool = False

        logger.info("Scanning all attributes starting with DATA_ for configuration %s", self.name)
        for k,v in self.configuration.items():
            if not k.startswith("DATA_"):
                continue

            data_attribute_name: str = k.removeprefix("DATA_")
            logger.info("Executing resolver chain on %s", k)
            if self.resolve_payload(v, data_attribute_name):
                ok_to_progress = True
            else:
                logger.warning("%s did not resolve due to an error (or empty output), configuration %s may only be partially injected...", data_attribute_name, self.name)

        return ok_to_progress

    def resolve_payload(self, data_package: str, payload_name: str) -> bool:
        resolver_chain, _, source = data_package.partition("::")
        payload = functools.reduce(resolvers.resolve, reversed(resolver_chain.split(":")), source)
        if not payload:
            return False

        self.payload[payload_name] = payload
        return True
