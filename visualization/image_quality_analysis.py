import pandas as pd
import seaborn as sns
import json
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.cm as cm
from mpl_toolkits.axisartist import SubplotZero
from scipy.spatial import ConvexHull
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import numpy as np

from scipy.stats import gaussian_kde as kde
from matplotlib.colors import Normalize
import matplotlib.colors as mcolors


def group_list(list_input, list_groups):
    outDict = {}
    for i in range(len(list_groups)):
        if list_groups[i] in outDict.keys():
            outDict[list_groups[i]].append(list_input[i])
        else:
            outDict[list_groups[i]] = [list_input[i]]
    return outDict

'''
    Code producing the figure plotting the source and fusion enhanced on the a-b plane in Lab color space.
    Images are saved in the domain_ab directory within the folder where the script is
    (Figure 5 in manuscript)
'''

def plot_lab_scatter_density(lab_values, lab_values_processed=None,val_key="mean"):
    domain_names = [
        "BI-I",
        "BI-II",
        "BI-III",
        "JA-I",
        "JA-II",
        "LO-I",
        "LO-II",
        "LO-III",
        "MS-I",
        "SL-I",
        "SL-II"
    ]

    mean_a_domain = group_list(lab_values[val_key+"_a"], lab_values["domain_labels"])
    mean_b_domain = group_list(lab_values[val_key+"_b"], lab_values["domain_labels"])
    if lab_values_processed:
        mean_a_domain_processed = group_list(lab_values_processed[val_key+"_a"], lab_values["domain_labels"])
        mean_b_domain_processed = group_list(lab_values_processed[val_key+"_b"], lab_values["domain_labels"])

    for k,v in mean_a_domain.items():
        mean_a_vals = v
        mean_b_vals = mean_b_domain[k]
        if lab_values_processed:
            mean_a_vals_processed = mean_a_domain_processed[k]
            mean_b_vals_processed = mean_b_domain_processed[k]
            a_array_processed = np.array(mean_a_vals_processed)
            b_array_processed = np.array(mean_b_vals_processed)
            samples_processed = np.stack([a_array_processed, b_array_processed])
            densObj_processed = kde(samples_processed)
            print(densObj_processed)


        a_array = np.array(mean_a_vals)
        b_array = np.array(mean_b_vals)
        samples_source = np.stack([a_array,b_array])
        densObj_source = kde(samples_source)

        def makeColours(vals, cmap):
            colours = np.zeros((len(vals), 3))
            norm = Normalize(vmin=vals.min(), vmax=vals.max())

            # Can put any colormap you like here.
            colours = [cm.ScalarMappable(norm=norm, cmap=cmap).to_rgba(val) for val in vals]

            return colours


        # FIGURE SIZE
        f = plt.gcf()
        f.set_size_inches(11.69/2, 8.27/2)
        ax = SubplotZero(f, 111)
        f.add_subplot(ax)
        # make arrows
        arr_a = ax.plot((1.0), (0.5), ls="", marker=">", ms=10, color="#545454",
                transform=ax.get_yaxis_transform(), clip_on=False)
        arr_b = ax.plot((0.5), (1.0), ls="", marker="^", ms=10, color="#545454",
                transform=ax.get_xaxis_transform(), clip_on=False)
        for direction in [ "right",  "top"]:
            # hides borders
            ax.axis[direction].set_visible(False)


        coloursSource = makeColours(densObj_source.evaluate(samples_source),cmap="winter")
        plt.axvline(0.5, linewidth=1.5, c="#545454", zorder=-1)
        plt.axhline(0.5, linewidth=1.5, c="#545454", zorder=-1)
        plt.grid(color="#aaaaaa", linewidth = 0.5,zorder=-2)
        #plt.title(domain_names[k], fontname="Times New Roman",fontsize=18)
        src_scat = ax.scatter(samples_source[0], samples_source[1], color=coloursSource, label="Source", alpha =0.7, edgecolors='black',linewidth=0.3)
        if lab_values_processed:
            coloursEnhc = makeColours(densObj_processed.evaluate(samples_processed),cmap="autumn")
            enc_scat = ax.scatter(samples_processed[0], samples_processed[1], color = coloursEnhc, label="Fusion Enhanced",alpha = 0.7 , edgecolors='black',linewidth=0.3)
        # combine them and build a new colormap
        colors1 = plt.cm.autumn_r(np.linspace(0,1,256,endpoint=False)+0.5/256)
        colors2 = plt.cm.winter(np.linspace(0,1,256,endpoint=False)+0.5/256)
        mycolors = np.vstack((colors1,colors2))
        mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', mycolors)
        cbar = f.colorbar(cm.ScalarMappable(cmap=mymap))
        cbar.set_ticks([0,0.5,1])
        cbar.set_ticklabels(['1', '0', '1'])
        plt.legend(bbox_to_anchor=(0.5, 1.17))

        # Plot axis text
        x_left, x_right = ax.get_xlim()
        y_low, y_high = ax.get_ylim()
        tck_x = plt.xticks()[0]
        print(tck_x)
        tck_y = plt.yticks()[0]
        tck_diff_x  = abs(tck_x[1] - tck_x[0])
        tck_diff_y = abs(tck_y[1] - tck_y[0])
        offset_a = 1/3
        a_y = 0.5-(abs(0.5-y_low)*0.1)
        x_len = x_right-x_left
        y_len = y_high-y_low
        plt.text(x_right-1/10*tck_diff_x, 0.5-1/15*y_len, "+a", fontweight="bold", fontsize="large")  # +a label (x axis)
        plt.text(0.5-1/10*x_len, y_high-1/10*tck_diff_y, "+b", fontweight="bold", fontsize="large")  # +b label (y axis)

        #plt.show()
        plt.savefig("./outputs/domains_ab/" + str(k) + ".png", dpi=300)
        plt.clf()

