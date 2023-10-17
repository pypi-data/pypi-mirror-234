
import fibphoflow as flow

from fibphoflow_processing import *

# The flow_config file needs to be in the working directory, otherwise the import
# path should be specified with sys.path.append('/path/to/script_directory').
# The config file should be modified according to the  tdt setup.
# For further instructions see the README and the flow_config file.
import fibphoflow_config as cfg

default_path = os.getcwd()

file = "tutorial_data.xlsx"

file = "CytokineStudies_Photometry_IL1B.xlsx"
# Import your data from xlsx file as a pandas dataframe
exp_df = flow.xlsx2dataframe(file, sheet_list=["90min Epoch"])

# Check the docstring for various functions to see different settings.
# The example below shows some of the settings for this function.
# Note that
# if no "sheet_list" argument is specified in the function then data from
# all sheets present in the xlsx file will be read in.
print(flow.xls2dataframe.__doc__)


sub_df = exp_df[exp_df["Experiment"].isin([48])]


channel_config = {
        "colors" : ["gcamp", "isos"],  #needs to stay in this order
        "gcamp" : {1 : {"_4701", "_470A" ,"_465A"}, 
                   2 : {"_4702", "_470B", "_465B"}},
        "isos" : {1 : {"_4051", "_405A"}, 
                  2 : {"_4052", "_405B"}}}
       
print(cfg.channel_config)

#recordings = extract_experiment(sub_df, channel_config, hdf5_name="CytokineStudies_PhotometryAnalysis_IL1Ball_draft20", down_hz=1)
recordings = flow.extract_experiment(sub_df, cfg.channel_config, hdf5_name="CytokineStudies_PhotometryAnalysis_IL1Ball", down_hz=1)

import os
print(os.getcwd())

#preinjection_epoch = ["Preinjection", 40, 5, 3]
#injection_epoch = ["Injection", 30, 5, 1]
injection_epoch = ["Injection", 60, 5, 3]
fooddrop_epoch = ["Food Drop", 14, 5, 1]

#epoch_list = [preinjection_epoch, injection_epoch, fooddrop_epoch]
epoch_list = [injection_epoch]
#epoch_list = [injection_epoch, fooddrop_epoch]

epoch_dict, r_epoch_dict = flow.group_epochs_extraction(sub_df, recordings, epoch_list, ema_smooth=False)
#epoch_dict, r_epoch_dict = group_epochs_extraction(sub_df, recordings, epoch_list, ema_smooth=True, ema_strength=1)

inspect_recordings(sub_df, r_epoch_dict) #plots individual traces

groups2compare = sub_df['Group'].tolist() #all groups in sub_df
#groups2compare = ["PBS_then_PBS", "PBS_then_IL1B", "Ketorolac_then_IL1B"]


a = flow.fig2_epochs_plt(sub_df, r_epoch_dict, groups2compare, exp_df_column="Group")


avg_epoch_dict = average_epochs(sub_df, epoch_dict, epoch_list, channel="isos") #gcamp_isocorr, gcamp, or isos

epoch_window_averaged = flow.average_window(avg_epoch_dict, groups2compare, injection_epoch[0], 20, 25)

plot_averagedepochs(avg_epoch_dict, groups2compare)

flow.averagedepochs_to_excel("epochdata.xlsx", avg_epoch_dict, groups2compare)

aucs = flow.auc_finder(avg_epoch_dict, "Injection", start_min = 0, end_min = 30)




import tdt
import numpy as np
from scipy.ndimage.filters import uniform_filter1d, median_filter
import pandas as pd
import os
import matplotlib.pyplot as plt
from math import sqrt
import time
import re
import tables as tb
import xlsxwriter
import os


def time2sec(time):
    #input is a string: "h,m,s" i.e. "0,2,3"
    time = [int(x) for x in time.split(',')]
    seconds = (time[0] * 60**2) + (time[1] * 60) + time[2]
    return seconds

       
