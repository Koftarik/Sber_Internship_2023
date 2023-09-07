import os
import cv2
import json
import easyocr
import numpy as np
from matplotlib import pyplot as plt

path = 'files/'
files = os.listdir(path)

data = []
for i in files:
    print(path + i)
    with open(path + i, encoding='utf-8') as fout:
        data.extend(json.load(fout))

filename_list = []
new_data = []

for i in range(len(data)):
    filename = data[i]['file_name']
    if filename not in filename_list:
        filename_list.append(filename)
        new_data.append(data[i])
data = new_data
data = [data[i] for i in range(len(data)) if len(data[i]['result']) != 0]

reader = easyocr.Reader(['ru'])

fin = open('ner_labels.json', 'w')
fin_encode = open('ner_labels_encode.json', 'w', encoding='utf-8')
all_files_dict = {}
for i in range(len(data)):
    img_name = data[i]['file_name']
    path = 'images/' + img_name
    img = cv2.imread(path)
    print(i)
    secret_key = str(list(data[i]['result'].keys())[0])
    marks = data[i]['result'][secret_key]['result']['marks']
    entities = []
    for j in marks:
        x = j['position']['x']
        y = j['position']['y']
        h = j['position']['height']
        w = j['position']['width']

        crop = img[y:y + h, x:x + w]
        try:
            text = reader.readtext(crop, detail=0)
        except:
            continue
        # entities.append( {j['entityId']: text} )
        if text:
            entities.append([j['entityId'], text])
    all_files_dict[img_name] = entities
json.dump(all_files_dict, fin)
json.dump(all_files_dict, fin_encode, ensure_ascii=False)
fin.close()
fin_encode.close()

plt.imshow(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
plt.show()
