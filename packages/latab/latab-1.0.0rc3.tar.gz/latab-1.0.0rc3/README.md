# LaTab

Utility to help convert numpy arrays to a LateX table. The main goal is to provide a code snippet with proper number and unit formatting, with a basic table layout. Formatting of the table itself is expected to be done manually by the user in the LateX document, but simpler features might be added in later versions if the need arises.

## Examples

### Imports and sample data

```
import numpy as np
from astropy import units
from latab import Table, FloatFormatter, FixError, AbsoluteError, RelativeError

array1 = np.array([13.35000606, 0.76642346, 1.42476496, 9.27577478, 3.83978828, 1.88922311])
array2 = np.array([1.8131508, 5.3586463, 5.6288616, 7.4245393, 8.1266426, 4.5811065]) * units.g / units.cm**3
array3 = np.array([9.47738782e+20, 9.06469621e+20, 2.50771562e+20, 8.85737743e+20, 7.04538193e+20,
                   8.90478371e+20]) * units.kg
errors = np.array([0.034574, 0.072827, 0.04782, 0.098236, 0.018896, 0.071311]) * units.g / units.cm**3
planets = ["Kepler137b", "Kepler137c", "Kepler137d", "Kepler137e", "Kepler137f", "Kepler137g"]
```

### Example

```
(Table("Nobody expects the Spanish inquisition.")
 .serialColumn("Planet", 6)
 .dataColumn("Semi-major Axis [AU]", array1, FixError(0.0005))
 .dataColumn("$\\varrho$", array2, AbsoluteError(errors), FloatFormatter(2, 2))
 .dataColumn("Mass", array3, RelativeError(0.05))).print()
```

```
\begin{table}
    \centering
    \begin{tabular}{|c|c|c|c|} \hline
        Planet & Semi-major Axis [AU] & $\varrho$ [$\mathrm{g/cm^{3}}$] & Mass [$\mathrm{kg}$] \\ \hline
        1. & $13.350 \pm 0.0005$  & $1.81 \pm 0.03$  & $(9.477 \pm 0.4739)\cdot 10^{20}$  \\ \hline
        2. & $0.766 \pm 0.0005$  & $5.36 \pm 0.07$  & $(9.065 \pm 0.4532)\cdot 10^{20}$  \\ \hline
        3. & $1.425 \pm 0.0005$  & $5.63 \pm 0.05$  & $(2.508 \pm 0.1254)\cdot 10^{20}$  \\ \hline
        4. & $9.276 \pm 0.0005$  & $7.42 \pm 0.10$  & $(8.857 \pm 0.4429)\cdot 10^{20}$  \\ \hline
        5. & $3.840 \pm 0.0005$  & $8.13 \pm 0.02$  & $(7.045 \pm 0.3523)\cdot 10^{20}$  \\ \hline
        6. & $1.889 \pm 0.0005$  & $4.58 \pm 0.07$  & $(8.905 \pm 0.4452)\cdot 10^{20}$  \\ \hline
    \end{tabular}
    \caption{Nobody expects the Spanish inquisition.}
\end{table}
```

![Example 1](https://astro.bklement.com/latab/imgage1.png)

### Localized example with different decimal separator

```
(Table("Aprócska kalapocska, benne csacska macska mocska.")
 .textColumn("Bolygó", planets)
 .dataColumn("Félnagytengely [AU]", array1, FixError(0.0005))
 .dataColumn("$\\varrho$", array2, AbsoluteError(errors), FloatFormatter(2, 2))
 .dataColumn("Tömeg", array3, RelativeError(0.05))).print(separator=',')
```

```
\begin{table}
    \centering
    \begin{tabular}{|c|c|c|c|} \hline
        Bolygó & Félnagytengely [AU] & $\varrho$ [$\mathrm{g/cm^{3}}$] & Tömeg [$\mathrm{kg}$] \\ \hline
        Kepler137b & $13,350 \pm 0,0005$  & $1,81 \pm 0,03$  & $(9,477 \pm 0,4739)\cdot 10^{20}$  \\ \hline
        Kepler137c & $0,766 \pm 0,0005$  & $5,36 \pm 0,07$  & $(9,065 \pm 0,4532)\cdot 10^{20}$  \\ \hline
        Kepler137d & $1,425 \pm 0,0005$  & $5,63 \pm 0,05$  & $(2,508 \pm 0,1254)\cdot 10^{20}$  \\ \hline
        Kepler137e & $9,276 \pm 0,0005$  & $7,42 \pm 0,10$  & $(8,857 \pm 0,4429)\cdot 10^{20}$  \\ \hline
        Kepler137f & $3,840 \pm 0,0005$  & $8,13 \pm 0,02$  & $(7,045 \pm 0,3523)\cdot 10^{20}$  \\ \hline
        Kepler137g & $1,889 \pm 0,0005$  & $4,58 \pm 0,07$  & $(8,905 \pm 0,4452)\cdot 10^{20}$  \\ \hline
    \end{tabular}
    \caption{Aprócska kalapocska, benne csacska macska mocska.}
\end{table}
```

![Example 2](https://astro.bklement.com/latab/imgage2.png)
