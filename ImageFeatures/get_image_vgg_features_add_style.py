
from tensorflow.python.keras.preprocessing import image
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.applications.vgg16 import VGG16
from tensorflow.python.keras.applications.vgg16 import preprocess_input
import numpy as np
import random
import math
import os
import h5py
import json
import sklearn
import sklearn.preprocessing
#import vgg16

FOLDER = "manga_data_ordered/raw_panel_images_original/"
TEXT_FLAG = False
PANEL_FLAG = True
LAYOUT_FLAG = False
INFO_SCORE_FLAG = False
H5_FILE_NAME = "manga_vgg_panel_panel"



def generateFeature(model, img_path, input_style):
    #model2.summary()

    #model.layers.pop()



    img = image.load_img(img_path, target_size=(224, 224, 3))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)

    #vgg16_feature = model.predict(img_data)
    vgg16_feature = model.predict(img_data)

    #print(vgg16_feature.shape)
    # print(vgg16_feature)

    #print(type(vgg16_feature))
    new = np.diag(vgg16_feature[0])
    #vgg16_feature.resize(9, 4096)

    list_array = []

    num_list = []
    for num in range(new.shape[1]):
        num_list.append(num)
    #print(num_list)
    random.shuffle(num_list)
    #print(len(num_list))


    need_number = 8
    remains = new.shape[1] % need_number
    #print(remains)
    new_num_list = num_list[0:new.shape[1]-remains]
    #print(len(new_num_list))

    new_arr = np.array(new_num_list)
    end_list = np.split(new_arr, need_number)
    #print(end_list)

    for i in range(need_number):
        list_array.append(end_list[i].tolist())

    #print("\n".join(map(str, list_array)))

    b = np.zeros((9,new.shape[1]))
    b[0,:] = np.sum(new[list_array[0],:],axis=0)
    b[1,:] = np.sum(new[list_array[1],:],axis=0)
    b[2,:] = np.sum(new[list_array[2],:],axis=0)
    b[3,:] = np.sum(new[list_array[3],:],axis=0)
    b[4,:] = np.sum(new[list_array[4],:],axis=0)
    b[5,:] = np.sum(new[list_array[5],:],axis=0)
    b[6,:] = np.sum(new[list_array[6],:],axis=0)
    b[7,:] = np.sum(new[list_array[7],:],axis=0)
    # b[8,:] = np.sum(new[list_array[8],:],axis=0)

    
    #### use the last feature vector as the style feature
    style_v = np.ones((1,new.shape[1]))
    b[8,:] = input_style**style_v

    # print(b)
    # print(b.shape)
    return b


