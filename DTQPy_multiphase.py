# -*- coding: utf-8 -*-
"""
DTQPy_multiphase
Solve the LQDO problem without mesh refinement

Contributor: Athul Krishna Sundarrajan (AthulKrishnaSundarrajan on Github)
Primary Contributor: Daniel R. Herber (danielrherber on Github)
"""
import numpy as np
from DTQPy_create import DTQPy_create
from DTQPy_SOLVER import DTQPy_SOLVER

def DTQPy_multiphase(setup,opts):
    
    H,f,c,A,b,Aeq,beq,lb,ub,setup,internal,opts = DTQPy_create(setup,opts)
    
    
    [X,F,internal,opts] = DTQPy_SOLVER(H,f,A,b,Aeq,beq,lb,ub,internal,opts)
    
    F = F+c
    
    nt = internal.nt;nu = internal.nu; ny = internal.ny; npl = internal.npl
    
    T = internal.t
    U = np.reshape(X[np.arange(0,nu*nt)],(nt,nu),order = 'F')
    Y = np.reshape(X[np.arange(nu*nt,(ny+nu)*nt)],(nt,ny),order = 'F')
    P = np.reshape(X[np.arange((nu+ny)*nt,(nu+ny)*nt+npl)],(npl,1),order = 'F')
    
    return T,U,Y,P,F,internal,opts