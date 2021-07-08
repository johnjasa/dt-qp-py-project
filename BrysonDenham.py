# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 14:48:48 2021

@author: rajan
"""

# import necessary libraries
import numpy as np
from scipy.optimize import minimize
from numpy.matlib import repmat
from scipy.sparse import csc_matrix
from scipy import sparse
from matplotlib.pyplot import spy
import time
import osqp
import matplotlib.pyplot as plt

# import dtqp specific libraries
from DTQPy_DEFECTS_TR import DTQPy_DEFECTS_TR
from DTQPy_create_bnds import DTQPy_create_bnds
from DTQPy_L import DTQPy_L
from DTQPy_SOLVER_osqp import DTQPy_SOLVER_osqp



# empty class aas a struct
class auxillary_data:
    pass

# struct to store problem details
ini = auxillary_data()

# System Matrices
A = np.array([[0,1],[0,0]])
B = np.array([[0],[1]])
G = np.array([])
d = np.array([])


x0 = np.array([[0],[0]])
xf = np.array([[0],[-1]])

xp = np.array([[1/9],[np.inf]])

L = np.array([1/2])

# DT details
ini.ny = np.size(B,0); ny = ini.ny
ini.nu = np.size(B,1); nu = ini.nu
ini.nt = 1000; nt = ini.nt
ini.npl = 0;
ini.nd = 0;
ini.auxdata = []
ini.nx = ini.nt*(nu+ny)
t0 = 0; tf = 1;

t = np.linspace(t0,tf,ini.nt)
ini.t = t.reshape(ini.nt,1);t = ini.t
ini.h = np.diff(t,axis=0);h = ini.h
ini.tm = np.array([])
ini.w = np.array([])
IN = [np.array([1]),np.array([2,3]),np.array([]),np.array([2,3]),np.array([2,3]),np.array([1])]
ini.IN = IN
I = np.arange(0,(ny+nu)*nt)
I = np.reshape(I,(nt,(ny+nu)),order = 'F')
ini.I_stored = I

dt = auxillary_data()
ini.NL = 1
dt.quadrature = 'CTR'

# begin measuring
begin = time.time()

# objective
Lfull = auxillary_data()
Lfull.left = 1;Lfull.right = 1; Lfull.matrix = np.array([1/2])
I,J,V = DTQPy_L(Lfull,ini,dt)
H = csc_matrix((V,(I,J)),shape = ((ny+nu)*nt,(ny+nu)*nt))
H = H+H.T

# UB,LB
UB = [auxillary_data() for n in range(3)]
LB = [auxillary_data() for n in range(2)]

UB[0].right = 4; UB[0].matrix = np.array([[0],[1]]) # initial states
LB[0].right = 4; LB[0].matrix =  np.array([[0],[1]])
UB[1].right = 5; UB[1].matrix = np.array([[0],[-1]]) # final states
LB[1].right = 5; LB[1].matrix = np.array([[0],[-1]])
UB[2].right = 2; UB[2].matrix = np.array([[1/9],[np.inf]]) # states

lb,ub = DTQPy_create_bnds(LB,UB,ini)

#spy(H)

# DEFECT_TR
Aeq,beq = DTQPy_DEFECTS_TR(A,B,G,d,ini)
#breakpoint()
#spy(Aeq)

# empty matrices
f = csc_matrix((1,1));Ain = csc_matrix((1,1));b = csc_matrix((1,1));
opts = {'eps_abs':1e-08,'eps_rel': 1e-08,'max_iter':10000}
#breakpoint()

prob = osqp.OSQP()

# combine problem elements in the way osqp needs
Al = sparse.vstack([Aeq,sparse.eye(ini.nx)]); Al = Al.tocsc()
Ul = np.vstack([beq.todense(),ub[None].T])
Ll = np.vstack([beq.todense(),lb[None].T])

# problem setup
prob.setup(P = H,q = None,A = Al,l = Ll,u = Ul, **opts)

# solve the problem
res = prob.solve()

# end time
end = time.time()

# extract result
X = res.x

# reshape
U = np.take(X,np.arange(0,nu*nt))
Y = np.take(X,np.arange(nu*nt,(nu+ny)*nt))
Y = np.reshape(Y,(nt,ny),order = 'F')

# plot
plt.close('all')
fig,ax = plt.subplots()
ax.plot(t, Y[:,0], label="x1")
ax.plot(t, Y[:,1], label="x2")
ax.set_xlabel('t')
ax.set_ylabel('x')
ax.set_title('States');

fig, a = plt.subplots()
a.plot(t,U,label = "u")
a.set_xlabel('t')
a.set_ylabel('u')
a.set_title('Controls');

          
        
        
        