def xlsx2dataframe1(xlsx_file, xlsx_path=None, sheet_list=None):
    """Sheets should just be an index"""
          
    if xlsx_path is None:
        working_dir = os.getcwd() 
        for root, dirs, files in os.walk(working_dir, topdown=True): #maybe add path option here for raw recordings    
            if xlsx_file in files:
                xlsx_path = r"{}".format(root + "/" + xlsx_file)

    xlsx_file = pd.ExcelFile(xlsx_path) #xlsx_file gets reassigned here
    sheet_names = xlsx_file.sheet_names
    df_list = []
    
    for i, sheet in enumerate(sheet_names):   
        if sheet_list == None:
            df_list.append(xlsx_file.parse(sheet_name=sheet, header=0))
        else: 
            if i in sheet_list or sheet in sheet_list:
                df_list.append(xlsx_file.parse(sheet_name=sheet, header=0))
                
    exp_df = pd.concat(df_list, ignore_index=True, sort=False)
    exp_df.dropna(how='all') #drop empty rows
    exp_df['Date'] = exp_df['Date'].dt.strftime("%m/%d/%y")
    index_list = []
    
    for i, row in exp_df.iterrows():
        if type(row["File"]) != str:
            print("Empty excel line at row ", i + 1)
            pass
        else: 
            filename = re.sub("-", "_", row["File"])
            identity = str(row["Mouse"]) + "_from_" + filename
            if identity[0] in "0123456789": #Need this for mice with no letter in front
                identity = "Mouse" + identity
            else: 
                identity = str(row["Mouse"]) + "_from_" + filename
            index_list.append(identity)
    exp_df.index = index_list    
    # have line that checks that the mouse is actually in the file as a failsafe
    return exp_df

    

def generate_recording(file_path, mouse_channel, channel_config, down_hz, smoothing_window=1):
    """TDT formatting: https://www.tdt.com/docs/sdk/offline-data-analysis/offline-data-python/00_Intro/"""
    
    data = tdt.read_block(file_path)
    
    data_channels = set(data.streams.keys()) 
     
    processed_traces = []
    for count, i in enumerate(channel_config["colors"]):

        possible_color_channels = channel_config[i][mouse_channel]
        color_channel = list(data_channels.intersection(possible_color_channels))[0]

        trace_raw = data.streams[color_channel].data
        raw_hz = data.streams[color_channel].fs
        
        #trace_smooth = uniform_filter1d(trace_raw, size=smoothing_window*(1000)) #rolling mean filter
        trace_smooth = median_filter(trace_raw, size=smoothing_window*(1000))
        trace_final = trace_smooth[0:(len(trace_smooth)-1):int(raw_hz/down_hz)]
        
        if count == 0:
            time_vec = np.linspace(0, (len(trace_final) - 1)/(down_hz * 60), len(trace_final))
            processed_traces.append(time_vec)
            
        processed_traces.append(trace_final)
    
    #to do: make it channel agnostic. For now time_vec, gcamp470, isos405 order should stay the same
    
    return processed_traces



