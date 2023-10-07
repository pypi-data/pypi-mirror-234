from abc import ABC, abstractmethod
import numpy as np


class Formatter(ABC):

    def __init__(self, precision: int, additionalErrorPrecision: int):
        self._precision = precision
        self._additionalErrorPrecision = additionalErrorPrecision

    @abstractmethod
    def format(self, value: float, error: float | None = None):
        pass

    def adjustAdditionalErrorPrecision(self, desiredErrorPrecision: int):
        self._additionalErrorPrecision = desiredErrorPrecision - self._precision


class FloatFormatter(Formatter):

    def __init__(self, precision: int = 3, additionalErrorPrecision: int = 1):
        super(FloatFormatter, self).__init__(precision, additionalErrorPrecision)

    def format(self, value: float, error: float | None = None):
        if error is None:
            return ("{:." + str(self._precision) + "f} ").format(value)
        else:
            errorPrecision = self._precision + self._additionalErrorPrecision
            template = ("${:." + str(self._precision) + "f} \pm " + "{:." + str(errorPrecision) + "f}" + "$ ")
            return template.format(value, error)


class ExponentialFormatter(Formatter):

    def __init__(self, precision: int = 3, additionalErrorPrecision: int = 1):
        super(ExponentialFormatter, self).__init__(precision, additionalErrorPrecision)

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
            errorPrecision = self._precision + self._additionalErrorPrecision
            s = "$({:." + str(self._precision) + "f} \\pm {:." + str(errorPrecision) + "f})\\cdot 10^"
            s = s.format(b, c)
            s += "{" + str(a) + "}$ "
        return s
