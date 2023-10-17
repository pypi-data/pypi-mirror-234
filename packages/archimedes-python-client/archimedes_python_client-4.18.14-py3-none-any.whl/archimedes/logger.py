"""
Logging configuration for the Archimedes client
"""
import logging

from archimedes.configuration import get_log_level

log_level = get_log_level()

logging.debug("Setting log level to %s", logging.getLevelName(log_level))

logger = logging.getLogger("archimedes.client")
logger.setLevel(log_level)
