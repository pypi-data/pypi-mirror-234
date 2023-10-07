""" Organization Element """
from rsa_835_parser.elements import Element

organizations = {
	'AV09311993': 'Availity',
	'ZIRMED': 'Zirmed'
}

class Organization(Element):
    """ Organization class """

    def parser(self, value: str) -> str:
        value = value.strip()
        return organizations.get(value, value)
