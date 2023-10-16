import abc
import typing

import pytest

import iservice


class ServiceA(iservice.Service, typing.Protocol):
    @staticmethod
    @abc.abstractmethod
    def method_a() -> str:
        """
        This method do something.
        """


class ServiceA1(ServiceA):
    @staticmethod
    def method_a() -> str:
        return "A1"


class ServiceA2(ServiceA):
    @staticmethod
    def method_a() -> str:
        return "A2"


def api_func_a(service: type[ServiceA]) -> str:
    return service.method_a()


@pytest.fixture
def api_func_a1() -> typing.Callable:
    return iservice.inject(api_func_a, ServiceA1)


@pytest.fixture
def api_func_a2() -> typing.Callable:
    return iservice.inject(api_func_a, ServiceA2)
