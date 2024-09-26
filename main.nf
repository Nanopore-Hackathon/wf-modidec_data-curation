#!/usr/bin/env nextflow

/* The following pipeline is intended for research purposes only */
nextflow.enable.dsl=2

/*

========================================================================================
    VALIDATE & PRINT PARAMETER SUMMARY
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

println """\
    wf-ModiDec
    ================================================
    v0.0.1
    """.stripIndent()

/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Import Required Workflows and Processes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/
// include { process_name } from "process_file"
include { Resquiggle_Remora } from "./bin/process.nf"

// WorkflowMain.initialise(workflow, params, log)


workflow {

    //Pinguscript.ping_start(nextflow, workflow, params)

    Resquiggle_Remora(file(params.pod5_files), file(params.bam_files), params.kmer_lvl_table,
    tuple(params.basecalling, params.mod_mapping, params.modified_data, params.use_modified_region, params.training_out, params.mod_type, params.mod_pos, params.bases_before_mod),
    tuple(params.batch_size, params.max_seq_length, params.chunk_length, params.time_shift, params.start_read_num, params.end_read_num),
    params.mod_list)
}

workflow.onError {
    //Pinguscript.ping_error(nextflow, workflow, params)
}

workflow.onComplete {
    println "Analysis Complete at: $workflow.complete"
    println "Execution Status: ${ workflow.success ? 'OK' : 'failed' }"
    println "Location of Output: ${ params.out_dir }"

    //Pinguscript.ping_complete(nextflow, workflow, params)
}