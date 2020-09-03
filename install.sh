# install miniconda - see https://docs.conda.io/en/latest/miniconda.html
export PATH=/bin:/usr/bin:${CONDA_EXE}
# . $HOME/miniconda3/etc/profile.d/conda.sh
conda init
source ~/.bashrc
conda env create -f environment.yml
conda activate havic_env
# echo "install.packages('Rcpp', repos='https://cloud.r-project.org')
# install.packages('magick', repos='https://cloud.r-project.org')
# install.packages('phytools',repos='https://cloud.r-project.org', type='source')
# install.packages('pheatmap', repos='https://cloud.r-project.org')
# install.packages('BiocManager', repos='https://cloud.r-project.org')
# BiocManager::install('GenomicAlignments')
# BiocManager::install('Biostrings')
# BiocManager::install('Rsamtools')
# BiocManager::install('ggtree')
# BiocManager::install('tidyverse')" | R --no-save
# havic test
