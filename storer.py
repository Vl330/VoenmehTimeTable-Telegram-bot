import logging
import shelve

logger = logging.getLogger(__name__)


class Storer(object):
    def __init__(self, filename):
        self.filename = filename

    def store(self, key, obj):
        database = shelve.open(self.filename)
        database[key] = obj
        database.close()

    def restore(self, key):
        database = shelve.open(self.filename)
        if key in database:
            obj = database[key]
            logger.info("Successful load data by key '%s' info from file %s",
                        key, self.filename)
        else:
            obj = None
            logger.info("Can't get data by key '%s' info from file %s",
                        key, self.filename)
        database.close()
        return obj

