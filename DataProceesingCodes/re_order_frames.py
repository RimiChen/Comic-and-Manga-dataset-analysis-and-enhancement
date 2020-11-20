from os import walk
import os
import math
import json
from random import randrange
from PIL import Image, ImageTk
import ComicBook_fun as COMIC_PRE

layout_layer_number = 6
transition_total_count = {}
transition_total_count["Total"] = 0
transition_total_count["Aspect"] = 0
transition_total_count["Scene"] = 0
transition_total_count["Subject"] = 0
transition_total_count["Action"] = 0
transition_total_count["Moment"] = 0
transition_total_count["Non"] = 0
transition_total_count["Other"] = 0
transition_count = {}

text_pro = {}
text_sum = {}
bound_line = 1.5
#text_sum["line"] = 1.5

def find_frame(target, frame_list):
    
    target_frame = frame_list[0]
    
    for frame in frame_list:
        if target == frame["id"]:
            target_frame = frame
    
    return target_frame
    
def parse_reading_order(reading_order_path, frame_annotation_path, book_index):
    print("==========================================")
    print(reading_order_path)
    print(frame_annotation_path)
    
    book_name_string = reading_order_path.split("/")
    last_file_name = book_name_string[-1].replace("_order.json", "") 
    
    if last_file_name not in transition_count:
        transition_count[last_file_name] = {}
        transition_count[last_file_name]["Total"] = 0
        transition_count[last_file_name]["Aspect"] = 0
        transition_count[last_file_name]["Action"] = 0
        transition_count[last_file_name]["Subject"] = 0
        transition_count[last_file_name]["Moment"] = 0
        transition_count[last_file_name]["Scene"] = 0
        transition_count[last_file_name]["Non"] = 0
        transition_count[last_file_name]["Other"] = 0
    
    reading_order_dict = {}
    with open(reading_order_path) as json_file:
    
        order_annotation = json.load(json_file)
        order_pages = order_annotation["pages"]
        reading_order_dict = order_pages
        # for key in order_pages:
        #     print(key)
        #print(type(order_annotation["pages"]))
        json_file.close()
        # print(order_pages )
        
    new_page_list = []
    with open(frame_annotation_path) as json_file:
        page_list = json.load(json_file)
        print(len(page_list))
    
        for page in page_list:
            # print(page)
            index = page["index"]
            
            if index == page_list[-1]["index"]:
                print(index)
            new_page = page
            

            layout = {}
            transitions = []
            for layer in range(layout_layer_number):
                layout[str(layer)] = []

            if str(index) in reading_order_dict:
                #print("page: "+str(index))
                reading_order = reading_order_dict[str(index)]["reading_order"]
                layout = reading_order_dict[str(index)]["layout"]
                transitions = reading_order_dict[str(index)]["transitions"]
                
                if len(transitions) > 0:
                    ## annotation exist
                    transition_total_count["Total"]  = transition_total_count["Total"] + len(transitions)
                    transition_count[last_file_name]["Total"] = transition_count[last_file_name]["Total"] + len(transitions)
                    for transition_anno in transitions:
                # "Action",
                # "Aspect",
                # "Non_sequitur",
                # "Other"
                # "Scene",
                # "Subject",
                # "Moment",

                        if transition_anno == "Action":
                            transition_total_count["Action"] = transition_total_count["Action"] + 1
                            transition_count[last_file_name]["Action"] = transition_count[last_file_name]["Action"] +1
                        elif transition_anno == "Aspect":
                            transition_total_count["Aspect"] = transition_total_count["Aspect"] + 1
                            transition_count[last_file_name]["Aspect"] = transition_count[last_file_name]["Aspect"] +1
                        elif transition_anno == "Moment":
                            transition_total_count["Moment"] = transition_total_count["Moment"] + 1
                            transition_count[last_file_name]["Moment"] = transition_count[last_file_name]["Moment"] +1                            
                        elif transition_anno == "Other":
                            transition_total_count["Other"] = transition_total_count["Other"] + 1
                            transition_count[last_file_name]["Other"] = transition_count[last_file_name]["Other"] +1                            
                        elif transition_anno == "Scene":
                            transition_total_count["Scene"] = transition_total_count["Scene"] + 1
                            transition_count[last_file_name]["Scene"] = transition_count[last_file_name]["Scene"] +1
                            
                        elif transition_anno == "Subject":
                            transition_total_count["Subject"] = transition_total_count["Subject"] + 1
                            transition_count[last_file_name]["Subject"] = transition_count[last_file_name]["Subject"] +1                            
                        elif transition_anno == "Non_sequitur":
                            transition_total_count["Non"] = transition_total_count["Non"] + 1
                            transition_count[last_file_name]["Non"] = transition_count[last_file_name]["Non"] +1
                            
                                                                                    
                frame_list = new_page["frames"]
                # print(len(frame_list))
                ordered_frame = []
                if len(reading_order) > 0 and len(frame_list) > 0:
                    # print("reorder")
                    for frame_id in reading_order:
                        next_frame = find_frame(frame_id, frame_list)
                        ordered_frame.append(next_frame)
                        
                new_page["frames"] = ordered_frame
            
            #else:
                #new_page["frames"] = ordered_frame
            new_page["layout"] = layout
            new_page["transitions"] = transitions
            new_page_list.append(new_page)
            
            if len(new_page["frames"]) > 0:
                if book_index in text_pro:
                    text_pro[book_index].append(len(new_page["texts"])/len(new_page["frames"]))
                else:
                    text_pro[book_index] =  []
                    text_pro[book_index].append(len(new_page["texts"])/len(new_page["frames"]))
                    
            
            
        
        json_file.close()
    
    json_file = open("ordered_frame/"+str(book_index)+"_ordered_pages.json", "w")
    # magic happens here to make it pretty-printed
    print("saved = "+str(len(new_page_list)))
    json_file.write(json.dumps( new_page_list, indent=4))
    json_file.close()
    
    
    if book_index in text_sum and  book_index in text_pro:
        text_sum[book_index] = sum(text_pro[book_index])/len(text_pro[book_index])
    else:
        text_sum[book_index] = sum(text_pro[book_index])/len(text_pro[book_index])
        
    
