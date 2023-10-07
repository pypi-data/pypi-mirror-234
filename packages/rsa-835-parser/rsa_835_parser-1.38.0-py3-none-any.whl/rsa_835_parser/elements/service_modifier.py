""" Service Modifier """
from typing import Optional

from rsa_835_parser.elements import Element
from rsa_835_parser.elements.utilities import split_element

class ServiceModifier(Element):
    """ Service Modifier class"""
    def parser(self, value: str) -> Optional[str]:
        value = split_element(value)
        if len(value) > 2:
            return value[2]
