""" Remark Qualifier """
from rsa_835_parser.elements import Element, Code

remark_qualifiers = {
	'HE': 'claim payment'
}


class RemarkQualifier(Element):
    """ Remark Qualifier class """

    def parser(self, value: str) -> Code:
        description = remark_qualifiers.get(value, None)
        return Code(value, description)
