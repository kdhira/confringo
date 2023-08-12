import functools
import logging
import os

from .. import config
from .. import resolvers
from .base import BaseInjector

logger: logging.Logger = logging.getLogger(__name__)


class FileInjector(BaseInjector):

    def inject(self) -> None:
        target: str = self.configuration["TARGET"]

        injection_file: str = os.path.join(config.WRITE_ROOT, target.lstrip('/'))
        logger.debug("Writing resolved payload for %s to %s", self.name, injection_file)

        parent_dir = os.path.dirname(injection_file)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
            logger.info("Created directory %s", parent_dir)

        with open(injection_file, 'w') as f:
            f.write("\n".join(self.payload.values()))
        logger.info("Content written to %s", injection_file)
