import logging
import ssl

logger: logging.Logger = logging.getLogger(__name__)

class TlsCertProbeResolver:
    @classmethod
    def resolve(cls, data: str) -> str:
        addr, _, port = data.partition(":")
        logger.info("Probing %s (port %s)", addr, port)
        return ssl.get_server_certificate((addr, int(port)))
