from typing import Protocol
import logging

from . import tls
from . import base64
from . import aws

logger: logging.Logger = logging.getLogger(__name__)

class Resolver(Protocol):
    @classmethod
    def resolve(cls, data: str) -> str:
        ...

class PlainTextResolver():
    @classmethod
    def resolve(cls, data: str) -> str:
        return data

__resolve_mapper: dict[str, Resolver] = {
    "tlscert": tls.TlsCertProbeResolver,
    "base64": base64.Base64Resolver,
    "plain": PlainTextResolver,
    "secretsmanager": aws.SecretsManagerResolver,
    "ssm": aws.ParameterStoreResolver,
}

def resolve(data: str, resolver: str) -> str:
    if not data:
        logger.warning("Resolver %s skipped because input data is empty", resolver)
        return ''
    if resolver not in __resolve_mapper:
        logger.error("Unknown resolver %s, resolver chain will fail to produce any data", resolver)
        return ''

    payload: str = __resolve_mapper[resolver].resolve(data)
    return payload
