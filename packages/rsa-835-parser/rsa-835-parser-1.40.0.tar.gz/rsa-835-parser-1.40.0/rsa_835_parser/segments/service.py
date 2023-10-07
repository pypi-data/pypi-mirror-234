""" Service segment """
from rsa_835_parser.elements.identifier import Identifier
from rsa_835_parser.elements.dollars import Dollars
from rsa_835_parser.elements.service_code import ServiceCode
from rsa_835_parser.elements.service_qualifier import ServiceQualifier
from rsa_835_parser.elements.service_modifier import ServiceModifier
from rsa_835_parser.elements.integer import Integer
from rsa_835_parser.segments.utilities import split_segment, get_element

class Service:
    """Service segment"""

    identification = "SVC"

    identifier = Identifier()
    charge_amount = Dollars()
    paid_amount = Dollars()
    code = ServiceCode()
    qualifier = ServiceQualifier()
    modifier = ServiceModifier()
    allowed_units = Integer()
    billed_units = Integer()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        self.code = segment[1]
        self.qualifier = segment[1]
        self.modifier = segment[1]
        self.charge_amount = segment[2]
        self.paid_amount = segment[3]

        # assume unit count of one if unit not provided
        default = 0 if self.paid_amount == 0 else 1
        self.allowed_units = get_element(segment, 5, default=default)

        self.billed_units = get_element(segment, 7, default=self.allowed_units)

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())


if __name__ == "__main__":
    pass
