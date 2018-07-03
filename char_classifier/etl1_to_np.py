import numpy as np
from read_etl1 import import_data

data, label, label_char = import_data(image_brightness=16)
print(type(data), type(label), type(label_char))
# all 63 x 64

print(data[0].shape)

for i in range(len(data)):
    tmp = np.zeros((1, 64))
    data[i] = np.concatenate([data[i], tmp], axis=0)
    # now they're all 64 x 64

# images
x = np.stack(data, axis=0)  # 130k x 64 x 64
# labels
label2id = dict()
id2label = []
y = []
for i in range(len(label_char)):
    _char = str(label_char[i])
    if _char not in label2id:
        label2id[_char] = len(id2label)
        id2label.append(_char)
    y.append(label2id[_char])
y = np.array(y)

np.save("etl1_images.npy", x)
np.save("etl1_labels.npy", y)
with open("etl1_id2label.txt", "w") as text_file:
    text_file.write("\n".join(id2label))
print("saved etl1 data into files")