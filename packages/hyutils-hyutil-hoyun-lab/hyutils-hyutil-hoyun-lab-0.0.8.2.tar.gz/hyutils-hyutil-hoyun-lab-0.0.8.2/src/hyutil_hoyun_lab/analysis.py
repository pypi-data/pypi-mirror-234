import os
from tqdm import tqdm
import matplotlib.pyplot as plt
import hyutil_hoyun_lab.dirjob as dirjob
import hyutil_hoyun_lab.xml_util as xmljob

SCALE_MAP = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def calc_scale(xml_path, input_size=None):
    global SCALE_MAP

    if input_size is None:
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