import base64
import logging

logger: logging.Logger = logging.getLogger(__name__)

class Base64Resolver:
    @classmethod
    def resolve(cls, data: str) -> str:
        logger.info("Base64 decoding data")
        return base64.b64decode(data).decode()
