"""
Run pales-linux to generate all RDCs from the PDBs of a directory.
The -H option determines which option to use when calling pales
"""
import glob, sys, os
import subprocess as subp
import argparse

def createPath(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def generate_rdcs_files(pales_path, initial_structure, initial_dipolar_coupling, dipolar_coupling_output, H):
    fileout =  open("/dev/null", 'w')
    if args.H:
        pales_call = '%s -pdb %s -inD %s -outD %s.rdcs -H' % (pales_path, initial_structure, initial_dipolar_coupling, dipolar_coupling_output)
    else:
        pales_call = '%s -pdb %s -inD %s -outD %s.rdcs' % (pales_path, initial_structure, initial_dipolar_coupling, dipolar_coupling_output)
    pales_call = pales_call.split()
    subp.call(pales_call, stdout = fileout, stderr=subp.STDOUT)

argparser = argparse.ArgumentParser(description="Extract RDC values from .pdb files using the PALES program.")
data=argparser.add_argument_group("")
data.add_argument('--path', '-p', help ="The path to the directory where the pales executable is.")
data.add_argument('--indirectory', '-id', help ="The directory where the pdbs are.")
data.add_argument('--outdirectory', '-od', help ="The directory where the RDCs outfiles are going to be.")
data.add_argument('--inD', '-i',  help ="Pales option. Dipolar Coupling PDB input file. Determine which rdcs to calculate.")
data.add_argument('-H', action='store_true', help ="Use -H option in Pales. Enable comparision of all PDB atoms. By default, all except Hydrogens")

global args
args = argparser.parse_args()

#Checking the Initial options

if not args.path: print('Define the path to the run_pales executable with --path option')
if args.indirectory:
    filelist_pdbs = glob.glob(args.indirectory +'/*.pdb') 
    filelist_pdbs.sort()
else: print('Define the path to the directory where the PDBs are with --directory option')
if args.outdirectory: createPath(args.outdirectory)
else: args.outdirectory=args.indirectory
if not args.inD: print('Provide the initial RDCS data into a table with --inD option')

#Executing generate_rdc_files. Storing in a .dat file the name of all the processed PDBs in order.

writer=open(args.outdirectory+'Processed_PDB.dat', mode='w')
print (args.outdirectory)
print('Generating %i rdcs from %s.'%(len(filelist_pdbs), args.indirectory))
for i, filename in enumerate(filelist_pdbs):
    print("\rDoing structure %5d" %(i,), end="")
    generate_rdcs_files(args.path, filename, args.inD, filename[:-4], args.H)
    subp.call(['mv', filename[:-4]+'.rdcs', args.outdirectory])
    writer.write(filename+'\n')
writer.close()
print()
