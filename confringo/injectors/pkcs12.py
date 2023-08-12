import os
import jks
import logging
import OpenSSL.crypto

from .. import config
from .base import BaseInjector

logger: logging.Logger = logging.getLogger(__name__)

class KeystoreInjector(BaseInjector):
    def resolve(self) -> bool:
        logger.info("Executing resolver chain on DATA_KEY")
        if not self.resolve_payload(self.configuration["DATA_KEY"], "KEY"):
            logger.error("DATA_KEY did not resolve correctly, can not continue...")
        logger.info("Executing resolver chain on DATA_CERT")
        if not self.resolve_payload(self.configuration["DATA_CERT"], "CERT"):
            logger.error("DATA_CERT did not resolve correctly, can not continue...")

        return True

    def inject(self) -> None:
        target: str = self.configuration["TARGET"]
        ks_password: str = self.configuration["KS_PASS"]

        cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, self.payload["CERT"].encode())
        key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, self.payload["KEY"].encode())
        p12 = OpenSSL.crypto.PKCS12()
        p12.set_privatekey(key)
        p12.set_certificate(cert)

        keystore_file: str = os.path.join(config.WRITE_ROOT, target.lstrip('/'))

        parent_dir = os.path.dirname(keystore_file)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
            logger.info("Created directory %s", parent_dir)

        logger.debug("Writing resolved payload for %s to %s", self.name, keystore_file)
        with open(keystore_file, 'wb') as f:
            f.write(p12.export(ks_password.encode()))
        logger.info("Content written to %s", keystore_file)
