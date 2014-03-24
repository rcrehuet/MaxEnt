MaxEnt v1.0
===========

Maximum Entropy. Fit a set of calculated RDCs to experimental or calculated RDCs

Mandatory arguments:


-c, --calculated                      Entry the file that contains the second set of RDCs. Average of calculated RDCs from                                       a molecular simulation.

-e, --experimental                    Entry the file that contains the first set od RDCS. Experimental or Calculated RDCs                                       ensemble. Are the values to which second set of RDCs values are going to be fitted.

-r, --initial_residue                 Enter the initial residue number

-f, --final_residue                   Enter the final residue number


Optional arguments:
  
-h,  --help                           Show the help message and exit

-s,  --save {dat,txt,npy}             Save the Optimized RDCs into a file type '.dat', '.txt' or '.npy'

-sw, --save_weights {dat,txt,npy}     Save the Optimized weights into a file type '.dat', '.txt' or '.npy'

-si, --save_image                     Save an image of the Optimized RDCs together with the initial RDCs sets in 'png' or                                       'jpeg' format


Usage example :

python3 MaxEnt-1.0.py --experimental '/home/melchor/CSIC/IDP/MaximumEntropy/sendai_rdcs_fm.png.dat' --calculated '/home/melchor/CSIC/IDP/MaximumEntropy/sendai2/new-rdcs-values-sendai-t01.npy' --initial_residue '12' --final_residue '42' --save 'dat' --save_weights 'dat' --save_image 'png'
