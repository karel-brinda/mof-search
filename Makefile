.PHONY: all help clean cleanall cluster

SHELL=/usr/bin/env bash -eo pipefail

.SECONDARY:

.SUFFIXES:

all:
	snakemake \
		--rerun-incomplete \
		-p -j all -k #--use-singularity

help: ## Print help message
	@echo "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\\x1b[36m\1\\x1b[m:\2/' | column -c2 -t -s : | sort)"

clean: ## Clean
	rm -f intermediate/{01_*,02*,03*,04*}/*.xz

cleanall: clean ## Clean all
	rm -f {asms,cobs}/*.xz

cluster:
	sbatch \
        -c 10 \
        -p priority \
        --mem=80GB \
        -t 0-02:00:00 \
        --wrap="snakemake --rerun-incomplete -p -j all -k"
