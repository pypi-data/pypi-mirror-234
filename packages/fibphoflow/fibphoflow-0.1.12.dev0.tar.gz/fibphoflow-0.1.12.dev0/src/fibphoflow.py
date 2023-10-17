# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 13:33:46 2020

@author: nwh5j
"""

#To do: save "snapshots" of the subset of hdf5 files used when making a jupyter report
#want to be able to run through photometry data and save the jupyter report
#look at https://github.com/LernerLab/GuPPy/blob/main/GuPPy/savingInputParameters.ipynb


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


def time2sec(time):
    #input is a string: "h,m,s" i.e. "0,2,3"
    time = [int(x) for x in time.split(',')]
    seconds = (time[0] * 60**2) + (time[1] * 60) + time[2]
    return seconds

       
def xlsx2dataframe(xlsx_file, path=None, sheet_list=False):
    """Sheets should just be an index. path=os.getcwd() is probably wha tyou want to default to"""
    
    if path is None:
        path = os.getcwd()
        
    for root, dirs, files in os.walk(path, topdown=True): #maybe add path option here for raw recordings    
        if xlsx_file in files:
            path_xlsx = r"{}".format(root + "/" + xlsx_file)

    xlsx_file = pd.ExcelFile(path_xlsx) #xlsx_file gets reassigned here
    sheet_names = xlsx_file.sheet_names
    df_list = []
    
    for i, sheet in enumerate(sheet_names):   
        if sheet_list == False:
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



def extract_experiment(exp_df, channel_config, hdf5_name, xlsx_path=None, hdf5_path=None, down_hz=1):
    """Recording files refer to the TDT folders that have the recording files within."""
    
    # xlsx_name argument
    # xlsx_file = "\\" + xlsx_name + ".xlsx"
    # exp_df = xlsx2dataframe(xlsx_file, xlsx_path)
    if xlsx_path is None:
        xlsx_path = os.getcwd()
    if hdf5_path is None:
        hdf5_path = os.getcwd()
    
    hdf5_name = hdf5_name + ".h5" 
    hdf5_title = "Photometry Data: " + hdf5_name
    hdf5_file = tb.open_file(hdf5_name, 'a', title = hdf5_title)  
      
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



def extract_intervention(full_recording, start_time, experiment_len, deltapercent, 
                         buff_len, buff_offset, ema_smooth, ema_strength, start_buff=True, sampling_hz=1):
    
    gcamp470 = full_recording[1]
    isos405 = full_recording[2]
    full_traces = [gcamp470, isos405] 
    start_time = time2sec(start_time) * sampling_hz #convert time format to sec to data point in time
    experiment_len = int(experiment_len * 60 * sampling_hz) #convert min to sec to data point scaled
    buff_len = int(buff_len * 60 * sampling_hz)
    buff_offset = int(buff_offset * 60 * sampling_hz)
     
    extracted_traces = []
    if start_buff == True: #the start buffer window prior to intervention is for normalization/visualization purposes
        for trace in full_traces:     
            extracted_trace = np.array(trace[(start_time - buff_len - buff_offset):(start_time + experiment_len + 1)])
           
            if ema_smooth == True:
                extracted_trace = pd.DataFrame(extracted_trace)
                extracted_trace = extracted_trace.ewm(span=(60*sampling_hz*ema_strength)).mean()
                extracted_trace = extracted_trace.values.tolist()
                extracted_trace = [element for sublist in extracted_trace for element in sublist]
                extracted_trace = np.array(extracted_trace)
            #formatted_time_vec = np.linspace(-(buff_len + buff_offset)/60, (len((extracted_trace) - (buff_len + buff_offset)))/60, num=len(extracted_trace))
            formatted_time_vec = np.linspace(-(buff_len + buff_offset)/(60 * sampling_hz), experiment_len/(60 * sampling_hz), num=len(extracted_trace))
            mean2normalize2 = np.mean(trace[(start_time - buff_len - buff_offset):(start_time - buff_offset)])
            trace_norm = (extracted_trace / mean2normalize2) - 1
            if deltapercent == True: #****
                trace_norm = trace_norm * 100 
            trace_data = (formatted_time_vec, trace_norm, extracted_trace)
            extracted_traces.append(trace_data)
                    
    else: 
        for trace in full_traces:
            extracted_trace = np.array(trace[start_time:(start_time + experiment_len)])
            if ema_smooth == True:
                extracted_trace = pd.DataFrame(extracted_trace)
                extracted_trace = extracted_trace.ewm(span=(60*sampling_hz*ema_strength)).mean()
                extracted_trace = extracted_trace.values.tolist()
                extracted_trace = [element for sublist in extracted_trace for element in sublist]
                extracted_trace = np.array(extracted_trace)
            formatted_time_vec = np.linspace(0, len(extracted_trace)/(60 * sampling_hz), num=len(extracted_trace))
            mean2normalize2 = np.mean(extracted_trace)
            trace_norm = (extracted_trace / mean2normalize2) - 1
            if deltapercent == True: #****
                trace_norm = trace_norm * 100 
            trace_data = (formatted_time_vec, trace_norm, extracted_trace) #This is the time vector, deltaF over F, trace
            extracted_traces.append(trace_data)
    
    gcamp470, isos405 = extracted_traces
    gcamp470_isocorr_norm = gcamp470[1] - isos405[1]
    gcamp460_isocorr_timevec = gcamp470[0]
    gcamp470_isocorr = (gcamp460_isocorr_timevec, gcamp470_isocorr_norm)
    
    return gcamp470_isocorr, gcamp470, isos405
       


def collate_traces(traces_list): 
    traces = []
    for trace in traces_list:
        traces.append(trace[1])
    time_vec = traces_list[0][0] #take tme vec from first trace
    mean_of_traces = np.mean(traces, axis=0)
    stderr_of_traces = np.std(traces, axis=0)/sqrt(len(traces))
    return time_vec, mean_of_traces, stderr_of_traces



def group_epochs_extraction(exp_df, recordings_dict, epoch_list, sampling_hz=1, ema_smooth=True, ema_strength=1, deltapercent=True):
    """epoch1 = ["Epoch Name from group_df",  epoch_length, normbufferlen_min, normbufferoffset_min] 
        epoch_list = [epoch1, epoch2, epoch3, etc]"""
    epoch_dict = {}
    reverse_epoch_dict = {}
    
    for identity, recording in recordings_dict.items():
        if identity not in exp_df.index:
            pass
        else:
            # create full length trace
            first_epoch_name, epoch_length, epoch_bufflen, epoch_buffoffset = epoch_list[0] #takes info from first epoch so should be chronological
            full_start = exp_df.loc[identity, first_epoch_name] 
            full_length =(len(recording[0]) - time2sec(full_start))/(60 * sampling_hz) #NEED TO check to make sure time vector is accurately aligned with data sampling
            full_trace = extract_intervention(recording, full_start, full_length, deltapercent, epoch_bufflen, epoch_buffoffset, ema_smooth, ema_strength)

            epoch_dict[identity] = epoch_dict.get(identity, {})
            epoch_dict[identity]["Full Trace"] = epoch_dict[identity].get("Full Trace", {})
            epoch_dict[identity]["Full Trace"] = (full_trace, full_start)
        
            reverse_epoch_dict["Full Trace"] = reverse_epoch_dict.get("Full Trace", {})
            reverse_epoch_dict["Full Trace"][identity] = reverse_epoch_dict["Full Trace"].get(identity, {})
            reverse_epoch_dict["Full Trace"][identity] = (full_trace, full_start)

            for epoch_data in epoch_list:
                epoch_name, epoch_length, epoch_bufflen, epoch_buffoffset = epoch_data
                epoch_start = exp_df.loc[identity, epoch_name]
                epoch_trace = extract_intervention(recording, epoch_start, epoch_length, deltapercent, epoch_bufflen, epoch_buffoffset, ema_smooth, ema_strength)
                full_epoch_length = (epoch_length + epoch_bufflen + epoch_buffoffset) * 60 * sampling_hz
                if full_epoch_length > len(epoch_trace[0][0]):
                    print(identity + " is shorter than " + epoch_name + " length! It is " + str(len(epoch_trace[0][0])) + " but needs to be " + str(full_epoch_length))
                epoch_dict[identity][epoch_name] = epoch_dict[identity].get(epoch_name, {})
                epoch_dict[identity][epoch_name] = (epoch_trace, epoch_start)
                
                reverse_epoch_dict[epoch_name] = reverse_epoch_dict.get(epoch_name, {})
                reverse_epoch_dict[epoch_name][identity] = reverse_epoch_dict[epoch_name].get(identity, {})
                reverse_epoch_dict[epoch_name][identity] = (epoch_trace, epoch_start)
                #sorted(reverse_epoch_dict.items(), key=exp_df.loc[reverse_epoch_dict.keys(), "Mouse"])
    return epoch_dict, reverse_epoch_dict



def inspect_recordings(exp_df, r_epoch_dict, show=True):
    """new one"""
    
    full_traces = r_epoch_dict["Full Trace"]
    
    for identity, full_trace in full_traces.items():
        
        fig1 = plt.figure(figsize=(15,12))
        
        rawtraces_plt = fig1.add_subplot(211)
        rawtraces_plt.set_ylabel(r'Fluorescence Units', fontsize=25, labelpad=15)
        rawtraces_plt.plot(full_trace[0][1][0], full_trace[0][1][2], label="GCaMP", linewidth=2, color="green")
        rawtraces_plt.plot(full_trace[0][2][0], full_trace[0][2][2], label="UV", linewidth=2, color="magenta")
        rawtraces_plt.legend(loc="upper left", fontsize="large", shadow=True)
        rawtraces_plt.axes.get_xaxis().set_visible(False)
    
        #axvspan    
        deltaF_plt = fig1.add_subplot(212)
        deltaF_plt.set_ylabel(r'% $\Delta$F/F', fontsize=25, labelpad=15)
        deltaF_plt.set_xlabel("Minutes", fontsize=25, labelpad=15)
        deltaF_plt.plot(full_trace[0][1][0], full_trace[0][1][1], label="Gcamp_original", linewidth=2, color="seagreen") #shows isosbestic trace
        deltaF_plt.plot(full_trace[0][1][0], full_trace[0][0][1], label="Gcamp_corrected", linewidth=2, color="red")
        deltaF_plt.legend(loc="upper left", fontsize="large", shadow=True)
        deltaF_plt.set_ybound((-50, 50)) 
        deltaF_plt.set_axisbelow(True)
        
        full_start = time2sec(r_epoch_dict["Full Trace"][identity][1])
        for epoch_name, epoch_data in r_epoch_dict.items(): 
            if  epoch_name != "Full Trace":
                epoch_start = time2sec(epoch_data[identity][1])
                deltaF_plt.axvline(x=(epoch_start-full_start)/60, color = "maroon", linestyle="--", zorder=1)    
        deltaF_plt.axhline(y=0, color = "k", linestyle="-", linewidth=1, zorder=1)
        # deltaF_plt.axhline(y=-0.25, color = "k", linestyle="-", linewidth=1)
    
        #deltaF_plt.yaxis.grid(which="major", color='k', linestyle='--', linewidth=0.5)
        #deltaF_plt.axhline(y=-0.2, linestyle="--")
        group = str(exp_df.loc[identity, "Group"])        
        mouse = str(exp_df.loc[identity, "Mouse"])
        date = exp_df.loc[identity, "Date"]
        rawtraces_plt.tick_params(axis="x", labelsize=15)     
        rawtraces_plt.tick_params(axis="y", labelsize=15)   
        deltaF_plt.tick_params(axis="x", labelsize=15)
        deltaF_plt.tick_params(axis="y", labelsize=15) 
        fig_title = group + " <" + str(mouse) + "> (" + str(date) + ")"
        fig1.suptitle(fig_title, fontsize=25, fontweight="bold")     
        fig1.tight_layout()
        if show == True:
            plt.show()



def average_epochs(sub_df, epoch_dict, epoch_list, channel = "gcamp_isocorr"):
    """Takes epochs and for each situation where a mouse has two recordings for one "group""
    experimental condition, it will average them together. For example, if there are a number
    of PBS traces. Returns a new epoch dict along with a data frame to be used for the graphing"""
    group_mouse_means_df = pd.DataFrame()
    group_mouse_means_df.insert(0, "Group",'')
    group_mouse_means_df.insert(1, "Mouse",'')
    list1 = list(sub_df.index)
    list2 = list(epoch_dict.keys())
    channel_dict = {"gcamp_isocorr":0, "gcamp":1, "isos":2}   #consider renaming channel, since two different meanings appear in codebase
    epoch_dict_averaged = {} #averages same mice within each group
    for epoch in epoch_list:
        epoch_dict_averaged[epoch[0]] = epoch_dict_averaged.get(epoch[0], {}) 
    for identity1 in list1:
        if identity1 in list2:
            list2collate = []
            mouse = sub_df.loc[identity1]["Mouse"]
            group_mouse_means_df["Mouse"] = mouse
            group = sub_df.loc[identity1]["Group"]
            group_mouse_means_df["Group"] = group
            for identity2 in list2:
                if (mouse == sub_df.loc[identity2]["Mouse"]) and (group == sub_df.loc[identity2]["Group"]):
                    list2collate.append(identity2)
            for epoch in epoch_list:
                    trace_list = []
                    epoch_name = epoch[0]
                    epoch_dict_averaged[epoch_name][group] = epoch_dict_averaged[epoch_name].get(group, {})
                    epoch_dict_averaged[epoch_name][group][mouse] = epoch_dict_averaged[epoch_name][group].get(mouse, [])
                    for identity in list2collate:
                        traces =  epoch_dict[identity][epoch_name][0][channel_dict[channel]] #modified this from 0
                        trace_list.append(traces[0:2]) #includes just time and deltaff traces
                    time_vec, mean_of_traces, stderr_of_traces = collate_traces(trace_list)
                    epoch_dict_averaged[epoch_name][group][mouse] = [time_vec, mean_of_traces]   
            for identity in list2collate:
                list2.remove(identity) #remove them from list so you don't redundantly add them
        else:
            pass
    return epoch_dict_averaged


def averagedepochs_to_excel(excel_name, epoch_dict_averaged, groups2compare):
    """Take an average reverse epoch dict (Epochs -> Individual Traces) and convert to dataframe.
        Name excel_name as a "string" "without using spaces or slashes or special characters. 
        example: avgepochdata_to_excel("epochdata.xlsx", avg_epoch_dict, groups2compare)"""
    workbook = xlsxwriter.Workbook(excel_name) #needs to include .xlsx
    for epoch_name, exp_group_data in epoch_dict_averaged.items():
        worksheet = workbook.add_worksheet(epoch_name)
        n = 0
        for exp_group_name, mice_data in exp_group_data.items():
            for mouse_name, epoch_trace in mice_data.items(): #epoch_trace includes [time, deltaf]     
                if n == 0:
                    column_content = ["Time", ""]
                    column_content.extend(epoch_trace[0])
                    worksheet.write_column(0, n, column_content)
                    n = n + 1
                #had an else below before
                column_content = [exp_group_name, mouse_name]
                column_content.extend(epoch_trace[1])
                worksheet.write_column(0, n, column_content)
                n = n + 1
    workbook.close()
    
    
    
def auc_finder(avg_epoch_dict, epoch_name, start_minute, end_minute):
    group_auc_dict = {}
    for epoch, groups in avg_epoch_dict.items():
        if epoch == epoch_name:
            group_auc_dict = {}
            for group, mice in groups.items():
                group_auc_dict[group] = ()
                auc_list = []
                for mouse, trace_data in mice.items():
                    start_min_ind = 0
                    end_min_ind = 0
                    time_vec, trace_vec = trace_data
                    for i in range(len(time_vec)):
                        if time_vec[i] == start_minute:
                            start_min_ind = i
                        if int(time_vec[i]) == end_minute:
                            end_min_ind = i
                            break
                    auc_time_vec = time_vec[start_min_ind:end_min_ind + 1]
                    auc_trace_vec = trace_vec[start_min_ind:end_min_ind + 1]
                    auc_time_vec = auc_time_vec.tolist()
                    auc_trace_vec = auc_trace_vec.tolist()
                    
                    auc = np.trapz(auc_trace_vec, auc_time_vec) #performs auc
                    auc_list.append(auc)
                group_auc_dict[group] = (auc_time_vec, auc_list)
    return group_auc_dict



def average_window(epoch_dict_averaged, groups2compare, epoch_name, start_minute, end_minute, down_hz=1):
    """times are in minutes"""
    
    epoch_dict_groups = epoch_dict_averaged[epoch_name]
    average_window_dict = {}

    for group in groups2compare:
        mice_data = epoch_dict_groups[group]
        average_window_dict[group] = average_window_dict.get(group, [])
        for mouse, traces in mice_data.items():
            time_trace = traces[0]
            gcamp_trace = traces[1]
            
            time_point_start = np.where(time_trace==float(start_minute)) 
            time_point_start = int(list(time_point_start)[0])
            time_point_end = np.where(time_trace==float(end_minute)) 
            time_point_end = int(list(time_point_end)[0])
            
            gcamp_window = gcamp_trace[time_point_start:time_point_end + 1] 
            
            gcamp_window_mean = gcamp_window.mean()
            average_window_dict[group].append((mouse, gcamp_window_mean))
            
    return average_window_dict
    



def fig2_epochs_plt(exp_df, reverse_epoch_dict, groups2compare, exp_df_column="Group", deltapercent=True):
    """Group legend follows order in groups2compare. group_traces is for the main graph
    comparing all groups whereas group_trace is for the within group graphs."""  
    for epoch_name, identities in reverse_epoch_dict.items():
        if epoch_name != "Full Trace":
            group_epoch_dict = {}
            for group in groups2compare:
                for identity, trace_data in identities.items():
                    if exp_df.loc[identity, "Group"] != group:
                        pass
                    else:
                        group_epoch_dict[group] = group_epoch_dict.get(group, [])
                        group_epoch_dict[group].append((identity, trace_data[0][0])) #just getting the deltaF trace
                            
            fig3 = plt.figure(figsize=(15,12))
            title = epoch_name + " Photometry Period"
            fig3.suptitle(title, fontsize="30", fontweight="bold")
            group_traces_plt = fig3.add_subplot(211)
            if deltapercent==True:
                group_traces_plt.set_ylabel(r'% $\Delta$F/F', fontsize="x-large")
            else:
                group_traces_plt.set_ylabel(r'$\Delta$F/F', fontsize="x-large")
            group_traces_plt.set_xlabel("Minutes", fontsize="x-large")

            for group_name, traces_info in group_epoch_dict.items():
                
                fig2 = plt.figure(figsize=(15,12))
                individual_traces_plt = fig2.add_subplot(211)
                group_trace_plt = fig2.add_subplot(212)
                if deltapercent==True:
                    group_trace_plt.set_ylabel(r'% $\Delta$F/F', fontsize="x-large")
                else:
                    group_traces_plt.set_ylabel(r'$\Delta$F/F', fontsize="x-large")
                group_trace_plt.set_ylabel(r'$\Delta$F/F', fontsize="x-large")
                group_trace_plt.set_xlabel("Minutes", fontsize="x-large")
                
                traces_data = []
                for identity, trace_data in traces_info:
                    traces_data.append(trace_data)
                    time_axis, trace = trace_data
                    individual_traces_plt.plot(time_axis, trace, linewidth=0.8, label=exp_df.loc[identity,"Mouse"])
                
                
                #handles,labels = individual_traces_plt.get_legend_handles_labels()
                #handles,labels = sorted(zip(handles,labels), key=labels) #sorts labels in alphabetical/numerical order, not in order because came out of dict

                individual_traces_plt.legend(loc="lower left", fontsize="medium", shadow=True)
                individual_traces_plt.axes.get_xaxis().set_visible(False)
                            
                time_axis, mean_trace, stderr_trace = collate_traces(traces_data)  
                group_trace_plt.plot(time_axis, mean_trace, linewidth=1, label="Mean Trace + Std.Error", color="darkcyan")
                group_trace_plt.fill_between(time_axis, mean_trace+stderr_trace, mean_trace-stderr_trace, alpha=0.4, color="salmon")  
                group_trace_plt.legend(loc="lower left", fontsize="medium", shadow=True)
                
                group_traces_plt.plot(time_axis, mean_trace, linewidth=1, label=group_name)
                group_traces_plt.fill_between(time_axis, mean_trace+stderr_trace, mean_trace-stderr_trace, alpha=0.35)  
                       
                fig2.suptitle((group_name + " (" + epoch_name + ")"), fontsize="30", fontweight="bold")
                fig2.tight_layout()
            
            group_traces_plt.legend(loc="upper right", fontsize="large", shadow=True)
            
            fig3.tight_layout()



def fig3_permouse_interventioncompare(exp_df, reverse_epoch_dict, groups2compare, mice2plot, exp_df_column="Group"):
       
    for mouse in mice2plot:   
        for epoch_name, identities in reverse_epoch_dict.items():
            if epoch_name != "Full Trace":
                group_epoch_dict = {}
                for identity, trace_data in identities.items():
                    if exp_df.loc[identity]["Mouse"] != mouse:
                        print("searching for " + exp_df.loc[identity]["Mouse"] + " but is " + mouse)
                        pass
                    else:
                        group_name = exp_df.loc[identity, exp_df_column] 
                        if group_name in groups2compare:
                            #print(identity + " " + group_name)
                            group_epoch_dict[group_name] = group_epoch_dict.get(group_name, [])
                            #mouse_name = exp_df.loc[identity, "Mouse"]
                            group_epoch_dict[group_name].append((identity, trace_data[0][0])) #just getting the deltaF trace
                        print("else")
                fig3 = plt.figure(figsize=(15,12))
                fig3.suptitle((mouse + " " + epoch_name), fontsize="27", fontweight="bold")
                group_traces_plt = fig3.add_subplot(211)
                group_traces_plt.set_ylabel(r'$\Delta$F/F', fontsize="x-large")
                group_traces_plt.set_xlabel("Minutes", fontsize="x-large")
                group_traces_plt.legend(loc="lower left", fontsize="large", shadow=True)
                
                fig3.tight_layout()
                


def plot_averagedepochs(avg_epoch_dict, groups2compare):
    """Group legend follows order in groups2compare"""  
    for epoch_name, groups in avg_epoch_dict.items():
        if epoch_name != "Full Trace":
            group_epoch_dict = {}
            for group, mice in groups.items():
                if group in groups2compare:
                    for mouse, trace_data in mice.items():
                        group_epoch_dict[group] = group_epoch_dict.get(group, [])
                        group_epoch_dict[group].append((mouse, trace_data)) 
    
            fig3 = plt.figure(figsize=(15,12))
            fig3.suptitle(epoch_name, fontsize="30", fontweight="bold")
            group_traces_plt = fig3.add_subplot(211)
            group_traces_plt.set_ylabel(r'$\Delta$F/F', fontsize="x-large")
            group_traces_plt.set_xlabel("Minutes", fontsize="x-large")
    
            for group_name, traces_info in group_epoch_dict.items():
                
                fig2 = plt.figure(figsize=(15,12))
                individual_traces_plt = fig2.add_subplot(211)
                group_trace_plt = fig2.add_subplot(212)
                group_trace_plt.set_ylabel(r'$\Delta$F/F', fontsize="x-large")
                group_trace_plt.set_xlabel("Minutes", fontsize="x-large")
                
                traces_data = []
                for mouse, trace_data in traces_info:
                    traces_data.append(trace_data)
                    time_axis, trace = trace_data
                    individual_traces_plt.plot(time_axis, trace, linewidth=0.8, label=mouse)
                
                
                #handles,labels = individual_traces_plt.get_legend_handles_labels()
                #handles,labels = sorted(zip(handles,labels), key=labels) #sorts labels in alphabetical/numerical order, not in order because came out of dict
    
                individual_traces_plt.legend(loc="lower left", fontsize="medium", shadow=True)
                individual_traces_plt.axes.get_xaxis().set_visible(False)
                            
                time_axis, mean_trace, stderr_trace = collate_traces(traces_data)  
                group_trace_plt.plot(time_axis, mean_trace, linewidth=1, label="Mean Trace + Std.Error", color="darkcyan")
                group_trace_plt.fill_between(time_axis, mean_trace+stderr_trace, mean_trace-stderr_trace, alpha=0.4, color="salmon")  
                group_trace_plt.legend(loc="lower right", fontsize="medium", shadow=True)
                
                group_traces_plt.plot(time_axis, mean_trace, linewidth=1, label=group_name)
                group_traces_plt.fill_between(time_axis, mean_trace+stderr_trace, mean_trace-stderr_trace, alpha=0.35)  
                       
                fig2.suptitle((group_name + " (" + epoch_name + ")"), fontsize="30", fontweight="bold")
                fig2.tight_layout()
            
            group_traces_plt.legend(loc="lower right", fontsize="large", shadow=True)
            
            fig3.tight_layout()


    