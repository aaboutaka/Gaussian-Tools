# Data-Extraction-Codes
## Quantum-related codes for extracting and using matrices.

**ExtractMOCoeff-AOOvlp**
is a python program that extracts MO matrices from fchk or fmat files and calculate SVD.

**Plots-Logfiles**
is a python program that plots the SCF, DIIS Error, and RMSPD versus number of SCF iterations for all log files present in the desired direcotry. This code overlaps the plots of all log files into one graph and then save it as PNG image files.

**Running the Script**

Example:

$python "ExtractMOCoeff-AOOvlp.py" h2.fchk 1 h2.fchk 1

- use flag 1 for alpha and flag -1 for beta
- the above example performs SVD for an alpha-alpha overlap