def extract_experiment1(exp_df, channel_config, hdf5_name, xlsx_path=None, hdf5_path=None, down_hz=1):
    """Recording files refer to the TDT folders that have the recording files within."""
    
    # xlsx_name argument
    # xlsx_file = "\\" + xlsx_name + ".xlsx"
    # exp_df = xlsx2dataframe(xlsx_file, xlsx_path)
    
    if xlsx_path is None:
        xlsx_path = os.getcwd()
    
    if hdf5_path is None:
        hdf5_path = os.getcwd()
    hdf5_path = os.path.join(hdf5_path, hdf5_name)
    hdf5_path = hdf5_path + ".h5" 
    
    hdf5_title = "Photometry Data: " + hdf5_name    
    hdf5_file = tb.open_file(hdf5_path, 'a', title = hdf5_title)  
    
    
    missing_hdf5recordings_bool = False
    missing_hdf5recordings = {}

    for identity, row in exp_df.iterrows():
        recording_file = row["File"]   
        if ("/" + identity) not in hdf5_file:
            missing_hdf5recordings[recording_file] = missing_hdf5recordings.get(recording_file, [])
            missing_hdf5recordings[recording_file].append(identity)
    print("")                   
    if len(missing_hdf5recordings.keys()) > 0: #if greater than 0 it means there are missing recordings
        raw_recordings_paths = {}
        for root, dirs, files in os.walk(xlsx_path, topdown=True): #maybe add path option here for raw recordings
            if "StoresListing.txt" in files:
                print(root)
                recording_file = root.split("\\")[-1]
                if recording_file in missing_hdf5recordings.keys(): #tells you if recordings not in hdf5 file but is in a path that can be uploaded
                    path = root
                    raw_recordings_paths[recording_file] = path
                    
        missing_raw_recordings_bool = False # *** Change this to set intersection
        for recording_file, identities in missing_hdf5recordings.items():
            if recording_file not in raw_recordings_paths.keys(): 
                missing_raw_recordings_bool = True  
                
        if missing_raw_recordings_bool == True:  # *** Change this to set intersection                        
            print(hdf5_name + " is missing recordings which it needs to be up to date based on excel data sheet.\n")
            print("The recordings that are not in working directory or subfolders:") 
            for recording_file, identities in missing_hdf5recordings.items():
                if recording_file not in raw_recordings_paths.keys():
                    print(recording_file) 
            print("")            
            question_continue = "Do you want to continue? Enter y or n: "
            answer_continue = input(question_continue)
            if answer_continue == "y":
                pass
            elif answer_continue == "n":
                hdf5_file.close()
                return None
            else:
                print("Input should be y or n")
                hdf5_file.close()
                return None
        
        if len(missing_hdf5recordings.keys()) > 0:                   
            print("Based on xlsx data sheet " + hdf5_name + " is missing these recordings which are ready to be added: ") 
            recordings_2b_added = set()
            for recording_file, identities in missing_hdf5recordings.items():
                if recording_file in raw_recordings_paths.keys(): 
                    recordings_2b_added.update(identities) 
                    print(" and ".join(identities))  
            
            question_hdf5_update = "Update " + hdf5_name + " to include recordings? Enter y or n: "
            answer_hdf5_update = input(question_hdf5_update)
            print("")

        if answer_hdf5_update == "y":
            for identity in recordings_2b_added:
                recording_name = str(exp_df.loc[identity]["File"]) #this appeared as a pandas.core.series.Series in a certain instance why??
                recording_group_name = exp_df.loc[identity]["Group"]
                recording_path = raw_recordings_paths[recording_name]       
                mouse_channel = exp_df.loc[identity]["Channel"]
                print("Adding " + identity + " downsampled to " + str(down_hz) + "hz")
                print("from group " + recording_group_name)
                recording_data = generate_recording(recording_path, mouse_channel, channel_config, down_hz)
                print("")
                
                recording_group = hdf5_file.create_group("/", str(identity), "")
                recording_group._v_attrs.identity = identity
                recording_group._v_attrs.group = recording_group_name
                hdf5_file.create_array(recording_group, "timevec", recording_data[0], ("Time vector " + str(down_hz) + "hz"))
                hdf5_file.create_array(recording_group, "gcamp470", recording_data[1], ("Gcamp470 " + str(down_hz) + "hz"))
                hdf5_file.create_array(recording_group, "isos405", recording_data[2], ("Isos405 " + str(down_hz) + "hz"))
                       
        elif answer_hdf5_update == "n":
            pass
        else:
            print("Input should be y or n")
            
    else:
        print("All recordings present in " + hdf5_name)
    
    recordings_dict = {}
    
    for rec_identity in hdf5_file.walk_groups():
        if "identity" in rec_identity._v_attrs:
            recordings_dict[rec_identity._v_attrs.identity] = (rec_identity.timevec.read(), 
                                                               rec_identity.gcamp470.read(), 
                                                               rec_identity.isos405.read())
            
    hdf5_file.close()
    
    return recordings_dict




recordings = extract_experiment1(sub_df, channel_config, hdf5_name="CytokineStudies_PhotometryAnalysis_IL1Ball", down_hz=1)















#Heatmap Section

my_cmap = sns.cubehelix_palette(as_cmap=True)
epoch_dim = dict({"Injection":(20, -40)})
heatmap_dim = (20, 4) #width, height

