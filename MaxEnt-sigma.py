#!/usr/bin/env python3
"""
A maximum entropy implementation to reproduce RDCs.
Giving two sets of RDCs values, optimizes the values
of one of the sets respect to the other.

This vesion includes a better way to include errors based on:
https://arxiv.org/abs/1801.05247

sigma2 is equivalent to the previous threshold and is the error in the exp. data assumed to be normally distributed.

Author: Ramon Crehuet, Melchor Sanchez-Martinez

Date: 03/04/2014
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as so
import argparse
plt.ion()

def qave(lam, q):
    """
    return the expected RDCs values for a given lambas
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

def grad_fit_rmsd2(lam, q, Q, sigma2, k):
    """
    return the gradient of fit_rmsd2 with respect to lam
    """
    Qtemp = Q + lam*sigma2
    # Gradient of qave (each row i is dq/dlambda_i)
    dq=-np.tensordot(q,(np.exp(np.dot(-q,lam))*q.T).T, axes=[0,0])
    # gradient of factq
    qa = qave(lam,q)
    qq = np.dot(qa,qa)
    qQ = np.dot(qa,Qtemp)
    s = np.sign(qQ)
    dfactq = s*np.dot(dq,Qtemp)*qq-2*np.abs(np.dot(Qtemp,qa))*np.dot(dq,qa)
    dfactq /= qq*qq
    #gradient of fit_rmsd2
    # factor coming from f1
    factq = np.abs(qQ)/qq
    vec = qa*factq - Qtemp
    df1 = 2*np.dot(np.outer(dfactq,qa)+factq*dq-sigma2*np.ones_like(lam), factq*qa-Qtemp)
    # factor coming from f2
    df2 = 2*k*lam
    return (df1+df2)/len(Q)

def fit_rmsd2(lam, q, Q, sigma2,k):
    """
    Return the f2 function. See the associated article.
    """
    qa = qave(lam, q)
    Qtemp = Q+lam*sigma2
    factq = np.abs(np.dot(Qtemp, qa))/np.dot(qa, qa)
    vec = qa*factq - Qtemp
    f1 = np.dot(vec, vec)
    f2 = k*np.dot(lam, lam)
    return (f1+f2)/len(Q)

def rmsd(lam, q, Q):
    """
    Return the RMSD between experiental and calculated RDCs. The f1 function in 
    the associated article.
    """
    qa = qave(lam, q)
    factq = np.abs(np.dot(Q, qa))/np.dot(qa, qa)
    vec = qa*factq - Q
    return np.sqrt(np.dot(vec, vec)/len(Q))


#Defining the arguments:
parser = argparse.ArgumentParser(description="Maximum Entropy fit of ensemble RDCs to experimental RDCs")
parser.add_argument("calculated", help="RDCs for each structure. A numpy array or a text file of shape (M,N).")
parser.add_argument("experimental", help = "Experimental RDCs. A numpy array or a text file of shape (2,N), where the first column is the residue number and the second its RDC value")
parser.add_argument("--save", "-s", \
    help="Save the Optimized RDCs in text or numpy format (according to extension)")
parser.add_argument("--save_weights", "-sw", \
   help="Save the Optimized weights in text or numpy (npy) format (according to extension).")
parser.add_argument("--save_image", "-si",  \
   help="Save an image of the Optimized RDCs together with the initial RDCs sets and the optimized weights")

parser.add_argument("--initial_residue", "-i", help = "Initial residue to fit by the RDCs", type=int)
parser.add_argument("--final_residue", "-f", help = "Final residue to fit by the RDCs", type=int)


args = parser.parse_args()

k = 10000000.

if args.experimental: # Experimental RDCs data is loaded.
    fileext = args.experimental.split(".")[-1]
    if fileext == "npy" :
        Q = np.load(args.experimental)
    else:
        Q = np.loadtxt(args.experimental)
resind = Q[:, 0]
resind = np.asarray(resind, dtype=np.int)
Q = Q[:, 1]

if args.calculated:# Calculated RDCs data is loaded.
    fileext = args.calculated.split(".")[-1]
    if fileext == "npy" :
        q = -np.load(args.calculated)
    else:
        q = -np.loadtxt(args.calculated)

if args.initial_residue:
    ini = args.initial_residue-1
else:
    ini = 0
if args.final_residue:
    fin = args.final_residue-1
else:
    fin = len(Q)    
residues = np.arange(int(ini), int(fin)+1)

q = q[:, residues]	

lam = np.zeros(len(Q)) #Lambda initialization
# Generate initial plot
fig = plt.figure(figsize=(11, 6))
ax = fig.add_subplot(121)
ref, = ax.plot(resind, Q, 'o-', label='experimental')

#The experimental error
sigma2 = 1.**2

#add the unscaled values
qnew = qave(lam, q)
factq = np.abs(np.dot(Q, qnew))/np.dot(qnew, qnew)
ax.plot(resind, factq*qnew, 'x-', label='inital')
axw = fig.add_subplot(122)
line, = ax.plot(resind, factq*qnew, 'o-', label='re-weighted')

#Plot Weights
wplot, = axw.semilogy(np.ones(len(q)), '-')
axw.set_ylim(0.1,10)
plt.draw()

#Minimize reducing k until threshold is reached
fit = rmsd(lam, q, Q)
print ("="*50)
print (" "*15, " Maximum Entropy Fit")
print ("="*50)
print ("%9s %12s %18s " %('Fit','k','Lambda'))
print
print ("="*50)
print("{:10.3f} {:15.1f} {:15.3e}".format(fit, k, 0.0))

first_time=True
while True:
    lam = so.fmin_ncg(fit_rmsd2, lam, fprime=grad_fit_rmsd2,
          args=(q, Q, sigma2,k), disp=False, epsilon = 1e-10)
    fit = rmsd(lam, q, Q)
    qnew = qave(lam, q)
    qnew *= np.abs(np.dot(Q, qnew))/np.dot(qnew, qnew)
    line.set_ydata(qnew)
    wplot.set_ydata(np.sort(w(lam,q)*len(q)))
    avelam = np.sqrt(np.dot(lam, lam)/len(lam))
    print("{:10.3f} {:15.1f} {:15.3e}" .format(fit, k, avelam))
    plt.draw()
    if first_time and fit < sigma2:
        lam *= 0.0
        k *= 1.5
    elif fit >= sigma2 :
        first_time=False
        k *= 0.9
    if not first_time and fit < sigma2: break

w_opt = w(lam, q)
ax.legend(fontsize='small', loc='best')
axw.set_ylim(10**np.floor(np.log10(np.min(len(q)*w_opt))),10**np.ceil(np.log10(np.max(len(q)*w_opt))))
plt.show()
# Save Optimized RDCS
if args.save:
    fileext = args.save.split(".")[-1]
    if fileext =='npy':
        np.save(args.save, np.c_[resind, qnew])
    else:
        np.savetxt(args.save, np.c_[resind,qnew])
#Save Optimized weights
if args.save_weights:
    fileext = args.save_weights.split(".")[-1]
    if fileext =='npy':
        np.save(args.save_weights, w_opt)
    else:
        np.savetxt(args.save_weights, w_opt)

#Save Iamge
if args.save_image:
    plt.savefig(args.save_image)

input()
