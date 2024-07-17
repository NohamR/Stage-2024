import numpy as np
import json, sys, os, shutil

## cliquer sur export dans Vott puis :

# prefix = "../exports_VOTT/CH01-20230614-083436-091514-Zone2/vott-json-export/"
# vottjson_filename = "Poulets-export.json"
# cc = 1000000

prefix = "./vott-json-export/"
vottjson_filename = "course-export.json"
cc = 1000000


with open(prefix+"/"+vottjson_filename, "r") as read_file:
    data = json.load(read_file)

for a in data["assets"]:
    asset = data["assets"][a]["asset"]
    regions = data["assets"][a]["regions"]
    img_name = asset["name"]
    width = asset["size"]["width"]
    height = asset["size"]["height"]
    print("\nimage name : ",img_name," width =",width," height =",height)
    shutil.copyfile(prefix+"/"+img_name,prefix+"/image_"+str(cc).zfill(12)+".jpg")
    f = open(prefix+"/image_"+str(cc).zfill(12)+".txt", "w")
    # f = open(prefix+"/"+img_name.replace(".jpg",".txt"), "w")
    for region in regions:
        boundingBox = region["boundingBox"]
        points = region["points"]
        print("    tags =",region["tags"]," boundingBox =",boundingBox," points =",points)
        # ## Labels :
        # D’après la doc on doit avoir :
        # Label_ID_1 X_CENTER_NORM Y_CENTER_NORM WIDTH_NORM HEIGHT_NORM
        # The label_id is the index number in the classes.names file. The id of the first label will be 0 and an increasing integer after that. Note all the position attributes in the label file are not absolute but normalised.
        # X_CENTER_NORM = X_CENTER_ABS/IMAGE_WIDTH   centre image
        # Y_CENTER_NORM = Y_CENTER_ABS/IMAGE_HEIGHT  centre image
        # WIDTH_NORM = WIDTH_OF_LABEL_ABS/IMAGE_WIDTH    largeur boite
        # HEIGHT_NORM = HEIGHT_OF_LABEL_ABS/IMAGE_HEIGHT hauteur boite
        # dans un repere dont l'origine est en haut a gauche et X de gauche à droite, Y du haut vers le bas
        Label_ID = "0" # 0 = poulet une seule classe ici
        X_CENTER_NORM = (boundingBox["left"]+boundingBox["width"]/2)/width
        Y_CENTER_NORM = (boundingBox["top"]+boundingBox["height"]/2)/height
        WIDTH_NORM = boundingBox["width"]/width
        HEIGHT_NORM = boundingBox["height"]/height
        f.write(Label_ID+" "+str(X_CENTER_NORM)+" "+str(Y_CENTER_NORM)+" "+str(WIDTH_NORM)+" "+str(HEIGHT_NORM)+"\n" ) # 0 = poulet si l'on a qu'une classe d'objet...
    f.close()
    cc += 1
    print("    written file :",prefix+"/"+img_name.replace(".jpg",".txt"))

