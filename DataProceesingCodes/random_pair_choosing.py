### This script is used to choose the random pairs from the dataset

import os
import random
import csv


NEEDED_PAIRS = 250
COMIC_ROOT_FOLDER = "../COMICS_Data/data/raw_panel_images/"
FORMAT_STRING = ".jpg"

### generate # of needed pairs and write the pairs to csv





files = folders = 0

path = COMIC_ROOT_FOLDER
random_book_list = []

for _, dirnames, filenames in os.walk(path):
  # ^ this idiom means "we won't be using this value"
    files += len(filenames)
    #print(len(filenames))
    folders += len(dirnames)
    if len(dirnames) > 0:
        #print("Here is the folder's name array")
        for i in range(NEEDED_PAIRS):
            random_book_list.append(random.choice(dirnames))
            
print("{:,} files, {:,} folders".format(files, folders))        
    
selected_book_panels = []
for book in random_book_list:
    book_path = COMIC_ROOT_FOLDER+book+"/"
    

    f = []

    for (dirpath, dirnames, filenames) in os.walk(book_path):
        if len(filenames) > 0:
            target_page = random.choice(filenames)
            is_selected = False
        
            target_pair = {}
            
            format_string = FORMAT_STRING
            while is_selected == False:
                name_string = target_page.replace(format_string, "")
                name_array = name_string.split("_")
                next_panel = int(name_array[1]) + 1
                next_panel_image = name_array[0]+"_"+str(next_panel)+format_string
                
                image_path = book_path+next_panel_image
                is_selected = os.path.exists(image_path)
                
                if is_selected == True:
                    target_pair["book"] = book
                    target_pair["pre_panel"] = target_page
                    target_pair["post_panel"] = next_panel_image
                else:
                    target_page = random.choice(filenames)
            
            selected_book_panels.append(target_pair)
            
        #f.extend(filenames)
        break

    file = open('selected_pairs.csv', 'w', newline ='') 
    
    with file: 
    # identifying header   
        header = ['Book', 'Prepanel', 'Postpanel'] 
        writer = csv.DictWriter(file, fieldnames = header) 
        
        # writing data row-wise into the csv file 
        writer.writeheader()
        for  pairs in selected_book_panels:
            writer.writerow({"Book" : pairs["book"],  
                            'Prepanel': pairs["pre_panel"],  
                            'Postpanel': pairs["post_panel"]}) 
        
        file.close()

    #print(f)
#print("\n".join(random_book_list))

