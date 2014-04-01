MaxEnt
======

MaxEnt is a script that re-weights a set of structures to fit a given set of Residual Dipolar Couplings (RDC) values. It is based on a Maximum Entropy principle. 

MaxEnt needs as inputs a matrix of MxN and a vector of N values. The MxN matrix should contain the N RDCs of the M structures in thet set, and the second vector should contain the experimental or objetive RDCs.
The RDCs will be scaled to fit the experimental RDCs.

To simplify the generation of RDCs from a set of PDB structures, we provide the python scripy RunPales.py.

The full algorithm is described in:

* M. Sanchez-Martinez, R. Crehuet "Application of the Maximum Entropy Principle to determine ensembles of Intrinsically Disordered Proteins from Residual Dipolar Couplings", submitted to _Phys. Chem. Chem. Phys._

Please, cite this reference if you use the MaxEnt code.

RunPales
========

RunPales is an script that execute the PALES (http://spin.niddk.nih.gov/bax/software/PALES/) pales-linux to
generate RDCs from PDB files. It then reads the Pales RDC files and converts the data into a numpy array. This array is the input MaxEnt reads.


Versions
=========
MaxEnt-1.0   03/2014
RunPales-1.0 03/2014


For any request:
-----------------

Ramon Crehuet Simon, ramon.crehuet@iqac.csic.es

Melchor Sanchez Martinez, melchor.sanchez@iqac.csic.es

Computational and Theoretical Chemistry Group, http://www.iqac.csic.es/qteor/


----------------------------------------------------------
 Every file of this repository is freely availabe under:
 
 . Licence   : GNU_V2   
 
 . Copyright : CSIC, Ramon Crehuet Simon (2014) © 
 
                                 

