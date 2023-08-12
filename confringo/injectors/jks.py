import os
import jks
import logging
import OpenSSL.crypto

from .. import config
from .base import BaseInjector

logger: logging.Logger = logging.getLogger(__name__)

class TrustStoreInjector(BaseInjector):
    def inject(self) -> None:
        target: str = self.configuration["TARGET"]
        ks_password: str = self.configuration["KS_PASS"]

        truststore_entries = [TrustStoreInjector.construct_trustore_entry(k, v) for k, v in self.payload.items()]

        truststore_file: str = os.path.join(config.WRITE_ROOT, target.lstrip('/'))

        parent_dir = os.path.dirname(truststore_file)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
            logger.info("Created directory %s", parent_dir)

        logger.debug("Writing resolved payload for %s to %s", self.name, truststore_file)
        truststore = jks.KeyStore.new('jks', truststore_entries)
        truststore.save(truststore_file, ks_password)
        logger.info("Content written to %s", truststore_file)

    @classmethod
    def construct_trustore_entry(cls, alias, certificate_string) -> jks.TrustedCertEntry:
        logger.info("Constructing truststore entry for alias: %s", alias)

        cert_pem = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, certificate_string.encode())
        cert_der = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_ASN1, cert_pem)

        return jks.TrustedCertEntry.new(alias, cert_der)
