import h5py
import numpy as np

DATA_PATH = "./manga_data_ordered/"


f = h5py.File(DATA_PATH+'vgg_features.h5', 'r')
#f = h5py.File(DATA_PATH+'manga_vgg_panel.h5', 'r')
#f = h5py.File(DATA_PATH+'manga_style_random_features.h5', 'r')

check_keys = list(f.keys())
print(check_keys)

for fold in check_keys:
    sub_keys = list(f[fold].keys())
    print(sub_keys)
    print(f[fold][sub_keys[0]].shape)

# count = 0
# for item in f[fold][sub_keys[0]]:
#     #print(item)
#     #print(type(item))
#     if count <= 1:
#         print(fold)
#         print(sub_keys[0])
#         print(item)
#         print(type(item))
#         print(item.shape)

#     count = count +1
