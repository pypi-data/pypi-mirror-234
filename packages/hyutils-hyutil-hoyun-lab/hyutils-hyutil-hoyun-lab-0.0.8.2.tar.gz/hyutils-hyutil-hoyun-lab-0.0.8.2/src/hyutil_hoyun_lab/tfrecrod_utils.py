import xml.etree.ElementTree as Et
from tqdm import tqdm
import os
import io
import random
import pandas as pd
import tensorflow as tf
import numpy as np
from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple
import glob
import shutil
import cv2


def xml_to_dataframe(xml_path, include_string, special_action=None):
    classes_names = []
    file_list = []
    xml_list = []

    # classes_names.clear()




    if not os.path.exists(xml_path) or len(include_string) == 0:
        print(f'invalid parameters: {xml_path} {include_string}')
        return

    xml_target = os.path.join(xml_path, include_string)
    file_list = glob.glob(xml_target)
    if special_action is not None and special_action == 'shake':
        random.shuffle(file_list)
        random.shuffle(file_list)

    for xml_file in tqdm(file_list, desc=include_string):
        # sprint('---> ', xml_file)
        tree = Et.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            classes_names.append(member.find('name').text)
            bndbox = member.find('bndbox')
            value = (root.find('filename').text,
                     int(root.find('size').find('width').text),
                     int(root.find('size').find('height').text),
                     member.find('name').text,
                     int(bndbox.find('xmin').text),
                     int(bndbox.find('ymin').text),
                     int(bndbox.find('xmax').text),
                     int(bndbox.find('ymax').text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    classes_names = list(set(classes_names))
    classes_names.sort()
    return xml_df, classes_names


"""
설명: 특정 경로와 확장자 정보(*.xml 등)를 입력받아서 입력된 경로의 모든 파일을 대상으로
     coco xml 파일 형식을 가정하고 읽어서 특정 경로 위 폴더에 csv 파일을 생성하고, 
     입력된 label map 파일명으로 입력되었던 특정 경로 바로 위 폴더에 라벨맵을 생성한다.
     
사용예:
  python 5_xml_to_csv_in_divided_data.py 
    --xml_path=D:\python_work\tf-train-data\faces\new_face_train_label 
    --include_string=01*.xml 
    --output_file=D:\python_work\tf-train-data\faces\new_face_train_label01.csv 
    --labelmap_name=new_face_labelmap_01.pbtxt 
"""


def convert_to_csv(xml_path, include_string, output_file, labelmap_path, special_action=None):

    xml_df, classes_names = xml_to_dataframe(xml_path, include_string, special_action)

    # label map 생성
    # labelmap_dir = os.path.dirname(output_file)
    # label_map_path = os.path.join(labelmap_dir, labelmap_name)
    print(f'label_map_path > {labelmap_path}')
    pbtxt_content = ""

    for i, class_name in enumerate(classes_names):
        pbtxt_content = (
                pbtxt_content
                + "item {{\n    id: {0}\n    name: '{1}'\n}}\n\n".format(i + 1, class_name)
        )
    pbtxt_content = pbtxt_content.strip()
    with open(labelmap_path, "w") as f:
        f.write(pbtxt_content)
        print(f'Successfully created {labelmap_path}')

    # csv 파일 생성.
    output_path = os.path.dirname(output_file)
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)

    xml_df.to_csv(output_file, index=None)


def __split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_one_tf_example(group, path, class_dict):
    with tf.io.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        if {'xmin_rel', 'xmax_rel', 'ymin_rel', 'ymax_rel'}.issubset(set(row.index)):
        # if set(['xmin_rel', 'xmax_rel', 'ymin_rel', 'ymax_rel']).issubset(set(row.index)):
            xmin = row['xmin_rel']
            xmax = row['xmax_rel']
            ymin = row['ymin_rel']
            ymax = row['ymax_rel']
            xmins.append(xmin)
            xmaxs.append(xmax)
            ymins.append(ymin)
            ymaxs.append(ymax)
        elif {'xmin', 'xmax', 'ymin', 'ymax'}.issubset(set(row.index)):
        # elif set(['xmin', 'xmax', 'ymin', 'ymax']).issubset(set(row.index)):
            xmn = row['xmin'] / width
            if xmn < 0.0:
                xmn = 0.0
            elif xmn > 1.0:
                xmn = 1.0
            xmins.append(xmn)

            xmx = row['xmax'] / width
            if xmx < 0.0:
                xmx = 0.0
            elif xmx > 1.0:
                xmx = 1.0
            xmaxs.append(xmx)

            ymn = row['ymin'] / height
            if ymn < 0.0:
                ymn = 0.0
            elif ymn > 1.0:
                ymn = 1.0
            ymins.append(ymn)

            ymx = row['ymax'] / height
            if ymx < 0.0:
                ymx = 0.0
            elif ymx > 1.0:
                ymx = 1.0
            ymaxs.append(ymx)

        # xmins.append(xmin)
        # xmaxs.append(xmax)
        # ymins.append(ymin)
        # ymaxs.append(ymax)
        classes_text.append(str(row['class']).encode('utf8'))
        classes.append(class_dict[str(row['class'])])

    tf_example = tf.train.Example(features=tf.train.Features(
        feature={
            'image/height': dataset_util.int64_feature(height),
            'image/width': dataset_util.int64_feature(width),
            'image/filename': dataset_util.bytes_feature(filename),
            'image/source_id': dataset_util.bytes_feature(filename),
            'image/encoded': dataset_util.bytes_feature(encoded_jpg),
            'image/format': dataset_util.bytes_feature(image_format),
            'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
            'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
            'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
            'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
            'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
            'image/object/class/label': dataset_util.int64_list_feature(classes), }))
    return tf_example


def class_dict_from_pbtxt(pbtxt_path):
    # open file, strip \n, trim lines and keep only
    # lines beginning with id or display_name

    with open(pbtxt_path, 'r', encoding='utf-8-sig') as f:
        data = f.readlines()

    name_key = None
    if any('display_name:' in s for s in data):
        name_key = 'display_name:'
    elif any('name:' in s for s in data):
        name_key = 'name:'

    if name_key is None:
        raise ValueError(
            "label map does not have class names, provided by values with the 'display_name' \
            or 'name' keys in the contents of the file"
        )

    data = [item.rstrip('\n').strip() for item in data if 'id:' in item or name_key in item]

    ids = [int(item.replace('id:', '')) for item in data if item.startswith('id')]
    names = [
        item.replace(name_key, '').replace('"', '').replace("'", '').strip() for item in data
        if item.startswith(name_key)]

    # join ids and display_names into a single dictionary
    class_dict = {}
    for i in range(len(ids)):
        class_dict[names[i]] = ids[i]

    return class_dict


# convert_to_csv(d:\python_work\tf-train-data\faces,
#                 "new_face_train_label01.csv,new_face_train_label02.csv",
#                 d:\python_work\tf-train-data\faces\face_label_map.pbtxt,
#                 d:\python_work\tf-train-data\faces\new_face_images,
#                 d:\python_work\tf-train-data\faces\new_face_train.tfrecord)
def convert_to_tfrecord(csv_path, csv_list, pbtxt_path, image_path, output_path):
    result = False

    image_path = os.path.join(image_path)

    class_dict = class_dict_from_pbtxt(pbtxt_path)
    writer = tf.compat.v1.python_io.TFRecordWriter(output_path)

    if len(csv_list) > 0:
        csv_list = csv_list.split(',')
        for csv_input in csv_list:
            csv_target = os.path.join(csv_path, csv_input.strip())

            examples = pd.read_csv(csv_target)
            grouped = __split(examples, 'filename')

            for group in tqdm(grouped, desc='groups'):
                tf_example = create_one_tf_example(group, image_path, class_dict)
                writer.write(tf_example.SerializeToString())

            print(f'{csv_input} was processed')
            writer.flush()

        writer.close()
        print('Successfully created the TFRecords: {}'.format(output_path))
        result = True

    return result


"""
주석이 들어있는 폴더를 입력받아서 xml 파일들을 랜덤으로 섞어서, 훈련 주석 0.8, 테스트 주석 0.2 비율로 나눈후,
test용 폴더에 test용 xml을, train 폴더에 train용 xml을 복사해준다.

python divide_annotation.py -a .\ANNOTATION_PATH -t1 .\train -t2 .\test
"""

def divide_annotation(annotation_path, train_label, test_label, train_rate = None):
    result = False
    if not os.path.exists(annotation_path):
        print('Not Found: {}'.format(annotation_path))
        return result

    if not os.path.exists(train_label):
        os.makedirs(train_label, exist_ok=True)

    if not os.path.exists(test_label):
        os.makedirs(test_label, exist_ok=True)


    if train_rate == None:
        return

    # annotation_target_path = os.path.join(annotation_path, '*.xml')
    # all_anno_list = os.listdir(annotation_target_path)
    all_anno_list = glob.glob(annotation_path + '/*.xml')
    total_size = len(all_anno_list)
    print('size:', total_size)
    random.shuffle(all_anno_list)
    random.shuffle(all_anno_list)
    train_count = int(total_size * train_rate)
    test_count = total_size - train_count
    print('train:{} test:{}'.format(train_count, test_count))

    # progress = tqdm(total_size)
    # idx = 0
    list_range = np.arange(0, total_size)
    for idx in tqdm(list_range, desc='dividing annotations to train & test set'):
        # while idx < total_size:
        # print(idx, '-', all_anno_list[idx])
        xml_fullpath = all_anno_list[idx]
        if not os.path.exists(xml_fullpath):
            print('Not Found: {}'.format(xml_fullpath))
            # progress.update()
            continue
        if idx < train_count:
            target_path = os.path.join(train_label, os.path.basename(all_anno_list[idx]))
        else:
            target_path = os.path.join(test_label, os.path.basename(all_anno_list[idx]))

        if os.path.exists(target_path):
            os.remove(target_path)
        shutil.copy(xml_fullpath, target_path)

    result = True
    return result


"""
설명: 입력된 이미지 저장 경로와 csv 파일 경로를 입력받아서, 
  csv의 1라인씩 읽어 width, height, xmin, ymin, xmax, ymax 값을 출력하고,
  대응하는 이미지를 읽어서 width, height를 읽어서 각 값들의 유효성을 체크하여,
  이후 tfrecord로 변환할 데이터의 유효성을 검증하고,
  이미지에 관심영역 box를 그려서 보여준다.

사용예:
  python temp_check_csv.py --image_path=.\images --csv_path=.\data.csv
"""


# 각 레코드를 파싱하기 위한 함수 정의
def parse_record(record):
    # 레코드의 feature 정의
    feature_description = {
        'image/encoded': tf.io.FixedLenFeature([], tf.string),
        'image/object/class/text': tf.io.VarLenFeature(tf.string),
        'image/object/bbox/xmin': tf.io.VarLenFeature(tf.float32),
        'image/object/bbox/xmax': tf.io.VarLenFeature(tf.float32),
        'image/object/bbox/ymin': tf.io.VarLenFeature(tf.float32),
        'image/object/bbox/ymax': tf.io.VarLenFeature(tf.float32),
        'image/width': tf.io.VarLenFeature(tf.int64),
        'image/height': tf.io.VarLenFeature(tf.int64),
        'image/filename': tf.io.FixedLenFeature([], tf.string)
    }
    # 레코드 파싱
    parsed_record = tf.io.parse_single_example(record, feature_description)
    # 이미지 데이터 디코딩
    image = tf.io.decode_image(parsed_record['image/encoded'])
    # 레이블 추출
    label = parsed_record['image/object/class/text']
    xmin = parsed_record['image/object/bbox/xmin']
    xmax = parsed_record['image/object/bbox/xmax']
    ymin = parsed_record['image/object/bbox/ymin']
    ymax = parsed_record['image/object/bbox/ymax']
    filename = parsed_record['image/filename']
    return image, label, filename, xmin, xmax, ymin, ymax


def tfrecord_valid_check(tfrecord_path, mode=None, key_touch=None):
    # for example in tf.io..tf_record_iterator(tfrecord_path):
    #     print(tf.train.Example.FromString(example))

    if os.path.exists(tfrecord_path):
        # 지정된 tfrecord 파일에 대한 데이터셋을 만듬.
        dataset = tf.data.TFRecordDataset(tfrecord_path)

        # 데이터셋에 map 함수를 사용하여 각 레코드 파싱
        parsed_dataset = dataset.map(parse_record)

        # 데이터셋 순회
        for image, label, filename, xmin, xmax, ymin, ymax in parsed_dataset:

            # 이미지 출력
            h, w, c = image.shape
            image = image.numpy()
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            xmin = tf.sparse.to_dense(xmin, default_value=0.0).numpy()
            xmax = tf.sparse.to_dense(xmax, default_value=0.0).numpy()
            ymin = tf.sparse.to_dense(ymin, default_value=0.0).numpy()
            ymax = tf.sparse.to_dense(ymax, default_value=0.0).numpy()
            label = tf.sparse.to_dense(label, default_value='???').numpy()

            if mode is not None:
                for idx in np.arange(0, len(label)):
                    print(f'filename:{filename}  label:{label[idx]} > xmin:{xmin[idx]} xmax:{xmax[idx]} \
                    ymin:{ymin[idx]} ymax:{ymax[idx]}, h:{h} w:{w} c:{c}')
                if c != 3:
                    print('---------------------- invalid image\'s channel size ----------------------')
                    if key_touch is not None and key_touch == 'touch':
                        cv2.waitKey(0)
                    else:
                        cv2.waitKey(500)
            else:
                # 레이블 출력
                for idx in np.arange(0, len(label)):
                    print(f'filename:{filename}  label:{label[idx]} > xmin:{xmin[idx]} xmax:{xmax[idx]} \
                    ymin:{ymin[idx]} ymax:{ymax[idx]}')
                    cv2.rectangle(image,
                                  (int(xmin[idx] * w), int(ymin[idx] * h)),
                                  (int(xmax[idx] * w), int(ymax[idx] * h)),
                                  (255, 255, 0), 2)

                cv2.imshow('image', image)

        # for d in raw_dataset:
        #     ex = tf.train.Example()
        #     ex.ParseFromString(d.numpy())
        #     m = json.loads(MessageToJson(ex))
        #     print(m['features']['feature'].keys())

        # for raw_record in dataset:
        #     example = tf.train.Example()
        #     example.ParseFromString(raw_record.numpy())
        #     print(example)
        #     print('-----------------------------------------------------------')
            key = cv2.waitKey(0)
            if key == 27:
                break

# def merge_multiple_tfrecords(record_list, output_path):
#     raw_dataset = tf.data.TFRecordDataset(record_list)
#     merged_dataset = raw_dataset.concatenate(tf.data.TFRecordDataset(output_path))