def load_domain_labels(json_file):
    with open(json_file,"r") as fp:
        labelsJsonDict = json.load(fp)
    return labelsJsonDict


def load_lab_values(json_file):
    lab_values = {
        "mean_a": [],
        "median_a": [],
        "var_a": [],
        "mean_b": [],
        "median_b": [],
        "var_b": [],
        "domain_labels": []
    }
    domainDict = load_domain_labels("./data/domain_labels_site_sensor_fix.json")
    with open(json_file,"r") as fp:
        labJsonDict = json.load(fp)
        for k,v in labJsonDict.items():
            if ".jpg" in k:
                lab_values["domain_labels"].append(domainDict[k])
                for lab_key, lab_val in v.items():
                    lab_values[lab_key].append(lab_val)
    return lab_values

def load_quality_values(json_file):
    quality_values = {
        "UW_INDEX": [],
        "UIQM": [],
        "domain_labels": []
    }
    domainDict = load_domain_labels("./data/domain_labels_site_sensor_fix.json")
    with open(json_file,"r") as fp:
        qualityJsonDict = json.load(fp)
        for k,v in qualityJsonDict.items():
            if ".jpg" in k:
                quality_values["domain_labels"].append(domainDict[k])
                for qual_key, qual_val in v.items():
                    quality_values[qual_key].append(qual_val)
    return quality_values

def load_uiqm_csv(csv_file):
    uiqm_values = {
        "UIQM": [],
        "domain_labels": []
    }
    domainDict = load_domain_labels("./data/domain_labels_site_sensor_fix.json")
    df_uiqm = pd.read_csv(csv_file,sep=";")
    for index,row in df_uiqm.iterrows():
        uiqm_values["UIQM"].append(row["uiqm"])
        uiqm_values["domain_labels"].append(domainDict[row["file_name"]])
    return uiqm_values

from statistics import mean
import collections
def get_stats(domain_vals_dict,text_separator):
    print("BEGIN "+text_separator)
    domain_vals_dict = collections.OrderedDict(sorted(domain_vals_dict.items()))
    for k,v in domain_vals_dict.items():
        print(str(k)+" "+str(len(v))," = ",round(mean(v),3))
    print("END " + text_separator)



if __name__=="__main__":
    json_file = "./data/quality_out.json"
    json_file_processed = "./data/quality_out_processed.json"
    json_file_lab = "./data/lab_out.json"
    json_file_processed_lab = "./data/lab_out_processed.json"
    uiqm_values = load_uiqm_csv("./data/uiqm_normal.csv")
    uiqm_values_processed = load_uiqm_csv("./data/uiqm_processed.csv")
    quality_values = load_quality_values(json_file)
    quality_values_processed = load_quality_values(json_file_processed)
    lab_values = load_lab_values(json_file_lab)
    lab_values_processed = load_lab_values(json_file_processed_lab)

    plot_lab_scatter_density(lab_values,lab_values_processed) # Creates images for figure 5

    # Calculate and print stats (UIQM and UW Index) for each domains
    uw_index_dict = group_list(quality_values["UW_INDEX"],quality_values["domain_labels"])
    get_stats(uw_index_dict,"UW INDEX SOURCE")
    uiqm_dict = group_list(quality_values["UIQM"],quality_values["domain_labels"])
    get_stats(uiqm_dict,"UIQM SOURCE")
    uw_index_processed_dict = group_list(quality_values_processed["UW_INDEX"],quality_values_processed["domain_labels"])
    get_stats(uw_index_processed_dict,"UW INDEX FUSION")
    uiqm_processed_dict = group_list(quality_values_processed["UIQM"],quality_values_processed["domain_labels"])
    get_stats(uiqm_processed_dict,"UIQM FUSION")

