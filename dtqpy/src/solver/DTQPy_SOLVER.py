# -*- coding: utf-8 -*-
"""
DTQPy_SOLVER
Obtain the solution to the DO problem using the selected solver

Contributor: Athul Krishna Sundarrajan (AthulKrishnaSundarrajan on Github)
Primary Contributor: Daniel R. Herber (danielrherber on Github)
"""
from dtqpy.src.solver.DTQPy_SOLVER_osqp import DTQPy_SOLVER_osqp
from dtqpy.src.solver.DTQPy_SOLVER_pyoptsparse import DTQPy_SOLVER_pyoptsparse

def DTQPy_SOLVER(H,f,A,b,Aeq,beq,lb,ub,internal,opts):
    
    displevel = opts.general.displevel

    # osqp
    if opts.solver.function == 'osqp':
        X,F,intrnal,opts = DTQPy_SOLVER_osqp(H,f,A,b,Aeq,beq,lb,ub,internal,opts)
        
    elif opts.solver.function == 'pyoptsparse':
        X,F,internal,opts = DTQPy_SOLVER_pyoptsparse(H,f,A,b,Aeq,beq,lb,ub,internal,opts)
    
        
    # TO DO: add other solvers
        
        
        
        
    return X,F,internal,opts
    
    
    




