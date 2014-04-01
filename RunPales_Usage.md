RunPales v1.0
=============

usage: `RunPales.py [-h] --path PATH [--outdirectory OUTDIRECTORY]
                   [--outarray OUTARRAY] --inD IND [-H]
                   indirectory`

Extract RDC values from .pdb files using the PALES program.

positional arguments:
  `indirectory`           The directory where the pdbs are.

optional arguments:
  `-h`, `--help`            show this help message and exit
  `--path PATH`, `-p PATH`  The path to the pales executable is.
  `--outdirectory OUTDIRECTORY`, `-outD OUTDIRECTORY`
                        The directory where the RDCs outfiles are going to be.
                        (Default is indirectory)
  `--outarray OUTARRAY`, `-outA OUTARRAY`
                        The name of the file containing the array of RDCs.
                        (Default is rdcs.npy)
  `--inD IND`             Dipolar Coupling input file. Determine which rdcs to
                        calculate (see Pales documpentation).
  `-H`                    Use -H option in Pales (see Pales documentation).



Usage examples:
```
python3 RunPales-1.0.py --path '/home/melchor/Software/pales/linux/pales' \
--indirectory '/home/melchor/CSIC/IDP/Pales/sendai/flexible_mecano/pdbs' \
--outdirectory './test'  -inD '/home/melchor/CSIC/IDP/Pales/sendai/rdcs' -H
```
