import json
import os, sys
import math
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns; sns.set()  # for plot styling
from PIL import Image

imgsize = int(input("Image size for train and run? "))
print("=> imgsize =",imgsize)
# imgsize = 256

BBDlabeldict = {"runner":0}

datasetpath = '/Users/noham/Documents/GitHub/Stage-2024/yolov7-setup/v2/datasetv2/'
images_path = datasetpath+"images"
labels_path = datasetpath+"labels"

filenames = sorted(os.listdir(images_path))
print("Nb d'images =",len(filenames))
w,h = [] , []
for i,file in enumerate(filenames):
    #print(file)
    try:
        # if True:
        im = Image.open(images_path+"/"+file)
        img_width = im.width
        img_height = im.height
        #print(img_width,img_height)
        fo = open(images_path.replace("images","labels")+"/"+file.replace("jpg","txt"), "r+")
        lines = fo.readlines()
        for line in lines:
            a = np.array(line.split(" ")).astype(float)
            w.append(a[3]*img_width)
            h.append(a[4]*img_height)
            if (a[3]*img_height<0.001) or (a[4]*img_height<0.001):
                print("!! ATTENTION : boite trop petite dans le fichier ",file, "=> il faut vérifier et supprimer la ligne dans le fichier label au format txt !!")
    except:
        pass
w=np.asarray(w)#+0.001*(np.random.random((len(w),)) - 0.5)
h=np.asarray(h)#+0.001*(np.random.random((len(w),)) - 0.5)
print("h => min =",h.min()," max =",h.max())
print("w => min =",w.min()," max =",h.max())
print("Nb objets entourés =",len(h))

x=[w,h]
x=np.asarray(x)
x=x.transpose()
##########################################   K- Means
##########################################

from sklearn.cluster import KMeans
kmeans3 = KMeans(n_clusters=9)
kmeans3.fit(x)
y_kmeans3 = kmeans3.predict(x)

##########################################
centers3 = kmeans3.cluster_centers_

yolo_anchor_average=[]
for ind in range (9):
    yolo_anchor_average.append(np.mean(x[y_kmeans3==ind],axis=0))

yolo_anchor_average=np.array(yolo_anchor_average)

plt.scatter(x[:, 0], x[:, 1], c=y_kmeans3, s=2, cmap='viridis')
plt.scatter(yolo_anchor_average[:, 0], yolo_anchor_average[:, 1], c='red', s=50)
yoloV3anchors = yolo_anchor_average
yoloV3anchors[:, 0] =yolo_anchor_average[:, 0] /1920 *imgsize
yoloV3anchors[:, 1] =yolo_anchor_average[:, 1] /1056 *imgsize
yoloV3anchors = np.rint(yoloV3anchors)
fig, ax = plt.subplots()
for ind in range(9):
    rectangle= plt.Rectangle((0.5*imgsize-yoloV3anchors[ind,0]/2,0.5*imgsize-yoloV3anchors[ind,1]/2), yoloV3anchors[ind,0],yoloV3anchors[ind,1] , fc='b',edgecolor='b',fill = None)
    ax.add_patch(rectangle)
ax.set_aspect(1.0)
plt.axis([0,imgsize,0,imgsize])
plt.savefig(datasetpath+"boites.png",dpi=150)
plt.show()

yoloV3anchors.sort(axis=0)
print("Your custom anchor boxes are {}".format(yoloV3anchors))

F = open(datasetpath+"YOLOV_BDD_Anchors_"+str(imgsize)+".txt", "w")
F.write("{}".format(yoloV3anchors))
F.close()

print("Anchors box for yaml file :")
s_anchors = yoloV3anchors[yoloV3anchors[:, 0].argsort()]
anchor_lists = [s_anchors[i:i+3].tolist() for i in range(0, len(s_anchors), 3)]
# anchor_lists = [[[14.0, 37.0], [15.0, 48.0], [19.0, 53.0]], [[21.0, 70.0], [24.0, 88.0], [31.0, 112.0]], [[34.0, 136.0], [35.0, 155.0], [76.0, 161.0]]]
p = [']  # P3/8', ']  # P4/16', ']  # P5/32']
out = "anchors:"
for l in anchor_lists:
    out += '\n' + "  - [" + ", ".join([f"{int(i[0])},{int(i[1])}" for i in l]) + p[anchor_lists.index(l)]
print(out)