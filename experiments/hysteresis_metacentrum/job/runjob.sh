#PBS -N EuropiumHyst
#PBS -l select=1:ncpus=12:mem=1gb:scratch_local=10gb:cluster=^haldir
#PBS -l walltime=24:00:00
#PBS -m ae
#PBS -M honya121@gmail.com

# additional info files
JOB_INFO=$PBS_O_WORKDIR/info.out
STD_OUT=$PBS_O_WORKDIR/uppasd.out

# setting the automatical cleaning of the SCRATCH
# trap 'clean_scratch' TERM EXIT

# load modules
module load intelcdk-19.0.4
module load intel-mkl/2019.4.243
module load openmpi

# set number of processors
export OMP_NUM_THREADS=$PBS_NUM_PPN

# create scratch
SCR=$SCRATCHDIR

# copy input files to the scratch
cp -r $PBS_O_WORKDIR/* $SCR
# cp $PBS_O_WORKDIR/inpsd.dat $SCR
# cp $PBS_O_WORKDIR/jfile $SCR
# cp $PBS_O_WORKDIR/dmfile $SCR
# cp $PBS_O_WORKDIR/pdfile $SCR
# cp $PBS_O_WORKDIR/posfile $SCR
# cp $PBS_O_WORKDIR/momfile $SCR

# change directory to the sratch
cd $SCR || exit

# run simulation
./run_hyst.sh
#/storage/praha1/home/balaz/local/UppASD-master-ifort/source/sd


# archive data
archive="results.tar"
tar -cvf $archive *
gzip $archive

# copy results to my Datadir
cp ./$archive".gz" $PBS_O_WORKDIR

# remove files from the scratch
rm -rf *

# exit job
exit
