# iservice

[![Supported Python versions](https://img.shields.io/pypi/pyversions/iservice.svg)](https://pypi.org/project/iservice)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/iservice)](https://pypi.org/project/iservice)

Helper class to make FastAPI dependencies with ease.

## Simple use

```python
# iservice_a.py
import typing

import iservice


class ServiceA(iservice.Service, typing.Protocol):
    @staticmethod
    def send(name: str) -> None: ...


# service_a1.py
def send(name: str) -> None:
    print(f"Hello {name}")


# service_a2.py
def send(name: str) -> None:
    print(f"Greetings {name}")


# service_a.py
import iservice_a
import service_a1
import service_a2


def _welcome_user(service: iservice_a.ServiceA, name: str) -> None:
    service.send(name)

# inject will provide an inferred type that are matching the expected signature
# (str) -> None
hello = iservice.inject(_welcome_user, service_a1)
greeting = iservice.inject(_welcome_user, service_a2)
```

In this case, in case of incorrect calls, mypy will raise errors like:

```python
hello(1)  # Argument 1 has incompatible type "int"; expected "str"
greeting(1)  # Argument 1 has incompatible type "int"; expected "str"
```
