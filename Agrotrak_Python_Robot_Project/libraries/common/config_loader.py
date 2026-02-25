import json
import os

class ConfigLoader:
    def __init__(self, dev_path=None, user_path=None):
        self.dev_path = dev_path
        self.user_path = user_path
        if dev_path and user_path:
            self.dev = self._load_json(dev_path)
            self.user = self._load_json(user_path)
        else:
            self.dev = {}
            self.user = {}

    def _load_json(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file not found: {path}")
        with open(path, 'r') as f:
            return json.load(f)

    def get_envs_with_explicit_keys(self):
        argotrak = {
            "argotrak_url": self.user["dummy_site_urls"]["argotrak"],
            "argotrak_username": self.user["credentials"]["argotrak"]["username"],
            "argotrak_password": self.user["credentials"]["argotrak"]["password"],
            "browser": self.dev["browser"],
            "implicit_wait": self.dev["implicit_wait"],
            "locator_file": self.dev["locator_files"]["argotrak"]
        }

        newgate = {
            "newgate_url": self.user["dummy_site_urls"]["newgate"],
            "newgate_username": self.user["credentials"]["newgate"]["username"],
            "newgate_password": self.user["credentials"]["newgate"]["password"],
            "browser": self.dev["browser"],
            "implicit_wait": self.dev["implicit_wait"],
            "locator_file": self.dev["locator_files"]["newgate"]
        }

        return {"argotrak": argotrak, "newgate": newgate}


# ✅ Expose keyword for Robot
def load_all_config(dev_path, user_path):
    loader = ConfigLoader(dev_path, user_path)
    return loader.get_envs_with_explicit_keys()


# path: libraries/common/config_loader.py
