""" TransactionSet class for parsing EDI 835 remittance advices """

# Standard library imports
from typing import List, Iterator, Optional
from collections import namedtuple
from idna import check_label

# Third party imports
import pandas as pd

# Local application imports
from rsa_835_parser.loops.claim import Claim as ClaimLoop
from rsa_835_parser.loops.service import Service as ServiceLoop
from rsa_835_parser.loops.organization import Organization as OrganizationLoop
from rsa_835_parser.segments.utilities import find_identifier
from rsa_835_parser.segments.interchange import Interchange as InterchangeSegment
from rsa_835_parser.segments.eob_information import CheckEFT
from rsa_835_parser.segments.financial_information import (
    FinancialInformation as FinancialInformationSegment,
)

BuildAttributeResponse = namedtuple(
    "BuildAttributeResponse", "key value segment segments"
)


class TransactionSet:
    """TransactionSet class for parsing EDI 835 remittance advices"""

    def __init__(
        self,
        check_information: CheckEFT,
        interchange: InterchangeSegment,
        financial_information: FinancialInformationSegment,
        claims: List[ClaimLoop],
        organizations: List[OrganizationLoop],
        file_path: str = None,
    ):
        self.check_information = check_information
        self.interchange = interchange
        self.financial_information = financial_information
        self.claims = claims if claims else []
        self.organizations = organizations if organizations else []
        self.file_path = file_path

    def __repr__(self):
        return "\n".join(str(item) for item in self.__dict__.items())

    @property
    def payer(self) -> OrganizationLoop:
        """return the payer organization"""
        payer = [o for o in self.organizations if o.organization.type == "payer"]
        assert len(payer) == 1
        return payer[0]

    @property
    def payee(self) -> OrganizationLoop:
        """return the payee organization"""
        payee = [o for o in self.organizations if o.organization.type == "payee"]
        assert len(payee) == 1
        return payee[0]

    def to_dataframe(self) -> pd.DataFrame:
        """flatten the remittance advice by service to a pandas DataFrame"""
        data = []

        for claim in self.claims:
            for service in claim.services:
                datum = TransactionSet.serialize_service(
                    self.check_information,
                    self.financial_information,
                    self.payer,
                    claim,
                    service,
                )

                for index, adjustment in enumerate(service.adjustments):
                    datum[f"adj_{index}_group"] = adjustment.group_code.code
                    datum[f"adj_{index}_code"] = adjustment.reason_code.code
                    datum[f"adj_{index}_amount"] = adjustment.amount

                for index, reference in enumerate(service.references):
                    datum[f"ref_{index}_qual"] = reference.qualifier.code
                    datum[f"ref_{index}_value"] = reference.value

                for index, remark in enumerate(service.remarks):
                    datum[f"rem_{index}_qual"] = remark.qualifier.code
                    datum[f"rem_{index}_code"] = remark.code.code

                data.append(datum)

        return pd.DataFrame(data)

    def to_dataframe_claims(self) -> pd.DataFrame:
        """flatten the remittance advice by Claims Summary Information to a pandas DataFrame"""
        data = []

        for claim in self.claims:
            datum = TransactionSet.serialize_claim(
                self.check_information, self.financial_information, self.payer, claim
            )

            data.append(datum)

        return pd.DataFrame(data)

    @staticmethod
    def serialize_service(
        check_information: CheckEFT,
        financial_information: FinancialInformationSegment,
        payer: OrganizationLoop,
        claim: ClaimLoop,
        service: ServiceLoop,
    ) -> dict:
        """serialize a service to a dictionary"""

        # if the service doesn't have a start date assume the service and claim dates match
        start_date = None
        if service.service_period_start:
            start_date = service.service_period_start.date
        elif claim.claim_statement_period_start:
            start_date = claim.claim_statement_period_start.date

        # if the service doesn't have an end date assume the service and claim dates match
        end_date = None
        if service.service_period_end:
            end_date = service.service_period_end.date
        elif claim.claim_statement_period_end:
            end_date = claim.claim_statement_period_end.date

        datum = {
            "marker": claim.claim.marker,
            "claim_number": claim.claim.claim_number,
            "patient": claim.patient.last_first_name,
            "code": service.service.code,
            "modifier": service.service.modifier,
            "qualifier": service.service.qualifier,
            "allowed_units": service.service.allowed_units,
            "billed_units": service.service.billed_units,
            "check_number": check_information.check_number,
            "transaction_date": financial_information.transaction_date,
            "charge_amount": service.service.charge_amount,
            "allowed_amount": service.allowed_amount,
            "paid_amount": service.service.paid_amount,
            "payer": payer.organization.name,
            "start_date": start_date,
            "end_date": end_date,
            "rendering_provider": claim.rendering_provider.name
            if claim.rendering_provider
            else None,
            "payer_classification": str(claim.claim.status.payer_classification),
        }

        return datum

    @staticmethod
    def serialize_claim(
        check_information: CheckEFT,
        financial_information: FinancialInformationSegment,
        payer: OrganizationLoop,
        claim: ClaimLoop,
    ) -> dict:
        """serialize a Claim Summary Data to a dictionary"""

        try:
            claim_start_date = str(claim.claim_statement_period_start)
        except TypeError:
            claim_start_date = ""

        try:
            claim_end_date = str(claim.claim_statement_period_end)
        except TypeError:
            claim_end_date = ""

        # Pending to Complete
        # --------------------
        datum = {
            "Service Dates": claim_start_date + " - " + claim_end_date,
            "Claim Number": claim.claim_number,
            "Payer": payer.organization.name,
            "Check/EFT Number (Check/EFT Date)": check_information.check_number
            + " ("
            + financial_information.transaction_date
            + ")",
            "Patient Name (Patient Control Number) (ID)": claim.patient.last_first_name
            + " ("
            + claim.patient.identification
            + ") ("
            + claim.patient.identification_code
            + ")",
            "Patient Amt": "",
            "Total Charged Amt": claim.claim.charge_amount,
            "Total Paid Amt": claim.claim.paid_amount,
        }

        return datum

    @classmethod
    def build(cls, file_path: str) -> "TransactionSet":
        """build a TransactionSet from a file path"""
        check_information = None
        interchange = None
        financial_information = None
        claims = []
        organizations = []

        with open(file_path) as f:
            file = f.read()

        segments = file.split("~")
        segments = [segment.strip() for segment in segments]

        segments = iter(segments)
        segment = None

        while True:
            response = cls.build_attribute(segment, segments)
            segment = response.segment
            segments = response.segments

            # no more segments to parse
            if response.segments is None:
                break

            if response.key == "check information":
                check_information = response.value

            if response.key == "interchange":
                interchange = response.value

            if response.key == "financial information":
                financial_information = response.value

            if response.key == "organization":
                organizations.append(response.value)

            if response.key == "claim":
                claims.append(response.value)

        return TransactionSet(
            check_information,
            interchange,
            financial_information,
            claims,
            organizations,
            file_path,
        )

    @classmethod
    def build_attribute(
        cls, segment: Optional[str], segments: Iterator[str]
    ) -> BuildAttributeResponse:
        """build an attribute from a segment and segments iterator"""

        if segment is None:
            try:
                segment = segments.__next__()
            except StopIteration:
                return BuildAttributeResponse(None, None, None, None)

        identifier = find_identifier(segment)

        if identifier == CheckEFT.identification:
            check_information = CheckEFT(segment)
            return BuildAttributeResponse(
                "check information", check_information, None, segments
            )

        if identifier == InterchangeSegment.identification:
            interchange = InterchangeSegment(segment)
            return BuildAttributeResponse("interchange", interchange, None, segments)

        if identifier == FinancialInformationSegment.identification:
            financial_information = FinancialInformationSegment(segment)
            return BuildAttributeResponse(
                "financial information", financial_information, None, segments
            )

        if identifier == OrganizationLoop.initiating_identifier:
            organization, segments, segment = OrganizationLoop.build(segment, segments)
            return BuildAttributeResponse(
                "organization", organization, segment, segments
            )

        elif identifier == ClaimLoop.initiating_identifier:
            claim, segments, segment = ClaimLoop.build(segment, segments)
            return BuildAttributeResponse("claim", claim, segment, segments)

        else:
            return BuildAttributeResponse(None, None, None, segments)


if __name__ == "__main__":
    pass
