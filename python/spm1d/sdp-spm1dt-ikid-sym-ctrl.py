# -*- coding: utf-8 -*-
"""
STEP DOWN AND PIVOT: MORE SYMPTOMATIC VS CTRL - SPM1D T-TEST
@author: Prasanna Sritharan
"""


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import spm1d
import pickle as pk



# Data file
srcpath = r"C:\Users\Owner\Documents\data\FORCe\outputdatabase\csvfolder"
srcfile = "force_sdp_results_subject_descriptives_normalised.csv"

# Output file
outpath = r"C:\Users\Owner\Documents\data\FORCe\outputdatabase\spm1d"
if not os.path.isdir(outpath): os.makedirs(outpath)
outfilename = "sdp-spm1dt-ikid-sym-ctrl"


# %% PREPARE DATA

# Load XLS data into a dataframe
df0 = pd.read_csv(os.path.join(srcpath, srcfile))

# Remove stdev rows
df1 = df0[df0["statistic"] == "mean"]

# Data labels
analyses = ["ik", "id"]
osimvars = {}
osimvars["ik"] = ["hip_flexion", "hip_adduction", "hip_rotation", "knee_angle", "ankle_angle", "lumbar_extension", "lumbar_bending", "lumbar_rotation"]
osimvars["id"] = [k + "_moment" for k in osimvars["ik"]]
subjtype = ["sym", "ctrl"]
subjtypefulllabel = ["symptomatic", "control"]

# Scenario labels
scenario = ["pivot", "nonpivot"]
trialcombo =[["pivot_more", "pivot"], ["pivot_less", "pivot"]]

# Get data into arrays
datamat = {}
eventmat = {}
for sn, n in enumerate(scenario):
    df = df1[df1["data_leg_role"] == n]
    datamat[n] = {}
    eventmat[n] = {}
    for a in analyses:
        datamat[n][a] = {}
        eventmat[n][a] = {}
        for v in ["time"] + osimvars[a]:
            
            datamat[n][a][v] = {}
            eventmat[n][a][v] = {}        
            
            # Group 1
            gp1data = df[(df["subj_type"] == subjtype[0]) & (df["trial_combo"] == trialcombo[sn][0]) & (df["analysis"] == a) & (df["variable"] == v)]
            datamat[n][a][v][subjtype[0]] = gp1data.loc[:, "t1":"t101"].to_numpy()
            eventmat[n][a][v][subjtype[0]] = gp1data.loc[:, "es1_PFO1":"es6_PFS4"].to_numpy()
        
            # Group 2
            gp2data = df[(df["subj_type"] == subjtype[1]) & (df["trial_combo"].str.contains(trialcombo[sn][1])) & (df["analysis"] == a) & (df["variable"] == v)]
            datamat[n][a][v][subjtype[1]] = gp2data.loc[:, "t1":"t101"].to_numpy()
            eventmat[n][a][v][subjtype[1]] = gp2data.loc[:, "es1_PFO1":"es6_PFS4"].to_numpy()



# %% EVENTS

# Event time steps and descriptives
events = {}
for n in scenario:
    events[n] = {}
    events[n]["data"] = {}
    events[n]["desc"] = {}
    descmat = np.zeros((2,6))
    for gn, g in enumerate(subjtype):
        events[n]["data"][g] = eventmat[n]["ik"]["time"][g]
        events[n]["desc"][g] = {}
        events[n]["desc"][g]["mean"] = np.round(np.mean(events[n]["data"][g], axis=0))
        events[n]["desc"][g]["sd"] = np.round(np.std(events[n]["data"][g], axis=0))
        descmat[gn, 0:6] = events[n]["desc"][g]["mean"]
    events[n]["desc"]["total"] = {}
    events[n]["desc"]["total"]["mean"] = np.mean(descmat, axis=0)
    events[n]["desc"]["total"]["sd"] = np.std(descmat, axis=0)



# %% RUN ANALYSES: DESCRIPTIVES, SPM{t}

# Calculate group ensemble descriptives from file
desc = {}
for n in scenario:
    desc[n] = {}
    for a in analyses:        
        desc[n][a] = {}
        for v in osimvars[a]:
            desc[n][a][v] = {}
            for s in subjtype:    
                desc[n][a][v][s] = {}                      
                desc[n][a][v][s]["mean"] = np.mean(datamat[n][a][v][s], axis = 0)
                desc[n][a][v][s]["sd"] = np.std(datamat[n][a][v][s], axis = 0)


