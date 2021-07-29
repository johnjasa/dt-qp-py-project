# -*- coding: utf-8 -*-
"""
DTQPy_CLASS_SETUP
Class to carry the information about different problem variables

Contributor: Athul Krishna Sundarrajan (AthulKrishnaSundarrajan on Github)
Primary Contributor: Daniel R. Herber (danielrherber on Github)
"""
import numpy as np
import types

class setup:
    def __init__(self,A = np.empty((0,0)),B = np.empty((0,0)),G = np.empty((0,0)),d = np.empty((0,0)),Lagrange = [], Mayer = [],Lquadratic = [],Llinear = [],Lconstant = [],Mquadratic = [],Mlinear = [],Mconstant = [], UB = [], LB = [], Y = [], Z = [],t0 = 0,tf = None,auxdata = None ):
        
        self.A = A; self.B = B; self.G = G; self.d = d;
        
        self.Lagrange = Lagrange; self.Mayer = Mayer
        self.Lquadratic = Lquadratic;self.Llinear = Llinear;self.Lconstant = Lconstant;
        self.Mquadratic = Mquadratic;self.Mlinear = Mlinear;self.Mconstant = Mconstant;
        self.t0 = t0; self.tf = tf;
        self.UB = UB; self.LB = LB
        self.Y = Y; self.Z = Z;
        self.auxdata = auxdata
        
    def Check_Struct(self):
        if isinstance(self.Lagrange,list):
            pass
        elif isinstance(self.Lagrange,LQ_objective):
            self.Lagrange = [self.Lagrange]
        #breakpoint()
        if isinstance(self.Mayer,list):
            pass
        elif isinstance(self.Mayer,LQ_objective):
            self.Mayer = [self.Mayer]
            
        if isinstance(self.UB,list):
            pass
        elif isinstance(self.UB,Simple_Bounds):
            self.UB = [self.UB]
        
        if isinstance(self.LB,list):
            pass
        elif isinstance(self.LB,Simple_Bounds):
            self.LB = [self.LB]
            
        if isinstance(self.Y,list):
            pass
        elif isinstance(self.Y,Simple_Linear_Constraints):
            self.Y = [self.Y]
          
        if isinstance(self.Z,list):
            pass
        elif isinstance(self.Z,Simple_Linear_Constraints):
            self.Z = [self.Z]
        
            
    def Check_Matrix_shape(self):
        if isinstance(self.A,np.ndarray):
            s = np.shape(self.A)
            
            if len(s) == 1:
                self.A = np.reshape(self.A,(s[0],1),order = 'F')
        else:
                 self.A = np.ones((1,1))*self.A  
        
        if isinstance(self.B,np.ndarray):
            s = np.shape(self.B)
            
            if len(s) == 1:
                self.B = np.reshape(self.B,(s[0],1),order = 'F')
        else:
                 self.B = np.ones((1,1))*self.B  
                 
        if isinstance(self.G,np.ndarray):
            s = np.shape(self.G)
            
            if len(s) == 1:
                self.G = np.reshape(self.G,(s[0],1),order = 'F')
        else:
                 self.G = np.ones((1,1))*self.G  
            
        
        
        
        
class LQ_objective:
    
    
    def __init__(self,left=None,right=None,matrix=np.empty((0,0))):
        '''
        Parameters
        ----------
        left : int, 
            . The default is None.
        right : TYPE, optional
            DESCRIPTION. The default is None.
        matrix : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        '''
        self.right = right
        self.left = left
        self.matrix = matrix
        
        
        
    def Check_shape(self):
        #breakpoint()
        if isinstance(self.matrix,(np.ndarray)):
            
            s = np.shape(self.matrix)
            
            if len(s) ==1:
                self.matrix = np.reshape(self.matrix,(s[0],1),order = 'F')
                
        else:
            self.matrix = np.ones((1,1))*self.matrix
            
            
   

class Simple_Bounds:
    
    
    def __init__(self,right=None,matrix = np.empty((0,0))):
        self.right = right
        self.matrix = matrix
        

    
    def Check_shape(self):
        #breakpoint()
        if isinstance(self.matrix,(np.ndarray)):
            
            s = np.shape(self.matrix)
            
            if len(s) == 1:
                self.matrix = np.reshape(self.matrix,(s[0],1),order = 'F')
                
        elif type(self.matrix) is types.LambdaType:
            temp = np.empty((1,1),dtype = 'O')
            temp[0,0] = self.matrix
            self.matrix = temp
        else:
            self.matrix = np.ones((1,1))*self.matrix
    
class Simple_Linear_Constraints:
    
    def __init__(self,linear=[],b = []):
        self.linear = linear
        self.b = b
        
    def Check_shape(self):
        
        if isinstance(self.linear,list):
            pass
        elif isinstance(self.linear,Simple_Bounds):
            self.linear = [self.linear]
            
        #breakpoint()
        if isinstance(self.b,(np.ndarray)):
            
            s = np.shape(self.b)
            
            if len(s) == 1:
                self.b = np.reshape(self.b,(s[0],1),order = 'F')
                
        elif type(self.b) is types.LambdaType:
            temp = np.empty((1,1),dtype = 'O')
            temp[0,0] = self.b
            self.b = temp
                
        else:
            self.b = np.ones((1,1))*self.b
        
            
class auxdata():
    pass