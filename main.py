#!/usr/bin/env python3
"""
Ver 1.0 - First version
Ver 2.0 - Uses database for match SUB file name and read Sublist.ini for match Sub string
Ver 3.0 - Uses GUI for parameter input
Ver 4.0 - Re-develop this application by Python3
Ver  4.1 - Add GUI
Ver 4.2 - Add convert  Sub file from simple chinese to TW traditional chinese function
"""
# import tkinter as tk

from tkinter import *
import tkinter.messagebox
import re
import configparser
import os
import replace_sub
import langconver

title = "Replace Sub"
version = "v4.02.00"
sub_database_name = "SubList.sdb"
sub_setting_name = "Settings.ini"
subpath = ""  # SUB file path, read from Settings.ini
subfiletype_list = ""  # SUB file type, read from Settings.ini, ex: *.ssa, *.ass


class replace_sub_gui(Frame):
    def __init__(self, master=None, subfilepath_ini=None, subfiletype_ini=None):
        Frame.__init__(self, master)
        self.subfiletype_list_ini = subfiletype_ini
        self.subpath_ini = subfilepath_ini
        self.user_input_path = ""
        self.user_input_type = ""
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        # -----First input entry-----
        self.sub_path_label = Label(self)
        self.sub_path_label["text"] = "SUB Path:"
        self.sub_path_label.grid(row=0, column=0)
        self.sub_path_entry = Entry(self)
        self.sub_path_entry["width"] = 60
        self.sub_path_entry.insert(0, self.subpath_ini)
        self.sub_path_entry.grid(row=0, column=1, columnspan=6)
        # -----File type entry
        self.sub_type_label = Label(self)
        self.sub_type_label["text"] = "SUB type:"
        self.sub_type_label.grid(row=1, column=0)
        self.sub_type_entry = Entry(self)
        self.sub_type_entry["width"] = 60
        self.sub_type_entry.insert(0, self.subfiletype_list_ini)
        self.sub_type_entry.grid(row=1, column=1, columnspan=6)
        # -----Button start-----
        self.start_button = Button(self)
        self.start_button["text"] = "Start"
        self.start_button["width"] = 5
        self.start_button["command"] = self.replace_all_sub_in_path
        self.start_button.grid(row=2, column=3)
        # -----Button Exit-----
        self.exit_button = Button(self)
        self.exit_button["text"] = "Help"
        self.exit_button["width"] = 5
        self.exit_button.grid(row=2, column=4)

        self.version_label = Label(self)
        self.version_label["text"] = version
        self.version_label["width"] = 6
        self.version_label.grid(row=3, column=6)

    def read_config(self, filename, section, key):
        config_lh = configparser.ConfigParser()
        file_ini_lh = open(filename, 'r', encoding='utf16')
        config_lh.read_file(file_ini_lh)
        file_ini_lh.close()
        return config_lh.get(section, key)

    def write_config(self, filename, sections, key, value):
        config_lh = configparser.ConfigParser()
        file_ini_lh = open(filename, 'r', encoding='utf16')
        config_lh.read_file(file_ini_lh)
        file_ini_lh.close()
        try:
            file_ini_lh = open(filename, 'w', encoding='utf16')
            config_lh.set(sections, key, value)
            config_lh.write(file_ini_lh)
            file_ini_lh.close()
        except Exception as ex:
            print('Error!!!! write fail')

    def conv_and_replace_sub_write_file(self, subfile_list, subdata_dic):
        status_lv = True

        # -----Test sub file format -----
        for i in subfile_list:
            try:
                subcontent_h = open(i, 'r+', encoding='utf8')
                sub_content_lv = subcontent_h.read()
            except:
                try:
                    subcontent_h.close()
                    subcontent_h = open(i, 'r+', encoding='utf16')
                    sub_content_lv = subcontent_h.read()
                except:
                    try:
                        subcontent_h.close()
                        subcontent_h = open(i, 'r', encoding='gbk')
                        sub_content_lv = subcontent_h.read()
                    except:
                        try:
                            subcontent_h.close()
                            subcontent_h = open(i, 'r', encoding='gb2312')
                            sub_content_lv = subcontent_h.read()
                        except:
                            status_lv = False
                            print("Error! can't read format:", i)
                            continue
                    # -----For GBK and GB2312 format -----
                    subcontent_h.close()
                    sub_content_temp_lv = sub_content_lv
                    # -----convert to TC language
                    tw_str_lv = langconver.s2tw(sub_content_lv)
                    tw_str_lv = replace_sub.replace_specif_string(tw_str_lv, subdata_dic)
                    if sub_content_temp_lv != tw_str_lv:
                        subcontent_write_h = open(i, 'w', encoding='utf8')
                        subcontent_write_h.seek(0, 0)
                        subcontent_write_h.write(tw_str_lv)
                        subcontent_write_h.close()
                    continue
            # -----for utf8 and utf16 format -----
            sub_content_temp_lv = sub_content_lv
            # -----convert to TC language
            tw_str_lv = langconver.s2tw(sub_content_lv)
            tw_str_lv = replace_sub.replace_specif_string(tw_str_lv, subdata_dic)
            # -----if sub file content is changed, write to origin file -----
            if sub_content_temp_lv != tw_str_lv:
                subcontent_h.seek(0, 0)
                subcontent_h.write(tw_str_lv)
            subcontent_h.close()
        return status_lv

    def replace_all_sub_in_path(self):
        # -----Get user input path-----
        self.user_input_path = self.sub_path_entry.get()
        # -----Get user input file types and Split type string then store to list-----
        self.user_input_type = self.sub_type_entry.get()
        # -----Check user input in GUI -----
        if self.user_input_path == "" or self.user_input_type == "":
            tkinter.messagebox.showinfo("message box", "Please input SUB file PATH and TYPE")
            return
        if not os.path.exists(self.user_input_path):
            tkinter.messagebox.showinfo("message box", "Error! can't find sub path")
            return

        # -----get config ini file setting -----
        self.subpath_ini = self.read_config(sub_setting_name, 'Global', 'subpath')
        self.subfiletype_list_ini = self.read_config(sub_setting_name, 'Global', 'subtype')

        # -----remove '\' or '/' in end of path string -----
        self.user_input_path = re.sub(r"/$", '', self.user_input_path)
        self.user_input_path = re.sub(r"\\$", "", self.user_input_path)

        # -----Store user input path and type into Setting.ini config file -----
        if not self.user_input_path == self.subpath_ini:
            print("path not match, write new path to ini")
            self.write_config(sub_setting_name,  'Global', 'subpath', self.user_input_path)
        if not self.user_input_type == self.subfiletype_list_ini:
            print("type not match, write new type list to ini")
            self.write_config(sub_setting_name, 'Global', 'subtype', self.user_input_type)

        # ----Split file type string and store to list
        re_lv = re.sub(r' ', '', self.user_input_type)
        self.user_input_type = re_lv.split(",")

        # Get sub file list by type
        sub_file_list = replace_sub.get_file_list(self.user_input_path, self.user_input_type)
        # Replace all file list string by dic structure
        # replace_sub.replace_string_write_to_file(sub_file_list, sub_data_dic)
        status = self.conv_and_replace_sub_write_file(sub_file_list, sub_data_dic)

        if status:
            tkinter.messagebox.showinfo("message box", "Replace All Sub Done.")
        else:
            tkinter.messagebox.showinfo("message box", "Error! Replace Sub error, please check log file.")
        # for i in self.user_input_type:
        #     print(i)

def check_all_file_status():
    if not os.path.exists(sub_database_name):
        return False
    if not os.path.exists(sub_setting_name):
        return False
    return True

# Check database is correct or not
if not check_all_file_status():
    tkinter.messagebox.showinfo("message box", "Error! SubList.sdb and Setting.ini not found or empty")
else:
    # Get database list to dic structure
    sub_data_dic = replace_sub.get_database_list(sub_database_name)
    # Get setting from Settings.ini
    file_ini_h = open(sub_setting_name, encoding='utf16')
    config_h = configparser.ConfigParser()
    config_h.read_file(file_ini_h)
    file_ini_h.close()
    subpath = config_h.get('Global', 'subpath')
    subfiletype_list = config_h.get('Global', 'subtype')

    # Start GUI
    if __name__ == '__main__':
        root = Tk()
        root.title(title)
        root.iconbitmap('icons\\main.ico')
        app = replace_sub_gui(master=root, subfilepath_ini=subpath, subfiletype_ini=subfiletype_list)
        app.mainloop()
