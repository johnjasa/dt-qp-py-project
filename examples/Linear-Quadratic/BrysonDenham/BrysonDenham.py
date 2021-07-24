# -*- coding: utf-8 -*-
"""
BrysonDenham
Bryson Denham problems

Contributor: Athul Krishna Sundarrajan (AthulKrishnaSundarrajan on Github)
Primary Contributor: Daniel R. Herber (danielrherber on Github)
"""

# import necessary libraries
import numpy as np

from src.classes.DTQPy_CLASS_OPTS import *
from src.classes.DTQPy_CLASS_SETUP import *
from src.DTQPy_solve import DTQPy_solve

#from DTQPy_create_bnds import DTQPy_create_bnds
import matplotlib.pyplot as plt

# empty class aas a struct
aux = auxdata()

opts = options()
opts.dt.nt = 1000

opts.solver.tolerence = 1e-5
#opts.solver.maxiters = 10000

# System Matrices
A = np.array([[0,1],[0,0]])
B = np.array([[0],[1]])


# # # DT details
# ini = auxdata()
# ini.ny = np.size(B,0); ny = ini.ny
# ini.nu = np.size(B,1); nu = ini.nu
# ini.nt = 1000; nt = ini.nt
# ini.npl = 0;
# ini.nd = 0;
# ini.auxdata = []
# ini.nx = ini.nt*(nu+ny)
# t0 = 0; tf = 1;

# t = np.linspace(t0,tf,ini.nt)
# ini.t = t.reshape(ini.nt,1);t = ini.t
# ini.h = np.diff(t,axis=0);h = ini.h
# ini.tm = np.array([])
# ini.w = np.array([])
# IN = [np.array([1]),np.array([2,3]),np.array([]),np.array([2,3]),np.array([2,3]),np.array([1])]
# ini.IN = IN
# I = np.arange(0,(ny+nu)*nt)
# I = np.reshape(I,(nt,(ny+nu)),order = 'F')
# ini.I_stored = I

# dt = auxillary_data()
# ini.NL = 1
# dt.quadrature = 'CTR'

# begin measuring
#begin = time.time()

# objective

L = LQ_objective(left = 1,right = 1,matrix = 1/2)
# Lfull = auxillary_data()
# Lfull.left = 1;Lfull.right = 1; Lfull.matrix = np.ones((1,1))*1/2
# Lfull = [Lfull]
# #breakpoint()
# I,J,V = DTQPy_L(Lfull,ini,dt)
# H = csc_matrix((V,(I,J)),shape = ((ny+nu)*nt,(ny+nu)*nt))
# H = H+H.T

# UB,LB
UB = [Simple_Linear_Bound() for n in range(3)]
LB = [Simple_Linear_Bound() for n in range(2)]
# UB = [auxillary_data() for n in range(3)]
# LB = [auxillary_data() for n in range(2)]

UB[0].right = 4; UB[0].matrix = np.array([[0],[1]]) # initial states
LB[0].right = 4; LB[0].matrix =  np.array([[0],[1]])
UB[1].right = 5; UB[1].matrix = np.array([[0],[-1]]) # final states
LB[1].right = 5; LB[1].matrix = np.array([[0],[-1]])
UB[2].right = 2; UB[2].matrix = np.array([[1/9],[np.inf]]) # states
#breakpoint()
#lb,ub = DTQPy_create_bnds(LB,UB,ini)
#breakpoint()
#spy(H)

# DEFECT_TR
#Aeq,beq = DTQPy_DEFECTS_TR(A,B,G,d,ini,[])
#breakpoint()
#spy(Aeq)

# empty matrices
# f = csc_matrix((1,1));Ain = csc_matrix((1,1));b = csc_matrix((1,1));
# opts = {'eps_abs':1e-8,'eps_rel': 1e-8,'max_iter':1000}
# breakpoint()

# prob = osqp.OSQP()

# # combine problem elements in the way osqp needs
# Al = sparse.vstack([Aeq,sparse.eye(ini.nx)]); Al = Al.tocsc()
# Ul = np.vstack([beq.todense(),ub[None].T])
# Ll = np.vstack([beq.todense(),lb[None].T])

# # problem setup
# prob.setup(P = H,q = None,A = Al,l = Ll,u = Ul, **opts)

# # solve the problem
# res = prob.solve()

# # end time
# end = time.time()

# # extract result
# X = res.x

# # reshape
# U = np.take(X,np.arange(0,nu*nt))
# Y = np.take(X,np.arange(nu*nt,(nu+ny)*nt))
# Y = np.reshape(Y,(nt,ny),order = 'F')

# combine
s = setup()

s.t0 = 0; s.tf = 1
s.A = A; s.B = B;
s.Lagrange = L
s.UB = UB; s.LB = LB
s.auxdata = aux


breakpoint()
T,U,Y,P,F,internal,opts = DTQPy_solve(s,opts)

# plot
plt.close('all')
fig,ax = plt.subplots()
ax.plot(T, Y[:,0], label="x1")
ax.plot(T, Y[:,1], label="x2")
ax.set_xlabel('t')
ax.set_ylabel('x')
ax.set_title('States');

fig, a = plt.subplots()
a.plot(T,U,label = "u")
a.set_xlabel('t')
a.set_ylabel('u')
a.set_title('Controls');

          
        
        
        
