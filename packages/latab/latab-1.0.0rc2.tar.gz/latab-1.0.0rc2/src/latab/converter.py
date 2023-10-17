from astropy.units import UnitBase
import numpy as np


def convertUnitToLateX(unit: UnitBase):
    s = "$\mathrm{"
    bases = unit.bases
    powers = unit.powers
    for i in range(len(bases)):
        if (i > 0):
            if (powers[i] > 0):
                s += "\\cdot "
            else:
                s += "/"
        s += str(bases[i])
        if (np.abs(powers[i]) != 1):
            s += "^{" + str(np.abs(powers[i])) + "}"
    return s + "}$"
