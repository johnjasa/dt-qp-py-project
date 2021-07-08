# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 01:49:41 2021

@author: rajan
"""

import numpy as np
from numpy.matlib import repmat

def DTQPy_getQPIndex(x,xtype,Flag,nt,I_stored):
    if (xtype ==1) or (xtype==2):
        I = I_stored[:,x-1]
        return I
    elif (xtype == 5) or (xtype == 7):
        I = I_stored[-1,x-1]
    elif (xtype == 0):
        I = 1
    else:
        I = I_stored[0,x]
        
            

def DTQPy_L(Lfull,ini,opts):
    
    nt = ini.nt; t = ini.t; tm = ini.tm; h = ini.h; w = ini.w;
    auxdata = ini.auxdata; IN = ini.IN; Istored = ini.I_stored;
    quadrature = opts.quadrature; 
    NL = ini.NL;
    
    OffFlag = (quadrature == 'CQHS')
    
    
    Isav = np.array([]); Jsav = np.array([]); HWsav = np.array([]); Qsav = np.array([])
    
    h0 = np.append(h,np.array([0]))
    
    for k in range(NL):
        
        Lleft = Lfull.left
        Lright = Lfull.right
        Lmatrix = Lfull.matrix
        
        # replaced by tmultiprod
        Lt = np.zeros((nt,1,1))
        
        for i in range(nt):
            Lt[i,:,:] = Lmatrix
        
        # to do include offlag
        
        
        if Lleft != 0:
            R = IN[Lleft-1]
        else:
            R = 0
            
        if Lright !=0:
            C = IN[Lright-1]
        else:
            C = 0
            
        #breakpoint()
        for i in range(len(R)):
            for j in range(len(C)):
                
                Lv = Lt[:,i,j]
                
                if Lv.any():
                    #breakpoint()
                    r = DTQPy_getQPIndex(R,Lleft,1,nt,Istored) # To do
                    c = DTQPy_getQPIndex(C,Lright,1,nt,Istored) # to do
                    #breakpoint()
                    
                    Isav = np.append(Isav,r)
                    Jsav = np.append(Jsav,c)
                    
                    # tp do
                    
                    HWsav = np.append(HWsav,h0)
                    
                    Qsav = np.append(Qsav,Lt)
                    #breakpoint()
                    
        V = (HWsav + np.roll(HWsav,1,axis=0))*Qsav/2
     
    return Isav,Jsav,V
        
        
    

                   
    