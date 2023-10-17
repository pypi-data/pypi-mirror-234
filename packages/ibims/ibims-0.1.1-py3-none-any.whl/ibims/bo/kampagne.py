"""
contains the BO model for kampagne
"""
from bo4e.bo.geschaeftsobjekt import Geschaeftsobjekt


class Kampagne(Geschaeftsobjekt):
    """
    A "Kampagne"/campaign models which marketing activities led customers to a product/tariff.
    """

    id: str  #: eindeutige (eher technische) bezeichnung der kampagne
    name: str  #: nicht unbedingt eindeutige aber menschenlesbare Bezeichnung e.g. "Social Media Kampagne Q3 2022
