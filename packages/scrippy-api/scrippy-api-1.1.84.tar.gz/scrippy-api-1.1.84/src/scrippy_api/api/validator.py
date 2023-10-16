import jsonschema
from scrippy_api import logger


def validate(instance, schema):
  logger.debug("[+] Validating parameters")
  try:
    jsonschema.validate(instance=instance, schema=schema)
  except Exception:
    logger.debug(" '-> Invalid parameters")
    return False
  logger.debug(" '-> Valid parameters")
  return True
