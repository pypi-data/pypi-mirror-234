import xml.etree.ElementTree as ET
import os
import shutil
import cv2
from tqdm import tqdm
from .dirjob import get_entry_count
from .dirjob import files_ext

"""
def indent

def read_xml

def make_xml

write_xml

check_xml_and_fix

"""


def indent(elem, level=0):  # 자료 출처 https://goo.gl/J8VoDK
    i = "\n" + level * " " * 4
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + " " * 4
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def remove_point(temp):
    pos = temp.find('.')
    if pos == -1:
        return temp
    else:
        return temp[0:pos]

def read_xml(annotation_file_path):
    xml_info = []
    is_ok = False
    if not os.path.exists(annotation_file_path):
        return is_ok, xml_info

    tree = ET.parse(annotation_file_path)
    root = tree.getroot()
    for member in root.findall('object'):
        class_item = member.find('name')
        if class_item is None:
            print(f'Xml item not found: name : {annotation_file_path}')
            return is_ok, xml_info
        class_name = class_item.text
        item = []
        item.append(class_name) # 0

        bndbox = member.find('bndbox')
        item.append(root.find('size').find('height').text) # 1
        item.append(root.find('size').find('width').text) # 2
        item.append(root.find('size').find('depth').text)  # 3
        temp_str = bndbox.find('xmin').text
        item.append(remove_point(temp_str)) # 4

        temp_str = bndbox.find('ymin').text
        item.append(remove_point(temp_str)) # 5

        temp_str = bndbox.find('xmax').text
        item.append(remove_point(temp_str)) # 6

        temp_str = bndbox.find('ymax').text
        item.append(remove_point(temp_str)) # 7
        xml_info.append(item)

    is_ok = True
    # xml_info (class_name, width, height, xmin, ymin, xmax, ymax)
    return is_ok, xml_info


def make_xml(class_data, image_filename):
    is_ok = False

    if len(class_data) == 0 or image_filename is None:
        print('invalid parameters')
        return is_ok, None

    already_root_created = False

    for cls in class_data:
        if already_root_created == False:
            data = ET.Element('annotation')
            element1 = ET.SubElement(data, 'folder')
            element1.text = ' '
            element1 = ET.SubElement(data, 'filename')
            element1.text = image_filename
            element1 = ET.SubElement(data, 'path')
            element1.text = image_filename
            element1 = ET.SubElement(data, 'source')
            element1_1 = ET.SubElement(element1, 'database')
            element1_1.text = 'hyl'
            element1 = ET.SubElement(data, 'size')
            element1_1 = ET.SubElement(element1, 'width')
            element1_1.text = cls[2]
            element1_1 = ET.SubElement(element1, 'height')
            element1_1.text = cls[1]
            element1_1 = ET.SubElement(element1, 'depth')
            element1_1.text = cls[3]
            element1 = ET.SubElement(data, 'segmented')
            element1.text = '0'
            already_root_created = True

        element1 = ET.SubElement(data, 'object')
        element1_1 = ET.SubElement(element1, 'name')
        element1_1.text = cls[0]
        element1_1 = ET.SubElement(element1, 'pose')
        element1_1.text = 'Unspecified'
        element1_1 = ET.SubElement(element1, 'truncated')
        element1_1.text = '0'
        element1_1 = ET.SubElement(element1, 'difficult')
        element1_1.text = '0'
        element1_1 = ET.SubElement(element1, 'bndbox')
        element1_2 = ET.SubElement(element1_1, 'xmin')
        element1_2.text = cls[4]
        element1_2 = ET.SubElement(element1_1, 'xmax')
        element1_2.text = cls[6]
        element1_2 = ET.SubElement(element1_1, 'ymin')
        element1_2.text = cls[5]
        element1_2 = ET.SubElement(element1_1, 'ymax')
        element1_2.text = cls[7]

    is_ok = True
    return is_ok, data

def write_xml(path, xml_data):
    indent(xml_data, level=0)  # xml 들여쓰기
    b_xml = ET.tostring(xml_data)
    # 주석(xml)기록
    with open(path, 'wb') as f:
        f.write(b_xml)


