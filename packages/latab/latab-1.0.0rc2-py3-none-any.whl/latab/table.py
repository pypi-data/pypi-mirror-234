from numpy import float64
from .columns import DataColumn, SerialNumberColumn, TextColumn
from astropy.units import Quantity
from numpy.typing import NDArray
from .formatters import Formatter
from .errors import Error


class Table():

    def __init__(self, caption: str = None):
        self.__columns = []
        self.__caption = caption

    def __checkRowCount(self, rowCount: int):
        if not hasattr(self, "_Table__rowCount"):
            self.__rowCount = rowCount
        elif rowCount != self.__rowCount:
            raise Exception("Columns have different lengths")

    def serialColumn(self, header: str, rowCount: int):
        self.__checkRowCount(rowCount)
        self.__columns.append(SerialNumberColumn(header, rowCount))
        return self

    def textColumn(self, header: str, texts: list):
        self.__checkRowCount(len(texts))
        self.__columns.append(TextColumn(header, texts))
        return self

    def dataColumn(self, header: str, data: NDArray[float64] | Quantity, error: Error = None, formatter: Formatter = None):
        self.__checkRowCount(len(data))
        self.__columns.append(DataColumn(header, data, error, formatter))
        return self

    def lines(self, tabLength: int = 4, separator: chr = '.'):
        lines = []
        lines.append("\\begin{table}")
        lines.append("\t\\centering".expandtabs(tabLength))
        lines.append(("\t\\begin{tabular}{|" + "c|" * len(self.__columns) + "} \\hline").expandtabs(tabLength))
        s = "\t\t".expandtabs(tabLength)
        for column in self.__columns:
            s += column.getHeader()
            s += " & "
        s = s[0:-2]
        s += "\\\\ \hline"
        lines.append(s)
        for i in range(self.__rowCount):
            s = "\t\t".expandtabs(tabLength)
            for column in self.__columns:
                cell = column.getCell(i)
                if isinstance(column, DataColumn) and separator != '.':
                    s += cell.replace(".", separator)
                else:
                    s += cell
                s += " & "
            s = s[0:-2]
            s += "\\\\ \hline"
            lines.append(s)
        lines.append("\t\\end{tabular}".expandtabs(tabLength))
        if self.__caption is not None:
            lines.append(("\t\caption{" + self.__caption + "}").expandtabs(tabLength))
        lines.append("\\end{table}")
        return lines

    def print(self, tabLength: int = 4, separator: chr = '.'):
        for line in self.lines(tabLength, separator):
            print(line)
