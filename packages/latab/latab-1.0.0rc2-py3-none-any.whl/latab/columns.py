from abc import ABC, abstractmethod
import numpy as np
from numpy.typing import NDArray
from .formatters import Formatter, FloatFormatter, ExponentialFormatter
from .errors import Error
from .converter import convertUnitToLateX
from astropy.units import Quantity


class Column(ABC):

    def __init__(self, header: str):
        self._header = header

    def getHeader(self):
        return self._header

    @abstractmethod
    def getCell(self, row: int):
        pass


class TextColumn(Column):

    def __init__(self, header: str, texts: list):
        super(TextColumn, self).__init__(header)
        self.__texts = texts

    def getCell(self, row: int):
        return self.__texts[row]

    def __len__(self):
        return len(self.__texts)


class SerialNumberColumn(TextColumn):

    def __init__(self, header: str, rowCount: int):
        texts = []
        for i in range(rowCount):
            texts.append("{}.".format(i + 1))
        super(SerialNumberColumn, self).__init__(header, texts)


class DataColumn(Column):

    def __init__(self, header: str, data: NDArray[np.float64] | Quantity, error: Error = None, formatter: Formatter = None):
        super(DataColumn, self).__init__(header)

        if isinstance(data, Quantity):
            self.__data = data.value
            self._header = self._header + " [" + convertUnitToLateX(data.unit) + "]"
        elif isinstance(data, np.ndarray):
            self.__data = data
        else:
            raise Exception("Data must be of type numpy.ndarray or astropy.units.Quantity")
        dataOrder = np.max(np.ceil(np.abs(np.log10(self.__data))))

        if formatter is None:
            if dataOrder > 4:
                self.__formatter = ExponentialFormatter()
            else:
                self.__formatter = FloatFormatter()
        elif not isinstance(formatter, Formatter):
            raise Exception("The argument 'formatter' must be a subclass of latab.Formatter")
        else:
            self.__formatter = formatter

        if error is not None:
            if isinstance(error, Error):
                self.__errors = error.getErrors(self.__data)
            else:
                raise Exception("Error must be of type latab.Error")

    def getHeader(self):
        return self._header

    def getCell(self, row: int):
        if hasattr(self, "_DataColumn__errors"):
            return self.__formatter.format(self.__data[row], self.__errors[row])
        else:
            return self.__formatter.format(self.__data[row])

    def __len__(self):
        return len(self.__data)
