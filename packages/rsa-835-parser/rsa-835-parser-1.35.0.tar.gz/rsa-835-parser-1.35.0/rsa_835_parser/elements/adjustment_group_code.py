""" Adjustment Group Code """
from rsa_835_parser.elements import Element, Code

# https://x12.org/codes/claim-adjustment-group-codes
adjustment_group_codes = {
	'CR': 'corrections and reversals',
	'OA': 'other adjustment',
	'PR': 'patient responsibility',
	'CO': 'contractual obligation',
	'PI': 'payor initiated reduction',
}


class AdjustmentGroupCode(Element):
    """ Adjustment Group Code class """

    def parser(self, value: str) -> Code:
        description = adjustment_group_codes.get(value, None)
        return Code(value, description)
