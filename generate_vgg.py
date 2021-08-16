import os
import glob
import json
import pickle
import cv2
import numpy as np
from icecream import ic
# import shutil


with open("via_project_16Aug2021_9h30m_json.json", 'rb') as base_export_file:
    base_json_dict = json.load(base_export_file)


for base_key, base_value in base_json_dict.items():
    file_name = os.path.splitext(base_value["filename"])[0]
    pickle_name = file_name + ".pickle"

    ic(base_key)
    ic(base_value)

    if os.path.exists(f'set_1_pickles/{file_name}.pickle'):

        # shutil.copy(f"dataset/{file_name}.jpeg", "set_1_images")
        with open(f'set_1_pickles/{file_name}.pickle', 'rb') as handle:
            prediction_groups = pickle.load(handle)
            print(prediction_groups)
        regions = []

        # SCALING
        big_img = cv2.imread(f"ds_set_images/{file_name}.jpeg")
        ic(big_img.shape)

        y_pdf = int(prediction_groups['height'])
        x_pdf = int(prediction_groups['width'])
        y_img = big_img.shape[0]
        x_img = big_img.shape[1]
        x_scale = x_img / x_pdf
        y_scale = y_img / y_pdf

        # x_scale = x_img / x_pdf 
        # y_scale = y_img / y_pdf

        ic(x_scale, y_scale)

        for bbox in prediction_groups['words']:
            print(bbox)
            # value, bbox = bbox
            # top_left = (bbox[0], bbox[1])
            # bot_right = (bbox[2], bbox[3])
            # x, y = int(top_left[0]), int(top_left[1])
            # w = int(bbox[2] - bbox[0])
            # h = int(bbox[3] - bbox[1])
            # print(x, y, w, h)
            x1 = int(np.round(bbox[0] * x_scale))
            y1 = int(np.round(bbox[1] * y_scale))
            x2 = int(np.round(bbox[2] * x_scale))
            y2 = int(np.round(bbox[3] * y_scale))

            inner_region_dict = {
                "shape_attributes": {
                    "name": "rect",
                    "x": x1,
                    "y": y1,
                    "width": x2 - x1,
                    "height": y2 - y1
                },
                "region_attributes": {
                    "label": "",
                    "text": bbox[4],
                }
            }
            regions.append(inner_region_dict)

        base_json_dict[base_key]["regions"] = regions

    else:
        print("non existent")
        # shutil.move(f"dataset/{file_name}.jpeg", "set_2_images")


with open("vgg_generic_generated_import.json", 'w') as generated_import_file:
    json.dump(base_json_dict, generated_import_file)