from typing import Protocol
import logging

from . import base
from . import file
from . import buildpacks
from . import jks
from . import pkcs12
logger: logging.Logger = logging.getLogger(__name__)

class Injector(Protocol):
    def resolve(self) -> bool:
        ...

    def inject(self) -> None:
        ...

__inject_mapper: dict[str, type] = {
    "file": file.FileInjector,
    "ca-certificates": buildpacks.CaCertifatesInjector,
    "jks": jks.TrustStoreInjector,
    "pkcs12": pkcs12.KeystoreInjector,
}

def from_cfg(name: str, cfg: dict[str, str]) -> Injector | None:
    injector = cfg["TYPE"]
    if injector not in __inject_mapper:
        logger.error("%s not a defined injector type. Can not continue processing %s...", injector, name)
        return None

    logger.info("Configuration %s has injector type: %s", name, injector)
    return __inject_mapper[injector](name, cfg)
