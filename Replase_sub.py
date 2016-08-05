#!/usr/bin/python3
"""
Ver 1.0 - First version
Ver 2.0 - Uses database for match SUB file name and read Sublist.ini for match Sub string
Ver 3.0 - Uses GUI for parameter input
Ver 4.0 - Re-develop this application by Python3
"""
import glob
import os
import re

subdata_dic = {}  # sub database
subpath = 'D:\ScripFile\python\Replase_sub\\test_sub'  # ssa or ass sub file path
subfile_list = []  # All sub file list that wait to replace
subfiletype_list = ['*.ssa', '*.ass']  # sub file type, ex: *.ssa ,*.ass...

"""
# -----Read sub databse file SubList.sdb and store to dict structure-----
Return: string database store in dic structure
"""
def get_database_list():
    subdata_dic_ld = {}
    subdata_tmp_lv = ''

    sublist_h = open("SubList.sdb", 'r', encoding='utf16')
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

"""
# -----Get all sub file list that need to replace-----
1. sub_path: sub file path
2. sub file type (example: *.ssa, *.ass)
Return: all sub file list
"""
def get_file_list(sub_path, file_type):
    subfile_list_ll = []
    subtemp_list_ll = []  # temp var for store sub list

    os.chdir(sub_path)
    for i in file_type:
        subtemp_list_ll = glob.glob(i)
        if subtemp_list_ll:
            subfile_list_ll.extend(subtemp_list_ll)
    return subfile_list_ll

"""
# -----Read all sub file and replace string that define in database file-----
1. sub file list
2. string database store in dic structure
Return: none
"""
def replace_string_write_to_file(subfile_list, subdata_dic):
    for i in subfile_list:
        sub_content_lv = ''
        sub_content_temp_lv = ''

        subcontent_read_h = open(i, 'r+', encoding='utf16')
        sub_content_lv = subcontent_read_h.read()
        sub_content_temp_lv = sub_content_lv

        for j, v in subdata_dic.items():
            #print(j, v)
            sub_content_lv = sub_content_lv.replace(j, v)
        if sub_content_temp_lv != sub_content_lv:
            subcontent_read_h.seek(0, 0)
            subcontent_read_h.write(sub_content_lv)
            # print("Find string need to modify")
        else:
            pass
            print("Sub file doesn't need to change:", i)
        # print(sub_content)
        subcontent_read_h.close()


# Get database list to dic structure
subdata_dic = get_database_list()
# Get sub file list by type
subfile_list = get_file_list(subpath, subfiletype_list)
# Replace all file list string by dic structure
replace_string_write_to_file(subfile_list, subdata_dic)

print("Replace Done")