# Run SPM{t} and inference across all legs, analyses, variables and group pairs
spmt = {}
spmtinf = {}
for n in scenario:
    spmt[n] = {}
    spmtinf[n] = {}   
    for a in analyses: 
        spmt[n][a] = {}
        spmtinf[n][a] = {}
        for v in osimvars[a]:
            Y0 = datamat[n][a][v][subjtype[0]]
            Y1 = datamat[n][a][v][subjtype[1]]
            spmt[n][a][v] = spm1d.stats.ttest2(Y0, Y1, equal_var=False)
            spmtinf[n][a][v] = spmt[n][a][v].inference(alpha = 0.05, two_tailed=True, interp=True)


# Combine for output
sdp = {}
sdp["desc"] = desc
sdp["events"] = events
sdp["spmt"] = spmt
sdp["spmtinf"] = spmtinf
            
# Pickle it
with open(os.path.join(outpath, outfilename + ".pkl"),"wb") as f: pk.dump(sdp, f)
    

# %% PLOT OUTPUT

# Plot parameters
eventlabels = ["PFO1", "PFS2", "NFO1", "NFS2", "PFO3", "PFS4"]
eventlabelalign = ["left", "right", "left", "right", "left", "right"]
eventlabeladjust = [0.01, -0.01, 0.01, -0.01, 0.01, -0.01]   

# Generate plots
for n in scenario:

    # Scenario parameters
    nsubjs = [np.size(datamat[n]["ik"]["time"][s], axis=0) for s in subjtype]
    eventlist = 100 * np.round(events[n]["desc"]["total"]["mean"]) / 101    

    # Create plot area
    fig = plt.figure(constrained_layout=True, figsize=(50, 15))   
    fig.suptitle("Step-down-and-pivot: %s vs %s (n%d vs n%d) - %s limb" % (subjtype[0].upper(), subjtype[1].upper(), nsubjs[0], nsubjs[1], n.title()), fontsize=20)
    heights = [2, 1, 0.5, 2, 1]
    spec = fig.add_gridspec(nrows = 5, ncols = len(osimvars["ik"]), height_ratios = heights) 
    
    # Plot results
    for s, subj in enumerate(subjtype):
    
        # Create plots
        x = range(101)
        for col in range(len(osimvars["ik"])):        
            
            # Mean + stdev
            for r, row in enumerate([0, 3]):        
                
                an = analyses[r]
                
                # Mean
                m0 = desc[n][an][osimvars[an][col]][subjtype[0]]["mean"]
                m1 = desc[n][an][osimvars[an][col]][subjtype[1]]["mean"]
                
                # Upper
                u0 = m0 + desc[n][an][osimvars[an][col]][subjtype[0]]["sd"]
                u1 = m1 + desc[n][an][osimvars[an][col]][subjtype[1]]["sd"]
                
                # Lower
                l0 = m0 - desc[n][an][osimvars[an][col]][subjtype[0]]["sd"]
                l1 = m1 - desc[n][an][osimvars[an][col]][subjtype[1]]["sd"]       
                
                # Plot
                ax = fig.add_subplot(spec[row, col], title=osimvars[an][col].replace("_", "-"))
                if (row == 0) and (col == 0):
                    ax.set_ylabel("Angle (deg)")
                elif (row == 3) and (col == 0):
                    ax.set_ylabel("Moment (%BW*HT)")   
                ax.fill_between(x, l0, u0, alpha = 0.4)
                ax.fill_between(x, l1, u1, alpha = 0.4)
                ax.plot(x, m0, label = subjtypefulllabel[0], linewidth = 2.0)
                ax.plot(x, m1, label = subjtypefulllabel[1], linewidth = 2.0) 
                ax.set_xlim([x[0], x[-1]])
                for v in range(1, 5): ax.axvline(x = eventlist[v], linewidth = 1.0, linestyle = ":", color = "k")
                if (row == 0 and col == 0): ax.legend(frameon = False, loc = "lower left")
            
                # Event labels
                for at in range(6): ax.text((eventlist[at] / 100) + eventlabeladjust[at], 0.95, eventlabels[at], transform = ax.transAxes, horizontalalignment = eventlabelalign[at], fontsize = 8)
            
            # SPM inference
            for r, row in enumerate([1, 4]):  
                
                an = analyses[r]
                
                # Plot
                ax = fig.add_subplot(spec[row, col], xlabel = "% task")
                if col == 0: ax.set_ylabel("SPM{t}") 
                for v in range(1, 5): ax.axvline(x = eventlist[v], linewidth = 1.0, linestyle = ":", color = "k")
                spmtinf[n][an][osimvars[an][col]].plot(plot_ylabel = False)
                    
                    
    # Save to pdf
    plt.savefig(os.path.join(outpath, outfilename + "-" + n + ".pdf"))