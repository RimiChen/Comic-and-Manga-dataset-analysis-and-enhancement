# Improting Image class from PIL module 
from os import walk
import os
import math
import json
from random import randrange
from PIL import Image, ImageTk
import ComicBook_fun as COMIC_PRE

SPLIT_IMAGE_PAGES = False
PROCESS_ANNOTATION = False
PROCESS_READING_ORDER = True
CROP_WITH_ORDER = True
PAGE_DIVISION_X = 10
PAGE_DIVISION_Y = 10
PAGE_TOLERANCE = 20

# SPLIT_FOLDER = "split_pages"
#MANGA_IMAGE_PATH = "manga_images/AisazuNihaIrarenai/"
#MANGA_IMAGE_PATH = "manga_images/Saisoku/"
#MANGA_ANNOTATION_PATH = "annotation_data/Saisoku/"

class Processed_ComicBook:
    def __init__(self):
        self.bookName = ""
        self.characters = []
        self.pageList = []
        # if needed, turn the translater on
        self.translateFlag = False

        # page {}:
        # frame []
        # frame {}:
        # text [], body [], face []


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
    print("load_manga_109_annotations")
    annotations = []
    book_dictionary = {}
    
    
    #json_file = open(json_path, "r")
    with open(json_path) as json_file:
    
        annotations = json.load(json_file)
        
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
def get_page_name(page_number):
    page_name = str(page_number)
    if page_number < 100:
        if page_number <10:
            page_name = "00"+str(page_number)
        else:
            page_name = "0"+str(page_number)
    
    return page_name

def split_pages(manga_book_path, book_index):
    manga_page_list = loadManga(manga_book_path)
    file_number = len(manga_page_list)
    book_name = get_book_name(manga_book_path)
    
    root_path = manga_book_path[:-1]
    root_path = root_path.replace(book_name, "")
    # json_path = book_name+"_pages.json"
    # book_annotation = load_manga_109_annotations(MANGA_ANNOTATION_PATH+json_path)
    #print("\n".join(manga_page_list))        
    
    folder_path = root_path+str(book_index)
    try:
        os.mkdir(folder_path)
    except OSError:
        print ("Creation of the directory %s failed" % folder_path)
    else:
        print ("Successfully created the directory %s " % folder_path)
    
    
    #get_OCR_file(book_annotation)
    
    
    
    #page = 2
    manga_page_number = len(manga_page_list)
    
    new_pages = {}
    
    new_page_count = 0
    for page in range(manga_page_number):
        image_obj = Image.open(manga_book_path+manga_page_list[page])
        image_id_record = {}
        new_image_list = {}
        new_image_list[page] = {}
        count = 0
        image_width, image_height = image_obj.size
        # print("w = "+str(image_width)+", h = "+str(image_height))
        min_x = {}
        min_y = {} 
        max_x = {}
        max_y = {}
        
        
        middle_x = math.floor(image_width/2)
        
        min_x[0] = middle_x
        min_x[1] = 0
        
        min_y[0] = 0
        min_y[1] = 0
         

        max_x[0] = image_width
        max_x[1] = middle_x
        
        max_y[0] = image_height
        max_y[1] = image_height
        

        
        new_image_1 = crop_image(image_obj, min_x[0], min_y[0], max_x[0], max_y[0])
        new_pages[new_page_count] = new_image_1       
        new_page_count = new_page_count +1

        new_image_2 = crop_image(image_obj, min_x[1], min_y[1], max_x[1], max_y[1])
        new_pages[new_page_count] = new_image_2       
        new_page_count = new_page_count +1        
        # for frame in book_annotation[page]["frames"]:
        #     image_id_record[count] = frame["id"]
        #     min_x = int(frame["xmin"])
        #     min_y = int(frame["ymin"])
        #     max_x = int(frame["xmax"])
        #     max_y = int(frame["ymax"])
        #     new_image = crop_image(image_obj, min_x, min_y, max_x, max_y)
        #     new_image_list[page][count] = new_image
        #     count = count + 1
        
        
    #new_image.show()
    for result_page in new_pages:
        need_image = new_pages[result_page]
        page_name = get_page_name(result_page)
        #print(page_name)
        need_image.save(folder_path+"/"+page_name+".jpg") 
    #print(book_annotation[2])     

def get_annotation_files(manga_book_path, book_index):
    # annotation_data
    book_name = get_book_name(book)
    annotation_file_path = "annotation_data/"+book_name+".xml"
    annotation_folder_path = "annotation_data/"+str(book_index)

    try:
        os.mkdir(annotation_folder_path)
    except OSError:
        print ("Creation of the directory %s failed" % annotation_folder_path)
    else:
        print ("Successfully created the directory %s " % annotation_folder_path)
        
    #COMIC_PRE.test_fun()
    
    COMIC_PRE.comic_annotaiton_processing(annotation_file_path, annotation_folder_path, book_index)
        
    
