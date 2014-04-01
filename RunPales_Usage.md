RunPales v1.0
=============

RunPales. Extract RDC values from .pdb files using the PALES program.

Mandatory arguments:

`-p`, `--path`                             Indicate the the path to the directory where the PALES executable is.

`-id`, `--indirectory`                         Indicate the localization of the directory where the pdbs are.

`-od`, `--outdirectory`                        Indicate the the directory where the RDCs outfiles are going to be generated.
  
`-i`,  `--inD` ,                            Pales option. Indicate where is the Dipolar Coupling input file,
                                           that determines which rdcs to calculate.




Optional arguments:

`--help`, `-h`                                 Show this help message and exit.


`-H`                                         PALES option.  Determine whether to use -H. This option, uses the explicit                                                hydrogens of the PDB. See the PALES documentation for further details.


Usage examples:
```
python3 RunPales-1.0.py --path '/home/melchor/Software/pales/linux/pales' \
--indirectory '/home/melchor/CSIC/IDP/Pales/sendai/flexible_mecano/pdbs' \
--outdirectory './test'  -inD '/home/melchor/CSIC/IDP/Pales/sendai/rdcs' -H
```
