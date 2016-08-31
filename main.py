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
Ver 4.3.0 -
    1. Add log widge and print log into log widge
    2. Add convert clipboard function
    3. Modify main process for error handling
    4. Add R/W setting file error handling
Ver 4.3.5 - Add rename sub file to match video file name
"""

from tkinter import *
from tkinter.ttk import *
from tkinter.font import Font
import tkinter.messagebox
import re
import configparser
import os
import shutil
# from tkinter.scrolledtext import ScrolledText
# from time import sleep
# from tkinter.commondialog import Dialog
from enum import Enum

import replace_sub
import langconver
import ajrename

title = "AJSub - 強力轉換! 轉碼君"
version = "v4.03.50"
sub_database_name = "SubList.sdb"
sub_setting_name = "Settings.ini"
backup_folder_name = "backfile"
subpath = ""  # SUB file path, read from Settings.ini
subfiletype_list = ""  # SUB file type, read from Settings.ini, ex: *.ssa, *.ass
progress_txt = "強力轉換中..."
progress_idle_txt = ""
progress_done_txt = "轉換完成!!"
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
    "   4. 字型設定若需新增或修改, 請直接修改SubList.sdb\n"\
    "   5. 按下Convert Clipboard後, 直接將剪貼簿的內容轉換為繁體\n\n"\
    "AJSub "+version+"\n"\
    "Copyright 2016\n\n"\
    "Implement by [Llona](https://github.com/Llona/AJ-sub).\n\n"\
    "This product includes OpenCC-python, develop by:\n"\
    "[Yichen (Eugene)](https://github.com/yichen0831/opencc-python).\n"\



class error_Type(Enum):
    NORMAL = 'NORMAL'  # define normal state
    FILE_ERROR = 'FILE_RW_ERROR'  # define file o/r/w error type


class replace_Sub_Gui(Frame):
    def __init__(self, master=None, subfilepath_ini=None, subfiletype_ini=None, help_text=None):
        Frame.__init__(self, master)
        self.master = master
        self.subfiletype_list_ini = subfiletype_ini
        self.subpath_ini = subfilepath_ini
        self.help_text = help_text
        self.user_input_path = ""
        self.user_input_type = ""
        self.app_current_path_lv = os.getcwd()
        # self.checkbutton_select = IntVar()
        # self.grid()
        # # -----Define all GUI item-----
        # self.sub_path_label = Label(self)
        # self.sub_path_entry = Entry(self)
        # self.sub_type_label = Label(self)
        # self.sub_type_entry = Entry(self)
        # self.rename_button = Button(self)
        # self.start_button = Button(self)
        # self.help_button = Button(self)
        # self.clip_button = Button(self)
        # self.empty_label = Label(self)
        # self.version_label = Label(self)
        # self.version_state = Label(self)
        # # self.hide_log_button = Button(self)
        # self.shlog_chbutton = Checkbutton(self)
        # # self.log_txt = ScrolledText(self, wrap='none', state="disabled")
        # # self.ren_frame_oriview_txt = Text(self, wrap='none', state="disabled")
        # self.vert_scrollbar = Scrollbar(self, orient=VERTICAL)
        # self.hor_scrollbar = Scrollbar(self, orient='horizontal')
        # self.log_txt = Text(self, wrap='none', state="disabled",
        #                     yscrollcommand=self.vert_scrollbar.set, xscrollcommand=self.hor_scrollbar.set)

        # -----Set Text log fone color-----


        root.bind('<Key-Return>', self.press_key_enter)

        self.create_widgets()

    def create_widgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.style.configure('Tuser_input_frame.TLabelframe', font=('iLiHei',9))
        self.style.configure('Tuser_input_frame.TLabelframe.Label', font=('iLiHei',9))
        self.user_input_frame = LabelFrame(self.top, text='輸入', style='Tuser_input_frame.TLabelframe')
        self.user_input_frame.place(relx=0.01, rely=0.013, relwidth=0.981, relheight=0.262)

        self.shlog_chbuttonVar = IntVar(value=0)
        self.style.configure('Tshlog_chbutton.TCheckbutton', font=('iLiHei',9))
        self.shlog_chbutton = Checkbutton(self.top, text='Show log', variable=self.shlog_chbuttonVar, style='Tshlog_chbutton.TCheckbutton')
        self.shlog_chbutton.place(relx=0.02, rely=0.235, relwidth=0.103, relheight=0.028)

        self.style.configure('Tlog_frame.TLabelframe', font=('iLiHei',9))
        self.style.configure('Tlog_frame.TLabelframe.Label', font=('iLiHei',9))
        self.log_frame = LabelFrame(self.top, text='log', style='Tlog_frame.TLabelframe')
        self.log_frame.place(relx=0.01, rely=0.287, relwidth=0.981, relheight=0.705)

        self.style.configure('Tsub_type_label.TLabel', anchor='w', font=('iLiHei',10))
        self.sub_type_label = Label(self.user_input_frame, text='SUB type:', style='Tsub_type_label.TLabel')
        self.sub_type_label.place(relx=0.01, rely=0.398, relwidth=0.074, relheight=0.205)

        self.sub_path_entryVar = StringVar(value=self.subpath_ini)
        self.sub_path_entry = Entry(self.user_input_frame, textvariable=self.sub_path_entryVar, font=('iLiHei',10))
        self.sub_path_entry.place(relx=0.094, rely=0.099, relwidth=0.698, relheight=0.155)

        self.style.configure('Trename_button.TButton', font=('iLiHei',9))
        self.rename_button = Button(self.user_input_frame, text='Sub Rename', command=self.show_rename_frame, style='Trename_button.TButton')
        self.rename_button.place(relx=0.822, rely=0.099, relwidth=0.137, relheight=0.205)

        self.style.configure('Tstart_button.TButton', font=('iLiHei',9))
        self.start_button = Button(self.user_input_frame, text='Start', command=self.replace_all_sub_in_path, style='Tstart_button.TButton')
        self.start_button.place(relx=0.302, rely=0.745, relwidth=0.105, relheight=0.205)

        self.style.configure('Thelp_button.TButton', font=('iLiHei',9))
        self.help_button = Button(self.user_input_frame, text='Help', command=self.print_about, style='Thelp_button.TButton')
        self.help_button.place(relx=0.531, rely=0.745, relwidth=0.105, relheight=0.205)

        self.style.configure('Tclip_button.TButton', font=('iLiHei',9))
        self.clip_button = Button(self.user_input_frame, text='Convert Clipboard', command=self.convert_clipboard, style='Tclip_button.TButton')
        self.clip_button.place(relx=0.822, rely=0.447, relwidth=0.137, relheight=0.205)

        self.style.configure('Tsub_path_label.TLabel', anchor='w', font=('iLiHei',10))
        self.sub_path_label = Label(self.user_input_frame, text='SUB Path:', style='Tsub_path_label.TLabel')
        self.sub_path_label.place(relx=0.01, rely=0.099, relwidth=0.072, relheight=0.149)

        self.style.configure('Tversion_state.TLabel', anchor='e', font=('iLiHei',9))
        self.version_state = Label(self.user_input_frame, text='idle', style='Tversion_state.TLabel')
        self.version_state.place(relx=0.863, rely=0.845, relwidth=0.116, relheight=0.106)

        self.sub_type_entryVar = StringVar(value=self.subfiletype_list_ini)
        self.sub_type_entry = Entry(self.user_input_frame, textvariable=self.sub_type_entryVar, font=('iLiHei',10))
        self.sub_type_entry.place(relx=0.094, rely=0.398, relwidth=0.698, relheight=0.155)

        self.VScroll1 = Scrollbar(self.log_frame, orient='vertical')
        self.VScroll1.place(relx=0.967, rely=0.018, relwidth=0.022, relheight=0.926)

        self.HScroll1 = Scrollbar(self.log_frame, orient='horizontal')
        self.HScroll1.place(relx=0.01, rely=0.942, relwidth=0.958, relheight=0.039)

        self.log_txtFont = Font(font=('iLiHei',10))
        self.log_txt = Text(self.log_frame, xscrollcommand=self.HScroll1.set, yscrollcommand=self.VScroll1.set, font=self.log_txtFont)
        self.log_txt.place(relx=0.01, rely=0.018, relwidth=0.958, relheight=0.926)
        self.log_txt.insert('1.0','')
        self.HScroll1['command'] = self.log_txt.xview
        self.VScroll1['command'] = self.log_txt.yview


        # -----Scrollbar for log text wiege-----
        # self.hor_scrollbar.config(command=self.log_txt.xview)
        # self.vert_scrollbar.config(command=self.log_txt.yview)
        # self.vert_scrollbar.grid(row=5, column=7, columnspan=8, sticky='NS')
        # self.hor_scrollbar.grid(row=6, column=0, columnspan=8, sticky='EW')
        # -----Button Hide log-----
        # self.hide_log_button["text"] = "Hide Log"
        # self.hide_log_button["command"] = self.hide_log_widge
        # self.hide_log_button.grid(row=7, column=0)
        # -----Checkbutton show/hide log-----
        # self.shlog_chbutton.config(variable=self.checkbutton_select, text='Show log', command=self.hide_log_widge)
        # self.shlog_chbutton.grid(row=4, column=0, columnspan=1, sticky='SNWE')

        self.log_txt.tag_config("error", foreground="#CC0000")
        self.log_txt.tag_config("info", foreground="#008800")
        self.log_txt.tag_config("info2", foreground="#404040")

        self.update_idletasks()

    def show_rename_frame(self):
        ajrename.rename_frame(self, self.sub_path_entry.get(), self.sub_type_entry.get(), sub_setting_name)

    def hide_log_widge(self):
        # if self.shlog_chbuttonVar.get():
        #     self.log_txt.grid_remove()
        #     self.vert_scrollbar.grid_remove()
        #     self.hor_scrollbar.grid_remove()
        #     # self.hide_log_button.grid_remove()
        #     self.version_state["text"] = progress_idle_txt
        #     self.update_idletasks()
        # else:
        #     # -----Show log widge-----
        #     if not self.log_txt.grid_info():
        #         self.log_txt.grid()
        #         self.vert_scrollbar.grid()
        #         self.hor_scrollbar.grid()
        #         # self.hide_log_button.grid()
        pass

    def press_key_enter(self, event=None):
        self.replace_all_sub_in_path()

    def convert_clipboard(self):
        clip_content_lv = self.clipboard_get()
        self.clipboard_clear()
        clip_content_lv = langconver.convert_lang_select(clip_content_lv, 's2t')
        self.clipboard_append(clip_content_lv)

    def print_about(self):
        tkinter.messagebox.showinfo("About", self.help_text)

    # def create_popup(self):
    #     pass
    #     # self.top_window = Toplevel()
    #     # self.top_window.overrideredirect(1)
    #     # msg = Label(self.top_window, text="轉換工作進行中...")
    #     # root.update_idletasks()
    #     # msg.pack(side=TOP, anchor=W, fill=X, expand=YES)
    #     # self.top_window['takefocus'] = True
    #     # self.top_window.grab_set()
    #     # self.top_window.focus_force()
    #     # msg.focus()
    #     # msg.grab_set()
    #     # root.update_idletasks()
    #
    # def close_popup(self):
    #     # self.top_window.destroy()
    #     pass

    def setlog(self, string, level=None):
        self.log_txt.config(state="normal")

        if (level != 'error') and (level != 'info') and (level != 'info2'):
            level = ""

        self.log_txt.insert(INSERT, string + "\n", level)
        # -----scroll to end of text widge-----
        self.log_txt.see(END)
        self.update_idletasks()

        self.log_txt.config(state="disabled")

    def setlog_large(self, string, level=None):
        self.log_txt.insert(INSERT, string + "\n", level)
        # -----scroll to end of text widge-----
        self.log_txt.see(END)
        self.update_idletasks()

    def read_config(self, filename, section, key):
        try:
            config_lh = configparser.ConfigParser()
            file_ini_lh = open(filename, 'r', encoding='utf16')
            config_lh.read_file(file_ini_lh)
            file_ini_lh.close()
            return config_lh.get(section, key)
        except:
            self.setlog("Error! Read setting ini file fail! "
                        "please create UTF-16 format " + filename + " in tool path", 'error')
            return error_Type.FILE_ERROR.value

    def write_config(self, filename, sections, key, value):
        try:
            config_lh = configparser.ConfigParser()
            file_ini_lh = open(filename, 'r', encoding='utf16')
            config_lh.read_file(file_ini_lh)
            file_ini_lh.close()

            file_ini_lh = open(filename, 'w', encoding='utf16')
            config_lh.set(sections, key, value)
            config_lh.write(file_ini_lh)
            file_ini_lh.close()
        except Exception as ex:
            self.setlog("Error! Write setting to ini file fail, "
                        "please create UTF-16 format "+filename+" in tool path", 'error')
            return error_Type.FILE_ERROR.value

    def store_origin_file_to_backup_folder(self, file, back_folder):
        shutil.copy2(file, back_folder)

    def conv_and_replace_sub_write_file(self, subfile_list, subdata_dic):
        status_lv = True
        self.log_txt.config(state="normal")
        subfile_list_lt = tuple(subfile_list)
        for i in subfile_list_lt:
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
                            self.setlog("Error! can't read format: " + i, 'error')
                            continue
                    # -----For GBK and GB2312 format-----
                    subcontent_h.close()
                    # -----backup origin sub file to backup folder-----
                    self.store_origin_file_to_backup_folder(i, self.user_input_path+'\\'+backup_folder_name)
                    sub_content_temp_lv = sub_content_lv
                    # -----convert to TC language-----
                    self.setlog_large("Convert: %s" % i)
                    tw_str_lv = langconver.s2tw(sub_content_lv)
                    self.setlog_large("Replace font set: %s" % i, 'info2')
                    tw_str_lv = replace_sub.replace_specif_string(tw_str_lv, subdata_dic)
                    if sub_content_temp_lv != tw_str_lv:
                        subcontent_write_h = open(i, 'w', encoding='utf8')
                        subcontent_write_h.seek(0, 0)
                        subcontent_write_h.write(tw_str_lv)
                        subcontent_write_h.close()
                    continue

            # -----backup origin sub file to backup folder-----
            self.store_origin_file_to_backup_folder(i, '%s\\%s' % (self.user_input_path, backup_folder_name))
            # -----for utf8 and utf16 format-----
            sub_content_temp_lv = sub_content_lv
            # -----convert to TC language-----
            self.setlog_large("Convert: %s" % i)
            tw_str_lv = langconver.s2tw(sub_content_lv)
            self.setlog_large("Replace font set: %s" % i, 'info2')
            tw_str_lv = replace_sub.replace_specif_string(tw_str_lv, subdata_dic)
            # -----if sub file content is changed, write to origin file-----
            if sub_content_temp_lv != tw_str_lv:
                subcontent_h.seek(0, 0)
                subcontent_h.write(tw_str_lv)
            subcontent_h.close()

        self.log_txt.config(state="disable")
        return status_lv

    def replace_all_sub_in_path(self):
        w_file_stat_lv = error_Type.NORMAL.value

        # -----Clear text widge for log-----
        self.log_txt.config(state="normal")
        self.log_txt.delete('1.0', END)
        self.log_txt.config(state="disable")

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
        if self.subpath_ini == error_Type.FILE_ERROR.value or self.subfiletype_list_ini == error_Type.FILE_ERROR.value:
            tkinter.messagebox.showerror("Error",
                                         "Error! Read setting ini file fail! "
                                         "please create UTF-16 format " + sub_setting_name + " in tool path")
            return

        # -----remove '\' or '/' in end of path string-----
        self.user_input_path = re.sub(r"/$", '', self.user_input_path)
        self.user_input_path = re.sub(r"\\$", "", self.user_input_path)

        # -----Store user input path and type into Setting.ini config file-----
        if not self.user_input_path == self.subpath_ini:
            self.setlog("Write new path setting to: " + sub_setting_name, "info")
            # print("path not match, write new path to ini")
            w_file_stat_lv = self.write_config(sub_setting_name,  'Global', 'subpath', self.user_input_path)
        if not self.user_input_type == self.subfiletype_list_ini:
            self.setlog("Write new type setting to: " + sub_setting_name, "info")
            # print("type not match, write new type list to ini")
            w_file_stat_lv = self.write_config(sub_setting_name, 'Global', 'subtype', self.user_input_type)
        if w_file_stat_lv == error_Type.FILE_ERROR.value:
            tkinter.messagebox.showerror("Error",
                                         "Error! Write setting ini file fail! "
                                         "please create UTF-16 format " + sub_setting_name + " in AJSub path")
            return

        # ----Split file type string and store to list-----
        re_lv = re.sub(r' ', '', self.user_input_type)
        self.user_input_type = re_lv.split(",")
        # -----remove duplicate item-----
        self.user_input_type = set(self.user_input_type)
        # print(self.user_input_type)

        # -----Dim button for string converting-----
        self.version_state["text"] = progress_txt
        # self.version_state["fg"] = "blue"
        self.start_button["state"] = 'disable'
        # self.help_button["state"] = 'disable'
        self.update_idletasks()

        # -----Get sub file list by type-----
        sub_file_list = replace_sub.get_file_list(self.user_input_path, self.user_input_type)
        # print(sub_file_list)
        # -----make backup folder for store origin sub files-----
        if not os.path.exists(self.user_input_path+'\\'+backup_folder_name):
            os.makedirs(self.user_input_path+'\\'+backup_folder_name)
        # -----Replace all file list string by dic structure-----
        status = self.conv_and_replace_sub_write_file(sub_file_list, sub_data_dic)

        # -----Set button and progressing state to normal-----
        self.version_state["text"] = progress_done_txt
        # self.version_state["fg"] = "blue"
        self.start_button["state"] = 'normal'
        # self.help_button["state"] = 'normal'
        self.update_idletasks()

        if status:
            self.setlog("***Success! Convert and Replace all file done.***", "info")
            tkinter.messagebox.showinfo("message", "Convert and Replace all file done.")
        else:
            self.setlog("***Error! Convert and Replace file error, please check the log.***", "error")
            tkinter.messagebox.showerror("message Error", "Convert and Replace file error, please check the log.")


def check_all_file_status():
    if not os.path.exists(sub_database_name):
        return False
    if not os.path.exists(sub_setting_name):
        return False
    if not os.path.exists('icons\\main.ico'):
        return False
    return True


if __name__ == '__main__':
    # -----MessageBox will create tkinter, so create correct setting tkinter first
    root = Tk()
    root.title(title)
    root.iconbitmap('icons\\main.ico')

    if not check_all_file_status():
        tkinter.messagebox.showerror("Error", "Necessary file is not found! \n\nPlease check below is exist or "
                                              "please re-install AJSub:\n"
                                              "1. " + sub_setting_name + "\n"
                                              "2. " + sub_database_name + "\n"
                                              "3. icons\\main.ico")
        sys.exit(0)

    try:
        # -----Get setting from Settings.ini-----
        file_ini_h = open(sub_setting_name, encoding='utf16')
        config_h = configparser.ConfigParser()
        config_h.read_file(file_ini_h)
        file_ini_h.close()
        subpath = config_h.get('Global', 'subpath')
        subfiletype_list = config_h.get('Global', 'subtype')
        config_h.clear()
    except:
        tkinter.messagebox.showerror("Error",
                                     "Read setting fail " + sub_setting_name + " or " + sub_database_name + " fail!\n"
                                     "Please check these file is correct (unicode format) or re-install AJSub")
        sys.exit(0)

    # -----Get database list to dic structure-----
    sub_data_dic = replace_sub.get_database_list(sub_database_name)
    # -----Start GUI class-----
    root.geometry('784x614')
    app = replace_Sub_Gui(master=root, subfilepath_ini=subpath,
                          subfiletype_ini=subfiletype_list, help_text=help_text)
    # -----Start main loop-----
    app.mainloop()
