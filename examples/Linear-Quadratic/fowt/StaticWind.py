# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 22:20:35 2021

@author: rajan
"""
from mat4py import loadmat
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

from src.classes.DTQPy_CLASS_SETUP import *
from src.classes.DTQPy_CLASS_OPTS import *
from src.DTQPy_solve import DTQPy_solve


Wdata = loadmat('072720_183300.mat')

X = Wdata['Chan']

W = X['RtVAvgxh']
tt = X['tt']

W = np.squeeze(np.array(W))
tt = np.squeeze(np.array(tt))

Wfun = interp1d(tt,W)

A = np.array([[0,0,1.0000,0,0,0,0,0],
     [0,0,0,1.0000,0,0,0,0],
   [-0.1441 ,   0.0219  ,  0.0093   , 0.0006  , -0.0006  , -0.0238 ,  -0.0072   ,      0],
   [29.1636  , -6.6630 , -35.5230 ,  -0.4159  , -0.6101  ,  3.3190  ,  1.0100  ,       0],
   [-0.0349 ,  -0.0007 ,  -2.3449 ,  -0.0176,   -0.1450 ,   0.0001 ,   0.0000,         0],
         [0  ,       0  ,  1.0000  ,       0    ,     0  , -0.8509 ,  -0.7347 ,  -0.2972],
         [0    ,     0  ,       0  ,       0     ,    0 ,   1.0000,         0 ,        0],
         [0   ,      0  ,       0  ,       0     ,    0 ,        0  ,  1.0000 ,        0]])

B = np.array([[0,         0,         0],
        [ 0     ,    0 ,        0],
   [-0.0000  ,  0.0000  , -0.0000],
    [0.1814  , -0.0000  , -9.7377],
    [0.0152  , -0.0000  , -0.6307],
         [0     ,    0  ,       0],
         [0     ,    0  ,       0],
         [0     ,    0  ,       0]])

Wavg = np.mean(W)

X0 = np.array([0.0524,0,         0   ,      0,    0.6283,         0 ,        0 ,        0])
X0 = X0[None].T

X0_avg = np.array([0.0476, 0.1848,0.0000 ,0.0000,0.7913 ,  -0.0000,-0.0000,0.0000])
X0_avg = X0_avg[None].T

U0_avg = np.array([Wavg,1.962e+07,0.2145])
#U0_avg = U0_avg[None].T

L0mat = np.zeros((3,8))
L0mat[1,4] = -1

L1mat = np.diag([0,1e-8,1e+8])

UB0mat = np.array([[lambda t: Wfun(t)-Wavg],[1.962e+07-1.962e+07],[0.3948-0.2145]])
LB0mat = np.array([[lambda t: Wfun(t)-Wavg],[1421000-1.962e+07],[5.324e-06-0.2145]])

UB2mat = np.inf*np.ones((8,1)); UB2mat[0,0] = np.deg2rad(3); UB2mat[4,0] = 0.7914;
LB2mat = -np.inf*np.ones((8,1))

opts = options()

opts.dt.nt = 1000;
opts.solver.tolerence = 1e-5
opts.solver.maxiters = 1000000

L = [LQ_objective() for n in range(2)]
idx = 0
L[idx].left = 1; L[idx].right = 2; L[idx].matrix = L0mat
idx+=1
L[idx].left = 1; L[idx].right = 1; L[idx].matrix = L1mat

UB = [Simple_Bounds() for n in range(3)]
LB = [Simple_Bounds() for n in range(3)]

UB[0].right = 1; UB[0].matrix = UB0mat
LB[0].right = 1; LB[0].matrix = LB0mat

UB[1].right = 4; UB[1].matrix = np.zeros((8,1))
LB[1].right = 4; LB[1].matrix = np.zeros((8,1))

UB[2].right = 2; UB[2].matrix = UB2mat-X0_avg
LB[2].right = 2; LB[2].matrix = LB2mat-X0_avg

s = setup()
s.A = A; s.B = B;
s.Lagrange = L;
s.UB = UB;
s.LB = LB;
s.t0 = 0;
s.tf = 600

T,Ul,Xl,P,F,internal,opts = DTQPy_solve(s,opts)

U = Ul + U0_avg
X = Xl + np.squeeze(X0_avg.T)



fig, ((ax1,ax2,ax3)) = plt.subplots(3,1,)

ax1.plot(T,U[:,0])
ax1.set_title('Wind Speed [m/s]')
ax1.set_xlim([0,600])

ax2.plot(T,U[:,1]/1e+07)
ax2.set_ylim([1.8,2])
ax2.set_title('Gen Torque [MWm]')
ax2.set_xlim([0,600])


ax3.plot(T,U[:,2])
ax3.set_ylim([0.2, 0.3])
ax3.set_title('Bld Pitch [rad/s]')
ax3.set_xlim([0,600])

fig.subplots_adjust(hspace = 0.65)

fig2, ((ax1,ax2)) = plt.subplots(2,1)

ax1.plot(T,np.rad2deg(X[:,0]))
ax1.set_xlim([0,600])
ax1.set_title('Ptfm Pitch [deg]')

ax2.plot(T,X[:,4])
ax2.set_xlim([0,600])
ax2.set_title('Gen Speed [rad/s]')

fig2.subplots_adjust(hspace = 0.65)

DTQPy_plotCommon