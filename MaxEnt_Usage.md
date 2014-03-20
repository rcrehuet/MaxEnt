MaxEnt v1.0
===========

Maximum Entropy. Fit calculate RDCs to experimental RDCs

Mandatory arguments:


-c, --calculated                      Entry the file that contains the calculated RDCs

-e, --experimental                    Entry the file that contains the experimental RDCs

-r, --initial_residue                 Enter the initial residue number

-f, --final_residue                   Enter the final residue number


Optional arguments:
  
-h, --help                           Show the help message and exit

-s, --save {dat,txt,npy}             Save the Optimized RDCs into a file type '.dat', '.txt' or '.npy'

-sw,  --save_weights {dat,txt,npy}   Save the Optimized weights into a file type '.dat', '.txt' or '.npy'



Usage example :

python3 MaxEnt-1.0.py --experimental '/home/melchor/CSIC/IDP/MaximumEntropy/sendai_rdcs_fm.png.dat' --calculated '/home/melchor/CSIC/IDP/MaximumEntropy/sendai2/new-rdcs-values-sendai-t01.npy' --initial_residue '12' --final_residue '42' --save 'dat' --save_weights 'dat' 
