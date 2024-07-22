#!/bin/bash

## <------------------ pour le cluster de calcul
####SBATCH -N 1 ## 1 noeud
#SBATCH --nodelist=node20
### #SBATCH --exclusive ## le noeud sera entierement dedié à notre job.
######SBATCH -t 12:00:00  ## job tué au bout de 12h
#SBATCH --gres=gpu:1 ## 4 GPU par noeud
### #SBATCH --constraint=gpudp ## noeuds GPU double précision
#SBATCH --job-name=GPU_yolov7_noham
#SBATCH --chdir=/home/noham.rivoirard/yolov7-tracker
# -- Optionnel, pour être notifié par email :
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=noham@noh.am
# -- Sortie standard et d'erreur dans le fichier .output :
#SBATCH --output=./%j.stdout
#SBATCH --error=./%j.stderr
# -- Contexte matériel
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1

echo "SLURM_STEP_GPUS : "${SLURM_STEP_GPUS}
echo "SLURM_JOB_GPUS : "$SLURM_JOB_GPUS
echo "SLURM_STEP/JOB_GPUS "${SLURM_STEP_GPUS:-$SLURM_JOB_GPUS}
echo "CUDA_VISIBLE_DEVICES : "${CUDA_VISIBLE_DEVICES}

source /usr/local/anaconda3/etc/profile.d/conda.sh

conda activate yolov7
which python

#export OMP_NUM_THREADS=8
#echo $OMP_NUM_THREADS
#
## doc
# squeue permet de voir les jobs en attente ou en train de tourner. S'ils tournent, il y aura un R dans la colonne ST.
# sattach permet d'attacher sur le terminal les E/S d'un job en train de tourner. Ça permet de surveiller l'avancée d'un job, ou par exemple d'interagir avec un debugger. ctrl-c permet de détacher de nouveau le job et de le laisser de nouveau tourner en fond (de manière non bloquante).
# scancel permet permet de supprimer une soumission ou d’arrêter le job s'il est en cours d’exécution.
# sstat donne des infos sur les ressources utilisées par un job

# python3 train.py --dataset datasetv2_20240722_ --epochs 600 --workers 1 --device 0 --batch-size 4 --data data/datasetv2/dataset.yaml  --img 1280 720 --cfg cfg/training/yolov7x_datasetv2.yaml --weights '' --name yolov7x-datasetv2_20240722 --hyp data/hyp.scratch.custom.yamlclear
# srun python3 train.py --dataset dataset1_2024_06_19__ --workers 1  --device ${CUDA_VISIBLE_DEVICES} --batch-size 4 --epochs 600 --data data/dataset1_2024_06_19/dataset.yaml  --img 1280 720 --cfg cfg/training/yolov7x_dataset1_2024_06_19.yaml  --weights ''  --name yolov7x-dataset1_2024_06_19  --hyp data/hyp.scratch.custom.yaml
srun python3 train.py --dataset datasetv2_20240722_ --epochs 600 --workers 1 --device ${CUDA_VISIBLE_DEVICES} --batch-size 4 --data data/datasetv2/dataset.yaml  --img 1280 720 --cfg cfg/training/yolov7x_datasetv2.yaml --weights '' --name yolov7x-datasetv2_20240722 --hyp data/hyp.scratch.custom.yaml