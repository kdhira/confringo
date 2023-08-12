import logging
import os
from .. import config
from .base import BaseInjector

logger: logging.Logger = logging.getLogger(__name__)

class CaCertifatesInjector(BaseInjector):
    def inject(self) -> None:
        binding_dir: str = os.path.join(config.WRITE_ROOT, 'bindings', 'confringo-ca-certificates')
        if not os.path.exists(binding_dir):
            os.makedirs(binding_dir)
            logger.info("Created directory %s", binding_dir)

        ca_certificates_type_file = os.path.join(binding_dir, 'type')
        if not os.path.isfile(ca_certificates_type_file):
            with open(ca_certificates_type_file, 'w') as f:
                f.write("ca-certificates")
                logger.info("Created binding type file %s", ca_certificates_type_file)
        for suffix, certificate in self.payload.items():
            injection_file: str = os.path.join(binding_dir, suffix + ".pem")
            logger.debug("Writing resolved payload %s for %s to %s", suffix, self.name, injection_file)

            with open(injection_file, 'w') as f:
                f.write(certificate)
            logger.info("Content written to %s", injection_file)
