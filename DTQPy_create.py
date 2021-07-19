# -*- coding: utf-8 -*-
"""
DTQPy_create
Transcribe the continuous problem formulations 

Contributor: Athul Krishna Sundarrajan (AthulKrishnaSundarrajan on Github)
Primary Contributor: Daniel R. Herber (danielrherber on Github)
"""
import numpy as np
from scipy import sparse
from DTQPy_CLASS_INTERNAL import DTQPy_initialize
from DTQPy_createH import DTQPy_createH
from DTQPy_createf import DTQPy_createf
from DTQPy_createc import DTQPy_createc
from DTQPy_DEFECTS import DTQPy_DEFECTS
from DTQPy_create_YZ import DTQPy_create_YZ
from DTQPy_create_bnds import DTQPy_create_bnds

def DTQPy_create(setup,opts):
    
    # initialize some stuff
    setup,internal = DTQPy_initialize(setup,opts.dt)
    #breakpoint()
    # objective function
    H = DTQPy_createH(setup.Lquadratic,setup.Mquadratic,internal,opts)
    f = DTQPy_createf(setup.Llinear,setup.Mlinear,internal,opts)
    c = DTQPy_createc(setup.Lconstant,setup.Mconstant,internal,opts)
    
    # constraints
    
    # defect constraints
    Aeq1,beq1 = DTQPy_DEFECTS(setup.A,setup.B,setup.G,setup.d,internal,opts)
    #breakpoint()
    # linear path and boundary equality constraints
    Aeq2,beq2 = DTQPy_create_YZ(setup.Y,internal)
    
    # combine linear equality constraints
    Aeq = sparse.vstack([Aeq1,Aeq2])
    beq = sparse.vstack([beq1,beq2])
    
    # path and boundary inequality constraints
    A,b = DTQPy_create_YZ(setup.Z,internal)
    
    # create simple bounds
    lb,ub = DTQPy_create_bnds(setup.LB,setup.UB,internal)
    
    #breakpoint()
    
    return H,f,c,A,b,Aeq,beq,lb,ub,setup,internal,opts