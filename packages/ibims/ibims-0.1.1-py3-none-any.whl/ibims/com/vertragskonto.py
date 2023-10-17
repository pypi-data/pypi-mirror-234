"""
New COMs to model the MBA and CBA structures in the customer loader.
"""
from datetime import datetime

from bo4e.bo.vertrag import Vertrag
from bo4e.com.adresse import Adresse
from bo4e.com.com import COM
from bo4e.enum.kontaktart import Kontaktart
from pydantic import field_validator
from pydantic_core.core_schema import FieldValidationInfo


class Vertragskonto(COM):
    """
    Bundle common attributes of MBA and CBA.
    """

    # required attributes

    ouid: int
    """
    This ID is unique in a defined scope.
    In this case, it is easier to construct the ouid before the CustomerLoader mapping because our solution to
    construct these ouids involve iteration over all MBAs and CBAs. This is easier in the mapping Powercloud -> BO4E.
    """
    vertrags_adresse: Adresse
    """
    Address related to the Vertragskonto which is only used to create a common mba for Vertragskontos with the same
    address.
    """
    vertragskontonummer: str
    """
    This `vertragskontonummer` is intended to be used for the field `name` in the billing account data
    (Customer Loader).
    """
    rechnungsstellung: Kontaktart
    """
    preferred way of delivering the bill to the customer
    """


class VertragskontoCBA(Vertragskonto):
    """
    Models a CBA (child billing account) which directly relates to a single contract. It contains information about
    locks and billing dates. But in the first place, CBAs will be grouped together by the address in their contracts.
    For each group of CBAs with a common address there will be created an MBA (master billing
    account) to support that the invoices for the CBAs can be bundled into a single invoice for the MBA.
    """

    vertrag: Vertrag
    """
    Contracts in the CBA account
    """

    erstellungsdatum: datetime
    """
    Creation date of the CBA account
    """

    rechnungsdatum_start: datetime
    """
    first billing date
    """
    rechnungsdatum_naechstes: datetime
    """
    next billing date
    """


class VertragskontoMBA(Vertragskonto):
    """
    Models an MBA (master billing account). Its main purpose is to bundle CBAs together having the same address in
    their related contracts. This feature supports a single invoice for all CBAs instead of several
    invoices for each.
    """

    cbas: list[VertragskontoCBA]

    @field_validator("cbas")
    @classmethod
    def validate_cbas_addresses(
        cls, value: list[VertragskontoCBA], info: FieldValidationInfo
    ) -> list[VertragskontoCBA]:
        """
        This validator ensures that the MBA and the related CBAs all have the same address. It also ensures that
        the MBA has at least one related CBA.
        """
        if len(value) == 0:
            raise ValueError("The MBA must have at least one CBA")
        for cba in value:
            if cba.vertrags_adresse != info.data["vertrags_adresse"]:
                raise ValueError(
                    f"The address of the cba with `vertragsnummer `{cba.vertrag.vertragsnummer} "
                    "mismatches the MBA's address."
                )
        return value
