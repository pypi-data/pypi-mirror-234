import os

from .decorators import endpoint
from .flasket import Flasket
from .templates import template_global

__all__ = [
    "Flasket",
    "endpoint",
]


rootpath = os.path.dirname(__file__)
