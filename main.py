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
Ver 4.4.0 - Add rename sub file to match video file name
Ver 4.5.0 -
    1. Add rename and mapping function
    2. Change all text and notify message
    3. Change icon
Ver 4.5.1 -
    1. Add S2TW, S2T, T2S convert function
    2. Add big5 type for convert function
    3. Add help button in rename function
    4. Add BIG5 format supported
    5. Modify ST dictionary
Ver 4.5.2 - Modify ST dictionary
Ver 4.5.3 - Modify ST dictionary
Ver 4.5.4 - Fix some folder name can't access issue
Ver 4.5.5 - Add convert all sub folder function
Ver 4.5.6 -
    1. Fix show error popup when file type didn't find in sub folder
    2. Fix didn't convert root folder when use sub folder convert function issue
Ver 4.5.7 -
    1. Add browser folder button
    2. Renew sub mapping database
    3. Improve open file process
    4. Modify GUI font
    5. Add select backup file function
    6. Improve exe file package method
    7. Fix GUI font blurry problem
Ver 4.5.8 -
    1. Set Dpi Awareness in windows OS only
    2. Fix path error issue
    3. Use os.join for folder path
    4. Change mapping rename to default
Ver 4.5.9 - Fix file path string show in log windows problem
"""

from tkinter import *
from tkinter.ttk import *
from tkinter.font import Font
from tkinter import filedialog
import tkinter.messagebox
import re
import configparser
import os
from os import path
import shutil
# from tkinter.scrolledtext import ScrolledText
# from time import sleep
# from tkinter.commondialog import Dialog
from enum import Enum

import replace_sub
import langconver
import ajrename
import sys

if sys.platform.startswith('win32'):
    from ctypes import windll

title = "AJSub - 強力轉換! 轉碼君"
version = "v4.05.9"
sub_database_name = "SubList.sdb"
sub_setting_name = "Settings.ini"
icon_name = 'main.ico'
backup_folder_name = "backfile"
subpath = ""  # SUB file path, read from Settings.ini
subfiletype_list = ""  # SUB file type, read from Settings.ini, ex: *.ssa, *.ass
progress_txt = "強力轉換中..."
progress_idle_txt = ""
progress_done_txt = "轉換完成!!"
show_help_text = \
    "AJSub "+version+"\n\n"\
    "本軟體會自動將指定目錄下的所有指定檔案簡轉繁或繁轉簡\n" \
    "建議使用簡體轉繁體+台灣慣用語\n\n"\
    "轉換完成後, AJSub會將檔案內容的字型設定部份轉為簡體\n" \
    "這樣使用某些字型時系統才會認得 (例如方正系列的字型)\n\n"\
    "UTF-8與UTF-16檔會照原格式儲存, 其餘會自動轉UTF-8格式\n"\
    "原始檔案備份在"+backup_folder_name+"目錄下\n\n"\
    "使用說明:\n"\
    "   1. 將檔案路徑輸入SUB type欄位\n"\
    "   2. 輸入檔案類型並用逗點隔開, 如*.ass, *.ssa\n"\
    "   3. 按下轉碼按鈕~ enjoy it!!!!\n"\
    "   4. 字型設定若需新增或修改, 請直接修改SubList.sdb\n"\
    "   5. 按下剪貼簿轉碼按鈕, 可直接轉換剪貼簿的內容\n"\
    "   6. 啟動~ 檔名君按鈕可開啟AJRen改名程式\n\n" \
    "轉碼功能使用Yichen (Eugene) (https://github.com/yichen0831/opencc-python) 提供的OpenCC python版本\n\n" \
    "AJSub由[Llona]設計維護, 問題回報與下載頁面: https://llona.github.io/AJ-sub/ \n\n"\
    "=====\n"\
    "AJSub "+version+"\n"\
    "Copyright 2016\n\n"\
    "This product includes OpenCC-python, develop by:\n"\
    "[Yichen (Eugene)](https://github.com/yichen0831/opencc-python).\n\n" \
    "AJSub is implement by [Llona], \n" \
    "Bug report and download page: https://llona.github.io/AJ-sub/"


class ErrorType(Enum):
    NORMAL = 'NORMAL'  # define normal state
    FILE_ERROR = 'FILE_RW_ERROR'  # define file o/r/w error type


class ReplaceSub(Frame):
    def __init__(self, master=None, subfilepath_ini=None, subfiletype_ini=None, help_text=None):
        Frame.__init__(self, master)
        self.master = master
        self.subfiletype_list_ini = subfiletype_ini
        self.subpath_ini = subfilepath_ini
        self.help_text = help_text
        self.user_input_path = ""
        self.user_input_type = ""
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

        self.style.configure('Tlog_frame.TLabelframe', font=('Microsoft YaHei', 10))
        self.style.configure('Tlog_frame.TLabelframe.Label', font=('Microsoft YaHei', 10))
        self.log_frame = LabelFrame(self.top, text='LOG', style='Tlog_frame.TLabelframe')
        self.log_frame.place(relx=0.01, rely=0.283, relwidth=0.973, relheight=0.708)

        self.style.configure('Tuser_input_frame.TLabelframe', font=('Microsoft YaHei', 10))
        self.style.configure('Tuser_input_frame.TLabelframe.Label', font=('Microsoft YaHei', 10))
        self.user_input_frame = LabelFrame(self.top, text='輸入', style='Tuser_input_frame.TLabelframe')
        self.user_input_frame.place(relx=0.01, rely=0.011, relwidth=0.973, relheight=0.262)

        self.VScroll1 = Scrollbar(self.log_frame, orient='vertical')
        self.VScroll1.place(relx=0.967, rely=0.010, relwidth=0.022, relheight=0.936)

        self.HScroll1 = Scrollbar(self.log_frame, orient='horizontal')
        self.HScroll1.place(relx=0.01, rely=0.940, relwidth=0.958, relheight=0.055)

        self.log_txtFont = Font(font=('Microsoft YaHei', 10))
        self.log_txt = Text(self.log_frame, wrap='none', xscrollcommand=self.HScroll1.set, yscrollcommand=self.VScroll1.set, font=self.log_txtFont)
        self.log_txt.place(relx=0.01, rely=0.010, relwidth=0.958, relheight=0.936)
        # self.log_txt.insert('1.0', '')
        self.HScroll1['command'] = self.log_txt.xview
        self.VScroll1['command'] = self.log_txt.yview

        self.style.configure('Tclip_button.TButton', font=('Microsoft YaHei', 9))
        self.clip_button = Button(self.user_input_frame, text='剪貼簿轉碼', command=self.convert_clipboard, style='Tclip_button.TButton')
        self.clip_button.place(relx=0.160, rely=0.788, relwidth=0.137, relheight=0.200)

        self.style.configure('Tstart_button.TButton', font=('Microsoft YaHei', 9))
        self.start_button = Button(self.user_input_frame, text='轉碼', command=self.replace_all_sub_in_path, style='Tstart_button.TButton')
        self.start_button.place(relx=0.327, rely=0.788, relwidth=0.105, relheight=0.200)

        self.style.configure('Thelp_button.TButton', font=('Microsoft YaHei', 9))
        self.help_button = Button(self.user_input_frame, text='Help', command=self.print_about, style='Thelp_button.TButton')
        self.help_button.place(relx=0.460, rely=0.788, relwidth=0.105, relheight=0.200)

        self.style.configure('Trename_button.TButton', font=('Microsoft YaHei', 9))
        self.rename_button = Button(self.user_input_frame, text='啟動~ 檔名君', command=self.show_rename_frame, style='Trename_button.TButton')
        self.rename_button.place(relx=0.832, rely=0.497, relwidth=0.137, relheight=0.200)

        self.style.configure('Trename_button.TButton', font=('Microsoft YaHei', 9))
        self.browser_button = Button(self.user_input_frame, text='瀏覽', command=self.browser_explorer, style='Trename_button.TButton')
        self.browser_button.place(relx=0.832, rely=0.166, relwidth=0.137, relheight=0.200)

        self.sub_path_entryVar = StringVar(value=self.subpath_ini)
        self.sub_path_entry = Entry(self.user_input_frame, textvariable=self.sub_path_entryVar, font=('Microsoft YaHei', 10))
        self.sub_path_entry.place(relx=0.01, rely=0.180, relwidth=0.80, relheight=0.180)

        self.sub_type_entryVar = StringVar(value=self.subfiletype_list_ini)
        self.sub_type_entry = Entry(self.user_input_frame, textvariable=self.sub_type_entryVar, font=('Microsoft YaHei', 10))
        self.sub_type_entry.place(relx=0.01, rely=0.520, relwidth=0.80, relheight=0.190)

        self.style.configure('Tversion_label.TLabel', anchor='e', font=('Microsoft YaHei', 9))
        self.version_label = Label(self.user_input_frame, text=version, state='disable', style='Tversion_label.TLabel')
        self.version_label.place(relx=0.843, rely=0.87, relwidth=0.147, relheight=0.13)

        self.style.configure('Tversion_state.TLabel', anchor='w', font=('Microsoft YaHei', 9))
        self.version_state = Label(self.user_input_frame, text=progress_idle_txt, style='Tversion_state.TLabel')
        self.version_state.place(relx=0.01, rely=0.87, relwidth=0.116, relheight=0.13)

        self.style.configure('Tsub_type_label.TLabel', anchor='w', font=('Microsoft YaHei', 10))
        self.sub_type_label = Label(self.user_input_frame, text='轉換檔案類型', style='Tsub_type_label.TLabel')
        self.sub_type_label.place(relx=0.01, rely=0.380, relwidth=0.200, relheight=0.13)

        self.style.configure('Tsub_path_label.TLabel', anchor='w', font=('Microsoft YaHei', 10))
        self.sub_path_label = Label(self.user_input_frame, text='轉換檔案路徑', style='Tsub_path_label.TLabel')
        self.sub_path_label.place(relx=0.01, rely=0.010, relwidth=0.200, relheight=0.166)

        self.ComboVar = StringVar()
        self.Combo = Combobox(self.user_input_frame, text='S2TW', state='readonly', textvariable=self.ComboVar,
                               font=('Microsoft YaHei', 9))
        self.Combo['values'] = ('簡轉繁+台灣慣用語', '簡轉繁', '繁轉簡')
        self.Combo.current(0)
        self.Combo.place(relx=0.600, rely=0.800, relwidth=0.190)
        # self.Combo.bind('<<ComboboxSelected>>', self.get_user_conv_type)

        self.sub_folder_chbuttonVar = IntVar(value=0)
        self.style.configure('Tlucky_sort_chbutton.TCheckbutton', font=('Microsoft YaHei', 9))
        self.sub_folder_chbutton = Checkbutton(self.user_input_frame, text='包含子目錄', variable=self.sub_folder_chbuttonVar, style='Tlucky_sort_chbutton.TCheckbutton')
        self.sub_folder_chbutton.place(relx=0.830, rely=0.730, relwidth=0.110)

        self.backup_chbuttonVar = IntVar(value=1)
        self.style.configure('Tbackup_chbutton.TCheckbutton', font=('Microsoft YaHei', 9))
        self.backup_chbutton = Checkbutton(self.user_input_frame, text='備份原始檔', variable=self.backup_chbuttonVar, style='Tbackup_chbutton.TCheckbutton')
        self.backup_chbutton.place(relx=0.830, rely=0.85, relwidth=0.110)

        # self.convert_clipboard
        # self.print_about
        # self.replace_all_sub_in_path
        # self.show_rename_frame

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

    def get_user_conv_type(self, event=None):
        conv_type_ls = self.Combo.current()
        # print(conv_type_ls)
        if conv_type_ls == 0:
            return 's2tw'
        elif conv_type_ls == 1:
            return 's2t'
        elif conv_type_ls == 2:
            return 't2s'
        else:
            print('Error! combobox input is error:%s ' % conv_type_ls)

    def show_rename_frame(self):
        ajrename.rename_frame(self, self.sub_path_entry.get(), self.sub_type_entry.get(), sub_setting_name, root_path)

    def browser_explorer(self):
        file_path = filedialog.askdirectory(initialdir=self.sub_path_entry.get())
        if file_path:
            file_path = os.path.abspath(file_path)
            self.sub_path_entry.delete(0, END)
            self.sub_path_entry.insert(0, file_path)

# def hide_log_widge(self):
    #     print(self.shlog_chbuttonVar.get())
    #     if not self.shlog_chbuttonVar.get():
    #         # self.log_frame.place_forget()
    #         # self.log_frame.grid_remove()
    #         # self.log_txt.grid_remove()
    #         # self.vert_scrollbar.grid_remove()
    #         # self.hor_scrollbar.grid_remove()
    #         # # self.hide_log_button.grid_remove()
    #         # self.version_state["text"] = progress_idle_txt
    #         self.update_idletasks()
    #     else:
    #         # -----Show log widge-----
    #         if not self.log_txt.grid_info():
    #             self.log_frame.place(relx=0.01, rely=0.287, relwidth=0.981, relheight=0.705)
    #             # self.log_txt.grid()
    #             # self.vert_scrollbar.grid()
    #             # self.hor_scrollbar.grid()
    #             # self.hide_log_button.grid()

    def press_key_enter(self, event=None):
        self.replace_all_sub_in_path()

    def convert_clipboard(self):
        # -----Clear text widge for log-----
        # self.log_txt.config(state="normal")
        # self.log_txt.delete('1.0', END)
        # self.log_txt.config(state="disable")

        clip_content_lv = self.clipboard_get()
        self.clipboard_clear()
        conv_ls = self.get_user_conv_type()
        # clip_content_lv = langconver.convert_lang_select(clip_content_lv, 's2t')
        # print(conv_ls)
        clip_content_lv = langconver.convert_lang_select(clip_content_lv, conv_ls)
        self.clipboard_append(clip_content_lv)

        self.setlog("剪貼簿轉換完成!", 'info')

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

        self.log_txt.insert(INSERT, "%s\n" % string, level)
        # -----scroll to end of text widge-----
        self.log_txt.see(END)
        self.update_idletasks()

        self.log_txt.config(state="disabled")

    def setlog_large(self, string, level=None):
        self.log_txt.insert(INSERT, "%s\n" % string, level)
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
        except Exception as ex:
            self.setlog("Error! 讀取ini設定檔發生錯誤! "
                        "請在AJSub目錄下使用UTF-16格式建立 " + filename, 'error')
            str(ex)
            return ErrorType.FILE_ERROR.value

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
            self.setlog("Error! 寫入ini設定檔發生錯誤! "
                        "請在AJSub目錄下使用UTF-16格式建立 " + filename, 'error')
            str(ex)
            return ErrorType.FILE_ERROR.value

    def store_origin_file_to_backup_folder(self, file, back_folder):
        if self.backup_chbuttonVar.get() == 1:
            shutil.copy2(file, back_folder)

    @staticmethod
    def get_file_content_format(file_path):
        format_list = ['utf8', 'utf-8-sig', 'utf16', 'big5', 'gbk', 'gb2312', None]
        for file_format in format_list:
            try:
                with open(file_path, 'r', encoding=file_format) as subcontent_h:
                    sub_content_lv = subcontent_h.read()
                    # print('find correct format {} in ini file: {}'.format(file_format, self.ini_full_path))
                return sub_content_lv, file_format
            except Exception as ex:
                str(ex)

        return None

    def conv_and_replace_sub_write_file(self, subfile_list, subdata_dic):
        status_lv = True
        self.log_txt.config(state="normal")
        subfile_list_lt = tuple(subfile_list)
        for i in subfile_list_lt:
            sub_content_lv, file_format = self.get_file_content_format(i)

            if not sub_content_lv:
                status_lv = False
                self.setlog("Error! 無法開啟檔案, 請確認檔案: %s " % i, 'error')
                continue

            if file_format == 'utf16' or file_format == 'utf-8-sig':
                write_file_format = file_format
            else:
                write_file_format = 'utf8'

            # -----backup origin sub file to backup folder-----
            self.store_origin_file_to_backup_folder(i, path.join(self.user_input_path, backup_folder_name))
            # -----for utf8 and utf16 format-----
            sub_content_temp_lv = sub_content_lv
            # -----convert-----
            self.setlog_large("轉碼中: %s" % i)
            # tw_str_lv = langconver.s2tw(sub_content_lv)
            conv_ls = self.get_user_conv_type()
            tw_str_lv = langconver.convert_lang_select(sub_content_lv, conv_ls)
            self.setlog_large("替換字串: %s" % i, 'info2')
            tw_str_lv = replace_sub.replace_specif_string(tw_str_lv, subdata_dic)
            # -----if sub file content is changed, write to origin file-----
            if sub_content_temp_lv != tw_str_lv:
                subcontent_h = open(i, 'w', encoding=write_file_format)
                subcontent_h.seek(0, 0)
                subcontent_h.write(tw_str_lv)
                subcontent_h.close()

        self.log_txt.config(state="disable")
        return status_lv

    def replace_all_sub_in_path(self):
        w_file_stat_lv = ErrorType.NORMAL.value

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
            tkinter.messagebox.showinfo("message", "請輸入路徑和類型")
            return
        if not os.path.exists(self.user_input_path):
            tkinter.messagebox.showerror("Error", "路徑錯誤")
            return
        # -----get config ini file setting-----
        self.subpath_ini = self.read_config(sub_setting_name, 'Global', 'subpath')
        self.subfiletype_list_ini = self.read_config(sub_setting_name, 'Global', 'subtype')
        if self.subpath_ini == ErrorType.FILE_ERROR.value or self.subfiletype_list_ini == ErrorType.FILE_ERROR.value:
            tkinter.messagebox.showerror("Error",
                                         "錯誤! 讀取ini設定檔發生錯誤! "
                                         "請在AJSub目錄下使用UTF-16格式建立 " + sub_setting_name)
            return

        # -----remove '\' or '/' in end of path string-----
        self.user_input_path = re.sub(r"/$", '', self.user_input_path)
        self.user_input_path = re.sub(r"\\$", "", self.user_input_path)

        # -----Store user input path and type into Setting.ini config file-----
        if not self.user_input_path == self.subpath_ini:
            self.setlog("新的路徑設定寫入設定檔: " + sub_setting_name, "info")
            # print("path not match, write new path to ini")
            w_file_stat_lv = self.write_config(sub_setting_name,  'Global', 'subpath', self.user_input_path)
        if not self.user_input_type == self.subfiletype_list_ini:
            self.setlog("新的檔案類型設定寫入設定檔: " + sub_setting_name, "info")
            # print("type not match, write new type list to ini")
            w_file_stat_lv = self.write_config(sub_setting_name, 'Global', 'subtype', self.user_input_type)
        if w_file_stat_lv == ErrorType.FILE_ERROR.value:
            tkinter.messagebox.showerror("Error",
                                         "錯誤! 寫入ini設定檔發生錯誤! "
                                         "請在AJSub目錄下使用UTF-16格式建立 " + sub_setting_name)
            return

        # ----Split file type string and store to list-----
        re_lv = re.sub(r' ', '', str(self.user_input_type))
        self.user_input_type = re_lv.split(",")
        # -----remove duplicate item-----
        self.user_input_type = set(self.user_input_type)
        # print(self.user_input_type)

        # ---only convert a specific folder---
        status = True
        if self.sub_folder_chbuttonVar.get() == 0:
            status = self.start_conversion()
        else:
            # ---convert all sub folder---
            ori_user_input_path = self.user_input_path
            sub_folder_lists = replace_sub.get_all_sub_folder_name(self.user_input_path)
            for sub_folder in sub_folder_lists:
                # skip backup folder
                if sub_folder.find(backup_folder_name) == -1:
                    self.setlog("轉換子目錄: %s" % sub_folder, "info")
                    self.user_input_path = sub_folder
                    status_tmp = self.start_conversion()
                    if not status_tmp:
                        status = status_tmp
            self.user_input_path = ori_user_input_path

        self.show_done_popup(status)

    def start_conversion(self):
        # -----Get sub file list by type-----
        sub_file_list = replace_sub.get_file_list(self.user_input_path, self.user_input_type)
        if not sub_file_list:
            # convert file list is empty
            if self.sub_folder_chbuttonVar.get() == 0:
                tkinter.messagebox.showwarning("Error", "錯誤! 在指定的目錄中找不到檔案! 請確認檔案路徑與類型")
                return False
            else:
                self.setlog("此目錄中無指定檔案類型: %s" % self.user_input_path, "error")
                return True

        # print(sub_file_list)

        # -----Dim button for string converting-----
        self.version_state["text"] = progress_txt
        # self.version_state["fg"] = "blue"
        self.start_button["state"] = 'disable'
        # self.help_button["state"] = 'disable'
        self.clip_button["state"] = 'disable'
        self.update_idletasks()

        # -----make backup folder for store origin sub files-----
        backup_folder_path = path.join(self.user_input_path, backup_folder_name)
        if not os.path.exists(backup_folder_path) and self.backup_chbuttonVar.get() == 1:
            os.makedirs(backup_folder_path)
        # -----Replace all file list string by dic structure-----
        status = self.conv_and_replace_sub_write_file(sub_file_list, sub_data_dic)

        # -----Set button and progressing state to normal-----
        self.version_state["text"] = progress_done_txt
        # self.version_state["fg"] = "blue"
        self.start_button["state"] = 'normal'
        # self.help_button["state"] = 'normal'
        self.clip_button["state"] = 'normal'
        self.update_idletasks()

        return status

    def show_done_popup(self, status):
        if status:
            self.setlog("***順利完成! 轉碼與取代字串成功***", "info")
            tkinter.messagebox.showinfo("message", "轉碼與取代字串成功")
        else:
            self.setlog("***錯誤! 轉碼與取代字串發生錯誤***", "error")
            tkinter.messagebox.showerror("Error", "轉碼與取代字串發生錯誤, 請參考log視窗")


def check_all_file_status(root_paths):
    if not os.path.exists(path.join(root_paths, sub_database_name)):
        return False
    if not os.path.exists(path.join(root_paths, sub_setting_name)):
        return False
    if not os.path.exists(path.join(root_paths, 'icons', icon_name)):
        return False
    return True


def set_all_file_path(root_paths):
    global sub_setting_name, sub_database_name, icon_name
    sub_setting_name = path.join(root_paths, sub_setting_name)
    sub_database_name = path.join(root_paths, sub_database_name)
    icon_name = path.join(root_paths, 'icons', icon_name)


def find_root_path():
    retry_count = 1
    root_path_local = sys.path[0]

    while retry_count <= 2:
        if check_all_file_status(root_path_local):
            return root_path_local
        else:
            root_path_local = path.abspath(path.join(root_path_local, path.pardir))
        retry_count += 1

    return None


if __name__ == '__main__':
    # -----MessageBox will create tkinter, so hide tkinter first
    root = Tk()
    root.withdraw()

    root_path = find_root_path()
    if not root_path:
        tkinter.messagebox.showerror("Error", "遺失必要檔案! \n\n請確認AJSub目錄有以下檔案存在, 或 "
                                              "重新安裝AJSub:\n"
                                              "1. " + sub_setting_name + "\n"
                                              "2. " + sub_database_name + "\n"
                                              "3. icons\\main.ico")
        sys.exit(0)
    set_all_file_path(root_path)

    if sys.platform.startswith('win32'):
        windll.shcore.SetProcessDpiAwareness(True)

    try:
        # -----Get setting from Settings.ini-----
        file_ini_h = open(sub_setting_name, encoding='utf16')
        config_h = configparser.ConfigParser()
        config_h.read_file(file_ini_h)
        file_ini_h.close()
        subpath = config_h.get('Global', 'subpath')
        subfiletype_list = config_h.get('Global', 'subtype')
        config_h.clear()
    except Exception as e:
        tkinter.messagebox.showerror("Error",
                                     "讀取設定檔 " + sub_setting_name + " 或 " + sub_database_name + " 錯誤!\n"
                                     "請確認檔案格式為UTF-16 (unicode format) 或重新安裝AJSub")
        str(e)
        sys.exit(0)

    # -----Get database list to dic structure-----
    sub_data_dic = replace_sub.get_database_list(sub_database_name)
    # -----Start GUI class-----
    root.title(title)
    root.iconbitmap(icon_name)
    root.geometry('880x670')
    # show GUI
    root.update()
    root.deiconify()
    app = ReplaceSub(master=root, subfilepath_ini=subpath,
                     subfiletype_ini=subfiletype_list, help_text=show_help_text)
    # -----Start main loop-----
    app.mainloop()
