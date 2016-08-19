#!/usr/bin/env python3
"""
Ver 1.0 - First version
Ver 2.0 - Uses database for match SUB file name and read Sublist.ini for match Sub string
Ver 3.0 - Uses GUI for parameter input
Ver 4.0 - Re-develop this application by Python3
Ver 4.1 - Add GUI
Ver 4.2 - Add convert  Sub file from simple chinese to TW traditional chinese function
Ver 4.2.1 - Add backup original sub file function
Ver 4.2.2 - Add About content, modify message box type for different message type
Ver 4.2.3 - Modify About content
"""

from tkinter import *
import tkinter.messagebox
import re
import configparser
import os
import shutil

import replace_sub
import langconver

title = "AJSub - 強力轉換! 轉碼君"
version = "v4.02.04"
sub_database_name = "SubList.sdb"
sub_setting_name = "Settings.ini"
backup_folder_name = "backfile"
subpath = ""  # SUB file path, read from Settings.ini
subfiletype_list = ""  # SUB file type, read from Settings.ini, ex: *.ssa, *.ass
progress_txt = "強力轉換中..."
idle_txt = "zzz..."
help_text = \
    "AJSub "+version+"\n\n"\
    "   本軟體會自動將指定目錄下的所有字幕檔簡體轉為繁體\n"\
    "   字型設定部份會轉為簡體, 這樣使用某些字型時系統才會認得\n"\
    "   (例如方正系列的字型)\n"\
    "   UTF-8與UTF-16檔會照原格式儲存, 其餘會自動轉UTF-8格式\n"\
    "   原始檔案備份在:"+backup_folder_name+"目錄下\n\n"\
    "   使用說明:\n"\
    "   1. 將字幕檔路徑輸入SUB type欄位\n"\
    "   2. 輸入字幕檔類型並用逗點隔開, 如*.ass, *.ssa\n"\
    "   3. 按下Start之後, enjoy it!!!!\n"\
    "   4. 字型設定若需新增或修改, 請直接修改SubList.sdb\n\n"\
    "AJSub "+version+"\n"\
    "Copyright 2016\n\n"\
    "Implement by [Llona](https://github.com/Llona/AJ-sub).\n\n"\
    "This product includes OpenCC-python, develop by:\n"\
    "[Yichen (Eugene)](https://github.com/yichen0831/opencc-python).\n"\



