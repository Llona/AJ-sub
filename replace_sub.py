#!/usr/bin/python3
"""
Provide function that for replace sub string need
"""
import glob
import os
import re


# # -----Read sub databse file SubList.sdb and store to dict structure-----
# 1. sub database file name
# Return: string database store in dic structure
def get_database_list(sub_database):
    subdata_dic_ld = {}

    if not os.path.exists(sub_database):
        return 0

    sublist_h = open(sub_database, 'r', encoding='utf16')

    while True:
        subdata_tmp_lv = sublist_h.readline()
        if subdata_tmp_lv:
            re_h = re.match(r'(.+);(.+)', subdata_tmp_lv)
            subdata_dic_ld[re_h.group(1)] = re_h.group(2)
            # print(re_h.group(1), re_h.group(2))
        else:
            break

    sublist_h.close()
    return subdata_dic_ld


# # -----Get all sub file list that need to replace-----
# 1. sub_path: sub file path
# 2. sub file type (example: *.ssa, *.ass)
# Return: all sub file list
def get_file_list(sub_path, file_type):
    subfile_list_ll = []
    file_ext_ll = []

    # os.chdir(sub_path)

    dir_list = os.listdir(sub_path)

    for type in file_type:
        ext = os.path.splitext(type)
        file_ext_ll.append(ext[1])

    for file_ext in file_ext_ll:
        for file in dir_list:
            file_full_path = os.path.join(sub_path, file)
            if os.path.isfile(file_full_path) and file.endswith(file_ext):
                subfile_list_ll.append(file_full_path)
        # subtemp_list_ll = glob.glob('%s\\%s' % (sub_path, i))
        # subtemp_list_ll = glob.glob(i)
        # if subtemp_list_ll:
        #     subfile_list_ll.extend(subtemp_list_ll)

    # os.chdir(app_current_path)
    return subfile_list_ll


def get_all_sub_folder_name(folder_path):
    sub_folder_list = []
    root = ""
    for root_n, dirs, files in os.walk(folder_path, topdown=False):
        root = root_n
        for name in dirs:
            sub_folder_list.append(os.path.join(root_n, name))
            # print(os.path.join(root_n, name))
    sub_folder_list.append(root)
    return sub_folder_list

# -----Read all sub file and replace string that define in database file-----
# 1. sub file list
# 2. string database store in dic structure
# Return: none
def replace_specif_string(content, subdata_dic):
    for j, v in subdata_dic.items():
        # print(j, v)
        content = content.replace(j, v)
    return content
