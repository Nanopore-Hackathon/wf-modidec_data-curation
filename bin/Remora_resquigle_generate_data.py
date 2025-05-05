#!/usr/bin/env python3
# ////////////////////////////////////////////////////////////////////////////////////////////
# DO NOT CHANGE ANYTHING IN THIS FILE !!!
# ////////////////////////////////////////////////////////////////////////////////////////////

import pod5
from remora import io , refine_signal_map, util
import os
import numpy as np
import argparse
import math
import polars as pl

def argparser():
    parser = argparse.ArgumentParser(description="Parser for pod5Viewer input parameters")

    parser.add_argument("--base_dir", required=True, type=str)
    # Required Input
    parser.add_argument("--bam_file", required=True, type=str, help="Path to the BAM files")
    parser.add_argument("--pod5_dir", required=True, type=str, help="Path to the pod5 directory")
    parser.add_argument("--kmer_lvl_table", required=True, type=str, help="Path to the kmer level table")
    
    parser.add_argument("--basecalling", required=True)
    parser.add_argument("--mod_mapping", required=True)
    parser.add_argument("--modified_data", required=True)
    parser.add_argument("--name_save_file", required=True, type=str)
    parser.add_argument("--modified_base", required=True, nargs="+")
    parser.add_argument("--mod_pos_initial", required=True, nargs="+", type = int)
    parser.add_argument("--start_base_resquigle", required=True, type=int)

    parser.add_argument("--batch_size", required=True, type=int)
    parser.add_argument("--start_index", required=True, type=int)
    parser.add_argument("--end_index", required=True, type=int)

    parser.add_argument("--mod_list", required=True, nargs="+")

    return parser

