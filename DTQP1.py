# -*- coding: utf-8 -*-
"""
DTQP1
Complex linear-quadratic dynamic optimization problem

"""

import numpy as np

from DTQPy_CLASS_SETUP import *
from DTQPy_CLASS_OPTS import *
from DTQPy_solve import DTQPy_solve

opts = options()
opts.dt.nt = 10
opts.solver.tolerence = 1e-5

# time horizon
t0 = 0; tf = 1;

# problem parameters
aux = auxdata()

aux.g = lambda t: np.sin(2*np.pi*t) + 0.5

# system dynamics
A = np.array([[-1,2,0,0],[3,-4,0,0],[1,2,-1,0],[1,0,0,0]])
B = np.array([[1,0],[-1,0],[0,1/20],[0,0]])
G = np.zeros((4,1))

L = [LQ_objective() for n in range(5)]

# Lagrange term
L[0].left = 1;L[0].right = 1;L[0].matrix = np.eye(2)/10
L[1].left = 1;L[1].right = 2;L[1].matrix = np.array([[1,1,0,0],[0,0,0,0]])
L[2].left = 2;L[2].right = 2;L[2].matrix = np.zeros((4,4));L[2].matrix[1,1] = 5
L[3].left = 0;L[3].right = 2;L[3].matrix =np.empty((1,4),dtype = 'O'); L[3].matrix[0,1] = lambda t: -5*2*aux.g(t);L[3].matrix[0,0] = 0;L[3].matrix[0,2] = 0;L[3].matrix[0,3] = 0
L[4].left = 0; L[4].right = 0;L[4].matrix =np.empty((1,1),dtype = 'O');L[4].matrix[0,0] = lambda t: 5*(aux.g(t))**2

# mayer term
M = LQ_objective()
M.left = 0; M.right = 3; M.matrix = 1

# linear constraints
Y = [Simple_Linear_constraints() for n in range(1)]

linearY = [Simple_Linear_Bound() for n in range(2)]

linearY[0].right = 4; linearY[0].matrix = np.array([[0],[1],[0],[0]])
linearY[1].right = 5; linearY[1].matrix = np.array([[0],[-1],[0],[0]])

Y[0].linear = linearY
Y[0].b = 0

Z = [Simple_Linear_constraints() for n in range(2)]

linearZ1 = [Simple_Linear_Bound() for n in range(2)]

linearZ1[0].right = 2; linearZ1[0].matrix = np.array([[-1],[0],[0],[0]])
linearZ1[1].right = 1; linearZ1[1].matrix = np.array([[0],[1/12]])

Z[0].linear = linearZ1
Z[0].b = 0

linearZ2 = [Simple_Linear_Bound() for n in range(2)]

linearZ2[0].right = 2; linearZ2[0].matrix = np.array([[0],[0],[1],[0]])
linearZ2[1].right = 3; linearZ2[1].matrix = np.ones((1,1))*-1

Z[1].linear = linearZ2
Z[1].b = 0

UB = [Simple_Linear_Bound() for n in range(3)]
LB = [Simple_Linear_Bound() for n in range(3)]

UB[0].right = 4;UB[0].matrix = np.array([[2],[np.inf],[0.5],[0]])
LB[0].right = 4; LB[0].matrix =  np.array([[2],[-np.inf],[0.5],[0]])

UB[1].right = 5;UB[1].matrix = np.array([[np.inf],[np.inf],[np.inf],[0]])
LB[1].right = 5; LB[1].matrix = -1*UB[1].matrix

UB[2].right = 1; UB[2].matrix = np.array([[np.inf],[10]])
LB[2].right = 1; LB[2].matrix = -1*UB[2].matrix

# UB[3].right = 2; UB[3].matrix = np.array([[np.inf],[lambda t: aux.g(t)],[np.inf],[np.inf]],dtype = 'O')

s = setup()
s.A = A; s.B = B; s.G = G;
s.Lagrange = L; s.Mayer = M 
s.Y = Y;   
s.Z = Z;
s.UB = UB; s.LB = LB; 
s.t0 = t0; s.tf = tf; s.auxdata = aux

T,U,X,P,F,internal,opts = DTQPy_solve(s,opts)
