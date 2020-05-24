#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 14:52:42 2020

@author: saraborchers
"""
import pandas as pd
import pandapower as pp
import pandapower.networks as nw
import numpy as np
import matplotlib.pyplot as plt


'''
Take a given network, print relevant results and record key outputs into plottable lists.
'''

def print_results(net):
    #TODO: Record relevant results to for plotting

    print("\nThe power (MW & MVar) provided by the external connection to the grid is: \n")
    print(net.res_ext_grid)
    
    print("\nThe power (MW & MVar) provided by each generator is: \n")
    print(net.res_gen)
    
#    print("\nThe voltage phasors, complex power, and marginal cost at each bus are: \n")
#    print(net.res_bus)   
    
    trafo = net.res_trafo.loading_percent
    trafo_mean_list.append(trafo.mean())
    trafo_max_list.append(trafo.max())
    print("\nThe loading percentages (%) of the transformers are: \n")
    print(trafo)
    
    line = net.res_line.loading_percent
    line_mean_list.append(line.mean())
    line_max_list.append(line.max())
    print("\nThe loading percentages (%) of the lines are: \n")
    print(line)    
    
    cost = net.res_cost
    cost_list.append(cost)
    print("\nThe total cost (EUR) is: \n")
    print(cost)


'''
Set voltage and loading constraints. Any params set to None are left unconstrained.
'''
def set_constraints(trafo_const, line_const, min_v_pu, max_v_pu):
    if trafo_const:
        net.trafo["max_loading_percent"] = trafo_const
    if line_const:
        net.line["max_loading_percent"] = line_const
    if min_v_pu: 
        net.bus["min_vm_pu"] = min_v_pu
    if max_v_pu:
        net.bus["max_vm_pu"] = max_v_pu


'''
Change the loads of default case to reflect installation of chargers, for a single time stamp.
hour_df is for a single hour and has two columns: 'Bus' and 'Load'
'''
def change_loads(net,hour_df):
    load_df = net.load #current df of load values
    for index, row in hour_df.iterrows():
        bus = row['Bus']
        load_df.at[bus,'p_mw'] = row['Load'] #modifies load_df in place


    
'''
Plot the line loading %, transformer loading %, and cost over 24 hours.
'''
def plot_results():
    pass


#Load IEEE 57 bus system (default)
#net = nw.case57(vn_kv_area1=115, vn_kv_area2=500, vn_kv_area3=138, vn_kv_area4=345, vn_kv_area5=230, vn_kv_area6=161) 
net = nw.example_multivoltage() 

gen_df = net.gen
gen_df.insert(8, 'max_p_mw',[100],True)
gen_df.insert(8, 'min_p_mw',[0],True)

#Create cost functions
costeg = pp.create_poly_cost(net, 0, 'ext_grid', cp1_eur_per_mw=10)
costgen1 = pp.create_poly_cost(net, 0, 'gen', cp1_eur_per_mw=10)
costgen2 = pp.create_poly_cost(net, 0, 'sgen', cp1_eur_per_mw=10)
costgen3 = pp.create_poly_cost(net, 1, 'sgen', cp1_eur_per_mw=10)
costgen4 = pp.create_poly_cost(net, 2, 'sgen', cp1_eur_per_mw=10)
costgen5 = pp.create_poly_cost(net, 3, 'sgen', cp1_eur_per_mw=10)
costgen6 = pp.create_poly_cost(net, 4, 'sgen', cp1_eur_per_mw=10)
costgen7 = pp.create_poly_cost(net, 5, 'sgen', cp1_eur_per_mw=10)
costgen8 = pp.create_poly_cost(net, 6, 'sgen', cp1_eur_per_mw=10)
costgen9 = pp.create_poly_cost(net, 7, 'sgen', cp1_eur_per_mw=10)
costgen10 = pp.create_poly_cost(net, 8, 'sgen', cp1_eur_per_mw=10)
costgen11 = pp.create_poly_cost(net, 9, 'sgen', cp1_eur_per_mw=10)
costgen12 = pp.create_poly_cost(net, 10, 'sgen', cp1_eur_per_mw=10)

#Create empty lists for outputs that will be plotted
trafo_mean_list = []
trafo_max_list = []
line_mean_list = []
line_max_list = []
cost_list = []

#Run OPF on unchanged default system
pp.runopp(net)
print("\nOPF Results with Unconstrained Default System \n")
print_results(net)

#Set constraints. Optional. To leave unconstrained, set to None. 
trafo_const = None
line_const = .9
min_v_pu = None
max_v_pu = None
set_constraints(trafo_const, line_const, min_v_pu, max_v_pu)

#Rerun OPF with constraints
pp.runopp(net)
print("\nOPF Results with Default System + Constraints \n")
print_results(net)

#Load the df of buses and associated hourly loads. Rows = buses, Cols = hours.
#TODO: Conner is creating this df
day_df = pd.read_csv('S1_012219')

#Create 0MW loads at all locations where chargers will be added
for index, row in day_df.iterrows():
    pp.create_load(net, row['Bus'], p_mw=0, controllable=False)

hours = list(day_df)
#Iterate through each column (hour)
for h in hours:
    hour_df = day_df[['Bus', h]].copy() #Create a 2 col df of buses and loads for that hour
    change_loads(net, hour_df) #Change the loads on the network accordingly
    pp.runopp(net) #Run OPF for that hour
    print_results(net)

plot_results()

#TODO: We should be adjusting ALL loads to be time series








