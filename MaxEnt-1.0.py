"""
A maximum entropy implementation to reproduce RDCs.
Giving two sets of RDCs values, optimizes the values 
of one of the sets respect to the other.
"""
import sys, io
import numpy as np 
import pylab as plt
import scipy.optimize as so
import argparse
plt.ion()

def qave(lam, q):
    """
    return the 'corrected' experimental RDCs values
    """
    f = np.exp(np.dot(-q,lam))
    return np.dot(f,q)

def w(lam, q):
    """
    return the weights
    """
    w = np.exp(np.dot(-q,lam))
    w /= w.sum()
    return w

def grad_fit_rmsd2(lam, q, Q, thres, k):
    """
    return the gradient of fit_rmsd2 with respect to lam
    """
    # Gradient of qave (each row i is dq/dlambda_i)
    dq=-np.tensordot(q,(np.exp(np.dot(-q,lam))*q.T).T, axes=[0,0])
    # gradient of factq
    qa = qave(lam,q)
    qq = np.dot(qa,qa)
    qQ = np.dot(qa,Q)
    s = np.sign(qQ)
    dfactq = s*np.dot(dq,Q)*qq-2*np.abs(np.dot(Q,qa))*np.dot(dq,qa)
    dfactq /= qq*qq
    #gradient of fit_rmsd2
    # factor coming from f1
    factq = np.abs(qQ)/qq
    vec = qa*factq - Q
    f1 = np.dot(vec, vec)/len(Q)
    if f1>thres*thres:
        df1 = 2*np.dot(np.outer(dfactq,qa)+factq*dq, factq*qa-Q)
    else:
        df1 = np.zeros_like(lam)
    # factor coming from f2
    df2 = 2*k*lam
    return (df1+df2)/len(Q)

def fit_rmsd2(lam, q, Q, thres,k):
    """
    Return the threshold value achieved
    The average diffenrence between the reweighted values
    and the previous ones
    """
    qa = qave(lam, q)
    factq = np.abs(np.dot(Q, qa))/np.dot(qa, qa)
    vec = qa*factq - Q
    f1 = np.dot(vec, vec)
    if f1<thres*thres : f1 = thres*thres
    f2 = k*np.dot(lam, lam)
    return (f1+f2)/len(Q)

def rmsd(lam, q, Q):
    """
    Return the RMSD between experiental and calculated RDCs
    """
    curr_qave = qave(lam, q)
    factq = np.abs(np.dot(Q, curr_qave))/np.dot(curr_qave, curr_qave)
    vec = curr_qave*factq - Q
    return np.sqrt(np.dot(vec, vec)/len(Q))


#Defining the arguments:
argparser = argparse.ArgumentParser(description="Maximum Entropy. Fit calculate RDCs to experimental RDCs")
data=argparser.add_argument_group("Initial_data", "Entry the files that contain the RDCs to evaluate.")
data.add_argument("--calculated", "-c", help="Second set of RDCs. Entry the file that contains the second set of RDCs. Calculated RDCs.")
data.add_argument("--experimental", "-e", help = "First set of RDCs. Experimental or Calculated RDCs ensemble to the second set is going to be fitted")
data.add_argument("--save", "-s", choices=["dat","txt","npy"], default=False, help="Save the Optimized RDCs")
data.add_argument("--save_weights", "-sw", choices=["dat","txt","npy"], default=False, help="Save the Optimized weights")
data.add_argument("--save_image", "-si",  choices=["png","jpeg"], default=False, help="Save an image of the Optimized RDCs together with the initial RDCs sets")


residues=argparser.add_argument_group("residues", "Range of residues represnted by the RDCs")
residues.add_argument("--initial_residue", "-r", help = "Initial residue")
residues.add_argument("--final_residue", "-f", help = "Final residue")


global args
args = argparser.parse_args()

k = 10000000. 

if args.experimental: # Experimental RDCs data is loaded. 
    type = args.experimental.split(".")[-1]
    if type == "txt" or type == "dat" :
        Q=np.loadtxt(args.experimental)
    elif type == "npy" or type == "npz":
        Q=np.load(args.experimental)        
resind = Q[:, 0]
Q = Q[:, 1]

if args.calculated:#  Calculated RDCs data is loaded. 
    type = args.calculated.split(".")[-1]
    if type == "txt"or type == "dat" :
        q=-np.loadtxt(args.calculated)
    elif type == "npy" or type == "npz":
        q=-np.load(args.calculated)

residues = np.arange(int(args.initial_residue), (int(args.final_residue)+1))
residues = np.asarray(residues)
q = q[:, residues]	

lam = np.zeros(len(Q)) #Lambda initialization
# Generate initial plot
fig = plt.figure(figsize=(11, 6))
ax = fig.add_subplot(121)
ax.set_xlim(int(args.initial_residue), int(args.final_residue))
ref, = ax.plot(residues, Q, 'o-')


#The maximum agreement we can expect is the same as for reweighting
threshold = 1.0

#add the unscaled values
qnew = qave(lam, q)
factq = np.abs(np.dot(Q, qnew))/np.dot(qnew, qnew)
ax.plot(residues, factq*qnew, 'x-')
axw = fig.add_subplot(122)
line, = ax.plot(residues, factq*qnew, 'o-')


#Plot Weights
wplot, = axw.semilogy(np.ones(len(q)), '-')
axw.set_ylim(0.01,100)
plt.draw()

#Minimize reducing k until threshold is reached
fit = rmsd(lam, q, Q)
print ("="*50)
print (" "*15, " Maximum Entropy ")
print ("="*50)
print ("%9s %12s %18s " %('Fit','k','Lambda'))
print
print ("="*50)
print("{:10.3f} {:15.1f} {:15.3e}".format(fit, k, 0.0))

first_time=True
while True:
    lam = so.fmin_ncg(fit_rmsd2, lam, fprime=grad_fit_rmsd2,
          args=(q, Q, threshold,k), disp=False, epsilon = 1e-10)
    fit = rmsd(lam, q, Q)
    qnew = qave(lam, q)
    factq = np.abs(np.dot(Q, qnew))/np.dot(qnew, qnew)
    line.set_ydata(factq*qnew)
    wplot.set_ydata(np.sort(w(lam,q)*len(q)))
    avelam = np.sqrt(np.dot(lam, lam)/len(lam))
    print("{:10.3f} {:15.1f} {:15.3e}" .format(fit, k, avelam))
    plt.draw()
    if first_time and fit < threshold*1.05:
        lam *= 0.0
        k *= 1.5
    elif fit > threshold*1.05 :
        first_time=False 
        k *= 0.8
    if not first_time and fit < threshold*1.05: break

# Save Optimized RDCS
if args.save == "txt" or args.save == "dat":
    np.savetxt('./Optimized_RDCs.'+args.save, qnew)
if args.save == "npy" :           
    np.save('./Optimized_RDCs', qnew)    
#Save Optimized weights
if args.save_weights == "txt" or args.save == "dat":
    np.savetxt('./Optimized_weights.'+args.save, np.sort(w(lam,q)))
if args.save_weights == "npy" :           
    np.save('./Optimized_weights', np.sort(w(lam,q)))
#Save Iamge
if args.save_image == "png":
	plt.savefig('Final_Optimized_RDCs.png')
if args.save_image == "jpeg":
	plt.savefig('Final_Optimized_RDCs.jpeg')    
input()
