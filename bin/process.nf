#!/usr/bin/env nextflow

// Using DSL-2
nextflow.enable.dsl=2

process load_kmer_tables {

    input:
    val(flowcell_type)
    output:
    path(kmer_lvl_table), emit:kmer_lvl_table
    script:

    //load kmer table from website
    """
    if [[ ${flowcell_type} == "RNA002" ]]; then
	wget "https://github.com/nanoporetech/kmer_models/blob/master/legacy/legacy_r9.4_180mv_70bps_5mer_RNA/template_median69pA.model" \$kmer_lvl_table
	else
    wget "https://github.com/nanoporetech/kmer_models/blob/master/rna004/9mer_levels_v1.txt" \$kmer_lvl_table
    fi
    """
}

process Resquiggle_Remora {

    label "modidec_dacu"
    publishDir "${params.outdir}/", overwrite: true, mode: 'move', pattern: "*.npz"

    input:
        // These are the paths to the input files
        path(pod5_files)
        path(bam_file)
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
            --bam_file $bam_file \
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
