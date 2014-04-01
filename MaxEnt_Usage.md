MaxEnt v1.0
===========
The program implements the Maximum Entropy fit of an ensemble of RDCs to a set of experimental RDCs as described in the publication [1].

We provide the RunPales code to generate an array of RDCs, but the initial RDCs can be generated with other software.

If you use this code, please cite the following publication:

[1] M. Sanchez-Martinez, R. Crehuet, "Application of the Maximum Entropy Principle to determine ensembles of Intrinsically Disordered Proteins from Residual Dipolar Couplings", submitted to _Phys. Chem. Chem. Phys._

##Usage:
```bash
MaxEnt.py [-h] [--save SAVE] [--save_weights SAVE_WEIGHTS]
                 [--save_image SAVE_IMAGE] [--initial_residue INITIAL_RESIDUE]
                 [--final_residue FINAL_RESIDUE] 
                 calculated experimental
```

Maximum Entropy fit of ensemble RDCs to experimental RDCs

positional arguments:

  `calculated`            RDCs for each structure. A numpy array or a text file
                        of shape (M,N).
                        
  `experimental`          Experimental RDCs. A numpy array or a text file of
                        shape (2,N), where the first column is the residue
                        number and the second its RDC value
                        

optional arguments:

  `-h`, `--help`            show this help message and exit
  
  `--save SAVE`, `-s SAVE`  Save the Optimized RDCs in text or numpy format
                        (according to extension)
                        
  `--save_weights SAVE_WEIGHTS`, `-sw SAVE_WEIGHTS`
                        Save the Optimized weights in text or numpy (npy)
                        format (according to extension).
                        
  `--save_image SAVE_IMAGE`, `-si SAVE_IMAGE`
                        Save an image of the Optimized RDCs together with the
                        initial RDCs sets and the optimized weights
                        
  `--initial_residue INITIAL_RESIDUE`, `-i INITIAL_RESIDUE`
                        Initial residue to fit by the RDCs
                        
  `--final_residue FINAL_RESIDUE`, `-f FINAL_RESIDUE`
                        Final residue to fit by the RDCs



Usage example :

`python3 ./MaxEnt-1.0.py new-rdcs-values-sendai-t01.npy sendai_rdcs_fm.png.dat -i 13 -f 43 -sw w.npy -si foo.png -s q.dat`
Alternatively, after download, you can convert the python file into an executable with: chmod +x MaxEnt-1.0.py. Then, you can call it with:
`./MaxEnt-1.0.py new-rdcs-values-sendai-t01.npy sendai_rdcs_fm.png.dat -i 13 -f 43 -sw w.npy -si foo.png -s q.dat`