def Remora_resquigle_Generation_data(base_dir, data_path, bam_file, level_table_file, save_path, \
    basecalling, mod_mapping, modified_data, name_save_file, Modified_base, \
    mod_pos_initial, start_base_resquigle, batch_size, \
    start_index, end_index, mod_list):

    if basecalling == "true":
        basecalling = 1
    else:
        basecalling = 0
        
    if mod_mapping == "true":
        mod_mapping = 1
    else:
        mod_mapping = 0
    
    if modified_data == "true":
        modified_data = 1
    else:
        modified_data = 0
        

    # /////// read the files //////

    pod5_dr = pod5.DatasetReader(data_path)
    bam_fh = io.ReadIndexedBam(bam_file)

        # /////// take the name reads////

    read_id = bam_fh.read_ids

        # /// define the function for resquile from Remora ///
        # // old version used for DNA. maybe DNA data has to be analysed again //

    level_table_file = level_table_file

    sig_map_refiner = refine_signal_map.SigMapRefiner(
                            kmer_model_filename=level_table_file,
                            do_rough_rescale=True,
                            scale_iters=0,
                            do_fix_guage=True)
        
    labels = len(mod_list)

    old_start = start_index
    training_data_to_save_list = {"read_id":[],
                                  "modified_data":[],
                                  "modification_type_if_modified":[],
                                  "start_index_on_original_signal":[],
                                  "end_index_on_original_signal":[],
                                  "raw_signal": [],
                                  "one_hot_encoded_base_sequence":[],
                                  "one_hot_encoded_modification_dictionairy":[],
                                  "reference_bam_file":[],
                                  "pod5_directory":[]
                                  }
    
    for name_id in read_id[old_start: end_index]: 

        start_index += 1
        seq_resquigle = ""
        position_adjusting = 0
        Error_read = False

            # /// extract the select read and info from bam file ///

        pod5_read = pod5_dr.get_read(name_id)
        bam_read = bam_fh.get_first_alignment(name_id)

            # /// after extraction, obtain the basecalling information ///

        if bam_read.is_reverse: #correct the signal for forward direction
            flip = False
        else:
            flip = True

        try:
            #/// read data
            read_analysed = io.Read.from_pod5_and_alignment(pod5_read, bam_read, reverse_signal = flip)
            # // resquigle the data with the refence
            read_analysed.set_refine_signal_mapping(sig_map_refiner, ref_mapping=True)

            start_of_mapping = read_analysed.extract_ref_reg(
                read_analysed.ref_reg.adjust(start_adjust = 0, end_adjust=read_analysed.ref_reg.len))

            Raw_signal = start_of_mapping.norm_signal
            seq_resquigle = start_of_mapping.seq
            start_end_resquigle = start_of_mapping.seq_to_sig_map
            #target_id = start_of_mapping.ref_reg.ctg

                # /// check if the modification position has to be adjusted ///
            position_adjusting =start_of_mapping.ref_reg.start
                
        except:

            print("error")
            position_adjusting = 0
            seq_resquigle = ""
            Error_read = True

            """
            mod_pos = mod_pos_initial - position_adjusting - 1            
            max_signal_length = Raw_signal[0 : mod_pos + time_segment]
            """
        
        val_total_seq = position_adjusting + len(seq_resquigle)
        high_threshold = max(mod_pos_initial) + 20
            
            # // select only high score quality, extrapolate signal and save data //

        start_analysis = False

        if mod_mapping:
            if high_threshold < val_total_seq and position_adjusting < max(mod_pos_initial) and not Error_read: 
                start_analysis = True

        else:
            if not Error_read:
                start_analysis = True

        
        if start_analysis: # ///////// TO CHECK !!! ////////////
            Signal_onehot = np.zeros([len(Raw_signal)+1,4 + 1])
            Output_onehot = np.zeros([len(Raw_signal)+1, labels + 2])
            base_dict_output = { "A":1, "C":1, "G":1, "T":1,"X":{}}
            
            for m_base in Modified_base:
                if mod_mapping:
                    value_modification = int(mod_list.index(m_base)) + 2
                    base_dict_output["X"][m_base] = value_modification
                
            base_dict = {"A":1, "C":2, "G":3, "T":4}
            seq_resquigle_mod = seq_resquigle 
            for m_base, mod_pos_init in zip(Modified_base,mod_pos_initial): 
                mod_pos = mod_pos_init - position_adjusting - 1          
                if modified_data:
                    seq_resquigle_mod = seq_resquigle_mod[:mod_pos] + "X" + seq_resquigle_mod[mod_pos + 1:]
                else:
                    seq_resquigle_mod = seq_resquigle
            for m_base, mod_pos_init in zip(Modified_base,mod_pos_initial): 
                mod_pos = mod_pos_init - position_adjusting - 1
                for k,base_identity in enumerate(seq_resquigle_mod):
                    if base_identity != "X":
                        start_resq = start_end_resquigle[k]
                        Signal_onehot[start_resq,base_dict[seq_resquigle[k]]] = 1
                        Output_onehot[start_resq,base_dict_output[seq_resquigle_mod[k]]] = 1
                if not modified_data:
                    mod_pos = 0
                if seq_resquigle_mod[mod_pos] == "X":
                    start_resq = start_end_resquigle[mod_pos]
                    Signal_onehot[start_resq,base_dict[seq_resquigle[mod_pos]]] = 1
                    Output_onehot[start_resq,base_dict_output[seq_resquigle_mod[mod_pos]][m_base]] = 1
            modification_counter = {}
            for m_base in Modified_base:
                modification_counter[m_base] = 0               
            for m_base, mod_pos_init in zip(Modified_base,mod_pos_initial):         
                mod_pos = mod_pos_init - position_adjusting - 1
                try:
                    if mod_mapping and modified_data:
                        mod_position = np.where(Output_onehot[:,base_dict_output["X"][m_base]] > 0)[0][modification_counter[m_base]]
                        modification_counter[m_base] += 1 
                            
                    if mod_mapping and not modified_data:
                        mod_position = np.where(Output_onehot[:,1] > 0)[0][mod_pos]
                        
                    if not mod_mapping and not modified_data:
                        mod_position = 0
                    
                    if not mod_mapping and modified_data:
                        mod_position = 0
                        
                    if mod_mapping:
                        minus_start = np.abs(start_end_resquigle[mod_pos - start_base_resquigle] - mod_position)
                        N_shift = int((400 + minus_start)/25)
                    else:
                        N_shift = int((len(Raw_signal) - 400)/25)
                    for n in range(int(N_shift/16)):
                        train1_batch = np.zeros([16, 400])
                        train2_batch = np.zeros([16, 40, 4])
                        output_batch = np.zeros([16, 40, 1 + labels])

                        for m in range(16):
                            if mod_mapping:
                                middle_mod_position = mod_position #+ int(0.5*np.abs(start_end_resquigle[mod_pos + 1] - start_end_resquigle[mod_pos]))
                                start = middle_mod_position - n*16*25 - m*25
                                end = start + 400

                            else:
                                start = n*16*25 + m*25
                                end = start + 400

                            output_for_batch = np.zeros([40,1 + labels])
                            train2_for_batch = np.zeros([40,4])

                                    # // here I am using a trick. All the bases has no zero value
                                    # making again the one-hot into an array and removing the 0 values,
                                    # I obtain the index of the final one-hot sequence for train2 and output

                            probe_1 = np.argmax(Signal_onehot[start:end,:], axis = -1)
                            probe_1 = probe_1[probe_1 != 0]
                            probe_1 = probe_1 - 1

                            probe_2 = np.argmax(Output_onehot[start:end,:], axis = -1)
                            probe_2 = probe_2[probe_2 != 0]
                            probe_2 = probe_2 - 1
                            
                            try:

                                for kk in range(len(probe_1)):
                                            
                                    train2_for_batch[kk, probe_1[kk]] = 1
                                    output_for_batch[kk, probe_2[kk]] = 1

                            except:
                                for kk in range(40):                                
                                    train2_for_batch[kk, probe_1[kk]] = 1
                                    output_for_batch[kk, probe_2[kk]] = 1

                                    # try/expect is places for data that are too short for storage
                                    # the problem is only related to modified data.

                            try:
                                train1_batch[m] = Raw_signal[start:end]
                                train2_batch[m] = train2_for_batch
                                output_batch[m] = output_for_batch
                                
                                training_data_to_save_list["read_id"].append(name_id)
                                training_data_to_save_list["raw_signal"].append(train1_batch[m])
                                training_data_to_save_list["one_hot_encoded_base_sequence"].append(train2_batch[m])
                                training_data_to_save_list["one_hot_encoded_modification_dictionairy"].append(output_batch[m])

                            except:
                                if mod_position < int(400/2):                            
                                    start = mod_position
                                    end = start + 400

                                else:     
                                    start = mod_position - int(400/2)
                                    end = start + 400

                                probe_1 = np.argmax(Signal_onehot[start:end,:], axis = -1)
                                probe_1 = probe_1[probe_1 != 0]
                                probe_1 = probe_1 - 1

                                probe_2 = np.argmax(Output_onehot[start:end,:], axis = -1)
                                probe_2 = probe_2[probe_2 != 0]
                                probe_2 = probe_2 - 1

                                try:

                                    for kk in range(len(probe_1)):
                                                
                                        train2_for_batch[kk, probe_1[kk]] = 1
                                        output_for_batch[kk, probe_2[kk]] = 1

                                except:
                                    for kk in range(40):
                                                
                                        train2_for_batch[kk, probe_1[kk]] = 1
                                        output_for_batch[kk, probe_2[kk]] = 1

                                train1_batch[m] = Raw_signal[start:end]
                                train2_batch[m] = train2_for_batch
                                output_batch[m] = output_for_batch
                                
                                training_data_to_save_list["read_id"].append(name_id)
                                training_data_to_save_list["raw_signal"].append(train1_batch[m])
                                training_data_to_save_list["one_hot_encoded_base_sequence"].append(train2_batch[m])
                                training_data_to_save_list["one_hot_encoded_modification_dictionairy"].append(output_batch[m])                                                        
                except Exception as e:
                    print("resquiggle error")
                    print(e)   
                    continue
    for batch_index in range(math.floor(len(training_data_to_save_list["read_id"])/batch_size)): 
        file_name = f"{os.path.basename(bam_file).split('.bam')[0]}_{batch_index}.npz"
        start_index=batch_index*batch_size
        end_index=(batch_index+1)*batch_size
        np.savez_compressed(file_name, train_input = training_data_to_save_list["raw_signal"][start_index:end_index],train_input2 = training_data_to_save_list["one_hot_encoded_base_sequence"][start_index:end_index], train_output = training_data_to_save_list["one_hot_encoded_modification_dictionairy"][start_index:end_index])
    print(f"Produced entities: {len(training_data_to_save_list['read_id'])}")
    print(f"Produced batches: {math.ceil(len(training_data_to_save_list['read_id'])/batch_size)}")
    
if __name__ == "__main__":
    args = argparser().parse_args()
    print(args)
    Remora_resquigle_Generation_data(args.base_dir, args.pod5_dir, args.bam_file, args.kmer_lvl_table, "output", \
        args.basecalling, args.mod_mapping, args.modified_data, args.name_save_file, args.modified_base, \
        args.mod_pos_initial, args.start_base_resquigle, args.batch_size, \
        args.start_index, args.end_index, args.mod_list)
