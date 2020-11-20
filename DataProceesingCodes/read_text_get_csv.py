
from os import walk
import os
import math
import json
from random import randrange
from PIL import Image, ImageTk
import csv


#FILE_NAME = "results/character_coherence_text_only.txt"
#FILE_NAME = "results/character_coherence_image_only.txt"
# Using readlines() 

# path_list = [
#     "results/random_text_cloze_text_only_easy.txt",    
#     "results/random_text_cloze_text_only_hard.txt",    
#     "results/random_text_cloze_image_only_easy.txt",    
#     "results/random_text_cloze_image_only_hard.txt",    
#     "results/random_text_cloze_image_text_easy.txt",    
#     "results/random_text_cloze_image_text_hard.txt",    
#     "results/random_visual_cloze_text_only_easy.txt",    
#     "results/random_visual_cloze_text_only_hard.txt",    
#     "results/random_visual_cloze_image_only_easy.txt",    
#     "results/random_visual_cloze_image_only_hard.txt",    
#     "results/random_visual_cloze_image_text_easy.txt",    
#     "results/random_visual_cloze_image_text_hard.txt"
#     # "results/random_character_coherence_text_only.txt",    
#     # "results/random_character_coherence_image_only.txt",    
#     # "results/random_character_coherence_image_text.txt" 
# ]
path_list = [
    #"results/ordered_text_cloze_text_only_hard.txt",    
    # "results/ordered_14_image_text_hard_1.txt",
    # "results/ordered_14_image_text_hard_2.txt",  
    # "results/ordered_14_image_text_hard_3.txt",  
    # "results/ordered_14_image_text_hard_4.txt",  
    #"results/ordered_11_text_text_hard_1.txt",      
    #"results/ordered_text_cloze_image_text_hard.txt",    
    # "results/ordered_visual_cloze_text_only_hard.txt",    
    # "results/ordered_visual_cloze_image_only_hard.txt",    
    # "results/ordered_visual_cloze_image_text_hard.txt"
    # "results/ordered_character_coherence_text_only.txt",    
    # "results/ordered_character_coherence_image_only.txt",    
    # "results/ordered_character_coherence_image_text.txt" 
    # "results/simple_both_image_hard.txt",
    # "results/simple_both_text_hard.txt",
    # "results/simple_image_image_hard.txt",
    # "results/simple_image_text_hard.txt",
    # "results/simple_text_image_hard.txt",
    # "results/style_comic_image_easy.txt",
    # "results/style_comic_image_hard.txt",
    # "results/style_mosaic_image_easy.txt",
    # "results/style_mosaic_image_hard.txt",
    # "results/style_tokyo_image_easy.txt",
    # "results/style_tokyo_image_hard.txt",
    # "results/style_udnie_image_easy.txt",
    # "results/style_udnie_image_hard.txt"
    # "manga_data_ordered/results/train_on_panels/panels_easy.txt",
    # "manga_data_ordered/results/train_on_panels/panels_hard.txt",
    # "manga_data_ordered/results/train_on_panels/pages_easy.txt",
    # "manga_data_ordered/results/train_on_panels/pages_hard.txt"
    # "manga_data_ordered/results/info_score/VGG_info_score_image_only_easy.txt",
    # "manga_data_ordered/results/info_score/VGG_info_score_image_only_hard.txt",
    # "manga_data_ordered/results/info_score/VGG_info_score_image_text_easy.txt",
    # "manga_data_ordered/results/info_score/VGG_info_score_image_text_hard.txt"   
    # "manga_data_ordered/results/info_score/VGG_info_score_text_only_text_easy.txt",
    # "manga_data_ordered/results/info_score/VGG_info_score_text_only_text_hard.txt",
    # "manga_data_ordered/results/info_score/VGG_info_score_image_text_text_easy.txt",
    # "manga_data_ordered/results/info_score/VGG_info_score_text_only_text_hard.txt",
    # "manga_data_ordered/results/layout_complexity/image_only_vis_easy.txt",
    # "manga_data_ordered/results/layout_complexity/image_only_vis_hard.txt",
    # "manga_data_ordered/results/layout_complexity/image_text_vis_easy.txt",
    # "manga_data_ordered/results/layout_complexity/image_text_vis_hard.txt",
    # "manga_data_ordered/results/layout_complexity/text_only_text_easy.txt",
    # "manga_data_ordered/results/layout_complexity/text_only_text_hard.txt",
    # "manga_data_ordered/results/layout_complexity/image_text_text_easy.txt",
    # "manga_data_ordered/results/layout_complexity/image_text_text_hard.txt",
    # "manga_data_ordered/results/panel_number/image_only_vis_easy.txt",
    # "manga_data_ordered/results/panel_number/image_only_vis_hard.txt",
    # "manga_data_ordered/results/panel_number/image_text_vis_easy.txt",
    # "manga_data_ordered/results/panel_number/image_text_vis_hard.txt",
    # "manga_data_ordered/results/panel_number/text_only_text_easy.txt",
    # "manga_data_ordered/results/panel_number/text_only_text_hard.txt",
    # "manga_data_ordered/results/panel_number/image_text_text_easy.txt",
    # # "manga_data_ordered/results/panel_number/image_text_text_hard.txt",
    # "manga_data_ordered/results/text_density/image_only_vis_easy.txt",
    # "manga_data_ordered/results/text_density/image_only_vis_hard.txt",
    # "manga_data_ordered/results/text_density/image_text_vis_easy.txt",
    # "manga_data_ordered/results/text_density/image_text_vis_hard.txt",
    # "manga_data_ordered/results/text_density/text_only_text_easy.txt",
    # "manga_data_ordered/results/text_density/text_only_text_hard.txt",
    # "manga_data_ordered/results/text_density/image_text_text_easy.txt",
    # "manga_data_ordered/results/text_density/image_text_text_hard.txt",

    # "manga_data_ordered/results/random/image_only_vis_hard.txt",
    # "manga_data_ordered/results/random/image_text_vis_hard.txt",
    "manga_data_ordered/results/random/text_only_text_hard.txt",
    "manga_data_ordered/results/random/image_text_text_hard.txt",


    # "manga_data_ordered/results/ordered/image_only_vis_hard.txt",
    # "manga_data_ordered/results/ordered/image_text_vis_hard.txt",
    # "manga_data_ordered/results/ordered/text_only_text_hard.txt",
    # "manga_data_ordered/results/ordered/image_text_text_hard.txt",


    # "manga_data_ordered/results/simple/image_only_vis_hard.txt",
    # "manga_data_ordered/results/simple/image_text_vis_hard.txt",
    # "manga_data_ordered/results/simple/text_only_text_hard.txt",
    # "manga_data_ordered/results/simple/image_text_text_hard.txt",

    # "manga_data_ordered/results/complex/image_only_vis_hard.txt",
    # "manga_data_ordered/results/complex/image_text_vis_hard.txt",
    # "manga_data_ordered/results/complex/text_only_text_hard.txt",
    # "manga_data_ordered/results/complex/image_text_text_hard.txt",


    # "manga_data_ordered/results/less/image_only_vis_hard.txt",
    # "manga_data_ordered/results/less/image_text_vis_hard.txt",
    # "manga_data_ordered/results/less/text_only_text_hard.txt",
    # "manga_data_ordered/results/less/image_text_text_hard.txt",

    # "manga_data_ordered/results/lot/image_only_vis_hard.txt",
    # "manga_data_ordered/results/lot/image_text_vis_hard.txt",
    # "manga_data_ordered/results/lot/text_only_text_hard.txt",
    # "manga_data_ordered/results/lot/image_text_text_hard.txt",

]
  




