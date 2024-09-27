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
