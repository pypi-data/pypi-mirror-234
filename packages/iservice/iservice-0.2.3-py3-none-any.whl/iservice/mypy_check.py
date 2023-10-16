import abc
import typing
from types import ModuleType

import iservice.mypy_check_2


class ServiceA(iservice.Service, typing.Protocol):
    def method_a(self) -> str:
        """
        This method do something.
        """


class ServiceA1(ServiceA):
    def method_a(self) -> str:
        return "A1"


def api_func_a(service: ServiceA) -> str:
    return service.method_a()


f3 = iservice.inject(api_func_a, iservice.mypy_check_2)
print(f3())
f1 = iservice.inject(api_func_a, ServiceA1())
