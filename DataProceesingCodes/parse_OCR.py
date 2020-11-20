

from os import walk
import os
import math
import json
from random import randrange
from PIL import Image, ImageTk
import csv
# count how many panels in a folder

if __name__ == "__main__":
    
    for x in os.walk("raw_panel_images"):
        target_list = x
        print(len(x))
        #if len(x[0])<1:
        #    print("SYSTEM: empty folder name!")
        #else:
        #print(x[0]+", "+str(len(x[0])))
        # if x[0].index(".json") > 0:
