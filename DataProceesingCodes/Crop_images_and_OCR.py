# Improting Image class from PIL module 
from os import walk
import os
import os.path
from os import path
import math
import json
from random import randrange
from PIL import Image, ImageTk


MANGA_IMAGE_PATH = "two_pages/"
MANGA_ANNOTATION_PATH = "ordered_frame/"
# MANGA_IMAGE_PATH = "manga_images/AisazuNihaIrarenai/"
# MANGA_ANNOTATION_PATH = "annotation_data/AisazuNihaIrarenai/"
# MANGA_IMAGE_PATH = "manga_images/Saisoku/"
# MANGA_ANNOTATION_PATH = "annotation_data/Saisoku/"

def crop_image(image_obj, min_x, min_y, max_x, max_y):
    
    # Opens a image in RGB mode 
    #im = Image.open(r"C:\Users\Admin\Pictures\geeks.png") 
    im = image_obj
    
    # Size of the image in pixels (size of orginal image) 
    # (This is not mandatory) 
    width, height = im.size 
    
    # Setting the points for cropped image 
    left = min_x
    top = min_y
    right = max_x
    bottom = max_y
    
    # Cropped image of above dimension 
    # (It will not change orginal image) 
    im_crop = im.crop((left, top, right, bottom)) 
    
    # Shows the image in image viewer 
    #im_crop.show()
    
    return im_crop
 
def loadManga(bookPath):
    #### from the path, load all image file names and make the path as a list
    print("SYSTEM: load magna {"+str(bookPath)+"}")
    

    filePathList = []
    for (_, _, filenames) in walk(bookPath):
        filePathList.extend(filenames)
        break
    
    # print("\n".join(filePathList))

    return filePathList

def load_manga_109_annotations(json_path):
    #print("load_manga_109_annotations")
    annotations = []
    book_dictionary = {}
    
    
    #json_file = open(json_path, "r")
    with open(json_path) as json_file:
    
        annotations = json.load(json_file)
        
        json_file.close()
        
    count = 0
    for annotation in annotations:
        
        book_dictionary[count] = annotation
        # print(annotation)
        count = count + 1
        
    return book_dictionary
    
def get_book_name(path_string):
    name_string_array = path_string.split("/")
    string_lenth = len(name_string_array)
    
    book_name_index = (string_lenth -1)-1
    
    book_name = name_string_array[book_name_index]
    return book_name


# def get_OCR_file(book_annotation):
        
if __name__ == "__main__":
    # book_path_list = [
    #     "manga_images/YumeiroCooking/",
    #     "manga_images/Saisoku/",
    #     "manga_images/AisazuNihaIrarenai/"
    # ]
    
    book_path_list = []
    root_directory = "two_pages/"
    for x in os.walk(root_directory):
        #if len(x[0])<1:
        #    print("SYSTEM: empty folder name!")
        #else:
        #print(x[0]+", "+str(len(x[0])))
        book_path_list.append(x[0]+"/")      
    
    ### 
    book_layout_complexity = {}
    layout_complexity_path = "ordered_layout_complexity.json"
    with open(layout_complexity_path ) as json_file:
    
        book_layout_complexity = json.load(json_file)
        
        json_file.close()    
    
    
    
    book_path_list.pop(0) 
    print("\n".join(book_path_list))
    
    book_index = {}
    book_count = 0
    
    for book in book_path_list:
        book_name = get_book_name(book)
        #print(book_name)
        # book_index[book_name] = book_count
        # book_count = book_count +1
        book_index[book_name] = int(book_name)

  
    
    
        manga_page_list = loadManga(book)
        file_number = len(manga_page_list)
        #print(file_number)
        json_name = get_book_name(book)
        json_root = MANGA_ANNOTATION_PATH
        json_path = json_name+"_ordered_pages.json"


        #print("process json_path = "+json_path)
        
        if path.exists(MANGA_ANNOTATION_PATH+json_path) == True:
            print("##process json_path = "+json_path)
            book_annotation = load_manga_109_annotations(MANGA_ANNOTATION_PATH+json_path)
            new_book_annotation = book_annotation
            #print("\n".join(manga_page_list))        
            
            #folder_path = "ordered_crop/"+book_name+"/"
            # folder_path = "ordered_crop/"+book_name+"/"
            # try:
            #     os.mkdir(folder_path)
            # except OSError:
            #     print ("Creation of the directory %s failed" % folder_path)
            # else:
            #     print ("Successfully created the directory %s " % folder_path)
        
        
        # get_OCR_file(book_annotation)
        
        
        
        # page = 2
            manga_page_number = len(manga_page_list)
            print(manga_page_number)
            page_count = 0
            
            for page in range(manga_page_number):
                image_obj = Image.open(book+manga_page_list[page])
                image_id_record = {}
                new_image_list = {}
                new_image_list[page] = {}
                count = 0
                
                recored_new_frame_features = []
                number_frame = len(book_annotation[page]["frames"])
                for frame in book_annotation[page]["frames"]:
                    image_id_record[count] = frame["id"]
                    
                    min_x = int(frame["xmin"])
                    min_y = int(frame["ymin"])
                    max_x = int(frame["xmax"])
                    max_y = int(frame["ymax"])
                    panel_total_area = (max_x - min_x)*(max_y - min_y)
                    ### minus textbox area
                    new_area = panel_total_area
                    total_textbox = 0
                    for textbox in book_annotation[page]["texts"]:
                        if int(textbox["xmin"]) > min_x and int(textbox["xmax"]) < max_x:
                            if int(textbox["ymin"]) > min_y and int(textbox["ymax"]) < max_y:
                                textbox_area = (int(textbox["xmax"])-int(textbox["xmin"])) *(int(textbox["ymax"])-int(textbox["ymin"]))
                                total_textbox = total_textbox + 1
                                if new_area - textbox_area >0:
                                    new_area =  new_area - textbox_area
                    
                    
                    
                    # w1∗IA+w2∗LS+(−1)∗w3∗P N+w4∗T N
                    ## IA
                    frame["image_area"] = new_area
                    ## LS
                    if book_name in book_layout_complexity:
                        frame["layout_complexity"] = book_layout_complexity[book_name]
                    else:
                        frame["layout_complexity"] = 0 
                    ## PN
                    frame["panel_number"] = number_frame
                    ## TN
                    frame["text_number"] = total_textbox
                    
                    
                    w1 = 0.00001
                    w3 = 0.1
                    w4 = 0.1
                    w2 = 1 -(w1+w3+w4)

                    frame["info_score"] = w1*float(frame["image_area"])+w2*float(frame["layout_complexity"])+(-1)*w3*float(frame["panel_number"])+w4*float(frame["text_number"])
                    
                    recored_new_frame_features.append(frame)
                            
                    
                    new_image = crop_image(image_obj, min_x, min_y, max_x, max_y)
                    new_image_list[page][count] = new_image
                    count = count + 1
                new_book_annotation[page]["frames"] = recored_new_frame_features
                
                #new_image.show()
                # for result_panel in new_image_list[page]:
                #     need_image = new_image_list[page][result_panel]
                #     need_image.save(folder_path+str(page_count)+"_"+str(result_panel)+".jpg") 
                #print(book_annotation[2]) 
                
                if len(book_annotation[page]["frames"]) > 0:
                    page_count =  page_count +1
                    
            json_file = open("new_features/"+book_name+"_new_feature.json", "w")
            # magic happens here to make it pretty-printed
            json_file.write(json.dumps(new_book_annotation, indent=4))
            json_file.close()   