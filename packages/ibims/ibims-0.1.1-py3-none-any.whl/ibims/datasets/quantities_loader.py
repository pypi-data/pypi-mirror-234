"""
Contains the dataset for the quantities loader
"""
from bo4e.bo.energiemenge import Energiemenge
from bo4e.bo.marktlokation import Marktlokation
from bo4e.bo.marktteilnehmer import Marktteilnehmer
from bo4e.bo.messlokation import Messlokation

from ibims.datasets.base import DataSetBaseModel
from ibims.targetmodels import TransaktionsdatenQuantities


class QuantitiesLoaderDataSet(DataSetBaseModel):
    """
    This is a bo4e dat set that consists out of
    * a Energiemenge
    * a Messlokation or Marktlokation
    * a Marktteilnehmer
    """

    energiemenge: Energiemenge
    """
    The following attributes need to be filled for this DataSet:
    - lokations_id
    - lokationstyp
    - energieverbrauch
    """

    lokation: Messlokation | Marktlokation
    """
    The following attributes need to be filled for this DataSet:
    - messlokations_id/marktlokations_id
    - sparte
    """

    sender: Marktteilnehmer
    """
    The following attributes need to be filled for this DataSet:
    - gewerbekennzeichnung
    - rollencodenummer
    - rollencodetyp
    """

    empfaenger: Marktteilnehmer
    """
    The following attributes need to be filled for this DataSet:
    - gewerbekennzeichnung
    - rollencodenummer
    - rollencodetyp
    """

    transaktionsdaten: TransaktionsdatenQuantities
