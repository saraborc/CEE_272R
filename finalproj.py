#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 16:37:59 2020

@author: saraborchers
"""

import pandapower as pp
import pandapower.networks as nw

print("YAY!!")
print("Hi Sara!!") # @cmgeery

# CREATE NETWORK: create network, establish ideal voltages by load type
net = nw.case57()

# ADJUST NETWORK LOADS: bump voltages in various areas according to scenarios
# SCENARIO 1: increased home charging

# SCENARIO 2: increased quick charging stations

# SCENARIO 3: mix of quick charging and home charging



# CREATE DEMAND PROFILES: time series calculations/load changes with time

# EVALUATE EV USER CHARGES

