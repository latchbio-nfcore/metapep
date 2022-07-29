process GENERATE_PEPTIDES {
    label 'process_long'
    label 'process_high_memory'
    label 'cache_lenient'

    conda (params.enable_conda ? "conda-forge::pandas=1.1.2 conda-forge::biopython=1.78 conda-forge::numpy=1.18.1" : null)
    container "${ workflow.containerEngine == 'singularity' && !task.ext.singularity_pull_docker_container ?
        'https://depot.galaxyproject.org/singularity/mulled-v2-1e9d4f78feac0eb2c8d8246367973b3f6358defc:41ffac721ff9b03ca1121742e969d0e7d78e589f-0' :
        'quay.io/biocontainers/mulled-v2-1e9d4f78feac0eb2c8d8246367973b3f6358defc:41ffac721ff9b03ca1121742e969d0e7d78e589f-0' }"

    input:
    path(proteins)

    output:
    path "peptides.tsv.gz",         emit: ch_peptides               // peptide_id, peptide_sequence
    path "proteins_peptides.tsv",   emit: ch_proteins_peptides      // protein_id, peptide_id, count
    path "versions.yml",            emit: versions
    //file "proteins_lengths.tsv"

    script:
    def min_pep_len = params.min_pep_len
    def max_pep_len = params.max_pep_len
    """
    generate_peptides.py -i $proteins \\
                        -min $min_pep_len \\
                        -max $max_pep_len \\
                        -p "peptides.tsv.gz" \\
                        -pp "proteins_peptides.tsv" \\
                        -l "proteins_lengths.tsv"

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        python: \$(python --version | sed 's/Python //g')
        pandas: \$(python -c "import pkg_resources; print(pkg_resources.get_distribution('pandas').version)")
        biopython: \$(python -c "import pkg_resources; print(pkg_resources.get_distribution('biopython').version)")
        numpy: \$(python -c "import pkg_resources; print(pkg_resources.get_distribution('numpy').version)")
    END_VERSIONS
    """
}
