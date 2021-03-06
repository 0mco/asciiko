import numpy as np
import random
import os
from helpers.read_etl_1_6 import import_data


def data_split(valid_size, test_size, etl='1'):

    assert etl in ["1", "6"]
    data, label, label_char = import_data(etl, image_brightness=16)
    # all 63 x 64

    for i in range(len(data)):
        tmp = np.zeros((1, 20))
        data[i] = np.concatenate([data[i], tmp], axis=0)
        # now they're all 64 x 64 (20 x 20)

    combined = list(zip(data, label_char))
    random.shuffle(combined)
    data, label_char = zip(*combined)
    data, label_char = list(data), list(label_char)

    # images
    x = np.stack(data, axis=0)  # 130k x 64 x 64 (20 x 20)
    # load id2label
    id2label = []
    with open("etl" + etl + "_id2label.txt", "r") as ins:
        for line in ins:
            line = line.strip()
            id2label.append(line)

    label2id = {}
    for i, _l in enumerate(id2label):
        label2id[_l] = i

    # labels
    label2id = dict()
    id2label = []
    y = []
    for i in range(len(label_char)):
        _char = str(label_char[i])
        assert _char in label2id:
        y.append(label2id[_char])
    y = np.array(y)

    assert len(y) > valid_size + test_size
    test_x, test_y = x[-test_size:], y[-test_size:]
    valid_x, valid_y = x[-(valid_size + test_size): -test_size], y[-(valid_size + test_size): -test_size]
    train_x, train_y = x[: -(valid_size + test_size)], y[: -(valid_size + test_size)]

    if not os.path.exists("parsed_etl_data"):
        os.mkdir("parsed_etl_data")

    np.save("parsed_etl_data/etl" + etl + "_images_train.npy", train_x)
    np.save("parsed_etl_data/etl" + etl + "_labels_train.npy", train_y)

    np.save("parsed_etl_data/etl" + etl + "_images_valid.npy", valid_x)
    np.save("parsed_etl_data/etl" + etl + "_labels_valid.npy", valid_y)

    np.save("parsed_etl_data/etl" + etl + "_images_test.npy", test_x)
    np.save("parsed_etl_data/etl" + etl + "_labels_test.npy", test_y)
    print("saved etl" + etl + " data into files")
