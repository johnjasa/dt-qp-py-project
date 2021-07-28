# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 11:07:01 2021

@author: rajan
"""

from mat4py import loadmat
import numpy as np
from scipy.interpolate import interp1d,PchipInterpolator, splprep, splev
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

LinearModels = loadmat('SS2py.mat')
Chan = LinearModels['Chan']


nl = len(Chan)
nx,nx = np.shape(Chan[0]['A'])
nx,nu = np.shape(Chan[0]['B'])

Aw = np.zeros((nl,nx,nx))
Bw = np.zeros((nl,nx,nu))
xw = np.zeros((nl,nx))
uw = np.zeros((nl,nu))
ws = np.zeros((nl))


for i in range(nl):
    Aw[i,:,:] = np.array(Chan[i]['A'])
    Bw[i,:,:] = np.array(Chan[i]['B'])
    
    xw[i,:] = np.squeeze(np.array(Chan[i]['xop']))
    uw[i,:] = np.squeeze(np.array(Chan[i]['uop']))
    ws[i] = Chan[i]['WindSpeed']
    
   
    
A_op_pp = PchipInterpolator(ws, Aw, axis = 0)
A_op = lambda w: A_op_pp(w)
B_op_pp = PchipInterpolator(ws, Bw, axis = 0)
B_op = lambda w: B_op_pp(w)

Uo_pp = PchipInterpolator(ws,uw)
Uo_fun = lambda w: Uo_pp(w)

Xo_pp = PchipInterpolator(ws, xw, axis = 0)
Xo_fun = lambda w: Xo_pp(w)

DXo_pp = Xo_pp.derivative 
DXo_pp = DXo_pp(nu=1)
DXo_fun = lambda w: DXo_pp(w)

windcase = 'Turb.mat'
# windcase = 'Step.mat'

Scenario =  loadmat(windcase)

Chan = Scenario['chan']
Chan = np.array(Chan)

Channame = Scenario['channame']

idx = Channame.index(["Time"])
tt = np.array(Chan[:,idx])
nls = len(tt)


U = np.zeros((nls,nu))

for i in range(3):
    
    if i == 0:
        idx = Channame.index(["Wind1VelX"])
        U[:,i] = np.array(Chan[:,idx])
        
    elif i == 1:
        idx = Channame.index(["GenTq"])
        U[:,i] = 1000*np.array(Chan[:,idx])
        
    elif i == 2:
        idx = Channame.index(["BldPitch1"])
        U[:,i] = np.array(np.deg2rad(Chan[:,idx]))
            
    
U_pp = PchipInterpolator(tt, U,axis = 0)
U_fun = lambda t: U_pp(t)
    
Wind_speed = U[:,0]

Wavg = np.mean(Wind_speed)

W_pp = PchipInterpolator(tt, Wind_speed,axis = 0)
dW_pp = W_pp.derivative 
dW_pp = dW_pp(nu = 1)

DW_fun = lambda t: dW_pp(t)
W_fun = lambda t: W_pp(t)

DXoDt_fun = lambda t: DXo_fun(W_fun(t))*DW_fun(t)

def odefun(t,x,A_op,B_op,W_fun,U_fun,Uo_fun,DXoDt_fun,Wavg,caseflag):
    
    if caseflag == 1:
        w = Wavg
        
        A = A_op(w)
        B = B_op(w)
        u = U_fun(t)
        Uo = Uo_fun(w)
        
        dydt = np.dot(A,x) + np.dot(B,(u-Uo))
        
    elif caseflag == 2:
        w = W_fun(t)
        
        A = A_op(w)
        B = B_op(w)
        u = U_fun(t)
        Uo = Uo_fun(w)
        dXoDt = DXoDt_fun(t)
        #breakpoint()
        xp = np.dot(A,x) + np.dot(B,(u-Uo))
        
        dydt = np.squeeze(xp) - dXoDt
        
    return dydt
    
tspan = np.linspace(tt[0],tt[-1],2000)

X01 = np.zeros((8,)); X01[0] = np.deg2rad(3); X01[4] = 6/9.5492965964254
X0 = X01 - Xo_fun(W_fun(0))
caseflag = 2

options = {'atol':1e-7}

sol = solve_ivp(odefun,[0,600],X0,method = 'RK45',args = (A_op,B_op,W_fun,U_fun,Uo_fun,DXoDt_fun,Wavg,caseflag),**options)

T = sol.t
Xl = sol.y

Xoff = Xo_fun(W_fun(T))

X = Xoff + Xl.T

plt.plot(T,X[:,0])
