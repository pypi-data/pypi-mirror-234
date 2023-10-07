""" Authorization Information Qualifier """
from typing import Optional

from rsa_835_parser.elements import Element


class AuthorizationInformationQualifier(Element):
    """Authorization Information Qualifier class"""

    def parser(self, value: str) -> Optional[str]:
        if value == "00":
            value = None

        return value
