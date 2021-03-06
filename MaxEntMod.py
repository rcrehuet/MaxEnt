#!/usr/bin/env python3
"""
A maximum entropy implementation to reproduce RDCs.

This vesion includes a better way to include errors based on:
https://arxiv.org/abs/1801.05247

sigma2 is the error in the exp. data assumed to be normally distributed.

This version is for chemical shifts, where one need not and cannot rescale (factq removed)

This version works as a module and should be importable.

Author: Ramon Crehuet

Date: 03/05/2018
"""

import numpy as np


def w(lam, q):
    """
    return the weights
    """
    delta = q.mean(0) #shift of q values to redue exp overflow
    w = np.exp(np.dot(-q+delta,lam))
    w /= w.sum()
    return w

def qave(lam, q):
    """
    return the expected data values for a given lambas
    """
    return np.dot(w(lam,q),q)


def _grad_gamma(lam, q, Q, sigma2):
    """
    return the gradient of gamma with respect to lam. Eq. 33
    """
    return Q - qave(lam,q) + lam*sigma2

def _gamma(lam, q, Q, sigma2):
    """
    Return the gamma function. Eq. 34. q Values shifted by Q to reduce Overflow in exp.
    """
    gamma = np.log(np.exp(-np.dot(q-Q,lam)).mean()) #sum / Ns
    gamma += 0.5*np.dot(sigma2, lam**2) #Gaussian error. See eq. 21
    return gamma


def rmsd(lam, q, Q):
    """
    Return the RMSD between experiental and calculated values.
    """
    qa = qave(lam, q)
    vec = qa - Q
    return np.sqrt(np.dot(vec, vec)/len(Q))

def n_eff(lam, q):
    """
    Return the normalized Kish n_effective size
    """
    return 1./np.sum(w(lam, q)**2)/q.shape[0]


def fit(q,Q, sigma2, lam=None):
    """
    Optimize the lambdas.
    Input:
    q - array of shape (N,M) with N structures and M observables (Chemical shifts).
    Q - array of shape (M,) with M experimental observables (Chemical Shifts).
    """
    import scipy.optimize as so
    #Minimize
    if lam is None:
        lam = np.zeros(len(Q)) #Lambda initialization
    if type(sigma2) is float or sigma2.size==1:
        sigma2 = sigma2*np.ones_like(lam)

    #result = so.minimize(_gamma, lam.astype(np.float128), jac=_grad_gamma,
    #  args=(q.astype(np.float128), Q.astype(np.float128), sigma2.astype(np.float128)))

    result = so.minimize(_gamma, lam, jac=_grad_gamma,
           args=(q, Q, sigma2))
    if not result.success: print("Minimisation not converged!")
    return result.x
        


if __name__=='__main__':
    import matplotlib.pyplot as plt
    plt.ion()
    q = np.load('q.npy')[:,:21]
    Q = np.load('Q.npy')[:21,1]
    resind = np.arange(1,len(Q)+1)
    # Generate initial plot
    fig = plt.figure(figsize=(11, 6))
    ax = fig.add_subplot(121)
    ref, = ax.plot(resind, Q, 'o-', label='experimental')

    #The experimental error
    sigma2 = 2.**2

    #add the unscaled values
    lam = np.zeros(len(Q))
    qnew = qave(lam, q)
    ax.plot(resind, qnew, 'x-', label='inital')
    axw = fig.add_subplot(122)
    line, = ax.plot(resind, qnew, 'o-', label='re-weighted')
    line2, = ax.plot(resind, Q, 's-', label="Exp. + error")

    #Plot Weights
    wplot, = axw.semilogy(np.ones(len(q)), '-')
    axw.set_ylim(0.1,10)
    plt.draw()

    current_rmsd = rmsd(lam, q, Q)
    print ("="*50)
    print (" "*15, " Maximum Entropy Fit")
    print ("="*50)
    print ("{:>10s} {:>15s} ".format('Fit','RMS Lambda'))
    print
    print ("="*50)
    print("{:10.3f}  {:15.3e}".format(current_rmsd, 0.0))
    
    lam = fit(q,Q, sigma2)
    
    current_rmsd = rmsd(lam, q, Q)

    qnew = qave(lam, q)
    line.set_ydata(qnew)
    line2.set_ydata(Q+lam*sigma2)
    wplot.set_ydata(np.sort(w(lam,q)*len(q)))
    rmslam = np.sqrt(np.dot(lam, lam)/len(lam))
    print("{:10.3f}  {:15.3e}" .format(current_rmsd, rmslam))
    print ("="*50)
    plt.draw()

    w_opt = w(lam, q)
    ax.legend(fontsize='small', loc='best')
    axw.set_ylim(10**np.floor(np.log10(np.min(len(q)*w_opt))),10**np.ceil(np.log10(np.max(len(q)*w_opt))))
    #plt.show()

    input()
