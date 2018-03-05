#!/usr/bin/env python3
"""
A maximum entropy implementation to reproduce experimental data.
Giving the experimental data (Q), and the calculated data for each member of the ensemble (q), calculates
weights to fit Q (with an gaussian error given by sigma)

This vesion includes a better way to include errors based on:
https://arxiv.org/abs/1801.05247

sigma2 is equivalent to the previous threshold and is the error in the exp. data assumed to be normally distributed.

This version is for chemical shifts, where one need not and cannot rescale (factq removed)

Author: Ramon Crehuet

Date: 02/02/2018
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as so
import argparse
plt.ion()


def w(lam, q):
    """
    return the weights
    """
    w = np.exp(np.dot(-q,lam))
    w /= w.sum()
    return w

def qave(lam, q):
    """
    return the expected data values for a given lambas
    """
    return np.dot(w(lam,q),q)


def grad_gamma(lam, q, Q, sigma2):
    """
    return the gradient of gamma with respect to lam. Eq. 34 and 32
    """
    return Q - qave(lam,q) + lam*sigma2

def gamma(lam, q, Q, sigma2):
    """
    Return the gamma function. Eq. 33
    """
    gamma = np.log(np.exp(-np.dot(q,lam)).mean()) #sum / Ns
    gamma += np.dot(lam,Q)
    gamma += 0.5*np.dot(sigma2, lam**2) #Gaussian error. See eq. 21
    return gamma

def rmsd(lam, q, Q):
    """
    Return the RMSD between experiental and calculated values.
    """
    qa = qave(lam, q)

    vec = qa - Q
    return np.sqrt(np.dot(vec, vec)/len(Q))


#Defining the arguments:
parser = argparse.ArgumentParser(description="Maximum Entropy fit of ensemble data to experimental data")
parser.add_argument("calculated", help="Data for each structure. A numpy array or a text file of shape (M,N).")
parser.add_argument("experimental", help = "Experimental data. A numpy array or a text file of shape (2,N), where the first column is the residue number and the second its data value")
parser.add_argument("--save", "-s", \
    help="Save the Optimized data in text or numpy format (according to extension)")
parser.add_argument("--save_weights", "-sw", \
   help="Save the Optimized weights in text or numpy (npy) format (according to extension).")
parser.add_argument("--save_image", "-si",  \
   help="Save an image of the Optimized data together with the initial data sets and the optimized weights")

parser.add_argument("--initial_residue", "-i", help = "Initial residue to fit", type=int)
parser.add_argument("--final_residue", "-f", help = "Final residue to fit", type=int)


args = parser.parse_args()

if args.experimental: # Experimental data is loaded.
    fileext = args.experimental.split(".")[-1]
    if fileext == "npy" :
        Q = np.load(args.experimental)
    else:
        Q = np.loadtxt(args.experimental)
resind = Q[:, 0]
resind = np.asarray(resind, dtype=np.int)
Q = Q[:, 1]

if args.calculated:# Calculated data is loaded.
    fileext = args.calculated.split(".")[-1]
    if fileext == "npy" :
        q = np.load(args.calculated)
    else:
        q = np.loadtxt(args.calculated)

if args.initial_residue:
    ini = args.initial_residue-1
else:
    ini = 0
if args.final_residue:
    fin = args.final_residue-1
else:
    fin = len(Q)    
residues = np.arange(int(ini), int(fin))

q = q[:, residues]	

lam = np.zeros(len(Q)) #Lambda initialization

#The experimental error (a vector)
sigma2 = 2.0**2
sigma2 = sigma2*np.ones_like(lam)

#Minimize reducing k until threshold is reached
fit = rmsd(lam, q, Q)
print ("="*50)
print (" "*15, " Maximum Entropy Fit")
print ("="*50)
print ("%9s %18s ".format('Fit','Lambda'))
print
print ("="*50)
print("{:10.3f}  {:15.3e}".format(fit, 0.0))

result = so.minimize(gamma, lam.astype(np.float128), jac=grad_gamma,
      args=(q.astype(np.float128), Q.astype(np.float128), sigma2.astype(np.float128)))
lam = result.x
fit = rmsd(lam, q, Q)
avelam = np.sqrt(np.dot(lam, lam)/len(lam))
print("{:10.3f}  {:15.3e}".format(fit, avelam))
print("="*10*len(lam))
print((len(lam)*"{:8.2e} ").format(*lam))

# Generate plots
fig = plt.figure(figsize=(11, 6))
ax = fig.add_subplot(121)
#ref, = ax.plot(resind, Q, 'o-', label='experimental')
ax.plot(resind, q.mean(0)-Q, 'x-', label='inital error')
qnew = qave(lam, q)
line, = ax.plot(resind, qnew-Q, 'o-', label='re-weighted error')
ax.hlines(0, resind[0], resind[-1])


#Plot Weights
axw = fig.add_subplot(122)
w_opt = w(lam, q)
wplot, = axw.semilogy(np.sort(w_opt*len(q)), '-')

ax.legend(fontsize='small', loc='best')
axw.set_ylim(10**np.floor(np.log10(np.min(len(q)*w_opt))),10**np.ceil(np.log10(np.max(len(q)*w_opt))))
#plt.show()
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
