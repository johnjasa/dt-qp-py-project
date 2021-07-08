# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 17:37:49 2021

@author: rajan
"""
import numpy as np

def DTQPy_getQPIndex(x,xtype,Flag,nt,I_stored):
    if (xtype ==1) or (xtype==2):
        I = I_stored[:,x-1]
        return I
    elif (xtype == 5) or (xtype == 7):
        I = I_stored[-1,x-1]
        return I
    elif (xtype == 0):
        I = 1
    else:
        I = I_stored[0,x-1]
        return I



def DTQPy_bnds(bnd,ini):
    nt = ini.nt; I_stored = ini.I_stored
    
    #breakpoint()
    
    # will change with t_multiprod
    Bndt = np.zeros((nt,ini.ny))
    
    for i in range(nt):
        Bndt[i,:] = bnd.matrix.T
        
    C = ini.IN[bnd.right-1]
    right = bnd.right
    Isav = np.array([],dtype = 'int');Vsav = np.array([])
    #breakpoint()
    
    
    for k in range(len(C)):
        
        if right in range(1,3):
            r = DTQPy_getQPIndex(C[k],right,1,nt,I_stored)
            
            if (len(np.shape(Bndt)) == 3):
                Vs = Bndt[:,:,k]
            else:
                Vs = Bndt[:,k]
                
            Isav = np.append(Isav,r)
            Vsav = np.append(Vsav,Vs)
            
        elif right in range(3,8):
            r = DTQPy_getQPIndex(C[k],right,0,nt,I_stored)
            #breakpoint()
            if (len(np.shape(Bndt)) == 3):
                Vs = Bndt[0,:,k]
            else:
                Vs = Bndt[0,k]
                
            Isav = np.append(Isav,r)
            Vsav = np.append(Vsav,Vs)
            
            
    
    #breakpoint()
    return Isav,Vsav