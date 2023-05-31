import inspect
from importlib import import_module

from cray_freelas_bot.domain.browser import IBrowser


def create_browser_from_module(module_name: str, *args, **kwargs) -> IBrowser:
    module = import_module(f'cray_freelas_bot.use_cases.{module_name}')
    for _, obj in inspect.getmembers(module):
        if obj in IBrowser.__subclasses__():
            return obj(*args, **kwargs)
