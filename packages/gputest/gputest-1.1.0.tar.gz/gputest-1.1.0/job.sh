#!/bin/bash

#SBATCH -p smart_health_01
#SBATCH --gres=gpu:1
#SBATCH -N 1
#SBATCH -o test_torch.log
#SBATCH -e test_torch.log

#source activate torch
#python -c "import torch;print(torch.cuda.is_available())"
python gpu_test.py
