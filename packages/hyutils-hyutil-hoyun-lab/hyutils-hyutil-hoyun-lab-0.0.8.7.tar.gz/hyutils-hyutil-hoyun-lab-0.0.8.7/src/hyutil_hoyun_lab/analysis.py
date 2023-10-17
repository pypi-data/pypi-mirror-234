import os
from tqdm import tqdm
import matplotlib.pyplot as plt
import hyutil_hoyun_lab.dirjob as dirjob
import hyutil_hoyun_lab.xml_util as xmljob

#          0     1.0  2.0  3.0  4.0  5.0   6.0  7.0  8.0  9.0   10.0
SCALE_MAP = [0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0]
#         0    16  32  64  128  512
SIZE_MAP = [0,   0,   0,   0,   0,   0]

def calc_scale(xml_path, input_size=None):
    global SCALE_MAP

    if input_size is None:
        return

    if input_size.find('x') == -1:
        return

    input_size_h, input_size_w = input_size.split('x')
    input_h = int(input_size_h)
    input_w = int(input_size_w)

    if os.path.exists(xml_path):
        count = dirjob.get_entry_count(xml_path, '.xml')
        pbar = tqdm(total=count)

        length = len(SCALE_MAP)
        for file in dirjob.files_ext(xml_path, '.xml'):
            final_xml_file = os.path.join(xml_path, file)
            if os.path.exists(final_xml_file):
                is_ok, xml_infos = xmljob.read_xml(final_xml_file)
                if is_ok == True and len(xml_infos) > 0:
                    for xml_info in xml_infos:
                        o_h = int(xml_info[1])
                        o_w = int(xml_info[2])
                        x_diff = int(xml_info[6]) - int(xml_info[4])
                        y_diff = int(xml_info[7]) - int(xml_info[5])
                        h_ratio = input_h / o_h
                        w_ratio = input_w / o_w
                        new_grount_truth_h = y_diff * h_ratio
                        new_ground_truth_w = x_diff * w_ratio
                        ratio = int(float(new_ground_truth_w / new_grount_truth_h))  # width / height

                        if ratio < (length - 1):
                            SCALE_MAP[ratio] = SCALE_MAP[ratio] + 1
                        else:
                            SCALE_MAP[length - 1] = SCALE_MAP[length - 1] + 1
            pbar.update()


        ret_file = os.path.join(xml_path, 'aspect_ratios.txt')
        with open(ret_file, 'wt') as new_f:
            bar_title = []
            bar_value = []
            for idx in range(0, length):
                bar_title.append(str(idx))
                bar_value.append(SCALE_MAP[idx])
                new_f.write(f'aspect ratio {idx} : {SCALE_MAP[idx]}\n')
            plt.bar(bar_title, bar_value)
            plt.show(block=True)

def calc_size_dist(xml_path, input_size=None):
    global SIZE_MAP
    #             0   16  32   64  128  512
    # SIZE_MAP = [0,  0,  0,   0,   0,   0]

    if input_size is None:
        return

    if input_size.find('x') == -1:
        return

    input_size_h, input_size_w = input_size.split('x')
    input_h = int(input_size_h)
    input_w = int(input_size_w)

    if os.path.exists(xml_path):
        count = dirjob.get_entry_count(xml_path, '.xml')
        pbar = tqdm(total=count)

        length = len(SIZE_MAP) # 6
        for file in dirjob.files_ext(xml_path, '.xml'):
            final_xml_file = os.path.join(xml_path, file)
            if os.path.exists(final_xml_file):
                is_ok, xml_infos = xmljob.read_xml(final_xml_file)
                if is_ok == True and len(xml_infos) > 0:
                    for xml_info in xml_infos:
                        o_h = int(xml_info[1])
                        o_w = int(xml_info[2])
                        x_diff = int(xml_info[6]) - int(xml_info[4])
                        y_diff = int(xml_info[7]) - int(xml_info[5])
                        h_ratio = input_h / o_h
                        w_ratio = input_w / o_w

                        new_size_h = y_diff * h_ratio
                        new_size_w = x_diff * w_ratio

                        #             0   16  32   64  128  512
                        # SIZE_MAP = [0,  0,  0,   0,   0,   0]

                        if new_size_h < 16:
                            SIZE_MAP[0] = SIZE_MAP[0]  + 1
                        elif new_size_h < 32:
                            SIZE_MAP[1] = SIZE_MAP[1] + 1
                        elif new_size_h < 64:
                            SIZE_MAP[2] = SIZE_MAP[2] + 1
                        elif new_size_h < 128:
                            SIZE_MAP[3] = SIZE_MAP[3] + 1
                        elif new_size_h < 512:
                            SIZE_MAP[4] = SIZE_MAP[4] + 1
                        else:
                            SIZE_MAP[5] = SIZE_MAP[5] + 1

                        if new_size_w < 16:
                            SIZE_MAP[0] = SIZE_MAP[0] + 1
                        elif new_size_w < 32:
                            SIZE_MAP[1] = SIZE_MAP[1] + 1
                        elif new_size_w < 64:
                            SIZE_MAP[2] = SIZE_MAP[2] + 1
                        elif new_size_w < 128:
                            SIZE_MAP[3] = SIZE_MAP[3] + 1
                        elif new_size_w < 512:
                            SIZE_MAP[4] = SIZE_MAP[4] + 1
                        else:
                            SIZE_MAP[5] = SIZE_MAP[5] + 1

            pbar.update()

        ret_file = os.path.join(xml_path, 'size_distribute.txt')
        with open(ret_file, 'wt') as new_f:
            bar_title = []
            bar_value = []
            tmp = 16
            for idx in range(0, length):
                idx2 = tmp - 1
                tmp = tmp * 2
                if idx == 0:
                    bar_title.append(str(idx + 1) + '-' + str(idx2))
                else:
                    bar_title.append(str(int((idx2 + 1) / 2)) + '-' + str(idx2))
                bar_value.append(SIZE_MAP[idx])
                new_f.write(f'size_distribute {idx} : {SIZE_MAP[idx]}\n')
            plt.bar(bar_title, bar_value)
            plt.show(block=True)