def plot_averagedepochs_with_heat(epoch_dim, avg_epoch_dict, groups2compare, heatmap_dim):
    """Group legend follows order in groups2compare"""  
    for epoch_name, groups in avg_epoch_dict.items():
        if epoch_name in epochs.keys():
            group_epoch_dict = {}
            for group, mice in groups.items():
                if group in groups2compare:
                    for mouse, trace_data in mice.items():
                        group_epoch_dict[group] = group_epoch_dict.get(group, [])
                        group_epoch_dict[group].append((mouse, trace_data)) 
    
            all_groups_plt = plt.figure(figsize=(15,12))
            all_groups_plt.suptitle(epoch_name, fontsize="30", fontweight="bold")
            group_traces_plt = all_groups_plt.add_subplot(211)
            group_traces_plt.set_ylabel(r'$\Delta$F/F %', fontsize="x-large")
            group_traces_plt.set_xlabel("Minutes", fontsize="x-large")
    
            for group_name, traces_info in group_epoch_dict.items():
                
                fig2 = plt.figure(figsize=(15,12))
                individual_traces_plt = fig2.add_subplot(211)
                group_trace_plt = fig2.add_subplot(212)
                group_trace_plt.set_ylabel(r'$\Delta$F/F %', fontsize="x-large")
                group_trace_plt.set_xlabel("Minutes", fontsize="x-large")
                
                mice_list = []
                traces_data = []
                for mouse, trace_data in traces_info:
                    mice_list.append(mouse)
                    traces_data.append(trace_data)
                    time_axis, trace = trace_data
                    individual_traces_plt.plot(time_axis, trace, linewidth=0.8, label=mouse)
                
                traces_fluorescence = [trace for time_axis, trace in traces_data]
                             
                time_axis = traces_data[0][0]
                fig_width = heatmap_dim[0]
                fig_height = heatmap_dim[1] #len(traces_fluorescence)
                fig_heattraces = plt.figure(figsize=(fig_width, (fig_height))) #fig_heattraces = plt.figure(figsize=(15,3))
                spec_heattraces = gridspec.GridSpec(ncols=fig_width, nrows=len(traces_fluorescence) + 2,
                                                    wspace=0, hspace=0, figure=fig_heattraces)
                
                row = 0
                subplot_dict = {}
                
                for trace in traces_fluorescence:
                    trace = np.expand_dims(trace, axis=0)
                    subplot_dict[row] = fig_heattraces.add_subplot(spec_heattraces[row, 0:])
                    if row != len(traces_fluorescence) - 1: #last row you want ticks
                        subplot_dict[row].tick_params(
                            axis='both',          # changes apply to the x-axis
                            which='both',      # both major and minor ticks are affected
                            bottom=False,      # ticks along the bottom edge are off
                            top=False,         # ticks along the top edge are off
                            left=True,
                            labelleft=True,
                            labelbottom=False  # labels along the bottom edge are off)
                        )
                        subplot_dict[row].ylabel("mouse")
                        #subplot_dict[row].set_ylabel('mouse')
                        #subplot_dict[row].set_yticks()
                        #subplot_dict[row].set_yticks([0.5], labels=["very long label"])

                        
                    elif row == len(traces_fluorescence) - 1: 
                        subplot_dict[row].tick_params(
                            axis='x',          # changes apply to the x-axis
                            which='both',      # both major and minor ticks are affected
                            bottom=True,       # ticks along the bottom edge are off
                            top=False,         # ticks along the top edge are off
                            labelbottom=True,  # labels along the bottom edge are off
                            labelsize=30
                        )
                        
                    vmax = epochs[epoch_name][0]
                    vmin = epochs[epoch_name][1]
                    norm_exp = mpl.colors.Normalize(vmin=vmin, vmax=vmax)     

                    aspect = "auto"
                    
                    subplot_dict[row].imshow(trace, norm=norm_exp, cmap = my_cmap, interpolation='bicubic', aspect=aspect,
                                       extent =[time_axis[0], time_axis[-1], (-10 * 1/len(traces_fluorescence)), (10 * 1/len(traces_fluorescence))])

                    subplot_dict[row].get_yaxis().set_visible(False)
                    row = row + 1
                

                cbarax = fig_heattraces.add_subplot(spec_heattraces[-1, int(fig_width/4) :int(fig_width*3/4)])                 
                cbar = fig_heattraces.colorbar(mpl.cm.ScalarMappable(norm=norm_exp, cmap=my_cmap), cax=cbarax, orientation="horizontal") #use_gridspec=True
                cbarax.tick_params(labelsize=20)

                fig_heattraces.tight_layout(pad=0)
              
                individual_traces_plt.legend(loc="lower left", fontsize="medium", shadow=True)
                individual_traces_plt.axes.get_xaxis().set_visible(False)
                individual_traces_plt.set_ybound((-40, 20)) 
                            
                time_axis, mean_trace, stderr_trace = collate_traces(traces_data)  
                group_trace_plt.plot(time_axis, mean_trace, linewidth=1, label="Mean Trace + Std.Error", color="darkcyan")
                group_trace_plt.fill_between(time_axis, mean_trace+stderr_trace, mean_trace-stderr_trace, alpha=0.4, color="salmon")  
                group_trace_plt.legend(loc="upper right", fontsize="small", shadow=True)
                group_trace_plt.set_ybound((-40, 20)) 
                
                group_traces_plt.plot(time_axis, mean_trace, linewidth=1, label=group_name)
                group_traces_plt.fill_between(time_axis, mean_trace+stderr_trace, mean_trace-stderr_trace, alpha=0.35)
                group_traces_plt.set_ybound((-40, 30)) 
                       
                fig2.suptitle((group_name + " (" + epoch_name + ")"), fontsize="30", fontweight="bold")
            
            group_traces_plt.legend(loc="lower left", fontsize="large", shadow=True)
            
            all_groups_plt.tight_layout()


a = plot_averagedepochs_with_heat(epochs, avg_epoch_dict, groups2compare, heatmap_dim)