class replace_Sub_Gui(Frame):
    def __init__(self, master=None, subfilepath_ini=None, subfiletype_ini=None, help_text=None):
        Frame.__init__(self, master)
        self.subfiletype_list_ini = subfiletype_ini
        self.subpath_ini = subfilepath_ini
        self.help_text = help_text
        self.user_input_path = ""
        self.user_input_type = ""
        self.grid()
        self.thread_is_running = False
        self.create_widgets()

        root.bind('<Key-Return>', self.press_key_enter)

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
        # -----Button Start-----
        self.start_button = Button(self)
        self.start_button["text"] = "Start"
        self.start_button["width"] = 5
        self.start_button["command"] = self.replace_all_sub_in_path
        self.start_button.grid(row=2, column=2, columnspan=2)
        # -----Button Help-----
        self.help_button = Button(self)
        self.help_button["text"] = "Help"
        self.help_button["width"] = 5
        self.help_button["command"] = self.print_about
        self.help_button.grid(row=2, column=3, columnspan=2)
        # -----Label version-----
        self.version_label = Label(self)
        self.version_label["text"] = version
        self.version_label["width"] = 6
        self.version_label["state"] = 'disable'
        self.version_label.grid(row=3, column=6, columnspan=2)
        # -----Label state-----
        self.version_state = Label(self)
        self.version_state["text"] = ""
        self.version_state["width"] = 15
        self.version_state.grid(row=3, column=0, columnspan=2, sticky='w')
        # self.version_state.grid(row=3, column=0, sticky='w')

    def press_key_enter(self, event):
        self.replace_all_sub_in_path()

    def print_about(self):
        tkinter.messagebox.showinfo("About", self.help_text)

    def create_popup(self):
        pass
        # self.top_window = Toplevel()
        # self.top_window.overrideredirect(1)
        # msg = Label(self.top_window, text="轉換工作進行中...")
        # root.update_idletasks()
        # msg.pack(side=TOP, anchor=W, fill=X, expand=YES)
        # self.top_window['takefocus'] = True
        # self.top_window.grab_set()
        # self.top_window.focus_force()
        # msg.focus()
        # msg.grab_set()
        # root.update_idletasks()

    def close_popup(self):
        #self.top_window.destroy()
        pass

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

    def store_origin_file_to_backup_folder(self, file, back_folder):
        shutil.copy2(file, back_folder)

    def conv_and_replace_sub_write_file(self, subfile_list, subdata_dic):
        status_lv = True

        for i in subfile_list:
            # -----Test sub file format-----
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
                    # -----For GBK and GB2312 format-----
                    subcontent_h.close()
                    # -----backup origin sub file to backup folder-----
                    self.store_origin_file_to_backup_folder(i, self.user_input_path+'\\'+backup_folder_name)
                    sub_content_temp_lv = sub_content_lv
                    # -----convert to TC language-----
                    tw_str_lv = langconver.s2tw(sub_content_lv)
                    tw_str_lv = replace_sub.replace_specif_string(tw_str_lv, subdata_dic)
                    if sub_content_temp_lv != tw_str_lv:
                        subcontent_write_h = open(i, 'w', encoding='utf8')
                        subcontent_write_h.seek(0, 0)
                        subcontent_write_h.write(tw_str_lv)
                        subcontent_write_h.close()
                    continue

            # -----backup origin sub file to backup folder-----
            self.store_origin_file_to_backup_folder(i, self.user_input_path + '\\' + backup_folder_name)
            # -----for utf8 and utf16 format-----
            sub_content_temp_lv = sub_content_lv
            # -----convert to TC language-----
            tw_str_lv = langconver.s2tw(sub_content_lv)
            tw_str_lv = replace_sub.replace_specif_string(tw_str_lv, subdata_dic)
            # -----if sub file content is changed, write to origin file-----
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
        # -----Check user input in GUI-----
        if self.user_input_path == "" or self.user_input_type == "":
            tkinter.messagebox.showinfo("message", "Please input SUB file PATH and TYPE")
            return
        if not os.path.exists(self.user_input_path):
            tkinter.messagebox.showerror("message", "Error! can't find sub path")
            return

        # -----get config ini file setting-----
        self.subpath_ini = self.read_config(sub_setting_name, 'Global', 'subpath')
        self.subfiletype_list_ini = self.read_config(sub_setting_name, 'Global', 'subtype')

        # -----remove '\' or '/' in end of path string-----
        self.user_input_path = re.sub(r"/$", '', self.user_input_path)
        self.user_input_path = re.sub(r"\\$", "", self.user_input_path)

        # -----Store user input path and type into Setting.ini config file-----
        if not self.user_input_path == self.subpath_ini:
            print("path not match, write new path to ini")
            self.write_config(sub_setting_name,  'Global', 'subpath', self.user_input_path)
        if not self.user_input_type == self.subfiletype_list_ini:
            print("type not match, write new type list to ini")
            self.write_config(sub_setting_name, 'Global', 'subtype', self.user_input_type)

        # ----Split file type string and store to list-----
        re_lv = re.sub(r' ', '', self.user_input_type)
        self.user_input_type = re_lv.split(",")

        # -----Dim button for string converting-----
        self.version_state["text"] = progress_txt
        self.version_state["fg"] = "blue"
        self.start_button["state"] = 'disable'
        self.help_button["state"] = 'disable'
        self.update_idletasks()

        # -----Get sub file list by type-----
        sub_file_list = replace_sub.get_file_list(self.user_input_path, self.user_input_type)
        # -----make backup folder for store origin sub files-----
        if not os.path.exists(self.user_input_path+'\\'+backup_folder_name):
            os.makedirs(self.user_input_path+'\\'+backup_folder_name)
        # -----Replace all file list string by dic structure-----
        status = self.conv_and_replace_sub_write_file(sub_file_list, sub_data_dic)

        # -----Set button and progressing state to normal-----
        self.version_state["text"] = ""
        self.start_button["state"] = 'normal'
        self.help_button["state"] = 'normal'
        self.update_idletasks()

        if status:
            tkinter.messagebox.showinfo("message", "Replace All Sub Done.")
        else:
            tkinter.messagebox.showerror("message Error", "Error! Replace Sub error, please check log file.")


def check_all_file_status():
    if not os.path.exists(sub_database_name):
        return False
    if not os.path.exists(sub_setting_name):
        return False
    return True


# -----Check database is correct or not-----
if not check_all_file_status():
    tkinter.messagebox.showinfo("message Error", "Error! SubList.sdb and Setting.ini not found or empty")
else:
    # -----Get database list to dic structure-----
    sub_data_dic = replace_sub.get_database_list(sub_database_name)
    # -----Get setting from Settings.ini-----
    file_ini_h = open(sub_setting_name, encoding='utf16')
    config_h = configparser.ConfigParser()
    config_h.read_file(file_ini_h)
    file_ini_h.close()
    subpath = config_h.get('Global', 'subpath')
    subfiletype_list = config_h.get('Global', 'subtype')

    # -----Start GUI-----
    if __name__ == '__main__':
        root = Tk()
        root.title(title)
        root.iconbitmap('icons\\main.ico')
        app = replace_Sub_Gui(master=root, subfilepath_ini=subpath, subfiletype_ini=subfiletype_list, help_text=help_text)
        app.mainloop()
