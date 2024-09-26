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
    required_input.add_argument("--index", required=True, type=int, help="Current index of the bam file")

    # Data for Training (grouped under a single flag with multiple values)
    training_group = parser.add_argument_group("Data for Training", "Parameters related to training the model")
    training_group.add_argument("--training_params", nargs="+", help="""
        Parameters related to training, in order:
            basecalling (bool), 
            mod_mapping (bool), 
            modified_data (bool), 
            use_modified_region (bool), 
            training_out (str), 
            mod_type (str), 
            mod_pos (int), 
            bases_before_mod (int), 
            mod_dict (str)
    """)

    # Segmentation Parameters (grouped under a single flag with multiple values)
    segmentation_group = parser.add_argument_group("Segmentation Params", "Parameters related to data segmentation")
    segmentation_group.add_argument("--segmentation_params", nargs="+", help="""
        Parameters related to segmentation, in order:
        batch_size (int), 
        max_seq_length (int), 
        chunk_length (int), 
        time_shift (int), 
        start_read_num (int), 
        end_read_num (int)
    """)

    return parser

def mod_str_to_mod_dict(mod_str: str) -> Dict[str, int]:
    """
    Parses the given mod_dict string to a proper python dict.

    Params:
        mod_str (str): Given mod_dict input
    
    Returns:
        Dict[str, int]: Dict with each mod as key and ints as corresponding indices
    """
    mod_str = mod_str.replace("{", "").replace("}", "").replace('"', "")
    mod_dict = {}
    print(mod_str)
    print(mod_str.split(","))
    for pair in mod_str.split(","):
        pair = pair.split(":")
        key = pair[0]
        value = int(pair[1])
        mod_dict[key] = value
    return mod_dict

def start_remora_resquiggle(pod5_files: str, bam_files: str, kmer_lvl_table: str,
                            training_params: List[str],
                            segmentation_params: List[str],
                            index: int) -> None:

    mod_dict = mod_str_to_mod_dict(training_params.pop(9))

    # data_path, 
    print(pod5_files)
    # bam_file, 
    print(bam_files)
    # level_table_file, 
    print(kmer_lvl_table)
    # save_path, 
    print("outdir")
    # Variables, 
    print(training_params)
    # variables_segmentation, 
    print(segmentation_params[:5])
    # Indexes, 
    print(segmentation_params[5:])
    # mod_dictionary, 
    print(mod_dict)
    # ind_loop
    print(index)

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

    start_remora_resquiggle(args.pod5_dir, 
                            args.bam_files, 
                            args.kmer_lvl_table, 
                            args.training_params, 
                            args.segmentation_params, 
                            args.index)


# python /root/wf-modidec_data-curation/bin/Resquiggle_remora.py \
#   --pod5_dir path/to/pod5 \
#   --bam_files /path/to/bamdir \
#   --kmer_lvl_table /path/to/kmerlevels \
#   --training_params True True True True a b 100 10 {"A":1,"B":2} \
#   --segmentation_params 100 200 20 1 0 10 \
#   --index 0