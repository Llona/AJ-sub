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
    os.chdir(sub_path)

    for i in file_type:
        subtemp_list_ll = glob.glob(i)
        if subtemp_list_ll:
            subfile_list_ll.extend(subtemp_list_ll)

    return subfile_list_ll


# # -----Read all sub file and replace string that define in database file-----
# 1. sub file list
# 2. string database store in dic structure
# Return: none
def replace_string_write_to_file(subfile_list, subdata_dic):

    for i in subfile_list:
        subcontent_read_h = open(i, 'r+', encoding='utf16')
        sub_content_lv = subcontent_read_h.read()
        sub_content_temp_lv = sub_content_lv

        for j, v in subdata_dic.items():
            # print(j, v)
            sub_content_lv = sub_content_lv.replace(j, v)

        if sub_content_temp_lv != sub_content_lv:
            subcontent_read_h.seek(0, 0)
            subcontent_read_h.write(sub_content_lv)
            print("Find string need to modify")
        else:
            pass
            print("Sub file doesn't need to change:", i)

        subcontent_read_h.close()
