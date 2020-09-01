# TOPSIS, PROMETHEE II and VIKOR MCDM methods
The file "3in1.py" contains an implementation for three Multi-Criteria Decision Analisys methods:
TOPSIS, PROMETHEE II and VIKOR. This program reads the decision matrix from Excel file and calculates
rankings (which alternative is better then rest) using each method. 

To run this program properly you need to prepare a ".xls" or ".xlsx" file which contains:
- decision matrix, where alternatives values are placed in rows,
- criteria benefits IN FIRST ROW (1 for maximizing and 0 for minimizing each criteria).

You can execute application by following command:
python 3in1.py <filename>

Requirements:
1) Python 3.X
2) installed packages:
- numpy
- pandas
- copy