def split_frame_location(annotation_file_name):
    postfix = "_split_pages.json"
    sub_file_name = annotation_file_name.replace("_pages.json","")
    new_file_name = sub_file_name+postfix
    
    #print(new_file_name)

    new_page_list = []
    page_count = 0
    with open(annotation_file_name) as json_file:
        
        page_list = json.load(json_file)
        
        min_x = 0
        min_y = 0
        
        for page in page_list:
            max_x = int(page["overallW"])
            max_y = int(page["overallH"])
            
            ref_x = math.floor((min_x+max_x)/2)
            ref_y = max_y
            
            
            page_index = page["index"]
            target_frames = page["frames"]
            target_faces= page["faces"]
            target_bodys = page["bodys"]
            target_texts = page["texts"]
            
            first_part = {}
            first_part["index"] = page_count
            first_part["overallW"] = ref_x
            first_part["overallH"] = ref_y
            first_part["frames"] = []
            first_part["faces"] = []
            first_part["bodys"] = []
            first_part["texts"] = []
            page_count = page_count +1
            
            second_part = {}
            second_part["index"] = page_count
            second_part["overallW"] = ref_x
            second_part["overallH"] = ref_y
            second_part["frames"] = []
            second_part["faces"] = []
            second_part["bodys"] = []
            second_part["texts"] = []  
            page_count = page_count +1          
            
            for frame in target_frames:
                if int(frame["xmin"]) >= ref_x and int(frame["xmax"]) >= ref_x:
                    frame["xmin"] = str(int(frame["xmin"]) - ref_x)
                    frame["xmax"] = str(int(frame["xmax"]) - ref_x)
                    first_part["frames"].append(frame)
                    
                elif int(frame["xmin"]) < ref_x and int(frame["xmax"]) < ref_x:
                    second_part["frames"].append(frame)
                else:
                    ## cross pages
                    duplicate_frame = frame

                    frame["xmin"] = str(ref_x - ref_x)
                    frame["xmax"] = str(int(frame["xmax"]) - ref_x)
                    
                    first_part["frames"].append(frame)


                    duplicate_frame["xmin"] = str(int(duplicate_frame["xmin"]))
                    duplicate_frame["xmax"] = str(ref_x)
                    
                    second_part["frames"].append(duplicate_frame)
            
            
            for face in target_faces:
                if int(face["xmin"]) >= ref_x and int(face["xmax"]) >= ref_x:
                    face["xmin"] = str(int(face["xmin"]) - ref_x)
                    face["xmax"] = str(int(face["xmax"]) - ref_x)
                    first_part["faces"].append(face)
                    
                elif int(face["xmin"]) < ref_x and int(face["xmax"]) < ref_x:
                    second_part["faces"].append(face)
                else:
                    ## cross pages
                    duplicate_face = face

                    face["xmin"] = str(ref_x - ref_x)
                    face["xmax"] = str(int(face["xmax"]) - ref_x)
                    
                    first_part["faces"].append(face)


                    duplicate_face["xmin"] = str(int(duplicate_face["xmin"]))
                    duplicate_face["xmax"] = str(ref_x)
                    
                    second_part["faces"].append(duplicate_face)       
        
            
            for body in target_bodys:
                if int(body["xmin"]) >= ref_x and int(body["xmax"]) >= ref_x:
                    body["xmin"] = str(int(body["xmin"]) - ref_x)
                    body["xmax"] = str(int(body["xmax"]) - ref_x)
                    first_part["bodys"].append(body)
                    
                elif int(body["xmin"]) < ref_x and int(body["xmax"]) < ref_x:
                    second_part["bodys"].append(body)
                else:
                    ## cross pages
                    duplicate_body = body

                    body["xmin"] = str(ref_x - ref_x)
                    body["xmax"] = str(int(body["xmax"]) - ref_x)
                    
                    first_part["bodys"].append(body)


                    duplicate_body["xmin"] = str(int(duplicate_body["xmin"]))
                    duplicate_body["xmax"] = str(ref_x)
                    
                    second_part["bodys"].append(duplicate_body)
                    

            for text in target_texts:
                if int(text["xmin"]) >= ref_x and int(text["xmax"]) >= ref_x:
                    text["xmin"] = str(int(text["xmin"]) - ref_x)
                    text["xmax"] = str(int(text["xmax"]) - ref_x)
                    first_part["texts"].append(text)
                    
                elif int(text["xmin"]) < ref_x and int(text["xmax"]) < ref_x:
                    second_part["texts"].append(text)
                else:
                    ## cross pages
                    duplicate_text = text

                    text["xmin"] = str(ref_x - ref_x)
                    text["xmax"] = str(int(text["xmax"]) - ref_x)
                    
                    first_part["texts"].append(text)


                    duplicate_text["xmin"] = str(int(duplicate_text["xmin"]))
                    duplicate_text["xmax"] = str(ref_x)
                    
                    second_part["texts"].append(duplicate_text)
                    
            
            
            new_page_list.append(first_part)
            new_page_list.append(second_part)                   
        
    json_file.close()
    
             
    json_file = open(new_file_name, "w")
    # magic happens here to make it pretty-printed
    json_file.write(json.dumps(new_page_list, indent=4))
    json_file.close()    
    
    #return new_page_list       


