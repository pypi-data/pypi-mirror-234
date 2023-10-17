from abc import ABC, abstractmethod
import numpy as np


class Formatter(ABC):

    def __init__(self, precision: int, errorPrecision: int):
        self._precision = precision
        self._errorPrecision = errorPrecision

    @abstractmethod
    def format(self, value: float, error: float | None = None):
        pass


class FloatFormatter(Formatter):

    def __init__(self, precision: int = 3, errorPrecision: int = 4):
        super(FloatFormatter, self).__init__(precision, errorPrecision)

    def format(self, value: float, error: float | None = None):
        if error is None:
            return ("{:." + str(self._precision) + "f} ").format(value)
        else:
            template = ("${:." + str(self._precision) + "f} \pm " + "{:." + str(self._errorPrecision) + "f}" + "$ ")
            return template.format(value, error)


class ExponentialFormatter(Formatter):

    def __init__(self, precision: int = 3, errorPrecision: int = 4):
        super(ExponentialFormatter, self).__init__(precision, errorPrecision)

    def format(self, value: float, error: float | None = None):
        if error is None:
            a = int(np.floor(np.log10(np.abs(value))))
            b = value / 10**a
            s = "${:." + str(self._precision) + "f} \\cdot 10^"
            s = s.format(b)
            s += "{" + str(a) + "}$ "
        else:
            a = int(np.floor(np.log10(np.abs(value))))
            b = value / 10**a
            c = error / 10**a
            s = "$({:." + str(self._precision) + "f} \\pm {:." + str(self._errorPrecision) + "f})\\cdot 10^"
            s = s.format(b, c)
            s += "{" + str(a) + "}$ "
        return s