if __name__ == '__main__':
    ### image root path = FOLDER
    print("Processing all images and get vgg features")
    
    model = VGG16(weights='imagenet', include_top=True, pooling='avg')
    #model.pop()
    #model.summary()
    #print("pop twice to get fc ")
    
    #### we want fc layer
    model._layers.pop()
    model2 = Model(model.input, model.layers[-1].output)




    train_vgg_features = []
    dev_vgg_features = []
    test_vgg_features = []

    #print([x[0]  for x in os.walk(FOLDER) if len(x[0].replace(FOLDER,"").replace(".jpg","")) > 0])

    folders = [x[0]  for x in os.walk(FOLDER)  if len(x[0].replace(FOLDER,""))> 0]
    #.replace(".jpg","")) > 0
    print("\n".join(folders))


    num_books = len(folders)
    ## load folders, know how many books
    ## dev, train, test
    
    print("book number = "+str(num_books))
  
    dev_pro = math.ceil(num_books/3)
    test_pro = math.ceil(num_books/6)
    print("dev = "+str(dev_pro)+", test = "+str(test_pro))
    
    dev_thresh = num_books - dev_pro
    test_thresh = num_books - test_pro

    ## test << dev << train
    
    
    ### "train", "test", "dev" | "vgg_feature"
    
    
    hf = h5py.File(H5_FILE_NAME+'.h5', 'w')
    stop_count = 0
    
    ## loop over folders
    
    set_count = 0
    for folder in folders:
        folder_name_array = folder.split("/")
        folder_name = folder_name_array[-1]
        #### read style features
        target_style_path = "new_features/"+folder_name+"_new_feature.json"
        
        page_list = {}
        
        with open(target_style_path) as json_file:
            book_annotations = json.load(json_file)
            json_file.close()   
            
        page_index = 0
        for page in book_annotations:
            #print(page)
            if len(book_annotations[page]["frames"])>0:
                page_list[page_index] = {}


                average_panel_number = []
                text_density = []
                layout_complexity_not_normalized = []
                info_score_not_normalized = []
                
                for frame in book_annotations[page]["frames"]:
                    average_panel_number.append(float(frame["panel_number"])*0.1)
                    text_density.append(float(frame["text_number"])*0.1)
                    layout_complexity_not_normalized.append(float(frame["layout_complexity"]))
                    info_score_not_normalized.append(float(frame["info_score"]))
                    
                #new_arr = np.array(new_num_list)
                layout_complexity_normalized = list(sklearn.preprocessing.minmax_scale( layout_complexity_not_normalized, feature_range=(0, 1), axis=0, copy=True))
                info_score_normalized = list(sklearn.preprocessing.minmax_scale( info_score_not_normalized, feature_range=(0, 1), axis=0, copy=True))
                
                
                page_list[page_index]["panel_number"] = average_panel_number
                page_list[page_index]["text_number"] = text_density
                page_list[page_index]["layout_complexity"] = layout_complexity_normalized
                page_list[page_index]["info_score"] = info_score_normalized

                page_index = page_index + 1   
        #print(page_list)             
                # print(layout_complexity_normalized)
                # #print(layout_complexity_normalized.shape)
                # print(type(layout_complexity_normalized))
                # print(info_score_normalized)
                # #print(info_score_normalized.shape)
                # print(type(info_score_normalized))
                
                # "image_area": 202709,
                # "layout_complexity": "0.25",
                # "panel_number": 6,
                # "text_number": 2,
                # "info_score": 1.8270875                    
                     

        for subdir, dirs, files in os.walk(folder):
            
            if set_count < (num_books - test_thresh):

                print(str(folder)+"----test")
            elif set_count <= (num_books - dev_thresh) and set_count >= (num_books - test_thresh):
                print(str(folder)+"----dev")
            else:
                print(str(folder)+"----train")
            
            for filename in files:
                filepath = subdir + os.sep + filename
                

                # if stop_count < 10:
                if filepath.endswith(".jpg"):
                    print("processing \'"+ filepath+"\'")
                    #print (filepath)
                    #print(filename)
                    filename_string = filename.replace(".jpg","") 
                    filename_array = filename_string.split("_")
                    
                    target_page = filename_array[0]
                    target_panel = filename_array[1]
                    

                # page_list[page_index]["panel_number"] = average_panel_number
                # page_list[page_index]["text_number"] = text_density
                # page_list[page_index]["layout_complexity"] = layout_complexity_normalized
                # page_list[page_index]["info_score"] = info_score_normalized

                    # print(page_list)
                    # print("page: " +str(target_page) )
                    # print(type(target_page))
                    # print("panel: " +str(target_panel ) )
                    
                    int_target_page = int(target_page)
                    int_target_panel = int(target_panel)
                    
                    if INFO_SCORE_FLAG == True:
                        if int_target_panel < len(page_list[int_target_page]["info_score"]):
                            target_feature = page_list[int_target_page]["info_score"][int_target_panel]
                        else:
                            target_feature = 0.0                        
                    elif TEXT_FLAG == True:
                        #target_feature = page_list[target_page]["text_number"][target_feature]
                        if int_target_panel < len(page_list[int_target_page]["text_number"]):
                            target_feature = page_list[int_target_page]["text_number"][int_target_panel]
                        else:
                            target_feature = 0.0 
                    elif PANEL_FLAG == True:
                        #target_feature = page_list[target_page]["panel_number"][target_feature]
                        if int_target_panel < len(page_list[int_target_page]["panel_number"]):
                            target_feature = page_list[int_target_page]["panel_number"][int_target_panel]
                        else:
                            target_feature = 0.0  
                    elif LAYOUT_FLAG == True:
                        #target_feature = page_list[target_page]["layout_complexity"][target_feature]                        
                        if int_target_panel < len(page_list[int_target_page]["layout_complexity"]):
                            target_feature = page_list[int_target_page]["layout_complexity"][int_target_panel]
                        else:
                            target_feature = 0.0 
                            
                                                  

                    #print(target_feature)
                    #name_list.append(filepath)    
                    # img_path = filepath.replace("\\","")
                    img_path = filepath
                    #print (img_path)
                    
                    # vgg_feature = [random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)] 
                    vgg_feature = generateFeature(model2, img_path, target_feature)
                    # print(vgg_feature)
                    # print(type(vgg_feature))
                    
                    if set_count < (num_books - test_thresh):
                        #print(str(filepath)+"----test")
                        test_vgg_features.append(vgg_feature)
                    elif set_count <= (num_books - dev_thresh) and set_count >= (num_books - test_thresh):
                        #print(str(filepath)+"----dev")
                        dev_vgg_features.append(vgg_feature)
                    else:
                        #print(str(filepath)+"----train")
                        train_vgg_features.append(vgg_feature)
                                            
                    # stop_count = stop_count + 1
            set_count = set_count + 1    
    
    vgg_array_train = np.array(train_vgg_features)
    vgg_array_dev = np.array(dev_vgg_features)
    vgg_array_test = np.array(test_vgg_features)
    
    hf.create_dataset("train/vgg_features",data = vgg_array_train)
    hf.create_dataset("dev/vgg_features",data = vgg_array_dev)
    hf.create_dataset("test/vgg_features",data = vgg_array_test)    
    
    hf.close()