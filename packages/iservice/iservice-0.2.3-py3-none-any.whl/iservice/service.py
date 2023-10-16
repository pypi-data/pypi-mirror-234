"""
This module contains the Service Protocol, a superclass for all service subclasses.
"""
import typing


class Service(typing.Protocol):
    """
    When subclassing Service, subclass must also inherit from typing.Protocol to extend
    the protocol. This class is used for runtime check and dependency injection.
    """
