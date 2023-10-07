""" Service Qualifier """
from rsa_835_parser.elements import Element
from rsa_835_parser.elements.utilities import split_element

class ServiceQualifier(Element):
    """Service Qualifier (SVC01) element class"""

    def parser(self, value: str) -> str:
        value = split_element(value)
        qualifier, *_ = value
        return qualifier
