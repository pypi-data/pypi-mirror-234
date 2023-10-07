""" Reference Qualifier """
from rsa_835_parser.elements import Element, Code

# https://ushik.ahrq.gov/ViewItemDetails?&system=sdo&itemKey=133213000
# https://ediacademy.com/blog/x12-reference-identification-qualifier/
reference_qualifiers = {
	'6R': 'provider control number',
	'0K': 'policy form identifying number',
	'PQ': 'payee identification',
	'TJ': 'federal taxpayer identification number',
	'LU': 'location number',
    'EA': 'medical record identification mumber',
}

class ReferenceQualifier(Element):
    """ Reference Qualifier class """

    def parser(self, value: str) -> Code:
        description = reference_qualifiers.get(value, None)
        return Code(value, description)
