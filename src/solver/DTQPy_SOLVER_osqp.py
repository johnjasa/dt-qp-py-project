# -*- coding: utf-8 -*-
"""
DTQPy_SOLVER_osqp
Reorganize matrices and solve the problem using osqp

Contributor: Athul Krishna Sundarrajan (AthulKrishnaSundarrajan on Github)
Primary Contributor: Daniel R. Herber (danielrherber on Github)
"""
import osqp 
from scipy import sparse
import numpy as np

def DTQPy_SOLVER_osqp(H,f,A,b,Aeq,beq,lb,ub,internal,opts):
    
    solver = opts.solver
    
    options = {'eps_abs':solver.tolerence,'eps_rel': solver.tolerence,'max_iter':solver.maxiters}
    
    
    Al = sparse.vstack([A,Aeq,sparse.eye(internal.nx)]); Al =  Al.tocsc()
    lbL = np.vstack([b.todense(),beq.todense(),lb[None].T])
    ubL = np.vstack([b.todense(),beq.todense(),ub[None].T])
    q = f.todense()
    
    prob = osqp.OSQP()
    
    #breakpoint()
    # problem setup
    prob.setup(P = H,q = q,A = Al,l = lbL,u = ubL, **options)
    
    # solve the problem
    res = prob.solve()
    
    # extract result
    X = res.x
    
    # extract objective function value
    F = res.info.obj_val
    
    return X,F,internal,opts
    
    