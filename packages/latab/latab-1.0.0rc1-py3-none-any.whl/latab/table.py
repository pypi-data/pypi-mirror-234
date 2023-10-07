import numpy as np
from .columns import Column, DataColumn


class Table():

    def __init__(self, columns: Column, caption: str = None):
        self.__columns = columns
        self.__rowCount = len(columns[0])
        if not np.all(np.array(list(map(len, columns))) == self.__rowCount):
            raise Exception("Columns have different lengths")
        self.__caption = caption

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

    def fromDictionary(dict: dict, caption: str = None):
        columns = []
        for header, data in dict.items():
            columns.append(DataColumn(header, data))
        return Table(columns, caption)
