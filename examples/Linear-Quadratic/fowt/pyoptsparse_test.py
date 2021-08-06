#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 09:12:42 2021

@author: athulsun
"""

from pyoptsparse import IPOPT, Optimization

import argparse

import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--opt",help = "optimizer",type = str, default = "IPOPT")
args = parser.parse_args()
optOptions = {}



class WrappedProblem(object):
    def __init__(self,a):
        self.a = a

    def objfunc(self,xdict):
        
        a = self.a
        
        x0 = xdict["x0"][0]
        x1 = xdict["x1"][0]
        x2 = xdict["x2"][0]
        x3 = xdict["x3"][0]
        
        funcs = {}
        funcs["obj"] = x0*x3*(x0+x1+x2) + a*x2
        funcs["con1"] = [x0*x1*x2*x3]
        funcs["con2"] = [x0*x0 + x1*x1 + x2*x2 + x3*x3]
        fail = False
        
        return funcs,fail


    def sens(self,xdict,funcs):
        x0 = xdict["x0"][0]
        x1 = xdict["x1"][0]
        x2 = xdict["x2"][0]
        x3 = xdict["x3"][0]
        
        funcsSens = {}
        funcsSens["obj"] = {
            "x0": np.array([x0 * x3 + x3 * (x0 + x1 + x2)]),
            "x1": np.array([x0 * x3]),
            "x2": np.array([x0 * x3 + 1.0, 0]),
            "x3": np.array([x0 * (x0 + x1 + x2)]),
        }
    
        funcsSens["con1"] = {
            "x0": np.array([[x1 * x2 * x3]]),
            "x1": np.array([[x0 * x2 * x3]]),
            # 'x2': np.array([[x0*x1*x3, 0]]),
            "x3": np.array([[x0 * x1 * x2]]),
        }
        #    ^
        #    |
        # If we don't return any one of the constraint Jacobian blocks,
        # pyoptsparse will assume it to be zero.
    
        funcsSens["con2"] = {
            "x0": np.array([[2.0 * x0]]),
            "x1": np.array([[2.0 * x1]]),
            "x2": np.array([[2.0 * x2, 0]]),
            "x3": np.array([[2.0 * x3]]),
        }
    
        fail = False
        return funcsSens, fail
    
WProb = WrappedProblem(a = 1)
    
optProb = Optimization("HS071 Constraint Problem",WProb.objfunc)
optProb.addObj("obj")

#
x0 = [1.0,5.0,5.0,1.0]
optProb.addVarGroup("x0",1,lower = 1, upper = 5, value = x0[0])
optProb.addVarGroup("x1",1,lower = 1, upper = 5, value = x0[1])
optProb.addVarGroup("x2",2,lower = 1, upper = 5, value = x0[2])
optProb.addVarGroup("x3",1,lower = 1, upper = 5, value = x0[3])

optProb.addConGroup("con1",1,lower = [25],upper = [1e19])
optProb.addConGroup("con2",1,lower = [40],upper = [40])

#Objective
#optProb.addObj("obj")

print(optProb)

opt = IPOPT(args.opt,options = optOptions)

sol = opt(optProb,sens = WProb.sens)

print(sol)