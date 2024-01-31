import json
from pycocotools.coco import COCO
import matplotlib.pyplot as plt
import os
import skimage.io as io
from tqdm import tqdm

'''
    Code used to generate the annotated images with polygon masks for the annotation visualization
    (Figure 6 in the manuscript)
    
    ALL_DIR - change to path to directory containing all images
    OUT_DIR - change to path to directory where the annotated images will be output
    JSON_PATH - change to path to dataset COCO annotation json file
'''

ALL_DIR = ".\\Seaclear Marine Debris Dataset\\all"
OUT_DIR = "./ann_plots"
JSON_PATH = "./dataset.json" # COCO annotation file

coco = COCO(JSON_PATH)

domain_img_dict = {
    "BI-I": "432.jpg", # Bluerobotics HD
    "BI-II": "2443.jpg", # Paralenz
    "BI-III": "2021_09_16_16_15_03_Front_03-34-13.jpg", # SIP-E323CV
    ###########################
    "JA-I": "4313.jpg", # Bluerobotics HD
    "JA-II": "4588.jpg", # Paralenz
    ###########################
    "LO-I": "43.jpg", # Bluerobotics HD
    "LO-II": "4237.jpg", # Paralenz
    "LO-III": "2021_09_15_10_17_40_Front_fixed_twice_19-20-04.jpg", # SIP-E323CV
    ###########################
    "MS-I": "Cam1_16_26_03_10_11_2020.mp4_00076.jpg", # SIP-E323CV
    ###########################
    "SL-I": "194.jpg", # Bluerobotics HD
    "SL-II": "4554.jpg" # Paralenz
}

def get_image_ids(data_dict, img_dict):
    id_dict = {}
    for k,v in img_dict.items():
        for imgEntry in data_dict["images"]:
            if imgEntry["file_name"]==v:
                id_dict[k] = imgEntry["id"]
                break
    return id_dict

def get_anns_single_image(coco,image_id):
    ann_ids = coco.getAnnIds(imgIds=[image_id])
    anns = coco.loadAnns(ann_ids)
    return anns

def plot_ann(image_name,image_id,title_text=None):
    anns = get_anns_single_image(coco, image_id)
    cats = coco.loadCats(ids=list(range(1,41)))
    I = io.imread(image_name)
    plt.axis('off')
    plt.imshow(I)
    plt.title(k, fontname="Times New Roman",fontsize=18)
    coco.showAnnsLabel(anns,cats,label_polygons=True)
    plt.savefig(os.path.join("outputs","ann_plots",image_name),dpi=300)
    plt.clf()


with open(JSON_PATH) as fp:
    data_dict = json.load(fp)
    image_id_dict = get_image_ids(data_dict, domain_img_dict)
    for k,v in tqdm(image_id_dict.items()):
        image_name = domain_img_dict[k]
        image_id = image_id_dict[k]
        plot_ann(image_name,image_id,title_text=k)


