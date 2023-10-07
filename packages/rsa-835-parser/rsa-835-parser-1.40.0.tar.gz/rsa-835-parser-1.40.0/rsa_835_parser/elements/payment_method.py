""" Payment Method (PMT) - 3 characters """
from rsa_835_parser.elements import Element

payment_methods = {
	'ACH': 'automatic deposit',
	'CHK': 'check',
	'NON': 'no payment'
}


class PaymentMethod(Element):
    """ Payment Method class """

    def parser(self, value: str) -> str:
        value = value.strip()
        return payment_methods.get(value, value)
