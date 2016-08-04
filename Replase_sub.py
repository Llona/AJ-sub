#!/usr/bin/python3
"""
Ver 1.0 - First version
Ver 2.0 - Uses database for match SUB file name and read Sublist.ini for match Sub string
Ver 3.0 - Uses GUI for parameter input
Ver 4.0 - Re-develop this application by Python3
"""
import re
import os
import glob

subdata_tmp = "" #Temp var for read file line
subdata_dic = {} #sub database
subpath = 'D:\ScripFile\python\Replase_sub\\test_sub' #ssa or ass sub file path
subfile_list = [] #All sub file list that wait to replase
subtemp_list = [] #temp var for store sub list
sub_content = "" #var for store sub file's content
subfiletype_list = ['*.ssa', '*.ass'] #sub file type, ex: *.ssa ,*.ass...

#-----Read sub databse file SubList.sdb and store to dict structure-----
sublist_h = open("SubList.sdb", 'r', encoding='utf16')
while True:
    subdata_tmp = sublist_h.readline()
    if subdata_tmp:
        re_h = re.match(r'(.+);(.+)', subdata_tmp)
        subdata_dic[re_h.group(1)] = re_h.group(2)
        #print(re_h.group(1), re_h.group(2))
    else:
        break

sublist_h.close()

#-----Get all sub file list that need to replace-----
os.chdir(subpath)
for i in subfiletype_list:
    subtemp_list=glob.glob(i)
    if subtemp_list:
        subfile_list.extend(subtemp_list)


#-----Read all sub file and replace string that define in database file-----
for i in subfile_list:
    subcontent_read_h = open(i, 'r+', encoding='utf16')
    sub_content = subcontent_read_h.read()
    sub_content_temp = sub_content

    for j, v in subdata_dic.items():
        #print(j,v)
        #strinfo_h = re.compile(j)
        #sub_content = strinfo_h.sub(v, sub_content)
        sub_content = sub_content.replace(j,v)
    if sub_content_temp != sub_content:
        subcontent_read_h.seek(0,0)
        subcontent_read_h.write(sub_content)
        #print("Find string need to modify")
    else:
        #print("")

    print(sub_content)
    sub_content = ''  #clean temp var
    sub_content_temp = '' #clean temp var
    subcontent_read_h.close()
