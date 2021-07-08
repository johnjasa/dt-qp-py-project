# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 17:05:33 2021

@author: rajan
"""
import numpy as np
from DTQPy_bnds import DTQPy_bnds

def DTQPy_create_bnds(LB,UB,ini):
    lb = np.ones((ini.nx,len(LB)))*-np.inf
    ub = np.ones((ini.nx,len(UB)))*np.inf
    
    for i in range(len(LB)):
      
        I,V = DTQPy_bnds(LB[i],ini)
        #breakpoint()
        lb[I,i] = V
        
    lb = np.max(lb,axis=1)
    #breakpoint()
    
    for i in range(len(UB)):
        I,V = DTQPy_bnds(UB[i],ini)
        #breakpoint()
        ub[I,i] = V
    
    ub = np.min(ub,axis=1)
   # breakpoint()
    return lb,ub