def get_order_frames(split_file_name):
    postfix = "_order_pages.json"
    sub_file_name = annotation_file_name.replace("_split_pages.json","")
    new_file_name = sub_file_name+postfix
    
    ordered_page_list = []
    
    tolerance = PAGE_TOLERANCE
    
    ## find all frame in right side
    # Assume all page was divide to 20
    division_y = PAGE_DIVISION_Y
    
    record_TOP = {}
    record_RIGHT = {}

    
    with open(split_file_name) as json_file:
        page_list = json.load(json_file)
        
        for page in page_list:
            target_frame_list = page["farmes"]
            
            for frame in target_frame_list:
                frame_id = frame["id"]
                record_TOP[frame_id] = {}
                record_TOP[frame_id]["xmin"] = frame["xmin"]
                record_TOP[frame_id]["xmax"] = frame["xmax"]
            
                record_RIGHT[frame_id] = {}
                record_RIGHT[frame_id]["ymin"] = frame["ymin"]
                record_RIGHT[frame_id]["ymax"] = frame["ymax"]            
            
            
            
            
            
            
    
    
        
    
    json_file = open(new_file_name, "w")
    # magic happens here to make it pretty-printed
    json_file.write(json.dumps(ordered_page_list, indent=4))
    json_file.close()    

def search_composition_x(divide, target_list, W, H):
    width = W
    height = H
    
    
    divide_w = math.floor(width / divide)
    divide_h = math.floor(height / divide)


    
    
    
    
#def search_composition_y(divide, target_list):
def getCenter(minX, minY, maxX, maxY):
    newX = (int(minX) + int(maxX))/2
    newY = (int(minY) + int(maxY))/2
    
    return newX, newY
        
def search_frame(target_x, target_y, frame_list):
    
    found_frame = ""
    
    for frame in frame_list:
        if target_x >= frame["xmin"] and target_x <= frame["xmax"]:
            if target_y >= frame["ymin"] and target_y <= frame["ymax"]:
                found_frame = frame["id"]
                
    return found_frame
                    

if __name__ == "__main__":
    # book_path_list = [
    #     "manga_images/YumeiroCooking/",
    #     "manga_images/Saisoku/",
    #     "manga_images/AisazuNihaIrarenai/"
    # ]

    root_directory = "two_pages/"
    book_path_list = []

    for x in os.walk(root_directory):
        #if len(x[0])<1:
        #    print("SYSTEM: empty folder name!")
        #else:
        #print(x[0]+", "+str(len(x[0])))
        book_path_list.append(x[0]+"/")
    
    book_path_list.pop(0) 
    print("\n".join(book_path_list))
    print("SYSTEM: book_number = "+str(len(book_path_list)))
    
    book_index = {}
    book_count = 0
    check_point = 3
    for book in book_path_list:
        book_name = get_book_name(book)
        book_index[book_name] = book_count
        
        if SPLIT_IMAGE_PAGES  == True:
            split_pages(book, book_index[book_name])
            
        if PROCESS_ANNOTATION == True:
            # process annotaiton data
            get_annotation_files(book, book_index[book_name])
        
        # if book_count > check_point:
        if book_count < check_point:
          # load and correct annotation
            annotation_directory = "split_annotation/"
            annotation_file_name = annotation_directory + str(book_count)+"_pages.json"
          
          # location mapping
            #frame_location =
            split_frame_location(annotation_file_name)
            
            split_file_name =  annotation_directory + str(book_count)+"_split_pages.json"
            print(split_file_name)
          # get structure and reading order
            # get_order_frames(split_file_name)
          # crop images with order
            folder_postfix = ""
            if CROP_WITH_ORDER == True:
                print("SYSTEM: image with order")
                folder_postfix = "order"
                # get OCR

            else:
                folder_postfix = "random"
                # get OCR

        
        
        book_count = book_count +1
        

    
    # json_file = open("title_index.json", "w")
    # # magic happens here to make it pretty-printed
    # json_file.write(json.dumps(book_index, indent=4))
    # json_file.close()   
    
