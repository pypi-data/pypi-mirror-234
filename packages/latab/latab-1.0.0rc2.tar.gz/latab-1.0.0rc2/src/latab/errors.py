from abc import ABC, abstractmethod
from astropy.units import Quantity
from numpy.typing import NDArray
import numpy as np


class Error(ABC):

    @abstractmethod
    def getErrors(self, data: NDArray[np.float64]):
        pass


class FixError(Error):

    def __init__(self, error: float | Quantity):
        if isinstance(error, Quantity):
            self.__error = error.value
        elif isinstance(error, float):
            self.__error = error
        else:
            raise Exception("Fix error must be of type float or astropy.units.Quantity")

    def getErrors(self, data: NDArray[np.float64]):
        return np.ones(len(data)) * self.__error


class AbsoluteError(Error):

    def __init__(self, errors: NDArray[np.float64] | Quantity):
        if isinstance(errors, Quantity):
            self.__errors = errors.value
        elif isinstance(errors, np.ndarray):
            self.__errors = errors
        else:
            raise Exception("Absolute error must be of type numpy.ndarray or astropy.units.Quantity")

    def getErrors(self, data: NDArray[np.float64]):
        # TODO length check
        return self.__errors


class RelativeError(Error):

    def __init__(self, error: float):
        if isinstance(error, float):
            self.__error = error
        else:
            raise Exception("Relative error must be of type float")

    def getErrors(self, data: NDArray[np.float64]):
        return data * self.__error
