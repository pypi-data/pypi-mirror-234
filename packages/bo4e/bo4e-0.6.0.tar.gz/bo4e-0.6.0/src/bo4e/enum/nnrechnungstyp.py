# pylint: disable=missing-module-docstring
from bo4e.enum.strenum import StrEnum


class NNRechnungstyp(StrEnum):
    """
    Abbildung verschiedener in der INVOIC angegebenen Rechnungstypen.
    """

    ABSCHLUSSRECHNUNG = "ABSCHLUSSRECHNUNG"  #: ABSCHLUSSRECHNUNG
    ABSCHLAGSRECHNUNG = "ABSCHLAGSRECHNUNG"  #: ABSCHLAGSRECHNUNG
    TURNUSRECHNUNG = "TURNUSRECHNUNG"  #: TURNUSRECHNUNG
    MONATSRECHNUNG = "MONATSRECHNUNG"  #: MONATSRECHNUNG
    WIMRECHNUNG = "WIMRECHNUNG"  #: WIMRECHNUNG
    ZWISCHENRECHNUNG = "ZWISCHENRECHNUNG"  #: ZWISCHENRECHNUNG
    INTEGRIERTE_13TE_RECHNUNG = "INTEGRIERTE_13TE_RECHNUNG"  #: INTEGRIERTE_13TE_RECHNUNG
    ZUSAETZLICHE_13TE_RECHNUNG = "ZUSAETZLICHE_13TE_RECHNUNG"  #: ZUSAETZLICHE_13TE_RECHNUNG
    MEHRMINDERMENGENRECHNUNG = "MEHRMINDERMENGENRECHNUNG"  #: MEHRMINDERMENGENRECHNUNG
