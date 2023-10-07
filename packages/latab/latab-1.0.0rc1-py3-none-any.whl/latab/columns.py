from abc import ABC, abstractmethod
import numpy as np
from numpy import typing as npt
from .formatters import Formatter, FloatFormatter, ExponentialFormatter
from astropy import units


class Column(ABC):

    def __init__(self, header: str):
        self._header = header

    def getHeader(self):
        return self._header

    @abstractmethod
    def getCell(self, row: int):
        pass


class SerialNumberColumn(Column):

    def __init__(self, header: str, rowCount: int):
        super(SerialNumberColumn, self).__init__(header)
        self.__rowCount = rowCount

    def getCell(self, row: int):
        if row >= self.__rowCount:
            raise IndexError()
        return "{}.".format(row + 1)

    def __len__(self):
        return self.__rowCount


class TextColumn(Column):

    def __init__(self, header: str, texts: list):
        super(TextColumn, self).__init__(header)
        self.__texts = texts

    def getCell(self, row: int):
        return self.__texts[row]

    def __len__(self):
        return len(self.__texts)


class EmptyColumn(TextColumn):

    def __init__(self, header: str, rowCount: int):
        super(EmptyColumn, self).__init__(header, [""] * rowCount)


class DataColumn(Column):

    def __init__(self,
                 header: str,
                 data: npt.NDArray[np.float64] | units.Quantity,
                 formatter: Formatter = None,
                 inlineUnit: bool = False,
                 maxOrder: int = 4):
        super(DataColumn, self).__init__(header)
        self.__maxOrder = maxOrder
        self.__setData(data)
        self.__setFormatter(formatter)
        self.__inlineUnit = inlineUnit
        self.__errors = None

    def fixError(self, error: float | units.Quantity, precision: int):
        if isinstance(error, units.Quantity):
            self.__errors = np.ones(len(self.__data)) * error.value
        elif isinstance(error, float):
            self.__errors = np.ones(len(self.__data)) * error
        else:
            raise Exception("Fix error must be of type float or astropy.units.Quantity")
        self.__formatter.adjustAdditionalErrorPrecision(precision)
        return self

    def relativeError(self, error: float):
        if isinstance(error, float):
            self.__errors = self.__data * error
        else:
            raise Exception("Relative error must be of type float")
        return self

    def absoluteError(self, errors: npt.NDArray[np.float64] | units.Quantity):
        if isinstance(errors, units.Quantity):
            self.__errors = errors.value
        elif isinstance(errors, np.ndarray):
            self.__errors = errors
        else:
            raise Exception("Absolute error must be of type numpy.ndarray or astropy.units.Quantity")
        return self

    def unit(self, unit: str | units.Unit | units.CompositeUnit | units.IrreducibleUnit):
        if self.__unit is not None:
            if self.__unit.startswith("$"):
                raise Exception("Unit is already set to {}".format(self.__unit[9:-2]))
            else:
                raise Exception("Unit is already set to {}".format(self.__unit))
        self.__setUnit(unit)
        return self

    def getHeader(self):
        if self.__inlineUnit or self.__unit is None:
            return self._header
        else:
            return self._header + " [" + self.__unit + "]"

    def getCell(self, row: int):
        if self.__errors is not None:
            cell = self.__formatter.format(self.__data[row], self.__errors[row])
            if self.__inlineUnit and self.__unit is not None:
                cell += self.__unit
            return cell
        else:
            cell = self.__formatter.format(self.__data[row])
            if self.__inlineUnit and self.__unit is not None:
                cell += self.__unit
            return cell

    def __len__(self):
        return len(self.__data)

    def __convertUnit(self, unit: units.Unit | units.CompositeUnit | units.IrreducibleUnit):
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

    def __setData(self, data: npt.NDArray[np.float64] | units.Quantity) -> None:
        if isinstance(data, units.Quantity):
            self.__data = data.value
            self.__setUnit(data.unit)
        elif isinstance(data, np.ndarray):
            self.__data = data
            self.__unit = None
        else:
            raise Exception("Data must be of type numpy.ndarray or astropy.units.Quantity")
        self.__dataOrder = np.max(np.ceil(np.abs(np.log10(self.__data))))

    def __setUnit(self, unit: str | units.Unit | units.CompositeUnit | units.IrreducibleUnit):
        if isinstance(unit, units.UnitBase):
            self.__unit = self.__convertUnit(unit)
        elif isinstance(unit, str):
            self.__unit = unit
        else:
            raise Exception("Unit must be of type str or a subclass of astropy.units.core.UnitBase")
        return self

    def __setFormatter(self, formatter: Formatter) -> None:
        if formatter is None:
            if self.__dataOrder > self.__maxOrder:
                self.__formatter = ExponentialFormatter(3)
            else:
                self.__formatter = FloatFormatter(3)
        elif not isinstance(formatter, Formatter):
            raise Exception("The argument 'formatter' must be a subclass of latab.Formatter")
        else:
            self.__formatter = formatter
