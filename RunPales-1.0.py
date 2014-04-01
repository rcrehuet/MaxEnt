#!/usr/bin/env python3
"""
Run pales-linux to generate all RDCs from the PDBs of a directory.
The -H option determines which option to use when calling pales

Author: Ramon Crehuet, Melchor Sanchez-Martinez
Date: 02/04/2014
"""
import sys, os
import glob
import subprocess as subp
import argparse
import numpy as np

def createPath(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def get_rdcs(name):
    filein = open(name, 'r')
    rdcs = []
    for line in filein:
        line = line.split()
        try: int(line[0])
        except ValueError: continue
        except IndexError: continue
        rdcs.append(float(line[8]))
    return np.asarray(rdcs)

def generate_rdcs_files(pales_path, initial_structure, initial_dipolar_coupling, dipolar_coupling_output, H):
    fileout = open("/dev/null", 'w')
    if args.H:
        pales_call = '%s -pdb %s -inD %s -outD %s.rdcs -H' % (pales_path, initial_structure, initial_dipolar_coupling, dipolar_coupling_output)
    else:
        pales_call = '%s -pdb %s -inD %s -outD %s.rdcs' % (pales_path, initial_structure, initial_dipolar_coupling, dipolar_coupling_output)
    pales_call_list = pales_call.split()
    out = subp.call(pales_call_list, stdout = fileout, stderr=subp.STDOUT)
    if out != 0:
        print("\nCould not locate executable pales or error executing the following pales call:")
        print(pales_call)
        sys.exit()

parser = argparse.ArgumentParser(description="Extract RDC values from .pdb files using the PALES program.")
parser.add_argument('--path', '-p', help ="The path to the pales executable is.", required=True)
parser.add_argument('indirectory', help ="The directory where the pdbs are.")
parser.add_argument('--outdirectory', '-outD', \
  help ="The directory where the RDCs outfiles are going to be. (Default is indirectory)")
parser.add_argument('--outarray', '-outA', default='rdcs.npy',\
  help ="The name of the file containing the array of RDCs. (Default is rdcs.npy)")
parser.add_argument('--inD',  \
        help ="Dipolar Coupling input file. Determine which rdcs to calculate (see Pales odcumpentation).", \
        required=True)
parser.add_argument('-H', action='store_true', help ="Use -H option in Pales (see Pales documentation).")

args = parser.parse_args()

#Checking the Initial options

filelist_pdbs = glob.glob(args.indirectory +'/*.pdb')
filelist_pdbs.sort()

if args.outdirectory: createPath(args.outdirectory)
else: args.outdirectory=args.indirectory

#Executing generate_rdc_files. Storing in a .dat file the name of all the processed PDBs in order.

writer=open(args.outdirectory+'Processed_PDB.dat', mode='w')
rdcs_array = []

print('Generating %i rdcs from %s in %s.'%(len(filelist_pdbs), args.indirectory, args.outdirectory))
for i, filename in enumerate(filelist_pdbs):
    print("\rDoing structure %5d" %(i+1,), end="")
    generate_rdcs_files(args.path, filename, args.inD, filename[:-4], args.H)
    if args.outdirectory!=args.indirectory: subp.call(['mv', filename[:-4]+'.rdcs', args.outdirectory])
    writer.write(filename+'\n')
    # Get the RDCS for the file
    rdcs_array.append(get_rdcs(filename))
  
writer.close()
print()

rdcs_array = np.asarray(rdcs_array)
np.save(args.outarray, rdcs_array)

