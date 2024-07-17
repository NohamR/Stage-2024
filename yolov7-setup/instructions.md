https://github.com/JackWoo0831/Yolov7-tracker
https://github.com/microsoft/VoTT?tab=readme-ov-file#build-and-run-from-source

# Yolov7-tracker
git clone https://github.com/JackWoo0831/Yolov7-tracker.git
mv Yolov7-tracker yolov7-tracker
cd yolov7-tracker
git checkout v2  # change to v2 branch !!

# Python：3.9, Pytorch: 1.12
conda create -n yolov7 python=3.9 pytorch=1.12
conda activate yolov7
pip3 install numpy scipy matplotlib cython pandas cuda-python
## ERROR: Could not find a version that satisfies the requirement cuda-python (from versions: none) Requires-Python >=3.10
pip3 install -r requirements.txt
pip3 install ultralytics==8.0.94

# Setup cluster
nvidia-smi 
=> cuda 11.4 sur node20

cf notes d'installation de pytorch pour trouver les bonnes versions : https://pytorch.org/get-started/previous-versions/
pip3 install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cu118
pip3 install filterpy

>>> import torch
>>> torch.cuda.is_available()
True

# Setup macos
conda install pytorch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 -c pytorch

# Config train
- create config tracker/config_files/dataset1_2024_06_19.yaml
data/files_dataset1_2024_06_19.yaml 

- export from VoTT as json 
- convert to Yolov using vott2yolov.py (data/dataset1_2024_06_19/vott2yolov.py) -> data/dataset1_2024_06_19/labels/dataset1/ + data/dataset1_2024_06_19/images/dataset1/
- edit data/dataset1_2024_06_19/dataset.yaml
- get box sizes from data/dataset1_2024_06_19/YOLOV_BDD_Anchors_1280.txt -> cfg/training/yolov7x_dataset1_2024_06_19.yaml

structure :
dataset_name
    |---images
        |---train
                |---sequence_name1
                        |---000001.jpg
                        |---000002.jpg ...
        |---val ...
        |---test ...

    |

# Launch train
python3 train.py --dataset dataset1_2024_06_19__ --workers 1  --device 0 --batch-size 4 --data data/dataset1_2024_06_19/datasetyaml  --img 1280 720 --cfg cfg/training/yolov7x_dataset1_2024_06_19.yaml  --weights ''  --name yolov7x-dataset1_2024_06_19  --hyp data/hyp.scratch.custom.yaml

python3 train.py --dataset dataset2fps_20240718_ --workers 1 --device 0 --batch-size 4 --data data/dataset2fps/dataset.yaml  --img 1280 720 --cfg cfg/training/yolov7x_dataset2fps.yaml --weights '' --name yolov7x-dataset2fps_20240718 --hyp data/hyp.scratch.custom.yaml


Si erreur : _pickle.UnpicklingError: STACK_GLOBAL requires str
Effacer les fichiers .cache : liste_images.cache par exemple...

Si erreur np.int => remplacer par des np.int64

Si erreur cuda/cpu dans loss.py :
you have to replace the line in the file yolo7/utils/loss.py
"from_which_layer.append((torch.ones(size=(len(b),)) * i)"
to "from_which_layer.append((torch.ones(size=(len(b),)) * i).to('cuda'))",
and add new line "fg_mask_inboxes = fg_mask_inboxes.to(torch.device('cuda'))"
after "fg_mask_inboxes = matching_matrix.sum(0) > 0.0"
so you need to do it 3 times in the file

<!-- https://wandb.ai/noham- -->

<!-- /Users/noham/Documents/GitHub/Stage/2024 -->
<!-- /Users/noham/Documents/GitHub/Stage-2024 -->