from os import walk
import os
import math
import json
from random import randrange
from PIL import Image, ImageTk
import csv


JSON_PATH = [
    "data/annotations/0_pages.json",
    "data/annotations/1_pages.json",
    "data/annotations/2_pages.json"
]

### for each page
global frameValueIndex
frameValueIndex = {}
# [id] = count_index
global textValueIndex
textValueIndex = {}
# [id] = count_index
global frameList
frameList = []

global csv_list
csv_list = []



    
def get_name(prefix, postfix, split, path):
    name = path
    name = name.replace(prefix, "")
    name = name.replace(postfix, "")
    
    split_string = name.split(split)
    length = len(split_string)
    
    final_name = split_string[length -1] 
    
    print("from "+path+" get "+final_name)
    
    return final_name


def get_OCR_csv(path):
    print("SYSTEM: get OCR csv.")
    global csv_list
    global frameValueIndex
    # [id] = count_index
    global textValueIndex
    # [id] = count_index
    global frameList
    ### assume textboxes are in frames

    ##  load _pages.json
    ## use position as key
    page_list = load_manga_109_annotations(path)
    book_index = get_name("", "_ordered_pages.json", "/", path)
    
    
    
    page_count = 0
    for page in page_list:
            frame_dict = {}
            
            frameValueIndex = {}        
            textValueIndex = {}
            frameList = []
            #page_index = int(page["index"]) -2
            # page_index = page["index"]
            page_index = page_count
            
            panel_count = 0
            for panel in page["frames"]:
                frameValueIndex[panel["id"]] = panel_count
                frameList.append(panel)
                panel_count = panel_count + 1                
            

            for text in page["texts"]:
                text_id = text["id"]
                text_minx = text["xmin"]
                text_maxx = text["xmax"]
                text_miny = text["ymin"]
                text_maxy = text["ymax"]

                center_x, center_y =  getCenter(text_minx, text_miny, text_maxx, text_maxy)           

                
                panel_index = inRange(center_x, center_y)
                
                if panel_index in frame_dict:
                    frame_dict[panel_index].append(text)

                else:
                    frame_dict[panel_index] = []
                    frame_dict[panel_index].append(text)
                    

                text_index = len(frame_dict[panel_index]) -1
                textValueIndex[text_id] = text_index
                
    
            for panel_index in frame_dict:
                #### frame_dict[] = text list
                #frame_dict[panel_index]
                
                for text in frame_dict[panel_index]:
                    # print("========================================================")
                    # print("book_id = "+ book_index+", page_index = "+ page_index)
                    # print("dialog_or_narration = "+str(len(frame_dict[panel_index])))
                    # text_index = textValueIndex[text["id"]]
                    # print("panel_index = "+ str(panel_index)+", text_index = "+ str(text_index))
                    # print("text = "+text["text"])
                    # print("minx = "+text["xmin"]+", maxx = "+text["xmax"])
                    # print("miny = "+text["ymin"]+", maxy = "+text["ymax"])
                    new_csv_node = {}
                    new_csv_node["comic_no"] = book_index
                    new_csv_node["page_no"] = page_index
                    new_csv_node["panel_no"] = panel_index
                    new_csv_node["textbox_no"] = textValueIndex[text["id"]]
                    new_csv_node["dialog_or_narration"] = len(frame_dict[panel_index])
                    new_csv_node["text"] = text["text"]
                    new_csv_node["x1"] = text["xmin"]
                    new_csv_node["y1"] = text["ymin"]
                    new_csv_node["x2"] = text["xmax"]
                    new_csv_node["y2"] = text["ymax"]
                    
                    csv_list.append(new_csv_node)
               
                # print("========================================================")
                
    
            #### because when crop, we omit pages with no frames
            if len(page["frames"]) >0:
                page_count = page_count +1
    
def getCenter(minX, minY, maxX, maxY):
    newX = (int(minX) + int(maxX))/2
    newY = (int(minY) + int(maxY))/2
    
    return newX, newY
    
def inRange(center_x, center_y):
    global frameValueIndex
    # [id] = count_index
    global textValueIndex
    # [id] = count_index
    global frameList
    
    index = 0
    
    for frame in frameList:
        if center_x > int(frame["xmin"]) and center_x <int(frame["xmax"]):
            if center_y > int(frame["ymin"]) and center_y <int(frame["ymax"]):
                #print(frame["id"])
                
                index = frameValueIndex[frame["id"]]
    
    return index
    
    
    
    
def load_manga_109_annotations(json_path):
    print("load_manga_109_annotations")
    annotations = []
    book_dictionary = {}
    
    
    #json_file = open(json_path, "r")
    with open(json_path) as json_file:
    
        annotations = json.load(json_file)
        
    return annotations    

if __name__ == "__main__":
    
    
    json_path_array = []
    
    #root_directory = "ordered_frame/"
    #root_directory = "more_text/"
    #root_directory = "less_text/"
    #root_directory = "panel_complex/"
    root_directory = "panel_simple/"

    for x in os.walk(root_directory):
        #if len(x[0])<1:
        #    print("SYSTEM: empty folder name!")
        #else:
        #print(x[0]+", "+str(len(x[0])))
        # if x[0].index(".json") > 0:
        target_list = x[2]
        for file_path in target_list:
            json_path_array.append(root_directory+file_path)  
        
    print("\n".join(json_path_array))
    
    
    for json_path in json_path_array:
        get_OCR_csv(json_path)
    
    # for json_path in JSON_PATH:
    #     get_OCR_csv(json_path)
    
    with open('OCR.csv', mode='w',encoding="utf-8",newline='') as csv_file:
                    # new_csv_node["comic_no"] = book_index
                    # new_csv_node["page_no"] = page_index
                    # new_csv_node["panel_no"] = panel_index
                    # new_csv_node["textbox_no"] = text_index
                    # new_csv_node["dialog_or_narration"] = len(frame_dict[panel_index])
                    # new_csv_node["text"] = text["text"]
                    # new_csv_node["x1"] = text["xmin"]
                    # new_csv_node["y1"] = text["ymin"]
                    # new_csv_node["x2"] = text["xmax"]
                    # new_csv_node["y2"] = text["ymax"]

        fieldnames = ['comic_no', 'page_no', 'panel_no',"textbox_no",  "dialog_or_narration", "text", "x1",  "y1", "x2", "y2"]       
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
            
        for csv_tuple in csv_list:

            writer.writerow({
                'comic_no':csv_tuple['comic_no'],
                'page_no':csv_tuple['page_no'],
                'panel_no':csv_tuple['panel_no'],
                "textbox_no":csv_tuple['textbox_no'],
                "dialog_or_narration":csv_tuple["dialog_or_narration"],
                "text":csv_tuple["text"],
                "x1":csv_tuple["x1"],
                "y1":csv_tuple["y1"],
                "x2":csv_tuple["x2"],
                "y2":csv_tuple["y2"]})
            #print(json.dumps(csv_tuple, indent = 4))

        #print("total = "+str(len(csv_list)))