#!/usr/bin/env python3
"""
Ver 1.0 - First version
Ver 2.0 - Uses database for match SUB file name and read Sublist.ini for match Sub string
Ver 3.0 - Uses GUI for parameter input
Ver 4.0 - Re-develop this application by Python3
"""
# import tkinter as tk
import replace_sub

subpath = 'D:\ScripFile\python\Replase_sub\\test_sub'  # ssa or ass sub file path
subfiletype_list = ['*.ssa', '*.ass']  # sub file type, ex: *.ssa ,*.ass...
sub_database_name = "SubList.sdb"
sub_file_list = []  # All sub file list that wait to replace
subdata_dic = {}  # sub database

#
# def btn_call_back():
#     print("Hello World.")
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     button = tk.Button(master=root,text="hello", command=btn_call_back)
#     text = tk.Entry()
#     text.pack()
#     button.pack()
#     root.mainloop()

# Get database list to dic structure
sub_data_dic = replace_sub.get_database_list(sub_database_name)
# Get sub file list by type
sub_file_list = replace_sub.get_file_list(subpath, subfiletype_list)
# Replace all file list string by dic structure
replace_sub.replace_string_write_to_file(sub_file_list, sub_data_dic)
print("Replace Done!!!")
