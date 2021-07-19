# -*- coding: utf-8 -*-
"""
DTQPy_tmultiprod
Evaluate the product of potentially time-varying matrices

Contributor: Athul Krishna Sundarrajan (AthulKrishnaSundarrajan on Github)
Primary Contributor: Daniel R. Herber (danielrherber on Github)
"""
import numpy as np
from DTQPy_tmatrix import DTQPy_tmatrix
import types

def DTQPy_tmultiprod(matrices,p,*args):
    
    # convert lambda function to a np array of type object
    if type(matrices) is types.LambdaType:
            Ae = np.empty((1,1),dtype ='O')
            Ae[0,0] = matrices
            matrices = Ae
            
    # empty matrix
    if len(matrices)==0:
        A = np.array([])
    else:
        # simgle matrix
        A = DTQPy_tmatrix(matrices,p,*args) 
        
        
    return A
        