#!/bin/bash
#set a job name  
#SBATCH --job-name=test
#################  
#a file for job output, you can check job progress
#SBATCH --output=test.out
#################
# a file for errors from the job
#SBATCH --error=test.err
#################
#time you think you need; default is one day
#in minutes in this case, hh:mm:ss
#SBATCH --time=24:00:00
#################
#number of tasks you are requesting, N for all cores
#SBATCH -N 1
#SBATCH --exclusive
#################
#partition to use
#SBATCH --partition=par-gpu-2
#################
#number of nodes to distribute n tasks across
#################

python test_abs_net_vs_datasize.py