if __name__ == "__main__":
    print("LOAD reading order annotation, and modify frame annotation")
    

    reading_order_path_list= []
    frame_annotation_path_list= []

    root_reading_order = "reading_order_annotation/"
    for (_, _, filenames) in walk( "reading_order_annotation/"):
        #print(filenames)
        for file_path in filenames:
            #print(file_path)
            book_index = file_path.replace("_order.json", "") 
            book_index = book_index.replace("reading_order_annotation/","")
            frame_path = "split_annotation/"+book_index +"_split_pages.json"
            #print(root_reading_order+file_path)
            reading_order_path_list.append(root_reading_order+file_path)
            frame_annotation_path_list.append(frame_path)
            #break
 
 
 
    
    # print(reading_order_path_list)
    # print(frame_annotation_path_list)
    
    #reading_order_path = "reading_order_annotation/0_order.json"
    #frame_annotation_path = "split_annotation/0_split_pages.json"
    count = 0
    
    stop_book = 11
    for path in reading_order_path_list:
        reading_order_path = path
        frame_annotation_path = frame_annotation_path_list[count]
        #if count < stop_book:
        book_index_string = reading_order_path.split("/")
        book_index = book_index_string[-1].replace("_order.json","")
            #print(reading_order_path)
        parse_reading_order(reading_order_path, frame_annotation_path, int(book_index))
        count = count + 1
    

 
    json_file = open("total_transitions.json", "w")
    # magic happens here to make it pretty-printed
    json_file.write(json.dumps(transition_total_count, indent=4))
    json_file.close()         
    
    json_file = open("separate_transitions.json", "w")
    # magic happens here to make it pretty-printed
    json_file.write(json.dumps(transition_count, indent=4))
    json_file.close()
    
    
    json_file = open("text_propotion.json", "w")
    # magic happens here to make it pretty-printed
    json_file.write(json.dumps(text_pro, indent=4))
    json_file.close()      


    text_more = []
    text_less = []
    for item in text_sum:
        #print(item)
        if text_sum[item] > bound_line:
            text_more.append(item)
        else:
            text_less.append(item)
    
    text_category = {}
    text_category["more"] = text_more
    text_category["less"] = text_less
    
    json_file = open("text_sum.json", "w")
    # magic happens here to make it pretty-printed
    json_file.write(json.dumps(text_sum, indent=4))
    json_file.close()
    
    
    json_file = open("text_cat.json", "w")
    # magic happens here to make it pretty-printed
    json_file.write(json.dumps(text_category, indent=4))
    json_file.close()                              