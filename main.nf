#!/usr/bin/env nextflow

/* The following pipeline is intended for research purposes only */
nextflow.enable.dsl=2


process Basecalling_and_Alignment {
    label "dorado_basecaller"
    publishDir "${params.outdir}/", overwrite: true, mode: 'copy'
    stageInMode "copy"
    input:
        path(pod5_files)
        path(reference_fasta)
        val(training_out)
    output:
        path("*.pod5"),includeInputs: true , emit: pod5_files
        path("*.bam"), emit: bam_file
    """
    dorado basecaller sup ./ --emit-moves | samtools fastq -T "*" | minimap2 -y --MD -ax map-ont ${reference_fasta} - | samtools view -b -F 4 > ${training_out}.bam
    """
}

// WorkflowMain.initialise(workflow, params, log)
process load_kmer_tables {
    input:
    val(flowcell_type)
    output:
    path("*.txt"), emit:kmer_lvl_table
    script:

    //load kmer table from website
    """
    if [[ ${flowcell_type} == "RNA002" ]]; then
	wget https://raw.githubusercontent.com/nanoporetech/kmer_models/refs/heads/master/rna_r9.4_180mv_70bps/5mer_levels_v1.txt
	else
    wget https://raw.githubusercontent.com/nanoporetech/kmer_models/refs/heads/master/rna004/9mer_levels_v1.txt
    fi
    """
}

process Resquiggle_Remora {
    label "modidec_dacu"
    publishDir "${params.outdir}/", overwrite: true, mode: 'move'
    stageInMode "symlink"
    input:
        // These are the paths to the input files
        path(pod5_files)
        path(bam_file)
        path(kmer_lvl_table)
    
        //The General variables for training data
        tuple val(basecalling), val(mod_mapping), val(modified_data), val(use_modified_region), val(training_out), val(mod_type), val(mod_pos), val(bases_before_mod)
        
        //The Segmentation variables for training data
        tuple val(batch_size), val(max_seq_length), val(chunk_length), val(time_shift), val(start_read_number), val(end_read_number)
        val(mod_list)

        val(curation_type)

    output:
        path("*")
    
    script:
        """
        if [ ${params.curation_type} == "Training" ]
        then
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
        else
            echo "Bamfile for analysis has been successfully created." > finished.log
        fi
        find . -type l -delete
        """
}


workflow {

    //Pinguscript.ping_start(nextflow, workflow, params)

    //bam_files_ch = Channel.fromPath("${params.bam_files}/*.bam")
    
    kmer_table = load_kmer_tables(params.flowcell_type)
    basecalling_and_alignment = Basecalling_and_Alignment(file("$params.pod5_files/*.pod5"), file(params.reference_fasta),params.training_out)
    Resquiggle_Remora(basecalling_and_alignment.pod5_files, basecalling_and_alignment.bam_file, kmer_table.kmer_lvl_table,
    tuple(params.basecalling, params.mod_mapping, params.modified_data, params.use_modified_region, params.training_out, params.mod_type, params.mod_pos, params.bases_before_mod),
    tuple(params.batch_size, params.max_seq_length, params.chunk_length, params.time_shift, params.start_read_num, params.end_read_num),
    params.mod_list, params.curation_type)
}

workflow.onError {
    //Pinguscript.ping_error(nextflow, workflow, params)
}

workflow.onComplete {
    println "Analysis Complete at: $workflow.complete"
    println "Execution Status: ${ workflow.success ? 'OK' : 'failed' }"
    println "Location of Output: ${ params.outdir }"
    //Pinguscript.ping_complete(nextflow, workflow, params)
}