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


class sigrm:
    
    data = []
    parameters = {}
    solution = {}
    initConditions={}
    paramNames = ['$beta_i$', '$beta_g$','$phi$','$gamma$','$mu$']
    bounds = [(0.3,2),(0.3,2),(0.1,0.9),(1/14,1/5),(1/100,1/4)]
    solutionNames = ['S','I','Ig','R']
    name = 'SIGRM'
    
    def __init__(self,data=None,initConditions=None):
        if data.empty:
            print('You need to pass a dataframe object with t and I as coloumns')
        else:
            self.data = data
        
        self.initConditions = initConditions
    
    # ------------------------------------ Init Conditions ---------------------------
    def init_s(self):        
        return 1 - self.initConditions['I']

    def init_i(self):        
        return self.initConditions['I']

    def init_r(self):        
        return self.initConditions['R']
    
    def init_id(self):
        return 0
    
    # ------------------------------------ Init Conditions ---------------------------     
    def run(self):
        self.estimateParameters()
        self.integrateModel()
        
    def estimateParameters(self):
        #Parameter estimation
        myModel=pde.PDEmodel(self.data,
                            self.model,
                            [self.init_s,self.init_i,self.init_id,self.init_r],
                            bounds=self.bounds,
                            param_names=self.paramNames, 
                            nvars=4, 
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
               [self.init_s(),self.init_i(),self.init_id(),self.init_r()],
               range(len(self.data)),
               args=argsInput) 
        
        solutionDict = {}
        for i,e in enumerate(self.solutionNames):
            solutionDict[e] = bestSol.T[i]
            
        self.solution = solutionDict
        
   # ------------------------------------ Models ---------------------------     
    # ODE Models
    def model(self,X,t,bi,bg,p,g,m):
        S,I,IG,R=X

        dS=-(bi*I+bg*IG)*S
        dI=(1-p)*(bi*I+bg*IG)*S-g*I
        dIG=p*(bi*I+bg*IG)*S-g*IG-m*IG
        dR=g*I+g*IG
        return[dS,dI,dIG,dR]

    # ------------------------------------ Plotting---------------------------     
    def plot(self,ax1 = None):
        flageOut = ax1
        if ax1==None:
            fig1,ax1=plt.subplots(1,1,figsize=(14,8))
        
        ax1.plot(range(len(self.data)),self.solution['I'],'-o',label='$\hat{y}$')
        ax1.plot(range(len(self.data)),self.solution['Ig']+self.solution['I'],'-o',label='$\hat{yg}$')
        ax1.plot(range(len(self.data)),self.data['I'],'-o',label='y')
        ax1.set_title(f"{self.name} Model")
        ax1.set_xlabel('Time (days)')
        ax1.set_ylabel('Proportion')
        ax1.legend()
            
        if flageOut!=None:
            return ax1