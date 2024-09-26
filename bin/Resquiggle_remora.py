#!/usr/bin/env python3

import argparse
from typing import List, Dict
from Remora_resquigle_generate_data import Remora_resquigle_Generation_data

def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Parser for pod5Viewer input parameters")

    # Required Input
    required_input = parser.add_argument_group("Required Input", "Parameters that are required.")
    required_input.add_argument("--pod5_dir", required=True, type=str, help="Path to the pod5 directory")
    required_input.add_argument("--bam_files", required=True, type=str, help="Path to the BAM files")
    required_input.add_argument("--kmer_lvl_table", required=True, type=str, help="Path to the kmer level table")
    
    required_input.add_argument("--basecalling", required=True, type=bool)
    required_input.add_argument("--mod_mapping", required=True, type=bool)
    required_input.add_argument("--modified_data", required=True, type=bool)
    required_input.add_argument("--take_mod_region", required=True, type=bool)
    required_input.add_argument("--name_save_file", required=True, type=str)
    required_input.add_argument("--modified_base", required=True, type=str, nargs="+")
    required_input.add_argument("--mod_pos_initial", required=True, type=int)
    required_input.add_argument("--start_base_resquigle", required=True, type=int)

    required_input.add_argument("--batch_size", required=True, type=int)
    required_input.add_argument("--max_label_length", required=True, type=int)
    required_input.add_argument("--time_segment", required=True, type=int)
    required_input.add_argument("--shift", required=True, type=int)

    return parser


def start_remora_resquiggle(pod5_files: str, bam_files: str, kmer_lvl_table: str,
                            training_params,
                            segmentation_params: List[str]):

    #mod_dict = mod_str_to_mod_dict(training_params.pop(-1))
    #print(mod_dict)
    # data_path, 
    #print(pod5_files)
    # bam_file, 
    #print(bam_files)
    # level_table_file, 
    #print(kmer_lvl_table)
    # save_path, 
    #print("outdir")
    # Variables, 
    print(training_params)
    #for item in training_params:
    #   print(item)
    # variables_segmentation, 
    #print(segmentation_params)
    #print(segmentation_params[:5])
    # Indexes, 
    #print(segmentation_params[5:])
    # mod_dictionary, 
    #print(mod_dict)
    # ind_loop
    #print(index)

    # Remora_resquigle_Generation_data(data_path = pod5_files,
    #                                  bam_file = bam_files,
    #                                  level_table_file = kmer_lvl_table,
    #                                  save_path = "outdir",
    #                                  Variables = training_params,
    #                                  variables_segmentation = segmentation_params[:5],
    #                                  Indexes = segmentation_params[5:],
    #                                  mod_dictionary = mod_dict,
    #                                  ind_loop = index)


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    print(args)
    print(args.training_params)
    start_remora_resquiggle(args.pod5_dir, 
                            args.bam_files, 
                            args.kmer_lvl_table, 
                            args.training_params, 
                            args.segmentation_params, 
                            #args.index)
    )


# python /root/wf-modidec_data-curation/bin/Resquiggle_remora.py \
#   --pod5_dir path/to/pod5 \
#   --bam_files /path/to/bamdir \
#   --kmer_lvl_table /path/to/kmerlevels \
#   --training_params True True True True a b 100 10 {"A":1,"B":2} \
#   --segmentation_params 100 200 20 1 0 10 \
#   --index 0