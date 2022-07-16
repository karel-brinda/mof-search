# MOF-search

This is the pipeline for BLAST-like search within the 661k collection.


## Dependencies

Some dependencies are packaged into `conda` environments that `snakemake` will automatically create.
Others are non-standard (which you might need to install) and stardard (which you probably have).

### Non-standard
* `python3`
* `snakemake`
* `mamba`
* `cobs`
* `yq`

### Standard
* `curl`
* `xz`
* `sed`
* `head`
* `grep`


## Commands

* `make`          Run everything
* `make download` Download the 661k assemblies and COBS indexes
* `make match`    Match queries using COBS (queries -> candidates)
* `make map`      Map candidates to the assemblies (candidates -> alignments)
* `make report`   Generate Snakemake report
* `make clean`    Clean intermediate search files
* `make cleanall` Clean all generated and downloaded file



## Directories

* `asms/`, `cobs/` Downloaded assemblies and COBS indexes
* `queries/` Queries, to be provided within one or more FASTA files (`.fa`)
* `intermediate/` Intermediate files
   * `00_cobs` Decompressed COBS indexes (tmp)
   * `01_match` COBS matches
   * `02_filter` Filtered candidates
   * `03_map` Minimap2 alignments
   * `fixed_queries` Sanitized queries
* `output/` Results