# References 
[Yolov7-tracker](https://github.com/JackWoo0831/Yolov7-tracker)

[VoTT](https://github.com/microsoft/VoTT?tab=readme-ov-file#build-and-run-from-source)

# Yolov7-tracker
```bash
git clone https://github.com/JackWoo0831/Yolov7-tracker.git
mv Yolov7-tracker yolov7-tracker
cd yolov7-tracker
git checkout v2  # change to v2 branch !!
```
```bash
conda create -n yolov7 python=3.9 pytorch=1.12
conda activate yolov7
pip3 install numpy scipy matplotlib cython pandas cuda-python
```

<!-- ## ERROR: Could not find a version that satisfies the requirement cuda-python (from versions: none) Requires-Python >=3.10 -->
```bash
pip3 install -r requirements.txt
pip3 install ultralytics==8.0.94
```

# Setup cluster
```bash
nvidia-smi => cuda 11.4 sur node20
```

cf notes d'installation de pytorch pour trouver les bonnes versions : https://pytorch.org/get-started/previous-versions/
```bash
pip3 install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cu118
pip3 install filterpy
```

```bash
>>> import torch
>>> torch.cuda.is_available()
True
```

# Setup macos
```bash
conda install pytorch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 -c pytorch
```

# Config train
- Create [DATASETNAME.yaml](../test/yolov7-tracker/tracker/config_files/dataset2fps.yaml) in tracker/config_files (config file of the dataset):
```yaml
DATASET_ROOT: '/data/DATASETNAME'
SPLIT: train
CATEGORY_NAMES: 
  - 'runner'

CATEGORY_DICT:
  0: 'runner'

CERTAIN_SEQS:
  - 

IGNORE_SEQS:  # Seqs you want to ignore
  - 
```

- Export from VoTT as json
- Convert to Yolov using [vott2yolov.py](../yolov7-setup/vott2yolov.py)
- Edit [dataset.yaml](../test/yolov7-tracker/data/dataset2fps/dataset.yaml) in data/DATASETNAME:
```yaml
train: data/DATASETNAME/liste_images.txt
val: data/DATASETNAME/liste_images.txt
nc: 1
names: ['runner']
```
- Get box sizes from the dataset using [compute_yolov3_anchors.py](../yolov7-setup/compute_yolov3_anchors.py), result as follow:
```
Your custom anchor boxes are [[ 13.  34.]
 [ 17.  46.]
 [ 18.  59.]
 [ 21.  79.]
 [ 26. 102.]
 [ 33. 111.]
 [ 34. 135.]
 [ 40. 155.]
 [ 76. 161.]]
Anchors box for yaml file:
anchors:
  - [13,34, 17,46, 18,59]  # P3/8
  - [21,79, 26,102, 33,111]  # P4/16
  - [34,135, 40,155, 76,161]  # P5/32
  ```
 - Replace anchors box in cfg/training/yolov7x_DATASETNAME.yaml, ex: [yolov7x_dataset2fps.yaml](../test/yolov7-tracker/cfg/training/yolov7x_dataset2fps.yaml)


# Launch train
GPU: 
```bash
python3 train.py --dataset dataset1_2024_06_19__ --workers 1  --device 0 --batch-size 4 --data data/dataset1_2024_06_19/datasetyaml  --img 1280 720 --cfg cfg/training/yolov7x_dataset1_2024_06_19.yaml  --weights ''  --name yolov7x-dataset1_2024_06_19  --hyp data/hyp.scratch.custom.yaml
```

<!-- python3 train.py --dataset dataset2fps_20240718_ --workers 1 --device 0 --batch-size 4 --data data/dataset2fps/dataset.yaml  --img 1280 720 --cfg cfg/training/yolov7x_dataset2fps.yaml --weights '' --name yolov7x-dataset2fps_20240718 --hyp data/hyp.scratch.custom.yaml -->
<!-- python3 train.py --dataset dataset2fps_20240718_ --epochs 20 --workers 1 --device cpu --batch-size 4 --data data/dataset2fps/dataset.yaml  --img 1280 720 --cfg cfg/training/yolov7x_dataset2fps.yaml --weights '' --name yolov7x-dataset2fps_20240718 --hyp data/hyp.scratch.custom.yaml  -->

CPU:
```bash
python3 train.py --dataset dataset2fps_20240718_ --epochs 20 --workers 1 --device cpu --batch-size 4 --data data/dataset2fps/dataset.yaml  --img 1280 720 --cfg cfg/training/yolov7x_dataset2fps.yaml --weights '' --name yolov7x-dataset2fps_20240718 --hyp data/hyp.scratch.custom.yaml
```

Note:
```
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
```

<!-- https://wandb.ai/noham- -->

<!-- /Users/noham/Documents/GitHub/Stage/2024 -->
<!-- /Users/noham/Documents/GitHub/Stage-2024 -->

# Result :
10 iterations on MBP M2 : [logs](test3.log)

On wandb : https://wandb.ai/noham-/YOLOR/runs/

PDF : [pdf](run_dataset2fps.pdf)

Weights : [best.pt](../test/yolov7-tracker/runs/train/yolov7x-dataset2fps_202407189/weights/best.pt)