"""
Contains the dataset for the product loader.
It also contains the validation logic for the product loader dataset.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from bo4e.bo.messlokation import Messlokation
from bo4e.bo.preisblatt import Preisblatt
from bo4e.com.adresse import Adresse
from bo4e.com.vertragskonditionen import Vertragskonditionen

from ibims.bo.kampagne import Kampagne
from ibims.com import PreisgarantieErweitert, VerbrauchErweitert, VertragskontoCBA
from ibims.datasets import DataSetBaseModel


class TripicaProductLoaderDataSet(DataSetBaseModel):
    """
    This is a bo4e data set that consists of
    a Preisblatt currently
    """

    preisblattBasis: list[Preisblatt]

    kampagne: Optional[list[Kampagne]] = None  #: models the tripica base characteristics signup(id)

    preisblattVerbrauch: list[Preisblatt]

    preisblattAbschlag: Preisblatt  #: used for tripica payment; filled from powercloud contract(tariffs)+product

    preisblattZaehlpunkt: Preisblatt  #: used for tripica delivery point

    preisblattSED: Preisblatt
    # SED is short for "Service Enercity Digital". It's meant to be a product for "deutscher energiemarkt" specific data
    # See the documentation of `def _create_sed_product` for details.

    preisblattRabatt: Preisblatt
    """
    used for the tripica discount product; filled from powercloud contract(tariffs(flexbonus))+product
    """

    prozentualer_rabatt: Optional[Decimal] = None
    """
    the percentage for tripica discount; the values are percentages from 0 to 100
    """
    absoluter_rabatt: Optional[Decimal] = None
    """
    the percentage for tripica discount; the values are percentages from 0 to 100
    """

    # I originally thought about it integrating the absolute/prozentual rabatt nicely into the preisblatt rabatt.
    # Then I remembered that the intermediate model is f***ed up anyway, so I'll just leave the fields on root level.
    # I'll just leave it here for now. https://github.com/Hochfrequenz/powercloud2lynqtech/issues/937

    verbrauch: VerbrauchErweitert

    lieferadresse: Adresse  #: used in the tripica delivery point characteristics; derived from powercloud contract

    messlokation: Messlokation

    cba: VertragskontoCBA

    vertragskonditionen: list[Vertragskonditionen]
    """
    original duration of the contract/product; used for tripica "sed" product agreement items:
     * "INITIAL_COMMITMENT"
     * "TERMINATION_NOTICE_TIME_END_OF_MONTH"

    read from powercloud contract tariffs
    """
    initiale_preisgarantie: list[PreisgarantieErweitert]
    """
    initial price guarantee; used for tripica "sed" product agreement item "INITIAL_PRICE_GUARANTEE".
    read from powercloud contract tariffs
    """
    erstellungsdatum: Optional[datetime] = None
    """erstellungsdatum des dem dataset zugrunde liegenden vertrags"""
    naechster_abschlagstermin: datetime  # tripica: sed/nextRenewalDate; powercloud: deposit/nextUseAt
    """Der Termin zu dem der nächste Abschlag abgebucht wird"""
