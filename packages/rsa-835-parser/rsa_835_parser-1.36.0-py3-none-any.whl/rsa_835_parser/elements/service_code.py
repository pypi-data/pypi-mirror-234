"""Service Code"""
from rsa_835_parser.elements import Element
from rsa_835_parser.elements.utilities import split_element

class ServiceCode(Element):
    """Service Code class"""

    def parser(self, value: str) -> str:
        value = split_element(value)
        _, code, *_ = value
        return code
