"""
Contains the dataset for the resource loader.
It also contains the validation logic for the resource loader dataset.
"""
from bo4e.bo.marktlokation import Marktlokation
from bo4e.bo.messlokation import Messlokation
from bo4e.bo.vertrag import Vertrag
from bo4e.bo.zaehler import Zaehler

from ibims.datasets import DataSetBaseModel


class TripicaResourceLoaderDataSet(DataSetBaseModel):
    """
    This is a bo4e data set that consists of
    * a Vertrag
    * a Marktlokation
    * a Messlokation
    * a Zaehler.
    In the context of this package is may be used to create Tripica Resources.
    """

    marktlokation: Marktlokation
    messlokation: Messlokation
    vertrag: Vertrag
    zaehler: Zaehler
