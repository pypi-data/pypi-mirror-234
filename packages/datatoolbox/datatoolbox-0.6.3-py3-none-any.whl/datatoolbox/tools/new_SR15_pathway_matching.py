#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 09:26:22 2023

@author: andreasgeiges
"""
from  fuzzywuzzy import fuzz
import numpy as np
mapping = dict()
import datatoolbox as dt




df_scenarios = dt.sets.SCENARIOS.compatible_20_sustainable

pathways = ['|'.join(i) for i in zip(df_scenarios["scenarios"].map(str),df_scenarios["models"])]


candidates = list(dt.findp(source='IPCC_SR15').pathway.unique())
mapping = dict()
for pathway in pathways:
    
    # scores = [fuzz.token_sort_ratio(pathways,x) for x in candidates]
    
    # max_idx = np.argmax(scores)
    # mapping[pathway] = candidates[max_idx]
    found =False
    for cand in candidates:
        
        if cand.replace(' ','_').replace('/','_') == pathway:
            mapping[pathway] = cand
            found = True
            
    if not found:
        
        print(pathway)
            
#100