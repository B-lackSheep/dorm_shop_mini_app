import importlib
import pkgutil
from aiogram import Router


def get_all_routers():
    routers = []

    for _, module_name, _ in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f".{module_name}", __name__)

        if hasattr(module, 'router') and isinstance(module.router, Router):
            routers.append(module.router)

    return routers
