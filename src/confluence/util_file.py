import os
from datetime import datetime, timezone
from ..utils import file
from ..utils.logger import logger

def save(path, data):
    logger.info(path)
    if not os.path.exists(path):
        file.save_json(path, data)

        return True

    if type(data) is dict and 'version' in data:
        mtime = datetime.fromtimestamp(os.stat(path).st_mtime, tz=timezone.utc)
        if mtime < datetime.fromisoformat(data['version']['createdAt']):
            file.save_json(path, data)

            return True
    else:
        file.save(path, data)

        return True

    return False
