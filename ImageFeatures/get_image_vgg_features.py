
from tensorflow.python.keras.preprocessing import image
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.applications.vgg16 import VGG16
from tensorflow.python.keras.applications.vgg16 import preprocess_input
import numpy as np
import random
import math
import os
import h5py
#import vgg16

FOLDER = "manga_data_random/"

def generateFeature(model, img_path):
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


    remains = new.shape[1] % 9
    #print(remains)
    new_num_list = num_list[0:new.shape[1]-remains]
    #print(len(new_num_list))

    new_arr = np.array(new_num_list)
    end_list = np.split(new_arr, 9)
    #print(end_list)

    for i in range(9):
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
    b[8,:] = np.sum(new[list_array[8],:],axis=0)

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
    
    
    hf = h5py.File('manga_vgg_panel_all.h5', 'w')
    stop_count = 0
    
    ## loop over folders
    
    set_count = 0
    for folder in folders:
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
                    # print (filepath)
                    #name_list.append(filepath)    
                    # img_path = filepath.replace("\\","")
                    img_path = filepath
                    #print (img_path)
                    # vgg_feature = [random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)] 
                    vgg_feature = generateFeature(model2, img_path)
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