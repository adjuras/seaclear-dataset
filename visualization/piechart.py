import json
import os
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

'''
    Creates a pie chart showing the proportions of annotated objects belonging to specific debris material, robot, animal and bio categories.
    (Figure 3 in the manuscript)
'''

group_dict = {
    'can_metal': 'metal',
    'tarp_plastic': 'plastic',
    'container_plastic': 'plastic',
    'bottle_plastic': 'plastic',
    'tube_cement': 'other_debris',
    'plant': 'plant',
    'container_middle_size_metal': 'metal',
    'animal_etc': 'animal',
    'animal_sponge': 'animal',
    'bottle_glass': 'glass',
    'wreckage_metal': 'metal',
    'unknown_instance': 'other_debris',
    'pipe_plastic': 'plastic',
    'net_plastic': 'plastic',
    'animal_shells': 'animal',
    'rope_fiber': 'fiber',
    'animal_urchin': 'animal',
    'cup_plastic': 'plastic',
    'brick_clay': 'other_debris',
    'bag_plastic': 'plastic',
    'sanitaries_plastic': 'plastic',
    'clothing_fiber': 'fiber',
    'cup_ceramic': 'other_debris',
    'boot_rubber': 'rubber',
    'tire_rubber': 'rubber',
    'jar_glass': 'glass',
    'rov_cable': 'robot',
    'rov_tortuga': 'robot',
    'branch_wood': 'other_debris',
    'furniture_wood': 'other_debris',
    'snack_wrapper_plastic': 'plastic',
    'lid_plastic': 'plastic',
    'cardboard_paper': 'other_debris',
    'rope_plastic': 'plastic',
    'cable_metal': 'metal',
    'animal_fish': 'animal',
    'snack_wrapper_paper': 'other_debris',
    'rov_vehicle_leg': 'robot',
    'rov_bluerov': 'robot',
    'animal_starfish': 'animal'
}

cat_distribution = {'can_metal': 1130, 'tarp_plastic': 31, 'container_plastic': 84, 'bottle_plastic': 1261, 'tube_cement': 1404, 'plant': 472,
 'container_middle_size_metal': 60, 'animal_etc': 3749, 'animal_sponge': 1110, 'bottle_glass': 2331, 'wreckage_metal': 265,
 'unknown_instance': 1195, 'pipe_plastic': 155, 'net_plastic': 960, 'animal_shells': 995, 'rope_fiber': 2039, 'animal_urchin': 6462,
 'cup_plastic': 329, 'brick_clay': 606, 'bag_plastic': 882, 'sanitaries_plastic': 55, 'clothing_fiber': 298, 'cup_ceramic': 123,
 'boot_rubber': 161, 'tire_rubber': 2556, 'jar_glass': 62, 'rov_cable': 389, 'rov_tortuga': 55, 'branch_wood': 430, 'furniture_wood': 15,
 'snack_wrapper_plastic': 172, 'lid_plastic': 20, 'cardboard_paper': 13, 'rope_plastic': 8, 'cable_metal': 149, 'animal_fish': 985,
 'snack_wrapper_paper': 8, 'rov_vehicle_leg': 461, 'rov_bluerov': 58, 'animal_starfish': 17}


def super_category_distribution(cat_dist, group_dict):
    super_dist = {}
    
    for k,v in cat_dist.items():
        super_cat = group_dict[k]
        super_cat = super_cat.replace("_"," ")
        super_cat = super_cat.capitalize()
        if super_cat in super_dist.keys():
            super_dist[super_cat] += cat_dist[k]
        else:
            super_dist[super_cat] = 0  
            super_dist[super_cat] += cat_dist[k]
    return super_dist

    

super_dist = super_category_distribution(cat_distribution,group_dict)
print(super_dist)
overall_num = sum(super_dist.values())
print("Overall number of anns: ", sum(super_dist.values()))
df = pd.DataFrame(list(super_dist.items()),columns = ["category", "value"])
#fig = px.pie(df, values='value', names='category', title='Trash distribution per categories')
fig = go.Figure(data=[go.Pie(labels=list(super_dist.keys()), values=list(super_dist.values()), pull=[0.1, 0.1, 0.1, 0, 0, 0.1, 0.1, 0.1, 0])])
fig.update_traces(hoverinfo = None, textinfo='label+value', textfont_size=24,insidetextfont=dict(color="#FFFFFF"),
                  marker=dict(colors=["#636363","#e85742","#00cc96","#ffed6f","#636efa","#9467bd","#eb70c6","#1f77b4","#9dd560"],line=dict(color='#000000', width=2)))
fig.update_layout(uniformtext_minsize=36, uniformtext_mode='hide', margin=dict( l = 50, r = 50, b = 100, t = 200), legend = dict(font = dict(size = 32, color = "black"), itemsizing='constant'), legend_x=0.8, title_x= 0.5, title=dict(text=f"Proportions of debris materials in <br> total no. annotations ({overall_num})", font=dict(size=50)))
fig.show()