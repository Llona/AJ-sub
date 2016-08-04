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
subfile_list = "" #All sub file list that wait to replase
sub_content = "" #var for store sub file sub_content


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

#-----Read ssa file-----
os.chdir(subpath)
subfile_list = glob.glob('*.ass')
#subfile_list.append(glob.glob('*.ssa'))
print (subfile_list)

for i in subfile_list:
    subcontent_h = open(i, 'r', encoding='utf16')
    sub_content = subcontent_h.read()
    #print(sub_content)

subcontent_h.close()

#sublist = sublist_h.read()


#for k, v in sublist_h.():
#    print(k, v)



