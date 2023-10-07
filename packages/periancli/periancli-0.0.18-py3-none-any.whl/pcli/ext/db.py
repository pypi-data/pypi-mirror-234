import os
from cement.utils import fs
import json


class DB:
    storage_path: str

    def __init__(self, storage_path):
        self.storage_path = storage_path

    def _exists(self):
        return os.path.exists(self.storage_path)

    def _store(self, data):
        with open(self.storage_path, "w") as outfile:
            json.dump(data, outfile)

    def get(self, key):
        if self._exists():
            f = open(self.storage_path)
            data = json.load(f)
            if key in data:
                return data[key]
            else:
                return None
        else:
            return None

    def set(self, key, value):
        if self._exists():
            f = open(self.storage_path)
            data = json.load(f)
            data[key] = value
            self._store(data)
        else:
            data = {}
            data[key] = value
            self._store(data)

    def clear(self):
        if self._exists():
            os.remove(self.storage_path)


def extend_db(app):
    app.log.debug('extending todo application with tinydb')
    db_file = app.config.get('perian', 'db_file')

    # ensure that we expand the full path
    db_file = fs.abspath(db_file)
    app.log.debug('tinydb database file is: %s' % db_file)

    # ensure our parent directory exists
    db_dir = os.path.dirname(db_file)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    app.extend('db', DB(db_file))