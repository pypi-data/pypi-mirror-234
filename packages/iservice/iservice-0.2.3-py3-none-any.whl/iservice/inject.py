import functools
import typing

import iservice

P = typing.ParamSpec("P")
R = typing.TypeVar("R")
S1 = typing.TypeVar("S1", bound=iservice.Service)
S2 = typing.TypeVar("S2", bound=iservice.Service)
S3 = typing.TypeVar("S3", bound=iservice.Service)
S4 = typing.TypeVar("S4", bound=iservice.Service)


@typing.overload
def inject(
    func: typing.Callable[typing.Concatenate[S1, P], R],
    service1: S1,
    /,
) -> typing.Callable[P, R]:
    ...


@typing.overload
def inject(
    func: typing.Callable[typing.Concatenate[S1, S2, P], R],
    service1: S1,
    service2: S2,
    /,
) -> typing.Callable[P, R]:
    ...


@typing.overload
def inject(
    func: typing.Callable[typing.Concatenate[S1, S2, S3, P], R],
    service1: S1,
    service2: S2,
    service3: S3,
    /,
) -> typing.Callable[P, R]:
    ...


@typing.overload
def inject(
    func: typing.Callable[typing.Concatenate[S1, S2, S3, S4, P], R],
    service1: S1,
    service2: S2,
    service3: S3,
    service4: S4,
    /,
) -> typing.Callable[P, R]:
    ...


def inject(
    func: typing.Callable[..., R],
    /,
    *services: iservice.Service,
) -> typing.Callable[..., R]:
    """Real implementation accept any number of services."""
    return functools.partial(func, *services)
