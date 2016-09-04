from tkinter import *
import tkinter.messagebox
from tkinter.font import Font
from tkinter.ttk import *
import glob
import os
import re
import configparser
from enum import Enum
# from time import sleep
# import time
# from datetime import datetime
from threading import Timer
from collections import OrderedDict
# import time


class error_Code(Enum):
    NORMAL = 0  # define normal state
    FILE_ERROR = 1  # define file o/r/w error type
    USER_SUB_INPUT_PATH_ERROR = 2
    USER_SUB_INPUT_TYPE_ERROR = 3
    USER_VIDEO_INPUT_PATH_ERROR = 4
    USER_VIDEO_INPUT_TYPE_ERROR = 5
    USER_VIDEO_INPUT_KEYWORD_ERROR = 6
    USER_SUB_INPUT_KEYWORD_ERROR = 7
    USER_RENAME_INPUT_ERROR = 8


class rename_frame:
    def __init__(self, parent, main_sub_path, main_sub_type, setting_name):
        self.main_sub_path = main_sub_path
        self.main_sub_type = main_sub_type
        self.rename_ori_and_rename_odic = OrderedDict()
        self.mapping_orisub_and_video_odic = OrderedDict()
        self.mapping_orisub_and_sub_odic = OrderedDict()
        self.app_current_path = os.getcwd()
        self.radiobutton_select = IntVar()
        # -----Timer-----
        self.timer_h = None
        self.timer_running_fl = False
        # -----Create TopLevel frame-----
        self.top = Toplevel(parent)
        self.top.geometry('1264x754')
        # self.top_window = Toplevel(parent)
        # self.top_window.overrideredirect(1)
        self.top['takefocus'] = True
        self.top.grab_set()
        self.top.focus_force()

        try:
            # -----Get setting from Settings.ini-----
            file_ini_h = open(setting_name, encoding='utf16')
            config_file_h = configparser.ConfigParser()
            config_file_h.read_file(file_ini_h)
            file_ini_h.close()
            self.videopath_ini = config_file_h.get('Rename', 'videopath')
            self.videotype_ini = config_file_h.get('Rename', 'videotype')
            self.videokeyword_ini = config_file_h.get('Rename', 'videokeyword')
            self.subkeyword_ini = config_file_h.get('Rename', 'subkeyword')
            # print(self.videopath_ini, self.videokeyword_ini, self.subkeyword_ini)
            config_file_h.clear()
        except:
            tkinter.messagebox.showerror("Error", "Read setting fail " + setting_name+" fail!\n"
                                         "Please check " + setting_name +
                                         " setting file is correct (unicode format) or re-install AJSub")

        self.show_rename_frame()

    def show_rename_frame(self):
        self.style = Style()

        self.style.configure('Trename_frame.TLabelframe', font=('iLiHei', 9))
        self.style.configure('Trename_frame.TLabelframe.Label', font=('iLiHei', 9))
        self.rename_frame = LabelFrame(self.top, text='Rename', style='Trename_frame.TLabelframe')
        self.rename_frame.place(relx=0.006, rely=0.605, relwidth=0.298, relheight=0.394)

        self.style.configure('Tmapping_frame.TLabelframe', font=('iLiHei', 9))
        self.style.configure('Tmapping_frame.TLabelframe.Label', font=('iLiHei', 9))
        self.mapping_frame = LabelFrame(self.top, text='Mapping Sub and Video', style='Tmapping_frame.TLabelframe')
        self.mapping_frame.place(relx=0.31, rely=0.605, relwidth=0.602, relheight=0.394)

        self.style.configure('Tview_right_frame.TLabelframe', font=('iLiHei', 9))
        self.style.configure('Tview_right_frame.TLabelframe.Label', font=('iLiHei', 9))
        self.view_right_frame = LabelFrame(self.top, text='配對結果預覽', style='Tview_right_frame.TLabelframe')
        # self.view_right_frame.place(relx=0.652, rely=0., relwidth=0.349, relheight=0.595)

        self.style.configure('Tview_center_frame.TLabelframe', font=('iLiHei', 9))
        self.style.configure('Tview_center_frame.TLabelframe.Label', font=('iLiHei', 9))
        self.view_center_frame = LabelFrame(self.top, text='結果預覽', style='Tview_center_frame.TLabelframe')
        self.view_center_frame.place(relx=0.500, rely=0., relwidth=0.500, relheight=0.595)
        # self.view_center_frame.place(relx=0.304, rely=0., relwidth=0.349, relheight=0.595)

        self.style.configure('Tview_left_frame.TLabelframe', font=('iLiHei', 9))
        self.style.configure('Tview_left_frame.TLabelframe.Label', font=('iLiHei', 9))
        self.view_left_frame = LabelFrame(self.top, text='原始檔名', style='Tview_left_frame.TLabelframe')
        self.view_left_frame.place(relx=0.006, rely=0., relwidth=0.500, relheight=0.595)
        # self.view_left_frame.place(relx=0.006, rely=0., relwidth=0.298, relheight=0.595)

        self.style.configure('Tvideo_path_label.TLabel', anchor='w', font=('iLiHei', 10))
        self.video_path_label = Label(self.rename_frame, text='Video Path', style='Tvideo_path_label.TLabel')
        self.video_path_label.place(relx=0.042, rely=0.081, relwidth=0.194, relheight=0.084)

        # self.style.configure('TCommand1.TButton', font=('新細明體',9))
        # self.Command1 = Button(self.rename_frame, text='Command1', command=self.Command1_Cmd, style='TCommand1.TButton')
        # self.Command1.place(relx=0.721, rely=0.835, relwidth=0.215, relheight=0.111)

        self.sub_type_entryVar = StringVar(value=self.main_sub_type)
        self.sub_type_entry = Entry(self.mapping_frame, textvariable=self.sub_type_entryVar, font=('iLiHei',10))
        self.sub_type_entry.place(relx=0.032, rely=0.512, relwidth=0.38, relheight=0.084)

        self.style.configure('Tstart_button.TButton', font=('iLiHei', 10))
        self.start_button = Button(self.mapping_frame, text='Start', command=self.start_rename, style='Tstart_button.TButton')
        self.start_button.place(relx=0.021, rely=0.835, relwidth=0.127, relheight=0.111)

        self.turnon_mapping_chbuttonVar = IntVar(value=0)
        self.style.configure('Tturnon_mapping_chbutton.TCheckbutton', font=('iLiHei', 10))
        self.turnon_mapping_chbutton = Checkbutton(self.mapping_frame, text='啟用', variable=self.turnon_mapping_chbuttonVar, style='Tturnon_mapping_chbutton.TCheckbutton')
        self.turnon_mapping_chbutton.place(relx=0.021, rely=0.081, relwidth=0.159, relheight=0.084)

        self.uses_samepath_chbuttonVar = IntVar(value=0)
        self.style.configure('Tuses_samepath_chbutton.TCheckbutton', font=('iLiHei', 10))
        self.uses_samepath_chbutton = Checkbutton(self.mapping_frame, text='使用相同路徑', variable=self.uses_samepath_chbuttonVar, style='Tuses_samepath_chbutton.TCheckbutton')
        self.uses_samepath_chbutton.place(relx=0.021, rely=0.189, relwidth=0.296, relheight=0.057)

        self.sub_path_entryVar = StringVar(value=self.main_sub_path)
        self.sub_path_entry = Entry(self.mapping_frame, textvariable=self.sub_path_entryVar, font=('iLiHei',10))
        self.sub_path_entry.place(relx=0.032, rely=0.323, relwidth=0.38, relheight=0.084)

        self.mapping_frameRadioVar = StringVar()
        self.style.configure('Tmanually_radio.TRadiobutton', font=('iLiHei', 10))
        self.manually_radio = Radiobutton(self.mapping_frame, text='手動模式', value=3, variable=self.radiobutton_select, style='Tmanually_radio.TRadiobutton')
        self.manually_radio.place(relx=0.463, rely=0.377, relwidth=0.254, relheight=0.084)

        self.style.configure('Tstrengthen_radio.TRadiobutton', font=('iLiHei', 10))
        self.strengthen_radio = Radiobutton(self.mapping_frame, text='強力模式', value=2, variable=self.radiobutton_select, style='Tstrengthen_radio.TRadiobutton')
        self.strengthen_radio.place(relx=0.463, rely=0.242, relwidth=0.17, relheight=0.111)

        self.style.configure('Tdefault_radio.TRadiobutton', font=('iLiHei', 10))
        self.default_radio = Radiobutton(self.mapping_frame, text='預設模式', value=1, variable=self.radiobutton_select, style='Tdefault_radio.TRadiobutton')
        self.default_radio.place(relx=0.463, rely=0.135, relwidth=0.127, relheight=0.084)

        self.style.configure('Tmanually_keyword_frame.TLabelframe', font=('iLiHei', 9))
        self.style.configure('Tmanually_keyword_frame.TLabelframe.Label', font=('iLiHei', 9))
        self.manually_keyword_frame = LabelFrame(self.mapping_frame, text='輸入關鍵字', style='Tmanually_keyword_frame.TLabelframe')
        self.manually_keyword_frame.place(relx=0.463, rely=0.485, relwidth=0.443, relheight=0.488)

        self.video_keyword_entryVar = StringVar(value=self.videokeyword_ini)
        self.video_keyword_entry = Entry(self.manually_keyword_frame, textvariable=self.video_keyword_entryVar, font=('iLiHei',10))
        self.video_keyword_entry.place(relx=0.047, rely=0.662, relwidth=0.834, relheight=0.172)

        self.sub_keyword_entryVar = StringVar(value=self.subkeyword_ini)
        self.sub_keyword_entry = Entry(self.manually_keyword_frame, textvariable=self.sub_keyword_entryVar, font=('iLiHei',10))
        self.sub_keyword_entry.place(relx=0.047, rely=0.276, relwidth=0.834, relheight=0.172)

        self.style.configure('Tvideo_keyword_label.TLabel', anchor='w', font=('iLiHei', 10))
        self.video_keyword_label = Label(self.manually_keyword_frame, text='Video Keyword', style='Tvideo_keyword_label.TLabel')
        self.video_keyword_label.place(relx=0.047, rely=0.552, relwidth=0.288, relheight=0.172)

        self.style.configure('Tsub_keyword_label.TLabel', anchor='w', font=('iLiHei', 10))
        self.sub_keyword_label = Label(self.manually_keyword_frame, text='Sub Keyword', style='Tsub_keyword_label.TLabel')
        self.sub_keyword_label.place(relx=0.047, rely=0.166, relwidth=0.335, relheight=0.172)

        self.style.configure('Tsub_type_label.TLabel', anchor='w', font=('iLiHei', 10))
        self.sub_type_label = Label(self.mapping_frame, text='SUB Type', style='Tsub_type_label.TLabel')
        self.sub_type_label.place(relx=0.032, rely=0.458, relwidth=0.075, relheight=0.084)

        self.style.configure('Tsub_path_label.TLabel', anchor='w', font=('iLiHei', 10))
        self.sub_path_label = Label(self.mapping_frame, text='SUB Path', style='Tsub_path_label.TLabel')
        self.sub_path_label.place(relx=0.032, rely=0.269, relwidth=0.085, relheight=0.084)

        self.video_type_entryVar = StringVar(value=self.videotype_ini)
        self.video_type_entry = Entry(self.rename_frame, textvariable=self.video_type_entryVar, font=('iLiHei', 10))
        self.video_type_entry.place(relx=0.042, rely=0.323, relwidth=0.915, relheight=0.084)

        self.HScroll3 = Scrollbar(self.view_right_frame, orient='horizontal')
        self.HScroll3.place(relx=0.018, rely=0.944, relwidth=0.946, relheight=0.038)

        self.VScroll3 = Scrollbar(self.view_right_frame, orient='vertical')
        self.VScroll3.place(relx=0.961, rely=0.015, relwidth=0.039, relheight=0.935)

        self.view_text_rightFont = Font(font=('iLiHei',10))
        self.view_right_text = Text(self.view_right_frame, wrap='none', xscrollcommand=self.HScroll3.set, yscrollcommand=self.VScroll3.set, font=self.view_text_rightFont)
        self.view_right_text.place(relx=0.018, rely=0.015, relwidth=0.946, relheight=0.930)
        self.HScroll3['command'] = self.view_right_text.xview
        self.VScroll3['command'] = self.view_right_text.yview

        self.video_path_entryVar = StringVar(value=self.videopath_ini)
        self.video_path_entry = Entry(self.rename_frame, textvariable=self.video_path_entryVar, font=('iLiHei', 10))
        self.video_path_entry.place(relx=0.042, rely=0.135, relwidth=0.915, relheight=0.084)

        self.HScroll2 = Scrollbar(self.view_center_frame, orient='horizontal')
        self.HScroll2.place(relx=0.018, rely=0.944, relwidth=0.946, relheight=0.038)

        self.VScroll2 = Scrollbar(self.view_center_frame, orient='vertical')
        self.VScroll2.place(relx=0.961, rely=0.015, relwidth=0.039, relheight=0.935)

        self.view_center_textFont = Font(font=('iLiHei', 10))
        self.view_center_text = Text(self.view_center_frame, wrap='none', xscrollcommand=self.HScroll2.set, yscrollcommand=self.VScroll2.set, font=self.view_center_textFont)
        self.view_center_text.place(relx=0.018, rely=0.015, relwidth=0.946, relheight=0.930)
        self.HScroll2['command'] = self.view_center_text.xview
        self.VScroll2['command'] = self.view_center_text.yview

        self.style.configure('Tvideo_type_label.TLabel', anchor='w', font=('iLiHei', 10))
        self.video_type_label = Label(self.rename_frame, text='Video Type', style='Tvideo_type_label.TLabel')
        self.video_type_label.place(relx=0.042, rely=0.269, relwidth=0.279, relheight=0.084)

        self.style.configure('Trename_input_label.TLabel', anchor='w', font=('iLiHei', 10))
        self.rename_input_label = Label(self.rename_frame, text='Input:', style='Trename_input_label.TLabel')
        self.rename_input_label.place(relx=0.042, rely=0.450, relwidth=0.279, relheight=0.084)

        self.rename_input_enrtyVar = StringVar(value='aa_*_aaa')
        self.rename_input_enrty = Entry(self.rename_frame, textvariable=self.rename_input_enrtyVar, font=('iLiHei', 10))
        self.rename_input_enrty.place(relx=0.042, rely=0.550, relwidth=0.915, relheight=0.084)

        # =======位數, 起始位數, 啟用反轉排序=====
        self.style.configure('Tdigit_number_label.TLabel', anchor='w', font=('iLiHei', 10))
        self.digit_number_label = Label(self.rename_frame, text='編號位數:', style='Tdigit_number_label.TLabel')
        self.digit_number_label.place(relx=0.042, rely=0.650, relwidth=0.279, relheight=0.084)

        self.digit_number_enrtyVar = StringVar(value='2')
        self.digit_number_enrty = Entry(self.rename_frame, textvariable=self.digit_number_enrtyVar, font=('iLiHei', 10))
        self.digit_number_enrty.place(relx=0.210, rely=0.650, relwidth=0.060, relheight=0.084)

        self.style.configure('Tstart_number_label.TLabel', anchor='w', font=('iLiHei', 10))
        self.start_number_label = Label(self.rename_frame, text='起始位數:', style='Tstart_number_label.TLabel')
        self.start_number_label.place(relx=0.280, rely=0.650, relwidth=0.279, relheight=0.084)

        self.start_number_enrtyVar = StringVar(value='1')
        self.start_number_enrty = Entry(self.rename_frame, textvariable=self.start_number_enrtyVar, font=('iLiHei', 10))
        self.start_number_enrty.place(relx=0.450, rely=0.650, relwidth=0.060, relheight=0.084)
        #
        self.lucky_sort_chbuttonVar = IntVar(value=0)
        self.style.configure('Tlucky_sort_chbutton.TCheckbutton', font=('iLiHei', 10))
        self.lucky_sort_chbutton = Checkbutton(self.rename_frame, text='碰運氣排序', variable=self.lucky_sort_chbuttonVar, style='Tlucky_sort_chbutton.TCheckbutton')
        self.lucky_sort_chbutton.place(relx=0.042, rely=0.750, relwidth=0.250, relheight=0.084)
        # =======

        self.HScroll1 = Scrollbar(self.view_left_frame, orient='horizontal')
        self.HScroll1.place(relx=0.021, rely=0.944, relwidth=0.936, relheight=0.038)

        self.VScroll1 = Scrollbar(self.view_left_frame, orient='vertical')
        self.VScroll1.place(relx=0.955, rely=0.015, relwidth=0.045, relheight=0.935)

        self.view_left_textFont = Font(font=('iLiHei', 10))
        self.view_left_text = Text(self.view_left_frame, wrap='none', xscrollcommand=self.HScroll1.set, yscrollcommand=self.VScroll1.set, font=self.view_left_textFont)
        self.view_left_text.place(relx=0.021, rely=0.015, relwidth=0.936, relheight=0.930)
        self.VScroll1['command'] = self.view_left_text.yview
        self.HScroll1['command'] = self.view_left_text.xview

        # ------Setting font color-----
        self.view_right_text.tag_config("error", foreground="#CC0000")
        self.view_right_text.tag_config("info", foreground="#008800")
        self.view_right_text.tag_config("info2", foreground="#404040")
        self.view_center_text.tag_config("error", foreground="#CC0000")
        self.view_center_text.tag_config("info", foreground="#008800")
        self.view_center_text.tag_config("info2", foreground="#404040")
        self.view_left_text.tag_config("error", foreground="#CC0000")
        self.view_left_text.tag_config("info", foreground="#008800")
        self.view_left_text.tag_config("info2", foreground="#404040")

        self.default_radio['command'] = self.radiokbutton_selected
        self.strengthen_radio['command'] = self.radiokbutton_selected
        self.manually_radio['command'] = self.radiokbutton_selected

        self.turnon_mapping_chbutton['command'] = self.turn_on_mapping_selected
        # self.uses_samepath_chbutton['command'] = self.turn_on_mapping_selected
        self.lucky_sort_chbutton['command'] = self.lucky_store_selected

        self.radiobutton_select.set(1)  # default uses default mapping method

        # -----Register for handler and key event-----
        # make the top right close button minimize (iconify) the main window
        self.top.protocol("WM_DELETE_WINDOW", self.close_ren_frame)
        self.top.bind('<Escape>', self.show_preview_on_textview)
        self.sub_path_entry.bind('<Key>', self.start_count_entry_input)
        self.sub_type_entry.bind('<Key>', self.start_count_entry_input)
        self.video_path_entry.bind('<Key>', self.start_count_entry_input)
        self.video_type_entry.bind('<Key>', self.start_count_entry_input)
        self.video_keyword_entry.bind('<Key>', self.start_count_entry_input)
        self.sub_keyword_entry.bind('<Key>', self.start_count_entry_input)
        self.rename_input_enrty.bind('<Key>', self.start_count_entry_input)
        self.digit_number_enrty.bind('<Key>', self.start_count_entry_input)
        self.start_number_enrty.bind('<Key>', self.start_count_entry_input)

        self.view_left_text.bind("<Control-Key-A>", self.view_select_all)
        self.view_left_text.bind("<Control-Key-a>", self.view_select_all)
        self.view_left_text.bind("<ButtonRelease-1>", self.view_select_get_and_mark_select)

        self.view_center_text.bind("<Control-Key-A>", self.view_select_all)  # just in case caps lock is on
        self.view_center_text.bind("<Control-Key-a>", self.view_select_all)  # just in case caps lock is on
        self.view_center_text.bind("<ButtonRelease-1>", self.view_select_get_and_mark_select)

        # -----Show rename preview on text-----

        self.show_preview_on_textview()

    def view_select_get_and_mark_select(self, event=None):
        user_mouse_left_select_list = ''
        self.stop_count_timer()
        if self.turnon_mapping_chbuttonVar.get() == 0:
            try:
                # -----view left select-----
                text_mark_start_lv = str(self.view_left_text.index(SEL_FIRST))
                text_mark_start_lv = text_mark_start_lv.split('.')
                text_mark_end_lv = str(self.view_left_text.index(SEL_LAST))
                text_mark_end_lv = text_mark_end_lv.split('.')

                self.view_left_text.tag_add(SEL, '%s.0' % text_mark_start_lv[0], '%s.%s' % (text_mark_end_lv[0], END))
                self.view_left_text.see(INSERT)

                temp_text_list = (self.view_left_text.get('%s.0' % text_mark_start_lv[0],
                                                          '%s.%s' % (text_mark_end_lv[0], END)))
                user_mouse_left_select_list = temp_text_list.split("\n")

                self.show_preview_on_textview(user_mouse_left_select_list)
            except:
                # if self.turnon_mapping_chbuttonVar.get() == 0:
                    print('not select any thing in left view')
                    self.show_preview_on_textview()

        # if self.view_center_text.focus:
        #     if self.turnon_mapping_chbuttonVar.get() == 1:
        #         try:
        #             # -----view center select-----
        #             text_mark_start_lv = str(self.view_center_text.index(SEL_FIRST))
        #             text_mark_start_lv = text_mark_start_lv.split('.')
        #             text_mark_end_lv = str(self.view_center_text.index(SEL_LAST))
        #             text_mark_end_lv = text_mark_end_lv.split('.')
        #
        #             self.view_center_text.tag_add(SEL, '%s.0' % text_mark_start_lv[0], '%s.%s' % (text_mark_end_lv[0], END))
        #             self.view_center_text.see(INSERT)
        #
        #             temp_text_list = (self.view_center_text.get('%s.0' % text_mark_start_lv[0],
        #                                                         '%s.%s' % (text_mark_end_lv[0], END)))
        #             user_mouse_center_select_list = temp_text_list.split("\n")
        #             # print(text_mark_end_lv)
        #             self.show_preview_on_textview(user_mouse_left_select_list, user_mouse_center_select_list)
        #         except:
        #             print('not select any thing in center view')
        #             self.show_preview_on_textview()

    def view_select_all(self, event=None):
        self.view_left_text.tag_add(SEL, "1.0", END)
        self.view_left_text.mark_set(INSERT, "1.0")
        self.view_left_text.see(INSERT)
        return 'break'

    def start_count_timer(self, sec):
        if self.timer_h and self.timer_h.isAlive():
            self.timer_h.cancel()
        self.timer_h = Timer(sec, self.timer_count_expired)

        self.timer_h.start()

    def stop_count_timer(self):
        if self.timer_h and self.timer_h.isAlive():
            # Stop the timer instance
            self.timer_h.cancel()
            # print('Timer stopped')

        self.timer_running_fl = False

    def timer_count_expired(self):
        self.stop_count_timer()
        print("===start preview===")
        self.show_preview_on_textview()
        self.timer_running_fl = False

    def start_count_entry_input(self, event=None):
        if not self.timer_running_fl:
            self.timer_running_fl = True
            self.start_count_timer(1)
        else:
            self.stop_count_timer()
            self.start_count_timer(1)

    def turn_on_mapping_selected(self):
        if not self.turnon_mapping_chbuttonVar.get():
            self.view_right_frame.place_forget()
            self.view_center_frame.place(relx=0.500, rely=0., relwidth=0.500, relheight=0.595)
            self.view_left_frame.place(relx=0.006, rely=0., relwidth=0.500, relheight=0.595)

        else:
            self.view_right_frame.place(relx=0.652, rely=0., relwidth=0.349, relheight=0.595)
            self.view_center_frame.place(relx=0.304, rely=0., relwidth=0.349, relheight=0.595)
            self.view_left_frame.place(relx=0.006, rely=0., relwidth=0.298, relheight=0.595)

        self.stop_count_timer()
        self.show_preview_on_textview()

    def lucky_store_selected(self):
        self.stop_count_timer()
        self.show_preview_on_textview()

    def radiokbutton_selected(self):
        self.stop_count_timer()
        self.show_preview_on_textview()
        if self.radiobutton_select.get() == 1:
            print("1")
            # set item dim
            pass
        if self.radiobutton_select.get() == 2:
            # set item activate
            print("2")
            pass
        if self.radiobutton_select.get() == 3:
            # set item dim
            print("3")
            pass

    def show_preview_on_textview(self, user_mouse_left_select_list=None, event=None):
        # turn on mapping function
        if self.turnon_mapping_chbuttonVar.get() == 1:
            # print(user_mouse_left_select_list)

            if not user_mouse_left_select_list:
                self.view_left_text.config(state="normal")
                self.view_left_text.delete('1.0', END)
                self.view_left_text.config(state="disable")
                self.view_center_text.config(state="normal")
                self.view_center_text.delete('1.0', END)
                self.view_center_text.config(state="disable")

            self.view_right_text.config(state="normal")
            self.view_right_text.delete('1.0', END)
            self.view_right_text.config(state="disable")

            # -----Clear previous mapping result-----
            self.mapping_orisub_and_video_odic.clear()
            self.mapping_orisub_and_sub_odic.clear()

            [status, sub_path_lv, sub_type_lv, video_path_lv, video_type_lv, sub_keyword_lv, video_keywork_lv] = \
                self.arrange_user_input_format()
            # print(status)
            if status == error_Code.NORMAL.value:
                for sub_type_i in sub_type_lv:
                    self.match_sub_and_video_file_update_odic(sub_path_lv, sub_type_i, video_path_lv, video_type_lv,
                                                              sub_keyword_lv, video_keywork_lv)
                self.show_list_on_view_text(self.mapping_orisub_and_video_odic, self.mapping_orisub_and_sub_odic)
        # Rename function
        else:
            self.view_right_text.config(state="normal")
            self.view_right_text.delete('1.0', END)
            self.view_right_text.config(state="disable")
            self.view_center_text.config(state="normal")
            self.view_center_text.delete('1.0', END)
            self.view_center_text.config(state="disable")

            if not user_mouse_left_select_list:
                self.view_left_text.config(state="normal")
                self.view_left_text.delete('1.0', END)
                self.view_left_text.config(state="disable")

            self.rename_ori_and_rename_odic.clear()

            [status, video_path_lv, video_type_lv, rename_input_lv, user_input_star_number_lv, user_input_digit_number_lv] = self.arrange_user_input_format()
            if status == error_Code.NORMAL.value:
                self.ori_rename_store_odic(status, video_path_lv, video_type_lv, rename_input_lv, user_input_star_number_lv, user_input_digit_number_lv, user_mouse_left_select_list)

    def arrange_user_input_format(self):
        status_lv = error_Code.NORMAL.value

        # -----Check user input video path-----
        user_input_video_path_lv = re.sub(r"/$", '', self.video_path_entry.get())
        user_input_video_path_lv = re.sub(r"\\$", "", user_input_video_path_lv)

        if not os.path.exists(user_input_video_path_lv):
            status_lv = error_Code.USER_VIDEO_INPUT_PATH_ERROR.value
            # return error_Code.USER_VIDEO_INPUT_PATH_ERROR.value

        # -----Check user input video path-----
        re_lv = re.sub(r' ', '', self.video_type_entry.get())
        user_input_video_type_ls = re_lv.split(",")
        # remove duplicate item
        user_input_video_type_ls = set(user_input_video_type_ls)

        if not user_input_video_type_ls:
            status_lv = error_Code.USER_VIDEO_INPUT_PATH_ERROR.value
        # --------------------------------------

        # for rename function
        if self.turnon_mapping_chbuttonVar.get() == 0:

            user_input_rename_input_lv = self.rename_input_enrty.get()
            if not user_input_rename_input_lv.find('*'):
                status_lv = error_Code.USER_RENAME_INPUT_ERROR.value

            user_input_star_number_lv = self.start_number_enrtyVar.get()
            # user_input_star_number_lv = re.math()
            # print(user_input_star_number_lv)
            if not user_input_star_number_lv.isdigit():
                user_input_star_number_lv = 1

            user_input_digit_number_lv = self.digit_number_enrtyVar.get()
            # user_input_star_number_lv = re.math()
            # print(user_input_star_number_lv)
            if not user_input_digit_number_lv.isdigit():
                user_input_digit_number_lv = 2

            return status_lv, user_input_video_path_lv, user_input_video_type_ls, user_input_rename_input_lv, \
                int(user_input_star_number_lv), int(user_input_digit_number_lv)

        # for mapping function
        else:
            # ----user input sub path-----
            user_input_sub_path_lv = re.sub(r"/$", '', self.sub_path_entry.get())
            user_input_sub_path_lv = re.sub(r"\\$", "", user_input_sub_path_lv)

            if self.uses_samepath_chbuttonVar == 1:
                user_input_sub_path_lv = user_input_video_path_lv
                user_input_sub_type_ls = user_input_video_type_ls
            else:
                if not os.path.exists(user_input_sub_path_lv):
                    status_lv = error_Code.USER_SUB_INPUT_PATH_ERROR.value
                    # return error_Code.USER_SUB_INPUT_PATH_ERROR.value

                re_lv = re.sub(r' ', '', self.sub_type_entry.get())
                user_input_sub_type_ls = re_lv.split(",")
                # -----remove duplicate item-----
                user_input_sub_type_ls = set(user_input_sub_type_ls)

                if not user_input_sub_type_ls:
                    status_lv = error_Code.USER_SUB_INPUT_TYPE_ERROR.value

            user_input_sub_keyword_lv = self.sub_keyword_entry.get()
            if not user_input_sub_keyword_lv.find('*'):
                status_lv = error_Code.USER_SUB_INPUT_KEYWORD_ERROR.value

            user_input_video_keyword_lv = self.video_keyword_entry.get()
            if not user_input_video_keyword_lv.find('*'):
                status_lv = error_Code.USER_VIDEO_INPUT_KEYWORD_ERROR.value


            return status_lv, user_input_sub_path_lv, user_input_sub_type_ls, user_input_video_path_lv, \
                user_input_video_type_ls, user_input_sub_keyword_lv, user_input_video_keyword_lv

    def ori_rename_store_odic(self, u_in_status, u_in_video_path, u_in_video_type, u_in_rename,
                              user_input_star_number_lv, user_input_digit_number_lv, user_mouse_select_list=None):
        file_list_ll = []
        file_list_odic = OrderedDict()
        key_prv = ''
        key_aft = ''

        video_key_re_h = re.match(r'(.*)\*(.*)', u_in_rename)
        if video_key_re_h:
            key_prv = video_key_re_h.group(1)
            key_aft = video_key_re_h.group(2)
            if not video_key_re_h.group(1):
                key_prv = ''
            if not video_key_re_h.group(2):
                key_aft = ''

        # -----user key-in some thing, need re-get file list
        if not user_mouse_select_list:
            # -----get sub file list-----
            os.chdir(u_in_video_path)
            for i in u_in_video_type:
                temp_list_lv = glob.glob(i)
                # temp_list_lv = glob.glob('%s\\%s' % (u_in_sub_path, u_in_sub_type))
                # print(temp_list_lv)
                if temp_list_lv:
                    file_list_ll.extend(temp_list_lv)

            if self.lucky_sort_chbuttonVar.get():
                # revert sort list, try to split TC and SC file name
                temp_ll = []
                split_sub_file_list_ll = []
                # print(sub_file_list_ll)
                for i in file_list_ll:
                    temp_ll.append(i[::-1])
                    temp_ll.sort()

                for i in temp_ll:
                    split_sub_file_list_ll.append(i[::-1])

                file_list_ll = split_sub_file_list_ll
                # print(file_list_ll)

            self.view_left_text.config(state="normal")
            for i in file_list_ll:
                self.view_left_text.insert(INSERT, '%s\n' % i)
            self.view_left_text.config(state="disable")

        # -----User use mouse select list, no need to re-get file list, change to uses selected file list
        else:
            file_list_ll = user_mouse_select_list
            # print(file_list_ll)

        # -----Store ori and rename file name to odic-----
        file_list_ll = tuple(file_list_ll)
        if u_in_status == error_Code.NORMAL.value:
            count = user_input_star_number_lv
            for i in file_list_ll:
                digit_count = user_input_digit_number_lv - len(str(count))
                c = os.path.splitext(i)
                if c[1]:
                    ext = c[1]
                else:
                    ext = ''

                if digit_count > 0:
                    digit_str = '0' * digit_count
                    file_list_odic[i] = '%s%s%s%s%s' % (key_prv, digit_str, count, key_aft, ext)
                else:
                    file_list_odic[i] = '%s%s%s%s' % (key_prv, count, key_aft, ext)
                count += 1

            self.rename_ori_and_rename_odic = file_list_odic

            # =======================================================================================
            self.view_center_text.config(state="normal")
            for i, v in file_list_odic.items():
                self.view_center_text.insert(INSERT, '%s\n' % i)
                self.view_center_text.insert(INSERT, '%s\n' % v, 'info')

            self.view_center_text.config(state="disable")

    def match_sub_and_video_file_update_odic(self, u_in_sub_path, u_in_sub_type, u_in_video_path, u_in_video_type,
                                             u_in_sub_keyword, u_in_video_keywork, user_input_digit_number_lv=None,
                                             user_mouse_left_select_list=None):
        temp_file_list_ll = []
        videofile_list_ll = []
        sub_file_list_ll = []
        spli_sub_file_list_ll = []
        videofile_list_odic = OrderedDict()
        subfile_list_odic = OrderedDict()
        # -----user two orderedDice to store ori sub , video and rename sub file,
        # these two orderDice uses the same key: orisub-----
        mapping_orisub_and_video_odic = OrderedDict()
        mapping_orisub_and_sub_odic = OrderedDict()
        videonum_re_h = ''
        subnum_re_h = ''
        # sub_type_fil_ext = ''

        # -----get video file list-----
        os.chdir(u_in_video_path)
        # glob.glob(sub_path + '\\' + i)
        for i in u_in_video_type:
            temp_list_lv = glob.glob(i)
            # temp_list_lv = glob.glob(u_in_video_path + '\\' + i)
            # temp_list_lv = glob.glob('%s\\%s' % (u_in_video_path, i))
            if temp_list_lv:
                videofile_list_ll.extend(temp_list_lv)


        # -----get sub file list-----
        os.chdir(u_in_sub_path)

        temp_list_lv = glob.glob(u_in_sub_type)
        # temp_list_lv = glob.glob('%s\\%s' % (u_in_sub_path, u_in_sub_type))
        # print(temp_list_lv)
        sub_type_fil_ext = u_in_sub_type.replace("*.", "")
        if temp_list_lv:
            sub_file_list_ll.extend(temp_list_lv)

        for i in sub_file_list_ll:
            # subfile_list_ls = tuple(subfile_list_ls)
            subfile_list_odic[i] = ""

        # -----Free memory-----
        del temp_file_list_ll
        del temp_list_lv

        # -----default matching method-----
        if self.radiobutton_select.get() == 1:
            if user_input_digit_number_lv and user_mouse_left_select_list:
                sub_file_list_ll = user_input_digit_number_lv
                videofile_list_ll = user_mouse_left_select_list

            # -----change to tuple type for speed up-----
            sub_file_list_ll = tuple(sub_file_list_ll)
            videofile_list_ll = tuple(videofile_list_ll)

            if sub_file_list_ll and videofile_list_ll:
                print("default mapping method, start mapping video and sub")

                count = 0
                for i in sub_file_list_ll:
                    c = os.path.splitext(videofile_list_ll[count])
                    mapping_orisub_and_video_odic[i] = videofile_list_ll[count]
                    mapping_orisub_and_sub_odic[i] = "%s.%s" % (c[0], sub_type_fil_ext)
                    count += 1

                # update mapping_orisub_and_video_odic, mapping_orisub_and_sub_odic
                self.mapping_orisub_and_video_odic.update(mapping_orisub_and_video_odic)
                self.mapping_orisub_and_sub_odic.update(mapping_orisub_and_sub_odic)
            return

        elif self.radiobutton_select.get() == 2:
            # TODO: 反轉字串重新排序, 可能可以分離TC, SC檔案
            temp_ll = []
            # print(sub_file_list_ll)
            for i in sub_file_list_ll:
                temp_ll.append(i[::-1])

                temp_ll.sort()

            for i in temp_ll:
                spli_sub_file_list_ll.append(i[::-1])

            print(spli_sub_file_list_ll)

            return
        # -----manually matching method-----
        else:
            # -----Generate video keyword compile-----
            video_key_re_h = re.match(r'(.*)\*(.*)', u_in_video_keywork)
            if video_key_re_h:
                key_prv = video_key_re_h.group(1)
                key_aft = video_key_re_h.group(2)
                if not video_key_re_h.group(1):
                    key_prv = ''
                if not video_key_re_h.group(2):
                    key_aft = ''
                videonum_re_h = re.compile(r'%s(.*)%s'
                                           % (re.escape(key_prv), re.escape(key_aft)))
            # -----Generate video keyword compile-----
            sub_key_re_h = re.match(r'(.*)\*(.*)', u_in_sub_keyword)
            if sub_key_re_h:
                key_prv = sub_key_re_h.group(1)
                key_aft = sub_key_re_h.group(2)
                if not sub_key_re_h.group(1):
                    key_prv = ''
                if not sub_key_re_h.group(2):
                    key_aft = ''
                subnum_re_h = re.compile(r'%s(.*)%s'
                                         % (re.escape(key_prv), re.escape(key_aft)))

            # -----if uses manually mapping method, remove video filename extension and save list to ordered dict-----
            # -----change to tuple type for speed up-----
            sub_file_list_ll = tuple(sub_file_list_ll)
            videofile_list_ll = tuple(videofile_list_ll)

            for i in videofile_list_ll:
                c = os.path.splitext(i)
                videofile_list_odic[i] = c[0]

            if subfile_list_odic and videofile_list_odic:
                print("start mapping video and sub")
                # -----save mapping table to dic-----
                for s_name_j in subfile_list_odic:
                    mapping_state_lv = 0
                    # s_key_lv = list(map(int, (subnum_re_h.findall(s_name_j))))
                    s_key_lv = subnum_re_h.findall(s_name_j)

                    if s_key_lv:
                        try:
                            s_key_lv = list(map(int, s_key_lv))
                        except:  # get key is not a number
                            continue
                    else:
                        continue
                    # print(s_key_lv)
                    # s_key_lv = ''.join(subnum_re_h.findall)
                    for v_fullname_i, v_name_nonext_j in videofile_list_odic.items():
                        # print(v_name_nonext_j)
                        # v_key_lv = list(map(int, (videonum_re_h.findall(v_name_nonext_j))))
                        v_key_lv = videonum_re_h.findall(v_name_nonext_j)
                        if v_key_lv:
                            try:
                                v_key_lv = list(map(int, v_key_lv))
                            except:  # get key is not a number
                                break
                        else:
                            break
                        # print(v_key_lv)
                        if v_key_lv == s_key_lv and v_key_lv:
                            mapping_state_lv = 1
                            # mapping_orisub_and_video_odic.update({v_name_i: s_name_j})
                            mapping_orisub_and_video_odic[s_name_j] = v_fullname_i
                            mapping_orisub_and_sub_odic[s_name_j] = "%s.%s" % (v_name_nonext_j, sub_type_fil_ext)
                            break

                    # -----Remove matched video file list for speedup-----
                    if mapping_state_lv == 1:
                        videofile_list_odic.pop(v_fullname_i, "key not found")
                        # for t, c in videofile_list_odic.items():
                        #     print(t, c)

            # update mapping_orisub_and_video_odic, mapping_orisub_and_sub_odic
            self.mapping_orisub_and_video_odic.update(mapping_orisub_and_video_odic)
            self.mapping_orisub_and_sub_odic.update(mapping_orisub_and_sub_odic)
            # self.show_list_on_view_text(mapping_orisub_and_video_odic, mapping_orisub_and_sub_odic)

    def show_list_on_view_text(self, mapping_orisub_and_video_odic, mapping_orisub_and_sub_odic):
        # print (mapping_orisub_and_sub_odic[])

        self.view_left_text.config(state="normal")
        self.view_center_text.config(state="normal")
        self.view_right_text.config(state="normal")
        for i, j in mapping_orisub_and_video_odic.items():
            # print(mapping_orisub_and_sub_odic[i])
            # if not (user_mouse_left_select_list or user_mouse_center_select_list):
            self.view_left_text.insert(INSERT, "%s\n" % i)
            self.view_center_text.insert(INSERT, "%s\n" % j)

            self.view_right_text.insert(INSERT, "%s\n" % i)
            self.view_right_text.insert(INSERT, "%s\n" % j)
            self.view_right_text.insert(INSERT, "%s\n" % mapping_orisub_and_sub_odic[i], 'info')
            # print(i, mapping_orisub_and_sub_odic[i])
        self.view_left_text.config(state="disable")
        self.view_center_text.config(state="disable")
        self.view_right_text.config(state="disable")

    def start_rename(self):
        pass

    def close_ren_frame(self, event=None):
        print("current path: "+os.getcwd())
        os.chdir(self.app_current_path)
        print("change to path: " + os.getcwd())
        if self.timer_h:
            self.stop_count_timer()
        self.top.destroy()
        return
