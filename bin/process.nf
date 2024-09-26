#!/usr/bin/env nextflow

// Using DSL-2
nextflow.enable.dsl=2


process Resquiggle_Remora {

    container "${params.container__modidec_dacu}"
    publishDir "${params.outdir}/", mode: "copy"

    input:
        // These are the paths to the input files
        path(pod5_files)
        path(bam_files)
        val(kmer_lvl_table)
    
        //The General variables for training data
        tuple val(modified_data), val(use_modified_region), val(training_out), val(mod_type), val(mod_pos), val(bases_before_mod), val(mod_dict)
        
        //The Segmentation variables for training data
        tuple val(batch_size), val(max_seq_length), val(chunck_length), val(time_shift), val(start_read_number), val(end_read_number)
        
    output:
        path("$params.outdir/*.npz"), emit:save_path
    script:
        def general_variables = [modified_data, use_modified_region, training_out, mod_type, mod_pos, bases_before_mod, mod_dict].join(',')
        def segmentation_variables = [batch_size, max_seq_length, chunck_length, time_shift,start_read_number, end_read_number].join(',')
        python bin 'Resquiggle_remora.py --{$pod5_files} --{$bam_files} --{$kmer_lvl_table} --{$general_variables} --{$segmentation_variables}'

    stub:
    """
       mkdir output
       touch output/${training_out}.npz
    """
}