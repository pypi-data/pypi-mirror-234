""" Integer Element """
from typing import Optional, Union

from rsa_835_parser.elements import Element


class Integer(Element):
    """ Integer class """

    def parser(self, value: str) -> Optional[Union[int, str]]:
        if value == '':
            return None

        try:
            value = int(value)
        except ValueError:
            pass

        return value
