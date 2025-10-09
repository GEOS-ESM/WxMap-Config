source /usr/share/lmod/lmod/init/csh

module purge
module use -a /discover/swdev/gmao_SIteam/modulefiles-SLES15

module load GEOSenv
module load comp/gcc/11.4.0
module load comp/intel/2021.6.0
module load mpi/impi/2021.13
module load ffmpeg/5.0
module load ImageMagick
module load python/GEOSpyD/Min23.5.2-0_py3.11
#module load python/GEOSpyD/24.11.3-0/3.12

setenv INSTALL_PATH /home/dao_ops/cylc8-workflows/EIC_fires
setenv GAVERSION 2.1.0.oga.1
setenv PYTHONPATH $INSTALL_PATH/lib:/discover/nobackup/dao_ops/jardizzo/software/lib/python3.11/site-packages

setenv PATH ${PATH}:$INSTALL_PATH/bin

umask 022
