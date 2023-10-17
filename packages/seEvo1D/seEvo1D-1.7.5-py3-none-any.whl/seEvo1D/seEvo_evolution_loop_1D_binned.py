import numpy as np
import math
import itertools
import scipy as sc
import copy
from threading import Thread
from multiprocessing import Pool

mdv = [1]

def death(iPop, pdt):
    return iPop[1,:] - pdt
    
def divide(iPop, pdv):
    return iPop[1,:] + pdv
    
def mutate(iPop, pdm):
    return iPop[1,:] + pdm

def seEvo1DnormBinned(iPop, cap, tau_x, A, mut_prob, mut_effect, simTime):
    global mdv
    popSize = sum(iPop[1,:])
    
    mdt = (popSize/cap)**A
    tau = tau_x
    simTime = simTime + tau

    if iPop[1,len(iPop[0,:]) - 1] > 0:
        c = np.array(range(int(iPop[0, len(iPop[0,:])-1])+1, int(iPop[0, len(iPop[0,:])-1])+501, 1))
        mdv = np.append(mdv, ((1+abs(mut_effect))**c)**(1-2*(mut_effect < 0)))
        a = len(iPop[0,:])
        iPop = np.array([np.append(iPop[0,:], np.zeros((500))), np.append(iPop[1,:], np.zeros((500)))], dtype=np.int32)
        iPop[0,a:len(iPop[1,:])] = c
    
    dt = np.zeros(len(iPop[1,:]))
    dv = np.zeros(len(iPop[1,:]))
    dm = np.zeros(len(iPop[1,:]))
    for i in range(len(iPop[1,:])):
        if all(iPop[1,i:len(iPop[1,:])] == 0):
            break
        pdv = 1 - np.exp(-tau*mdv[i])
        pdt = 1 - np.exp(-tau*mdt)
        
        pdv = pdv * (1 - pdt)
        pdm = pdv * mut_prob
        pdv = pdv * (1 - mut_prob)
        pdr = 1 - pdv - pdm - pdt
        
        R = np.random.multinomial(iPop[1,i], [pdt, pdv, pdm, pdr])
        dt[i] = R[0]
        dv[i] = dv[i] + R[1]
        dm[i + 1] = R[2]        
    
    # R = np.random.multinomial(1, np.array([dt, dv, dm, dr]).T, iPop[1,:])
    
    iPop[1,:] = divide(iPop, dv)
    
    iPop[1,:] = mutate(iPop, dm) 
    
    iPop[1,:] = death(iPop, dt)
    
    if iPop[1,0] == 0 and iPop[1,1]:
        mdv = mdv[1:len(iPop[0,:])]
        iPop = iPop[:,1:len(iPop[0,:])]
    
    return iPop, simTime