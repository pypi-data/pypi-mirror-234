"""
Contains the dataset for the customer loader.
It also contains the validation logic for the customer loader dataset.
"""

from bo4e.com.adresse import Adresse

from ibims.bo import GeschaeftspartnerErweitert
from ibims.com import Bankverbindung, VertragskontoMBA
from ibims.datasets import DataSetBaseModel


class TripicaCustomerLoaderDataSet(DataSetBaseModel):
    """
    This is a bo4e data set that consists of
    * a GeschaeftspartnerErweitert
    * a Adresse
    * a List of Bankverbindung
    * a List of Vertragskonto
    In the context of this package is may be used to create Tripica Customer Data.
    """

    powercloud_customer_id: str  #: the powercloud customer id that was used to create this data set
    # this allows us to track a customer from its source up the target
    # https://github.com/Hochfrequenz/bo4e_migration_framework/blob/6f091b76ff4e7a72bb0ff6ecb46a8477d35b5bf8/src/bomf/model/__init__.py#L70

    geschaeftspartner_erw: GeschaeftspartnerErweitert
    """
    The following attributes need to be filled for this DataSet:
    - name1 (Surname)
    - name2 (Firstname)
    - name3 (Title e.g. Dr.)
    - erstellungsdatum
    - geburtstag
    - telefonnummer_privat
    - telefonnummer_mobil
    - telefonnummer_geschaeft
    - kontaktweg
    and within each kontaktweg:
    - list[Kontaktart (ANSCHREIBEN/E_MAIL/TELEFONAT)]
    - externe_referenzen
    and within each externe referenz:
    - customerID
    """

    liefer_adressen: dict[str, Adresse]  # [contract_id, Adresse]
    """
    The following attributes need to be filled for this DataSet:
    - postleitzahl
    - ort
    - strasse
    - hausnummer
    - landescode
    """

    rechnungs_adressen: dict[str, Adresse]  # [contract_id, Adresse]
    """
    The following attributes need to be filled for this DataSet:
    - postleitzahl
    - ort
    - strasse
    - hausnummer
    - landescode
    """

    banks: dict[str, Bankverbindung]  # [contract_id, Bankverbindung]
    """
    Each Bankverbindung in banks requires the following attributes to be filled for this DataSet:
    - iban
    - bic
    - bankname
    - kontoinhaber
    - sepa_info
    and within each sepa_info:
    - sepa_id
    - gueltig_seit
    """

    vertragskonten_mbas: list[VertragskontoMBA]  # MBA
    """
    Each VertragskontoMBA (master billing account) needs the following Attributes:
    - ouid
    - vertragskontonummer
    - vertrags_adresse
    # -billing_cycle might be necessary, if so, it still needs to be implemented.
    # https://github.com/Hochfrequenz/powercloud_to_lynqtech_data_model_transformation/issues/271
    - cbas
    And within each CBA:
    - this contains all child billing accounts grouped together by the vertragsadresse. I.e. an MBA and all its
    CBAs share a common `vertrags_adresse`.
    """

    def get_id(self) -> str:
        return self.powercloud_customer_id
