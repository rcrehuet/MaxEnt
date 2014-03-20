RunPales v1.0
=============

Usage

Extract RDC values from .pdb files using the PALES program.

Mandatory options:

-p, --path                                 Indicate the the path to the directory where the PALES executable is.

-id, --indirectory                         Indicate the localization of the directory where the pdbs are.

-od, --outdirectory                        Indicate the the directory where the RDCs outfiles are going to be generated.
  
-i,  --inD IND,                            Pales option. Indicate where is the Dipolar Coupling PDB input file, that                                                 determines which rdcs to calculate.




Optional Options:

--help, -h                                   Show this help message and exit.


--H                                          PALES option.  Determine ehether to use -H. This option, enables the                                                      comparision of all PDB atoms. By default, PALES Ccomapre all the PDB atoms                                                except Hydrogens.


Usage example:

python3 RunPales-1.0.py --Path '/home/melchor/Software/pales/linux/pales' 
--indirectory '/home/melchor/CSIC/IDP/Pales/sendai/flexible_mecano/pdbs'
--outdirectory'./test'  -inD '/home/melchor/CSIC/IDP/Pales/sendai/rdcs' --H
