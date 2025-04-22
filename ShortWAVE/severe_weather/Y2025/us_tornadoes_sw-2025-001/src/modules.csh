
source /usr/share/lmod/lmod/init/csh

module purge

module use -a /discover/swdev/gmao_SIteam/modulefiles-SLES15

module load GEOSenv
module load comp/gcc/11.4.0
module load comp/intel/2021.6.0
module load mpi/impi/2021.13
module load ffmpeg/5.0
module load ImageMagick
module load python/GEOSpyD/Min24.4.0-0_py3.11
#module load python/GEOSpyD/24.11.3-0/3.12

setenv GAVERSION 2.1.0.oga.1
setenv PYTHONPATH /home/dao_ops/gmao_packages/WxMap/lib

setenv PATH ${PATH}:/home/dao_ops/gmao_packages/WxMap/utils:$SHARE/dasilva/opengrads/Contents
