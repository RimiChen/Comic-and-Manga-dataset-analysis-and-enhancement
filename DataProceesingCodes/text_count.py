from os import walk
import os
import math
import json
from random import randrange
from PIL import Image, ImageTk
import ComicBook_fun as COMIC_PRE


root_reading_order = "split_annotation/"

reading_order_path_list = []

text_pro = {}
text_sum = {}
if __name__ == "__main__":
    for (_, _, filenames) in walk( root_reading_order):
        #print(filenames)
        for file_path in filenames:
            #print(file_path)
            #print(root_reading_order+file_path)
            reading_order_path_list.append(root_reading_order+file_path)
            #break

    for path in reading_order_path_list:
        print(path)
        book_index = path.replace("_split_pages.json", "") 
        book_index = book_index.replace(root_reading_order,"")

        with open(path) as json_file:
            
            order_annotation = json.load(json_file)
            #print(type(order_annotation))
            for new_page in order_annotation:
                if len(new_page["frames"]) > 0:
                    if book_index in text_pro:
                        text_pro[book_index].append(len(new_page["texts"])/len(new_page["frames"]))
                    else:
                        text_pro[book_index] =  []
                        text_pro[book_index].append(len(new_page["texts"])/len(new_page["frames"]))        
                
            json_file.close()

        
        text_sum[book_index] = sum(text_pro[book_index])/len(text_pro[book_index])



    json_file = open("new_text_propotion.json", "w")
    # magic happens here to make it pretty-printed
    json_file.write(json.dumps(text_pro, indent=4))
    json_file.close()      


    text_more = []
    text_less = []
    
    sum_number = 0
    for item in text_sum:
        sum_number = sum_number + text_sum[item]
    
    bound_line = sum_number/ len(text_sum)
    
    print("average bound line = " +str(bound_line))
    
    for item in text_sum:
        #print(item)
        if text_sum[item] > bound_line:
            text_more.append(item)
        else:
            text_less.append(item)
            



    text_category = {}
    text_category["more"] = text_more
    text_category["less"] = text_less

    json_file = open("new_text_sum.json", "w")
    # magic happens here to make it pretty-printed
    json_file.write(json.dumps(text_sum, indent=4))
    json_file.close()


    json_file = open("new_text_cat.json", "w")
    # magic happens here to make it pretty-printed
    json_file.write(json.dumps(text_category, indent=4))
    json_file.close()       