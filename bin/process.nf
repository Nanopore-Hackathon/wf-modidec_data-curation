#!/usr/bin/env nextflow

// Using DSL-2
nextflow.enable.dsl=2


process Resquigle_Remora {
    container "${params.container__modidec_dacu}"
    publishDir "${params.output_folder}/GATK/", mode: "copy", overwrite: true

    input:
    path(pod5)
    path(bam)
    path(kmer_table)
    output:
    path(save_path), emit:save_path
    script:
    bin 'Resquigle_remora.py -- -- -- -- -- --'
}


workflow {

    take:
    pod5
    main:
    Resquigle_Remora(
        pod5,
        bam,
        kmer_table
        )
    emit:
    output = Resquigle_Remora.out.save_path

}