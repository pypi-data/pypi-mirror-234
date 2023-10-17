import os
import time
import json

class Cache:
    def __init__(self, cache_dir="cache"):
        self.cache_dir = cache_dir

    def get(self, key):
        path = self._get_path(key)

        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
                if self._is_expired(data):
                    return None
                else:
                    return data["value"]
        else:
            return None

    def set(self, key, value, ttl=None):
        path = self._get_path(key)
        data = {"value": value, "created_at": time.time(), "ttl": ttl}
        with open(path, "w") as f:
            json.dump(data, f)

    def get_all(self):
        all_data = {}
        for filename in os.listdir(self.cache_dir):
            path = os.path.join(self.cache_dir, filename)
            if os.path.isfile(path) and filename.endswith(".json"):
                with open(path, "r") as f:
                    data = json.load(f)
                    if not self._is_expired(data):
                        all_data[filename[:-5]] = data["value"]
        return all_data

    def delete(self, key):
        path = self._get_path(key)
        if os.path.exists(path):
            os.remove(path)

    def delete_all(self):
        for filename in os.listdir(self.cache_dir):
            path = os.path.join(self.cache_dir, filename)
            if os.path.isfile(path) and filename.endswith(".json"):
                os.remove(path)

    def _get_path(self, key):
        filename = "{}.json".format(key)
        path = os.path.join(self.cache_dir, filename)
        return path

    def _is_expired(self, data):
        if data["ttl"] and time.time() - data["created_at"] > data["ttl"]:
            return True
        elif not data["ttl"] and time.time() - data["created_at"] > 60:
            return True
        else:
            return False
