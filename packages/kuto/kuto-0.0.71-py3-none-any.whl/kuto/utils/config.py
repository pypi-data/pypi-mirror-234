import os
import yaml
import random


local_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.dirname(local_path)


class Config:
    def __init__(self):
        self.file_path = os.path.join(root_path, 'running', 'conf.yml')

    def get(self, module, key):
        with open(self.file_path, "r", encoding="utf-8") as f:
            yaml_data = yaml.load(f.read(), Loader=yaml.FullLoader)
        return yaml_data[module][key]

    def get_common(self, key):
        return self.get('common', key)

    def get_api(self, key):
        return self.get('api', key)

    def get_app(self, key):
        return self.get('app', key)

    def get_web(self, key):
        return self.get('web', key)

    def set(self, module, key, value):
        with open(self.file_path, "r", encoding="utf-8") as f:
            yaml_data = yaml.load(f.read(), Loader=yaml.FullLoader)
        yaml_data[module][key] = value
        with open(self.file_path, 'w', encoding="utf-8") as f:
            yaml.dump(yaml_data, f)

    def set_common(self, key, value):
        self.set('common', key, value)

    def set_api(self, key, value):
        self.set('api', key, value)

    def set_app(self, key, value):
        self.set('app', key, value)

    def set_web(self, key, value):
        self.set('web', key, value)

    def add_devices(self, devices: list):
        old_devices = self.get_app("devices")
        new_devices = old_devices + devices
        self.set_app("devices", new_devices)

    def set_devices(self, devices: list):
        self.set_app("devices", devices)

    def get_all_device(self):
        return self.get_app("devices")

    def get_random_device(self):
        devices: list = self.get_all_device()
        if devices:
            device = random.choice(devices)
            devices.remove(device)
            self.set_devices(devices)
            return device
        return []

    def clear_devices(self):
        new_devices = []
        self.set_app("devices", new_devices)


class FreeConfig:
    def __init__(self):
        self.file_path = os.path.join(root_path, 'running', 'free_devices.yml')

    def get(self, key):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                yaml_data = yaml.load(f.read(), Loader=yaml.FullLoader)
            return yaml_data[key]
        except:
            return []

    def set(self, key, value):
        with open(self.file_path, "r", encoding="utf-8") as f:
            yaml_data = yaml.load(f.read(), Loader=yaml.FullLoader)
        yaml_data[key] = value
        with open(self.file_path, 'w', encoding="utf-8") as f:
            yaml.dump(yaml_data, f)

    def add_devices(self, devices: list):
        old_devices = self.get("devices")
        new_devices = old_devices + devices
        self.set("devices", new_devices)

    def set_devices(self, devices: list):
        self.set("devices", devices)

    def get_all_device(self):
        return self.get("devices")

    def get_random_device(self):
        devices: list = self.get_all_device()
        if devices:
            device = random.choice(devices)
            devices.remove(device)
            self.set_devices(devices)
            return device
        return []

    def clear_devices(self):
        new_devices = []
        self.set("devices", new_devices)


config = Config()
free_config = FreeConfig()


if __name__ == '__main__':
    pass