for path in path_list:

    file1 = open(path, 'r') 
    Lines = file1.readlines()     

    csv_name = path
    csv_name = csv_name.replace("txt","csv")

    # Strips the newline character 
    with open(csv_name, mode='w',encoding="utf-8",newline='') as csv_file:
        fieldnames = ['epoch', 'loss', 'dev',"test"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()    
        
        epoch_count = 0    
        count = 0 
        while count < len(Lines): 
            #print(Lines[0])
            #print("==========")
            #print("Line{}: {}".format(count, line.strip())) 
            loss = Lines[count]
            split_loss = loss.split(" ")
            loss = float(split_loss[-1])
            count = count +1
                
            dev_acc = Lines[count]
            dev_acc = dev_acc.replace(" accuracy","")
            split_dev = dev_acc.split(" ")
            dev_acc = float(split_dev[-1])
            count = count +1
            
            test_acc = Lines[count]
            test_acc = test_acc.replace(" accuracy","")
            split_test = test_acc.split(" ")
            test_acc = float(split_test[-1])#+ float(0.03)   
            count = count +1
            

            # print(loss)
            # print(dev_acc)
            # print(test_acc)
            # print("==============")

    

            writer.writerow({
                'epoch':epoch_count,
                'loss':loss,
                'dev':dev_acc,
                "test":test_acc
            })    
            
            epoch_count = epoch_count + 1
            
        csv_file.close()        