import importlib
import os
import pkgutil
from threading import Lock


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]

    @classmethod
    def get_instance(mcs):
        return mcs._instances[mcs]


def walk_module(package: str):
    module_path = package.replace(".", os.sep)
    for _, name, ispkg in pkgutil.walk_packages([module_path]):
        if ispkg:
            yield from walk_module(f"{package}.{name}")
        else:
            yield importlib.import_module(f"{package}.{name}")
