"""
Contains the dataset for the usage loader.
It also contains the validation logic for the usage loader dataset.
"""
from bo4e.bo.energiemenge import Energiemenge
from bo4e.bo.messlokation import Messlokation
from bo4e.bo.zaehler import Zaehler
from bomf.model import Bo4eDataSet


class TripicaUsageLoaderDataSet(Bo4eDataSet):
    """
    This is a bo4e data set that consists of
    * an Energiemenge
    * a Messlokation
    * a Zaehler.
    In the context of this package it contains all information to construct
    the tripica loader model.
    """

    energiemenge: Energiemenge
    messlokation: Messlokation
    zaehler: Zaehler
