#PBS -N UPPASDHEISDM2D
#PBS -l select=1:ncpus=10:mem=4gb:scratch_local=50gb:cluster=^haldir
#PBS -l walltime=24:00:00

# additional info files
JOB_INFO=$PBS_O_WORKDIR/info.out
STD_OUT=$PBS_O_WORKDIR/uppasd.out

# setting the automatical cleaning of the SCRATCH
# trap 'clean_scratch' TERM EXIT

# load modules
# module load intelcdk-19.0.4
# module load intel-mkl/2019.4.243
# module load openmpi

module add python36-modules-gcc

# set number of processors
export OMP_NUM_THREADS=10

# create scratch
SCR=$SCRATCHDIR

# change directory to the sratch
cd $SCR || exit

#DELTAJ=$1
#DM=$2

# run simulation
export SD_PATH=/storage/praha1/home/jpriessnitz/UppASD/source/sd
export PYTHONPATH=$PYTHONPATH:/storage/praha1/home/jpriessnitz/europium
python /storage/praha1/home/jpriessnitz/europium/pysd_hysteresis_T_fm/hysteresis.py $DM $TEMP $STEPS
#/storage/praha1/home/balaz/local/UppASD-master-ifort/source/sd


# copy results to my Datadir
cp experiment.out $PBS_O_WORKDIR/

# remove files from the scratch
rm -rf *

# exit job
exit
