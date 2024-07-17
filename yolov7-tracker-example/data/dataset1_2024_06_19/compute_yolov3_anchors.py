import json
import os, sys
import math
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns; sns.set()  # for plot styling
from PIL import Image

# os.chdir("/media/deniz/02B89600B895F301/BBD100K")
# train_path = "data/labels/train/bdd100k_labels_images_train.json"
#
# with open(train_path,"r") as ftr:
#     trlabel = json.load(ftr)
#
# BBDlabeldict = {"bike":0,
#              "bus":1,
#              "car":2,
#              "motor":3,
#              "person":4,
#              "rider":5,
#              "traffic light":6,
#              "traffic sign":7,
#              "train":8,
#              "truck":9,
#              "drivable area":[],
#              "lane":[]}

# BBDlabeldict = {"bacterie":0}
# imgsize = 256
#
# images_path = "data/bacteries/images/train_and_test1"
# # images_path = "data/poulets/images/train_and_test1"

imgsize = int(input("Image size for train and run? "))
print("=> imgsize =",imgsize)
# imgsize = 256

BBDlabeldict = {"runner":0}

datasetpath = '/Users/noham/Documents/GitHub/Stage/2024/test/yolov7-tracker/data/dataset2fps/'
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

# sys.exit()
# for ind1 in range(len(trlabel)):
#     for ind2 in range(len(trlabel[ind1]["labels"])):
#         try:
#             a=trlabel[ind1]["labels"][ind2]["box2d"]   #traffic sign
#             x1,y1,x2,y2 = list(a.values())
#             width = abs(x1-x2)
#             height = abs(y1-y2)
#             w.append(width)
#             h.append(height)
#         except:
#             pass
# w=np.asarray(w)
# h=np.asarray(h)

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
plt.scatter(yolo_anchor_average[:, 0], yolo_anchor_average[:, 1], c='red', s=50);
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
plt.savefig("boites.png",dpi=150)
plt.show()

yoloV3anchors.sort(axis=0)
print("Your custom anchor boxes are {}".format(yoloV3anchors))

F = open(datasetpath+"YOLOV_BDD_Anchors_"+str(imgsize)+".txt", "w")
F.write("{}".format(yoloV3anchors))
F.close()