def check_xml_n_fix(xml_path, image_path):
    result = False
    if os.path.exists(xml_path) and os.path.exists(image_path):
        # index = 0
        count = get_entry_count(xml_path, '.xml')
        pbar = tqdm(total=count)
        for file in files_ext(xml_path, '.xml'):
            # index += 1
            # if index % 1000 == 0:
            #     print(f'> {index} <')

            xml_file = os.path.join(xml_path, file)
            xml_name = os.path.splitext(file)[0]
            image_name = xml_name + '.jpg'
            image_file = os.path.join(image_path, image_name)
            if os.path.exists(image_file):
                img_mat = cv2.imread(image_file)
                if img_mat is None:
                    print(f'invalid image: {file}')
                    continue
                h, w, c = img_mat.shape

                xml_info = []
                xml_info.clear()
                tree = ET.parse(xml_file)
                root = tree.getroot()
                invalid = False
                for member in root.findall('object'):
                    class_item = member.find('name')
                    if class_item is not None:
                        class_name = class_item.text

                        item = []
                        item.clear()
                        item.append(class_name)  # 0

                        bndbox = member.find('bndbox')

                        width = int(root.find('size').find('width').text)
                        height = int(root.find('size').find('height').text)
                        xmax = int(bndbox.find('xmax').text)
                        ymax = int(bndbox.find('ymax').text)

                        if h != height or w != width:
                            item.append(str(h))  # 1
                            item.append(str(w))  # 2
                            item.append(str(c)) # 3
                            print(f'invalid width or height value: {file}')
                            invalid = True
                        else:
                            item.append(root.find('size').find('height').text)  # 1
                            item.append(root.find('size').find('width').text)  # 2
                            item.append(root.find('size').find('depth').text)  # 3

                        item.append(bndbox.find('xmin').text)  # 4
                        item.append(bndbox.find('ymin').text)  # 5

                        if xmax > w:
                            item.append(str(w))  # 6
                            print(f'invalid xmax value: {file} , xmax: {xmax}')
                            invalid = True
                        else:
                            item.append(bndbox.find('xmax').text)  # 6

                        if ymax > h:
                            item.append(str(h))  # 7
                            print(f'invalid ymax value: {file} , ymax: {ymax}')
                            invalid = True
                        else:
                            item.append(bndbox.find('ymax').text)  # 7

                        xml_info.append(item)

                    else:
                            print(f'Xml item not found: name : {xml_file}')

                if invalid == True: # replace old xml with new xml
                    new_xml_file = xml_file + '.xml'
                    is_ok, data = make_xml(xml_info, image_name)
                    if is_ok == True:
                        write_xml(new_xml_file, data)
                        os.remove(xml_file)
                        shutil.move(new_xml_file, xml_file)
            pbar.update()

        result = True
    return result


def check_csv(image_path, csv_path):
    result = False

    if not os.path.exists(image_path)\
        or not os.path.exists(csv_path):
        return result

    invaild_detected = False
    # idx = 0

    f = open(csv_path, 'rt')
    count = len(f.readlines())
    pbar = tqdm(total=count)

    new_csv_path = csv_path + '.txt'
    with open(csv_path, 'rt') as f:
        with open(new_csv_path, 'wt') as new_f:
            line = f.readline()
            new_f.write(line)
            # idx += 1
            pbar.update()
            # print(f'{idx} > {line}')
            if line:
                while len(line) > 0:
                    line = f.readline()
                    if len(line) == 0:
                        break
                    line = line.strip()
                    # if (idx % 1000) == 0:
                    #     print(f'{idx}')
                    # idx += 1
                    # print('{} > {}'.format(idx, line))
                    pbar.update()

                    splited = line.split(',')
                    if len(splited) != 8:
                        print(f'invalid item count {splited[0]}')
                        invaild_detected = True
                    img_name = splited[0]
                    img_full_path = os.path.join(image_path, img_name)
                    img_width = int(splited[1])
                    img_height = int(splited[2])
                    img_class = splited[3]
                    img_xmin = int(splited[4])
                    img_ymin = int(splited[5])
                    img_xmax = int(splited[6])
                    img_ymax = int(splited[7])
                    # print('{} > {} {} {} {}'
                    #       .format(img_name, img_xmin / img_width, \
                    #               img_ymin / img_height, img_xmax / img_width, img_ymax / img_height))
                    img_mat = cv2.imread(img_full_path)
                    h, w, c = img_mat.shape

                    if img_height != h or img_width != w:
                        print(f'not matched width, height {img_name} : {img_height} -> {h} , {img_width} -> {w}')
                        invaild_detected = True

                    if img_xmin == 0:
                        img_xmin += 1
                    if img_ymin == 0:
                        img_ymin += 1
                    if img_xmax > w or img_ymax > h:
                        print(f'xmax or ymax is greater than width or height {img_name} -> {img_xmax} {w} , {img_ymax} {h}  We will fixing')
                        if (img_xmax - w) == 1:
                            img_xmax = w
                        if (img_ymax - h) == 1:
                            img_ymax = h
                        invaild_detected = True
                    if (img_xmax - img_xmin) > img_width or \
                            (img_ymax - img_ymin) > img_height:
                        print(f'invalid rectangle {img_name}')
                        invaild_detected = True

                    new_f.write(f'{img_name},{img_width},{img_height},{img_class},{img_xmin},{img_ymin},{img_xmax},{img_ymax}\n')


    if invaild_detected == False:
        os.remove(new_csv_path)
        result = True
    else:
        print(f'data is invalid. please check the file [{new_csv_path}]')
    return result