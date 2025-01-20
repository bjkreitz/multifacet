#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 13:55:50 2019

@author: bjarne
"""
#This model runs the equilibrium calculation and computes yield vs. equilibrium yield
#Very useful model
import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import sys

plt.rcParams['figure.figsize']=(7,6)
#plt.rcParams['mathtext.fontset'] = 'cm'
#plt.rcParams['font.family']='serif'
plt.rcParams['axes.titlesize']=16
plt.rcParams['axes.linewidth'] = 2 #set the value globally
plt.rc('xtick', labelsize=14)
plt.rc('ytick', labelsize=14)
plt.rc('axes', labelsize=16)
plt.rc('legend', fontsize=14)
plt.rcParams['lines.markersize'] = 10
plt.rcParams['xtick.direction']='in'
plt.rcParams['ytick.direction']='in'
plt.rcParams['xtick.major.size']=10
plt.rcParams['xtick.major.width']=2
plt.rcParams['ytick.major.size']=10
plt.rcParams['ytick.major.width']=2
plt.rcParams['legend.edgecolor']='k'

t=np.linspace(100,800,10) #temperature of the CSTR

Yieldeq=[]
xCH4eq=np.zeros(len(t))
xCOeq=np.zeros(len(t))
xCO2eq=np.zeros(len(t))
xH2eq=np.zeros(len(t))
xH2Oeq=np.zeros(len(t))
xAreq=np.zeros(len(t))
Ueq=np.zeros(len(t))
Seq_CH4=np.zeros(len(t))
Seq_CO=np.zeros(len(t))
Yeq=np.zeros(len(t))
for j in range(len(t)):
    p=1 #pressure of the CSTR
# input file containing the surface reaction mechanism
    cti_file = 'chem.cti'
    T=t[j]+273.15
    # import the gas model and set the initial conditions
    print(T)
    gaseq = ct.Solution(cti_file, 'gas')
    gaseq.TPX = T, p*ct.one_atm, 'Ar:0.7528, CH4(1):0, H2O(3):0, CO2(2):0.0502, H2(4):0.197, CO(5):0.0'
    q1=ct.Quantity(gaseq, moles=1)
    
    i_ch4eq=q1.species_index('CH4(1)')
    i_co2eq=q1.species_index('CO2(2)')
    i_coeq=q1.species_index('CO(5)')
    i_h2eq=q1.species_index('H2(4)')
    i_h2oeq=q1.species_index('H2O(3)')
    i_areq=q1.species_index('Ar')  
    
    q1.equilibrate('TV',solver='auto',rtol=1.0e-9, maxsteps=10000, loglevel=1)
    
    xCH4eq[j]=q1.X[i_ch4eq]#*q1.moles 
    xCO2eq[j]=q1.X[i_co2eq]#*q1.moles
    xCOeq[j]=q1.X[i_coeq]#*q1.moles
    xH2eq[j]=q1.X[i_h2eq]#*q1.moles
    xH2Oeq[j]=q1.X[i_h2oeq]#*q1.moles
    xAreq[j]=q1.X[i_areq]#*q1.moles
    
    Ueq[j]=1-(0.7528*xCO2eq[j]/xAreq[j]/0.0502)
    Seq_CH4[j]=xCH4eq[j]/(xCH4eq[j]+xCOeq[j])
    Seq_CO[j]=xCOeq[j]/(xCH4eq[j]+xCOeq[j])
    Yeq[j]=Ueq[j]*Seq_CH4[j]
    
###Ergebnis in txt Datei schreiben
myFields = ['t', 'CH4', 'CO2', 'CO', 'H2', 'H2O', 'Ar', 'U', 'S_CH4', 'S_CO', 'Y']
myData = zip(t, xCH4eq,xCO2eq, xCOeq, xH2eq, xH2Oeq,xAreq, Ueq, Seq_CH4, Seq_CO, Yeq)
myFile = open('TPR_Equilibrium.txt', 'w')  
with myFile as output:
      writer = csv.writer(output, lineterminator='\n', delimiter='\t')
      writer.writerow(myFields)
      writer.writerows(myData)  
    
import matplotlib.gridspec as gridspec

gs = gridspec.GridSpec(1, 2)
gs.update(wspace = 0.3)
ax0 = plt.subplot(gs[0])

#ax0.plot(t+273.15,Ueq*100, label='U')
#ax0.plot(t+273.15,Seq_CH4*100, label='S_CH4')
#ax0.plot(t+273.15,Seq_CO*100, label='S_CH4')
#ax0.plot(t+273.15,Yeq*100, label='Y_CH4')
ax0.plot(t,xCH4eq*100, label='CH4')
ax0.plot(t,xCO2eq*100, label='CO2')
ax0.plot(t,xCOeq*100, label='CO')
ax0.plot(t,xH2eq*100, label='H2')
ax0.plot(t,xAreq*100, label='H2')
ax0.plot(t,xH2Oeq*100, label='H2')
ax0.set_xlim([450,750])
ax0.legend()
plt.show()


