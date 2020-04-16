## Add the parent directory to the path name
import sys
import os
p_dir_path = os.path.abspath('../')
sys.path.append(p_dir_path)
##

import utilities.PDEparams as pde
import pandas as pd
import numpy as np
from scipy.integrate import odeint

import matplotlib.pyplot as plt


class sir:
    
    data = []
    parameters = {}
    solution = {}
    initConditions={}
    paramNames = ['$beta$', '$gamma$']
    bounds = [(0.3,2),(1/14,1/5)]
    solutionNames = ['S','I','R']
    name = 'SIR'
    
    def __init__(self,data=None,initConditions=None):
        if data.empty:
            print('You need to pass a dataframe object with t and I as coloumns')
        else:
            self.data = data
        
        self.initConditions = initConditions
    
    # ------------------------------------ Init Conditions ---------------------------
    def init_s(self):
        global S
        return 1 - self.initConditions['I']

    def init_i(self):
        global I
        return self.initConditions['I']

    def init_r(self):
        global R
        return self.initConditions['R']
    
    # ------------------------------------ Init Conditions ---------------------------     
    def run(self):
        self.estimateParameters()
        self.integrateModel()
        
    def estimateParameters(self):
        #Parameter estimation
        myModel=pde.PDEmodel(self.data,
                            self.model,
                            [self.init_s,self.init_i,self.init_r],
                            bounds=self.bounds,
                            param_names=self.paramNames, 
                            nvars=3, 
                            ndims=0, 
                            nreplicates=1, 
                            obsidx=[1], 
                            outfunc=None)
        
        myModel.fit()
        
        self.error = myModel.best_error
        
        paramDict = {}
        for pName in self.paramNames:
            paramDict[pName] = myModel.best_params[pName][0]
        
        self.parameters = paramDict
            
    def integrateModel(self):
        
        argsInput = []
        for pKey in self.parameters:
            argsInput.append(self.parameters[pKey])
        argsInput = tuple(argsInput)
        
        # Solve 
        bestSol=odeint(self.model,
               [self.init_s(),self.init_i(),self.init_r()],
               range(len(self.data)),
               args=argsInput) 
        
        solutionDict = {}
        for i,e in enumerate(self.solutionNames):
            solutionDict[e] = bestSol.T[i]
            
        self.solution = solutionDict
        
   # ------------------------------------ Models ---------------------------     
    # ODE Models
    def model(self,X,t,b,g):
        s,i,r=X

        ds=-b*(s*i)
        di=b*(s*i)-g*i
        dr=g*i
        return[ds,di,dr]
    
    # ------------------------------------ Plotting---------------------------     
    def plot(self,ax1 = None):
        flageOut = ax1
        if ax1==None:
            fig1,ax1=plt.subplots(1,1,figsize=(14,8))
        
        ax1.plot(range(len(self.data)),self.solution['I'],'-o',label='$\hat{y}$')
        ax1.plot(range(len(self.data)),self.data['I'],'-o',label='y')
        ax1.set_title(f"{self.name} Model")
        ax1.set_xlabel('Time (days)')
        ax1.set_ylabel('Proportion')
        ax1.legend()
            
        if flageOut!=None:
            return ax1