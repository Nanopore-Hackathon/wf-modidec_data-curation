#!/usr/bin/env nextflow

// Using DSL-2
nextflow.enable.dsl=2


process Resquiggle_Remora {

    label "modidec_dacu"
    publishDir "${params.outdir}/", overwrite: true, mode: 'copy', pattern: "*.npz"

    input:
        // These are the paths to the input files
        path(pod5_files)
        path(bam_files)
        val(kmer_lvl_table)
    
        //The General variables for training data
        tuple val(basecalling), val(mod_mapping), val(modified_data), val(use_modified_region), val(training_out), val(mod_type), val(mod_pos), val(bases_before_mod)
        
        //The Segmentation variables for training data
        tuple val(batch_size), val(max_seq_length), val(chunk_length), val(time_shift), val(start_read_number), val(end_read_number)
        val(mod_list)
    
    output:
        path("*.npz")
    
    script:

        """
    
        Remora_resquigle_generate_data.py \
            --base_dir ${baseDir} \
            --pod5_dir $pod5_files \
            --bam_file_dir $bam_files \
            --kmer_lvl_table $kmer_lvl_table \
            \
            --basecalling $basecalling \
            --mod_mapping $mod_mapping \
            --modified_data $modified_data \
            --take_mod_region $use_modified_region \
            --name_save_file $training_out \
            --modified_base $mod_type \
            --mod_pos_initial $mod_pos \
            --start_base_resquigle $bases_before_mod \
            \
            --batch_size $batch_size \
            --max_label_length $max_seq_length \
            --time_segment $chunk_length \
            --shift $time_shift \
            --start_index $start_read_number \
            --end_index $end_read_number \
            \
            --mod_list $mod_list
            
        """

    stub:
    """
       mkdir output
       touch output/${training_out}.npz
    """
}