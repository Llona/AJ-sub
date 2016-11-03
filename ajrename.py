from tkinter import *
import tkinter.messagebox
from tkinter.font import Font
from tkinter.ttk import *
import glob
import os
import re
import configparser
from enum import Enum
from time import sleep
from threading import Timer
from collections import OrderedDict


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
    MAPPING_LIST_EMPTY = 9
    UNKNOW_ERROR = 10


class rename_frame:
    def __init__(self, parent, main_sub_path, main_sub_type, setting_name):
        self.status = error_Code.NORMAL.value
        self.select_turn_on_mapping_fl = False
        self.main_sub_path = main_sub_path
        self.main_sub_type = main_sub_type
        self.setting_ini_file_name = setting_name
        self.setting_ini_dic = {}
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
        self.top.title("AJRen - 全力修改! 檔名君")
        self.top.iconbitmap('icons\\rename.ico')
        # self.top_window = Toplevel(parent)
        # self.top_window.overrideredirect(1)
        self.top['takefocus'] = True
        self.top.grab_set()
        self.top.focus_force()

        self.help_text = \
            "AJRen \n\n" \
            "本軟體為 AJSub 附屬應用程式, 可快速方便的批次更改檔名\n" \
            "原始檔名視窗為目錄中的原始檔名, \n"\
            "在結果預覽視窗可預覽改名結果, 黑色為原始檔名, 綠色為更改後的檔名\n\n"\
            "更改檔名使用說明:\n" \
            "1. 輸入檔案路徑與檔案類型, 如*.ass, *.ssa\n" \
            "2. 取代為欄位中, *的部份會替代為數字, 例如輸入*_image\n" \
            "    會將原始檔改名為如01_image, 02_image...\n"\
            "3. 輸入編號位數與起始位數\n"\
            "4. 在預覽視窗確認改名結果正確後, 按下更改檔名按鈕\n"\
            "    即可照設定修改檔名\n"\
            "5. 如果目錄同時有簡體和繁體字幕檔, 例如xxxSC.xx 和xxxTC.xx\n" \
            "    勾選碰運氣排序, 運氣好可以分離這些檔案喔\n"\
            "6. 在同一目錄中若只想針對幾個檔案改名\n"\
            "    可在原始檔名視窗用滑鼠標記起來, 預覽視窗可看到結果\n\n" \
            "比對更改檔名模式:\n"\
            "批次將原始檔案配合比對檔案修改成對應的檔名, 例如:\n"\
            "    目錄中有aa_01.ssc, 01_video.mp4, 可透過此功能比對後, 將\n"\
            "    aa_01.ssc改為01_video.ssc (02, 03, 04...etc, 一次修改完成)\n\n"\
            "AJRen由Llona開發維護, \n" \
            "詳細功能說明, 問題回報與下載頁面: https://llona.github.io/AJ-sub/ \n\n" \
            "Implement by [Llona], \n" \
            "Bug report and download page: https://llona.github.io/AJ-sub/"

        try:
            # -----Get all setting from Settings.ini-----
            file_ini_h = open(setting_name, encoding='utf16')
            config_file_h = configparser.ConfigParser()
            config_file_h.read_file(file_ini_h)
            file_ini_h.close()
            self.setting_ini_dic['input_rename_ini'] = config_file_h.get('Rename', 'input_rename')
            self.setting_ini_dic['digit_number_ini'] = config_file_h.get('Rename', 'digit_number')
            self.setting_ini_dic['start_number_ini'] = config_file_h.get('Rename', 'start_number')

            self.setting_ini_dic['videopath_ini'] = config_file_h.get('Mapping', 'mappingpath')
            self.setting_ini_dic['videotype_ini'] = config_file_h.get('Mapping', 'mappingtype')
            self.setting_ini_dic['videokeyword_ini'] = config_file_h.get('Mapping', 'videokeyword')
            self.setting_ini_dic['subkeyword_ini'] = config_file_h.get('Mapping', 'subkeyword')
            self.setting_ini_dic['use_same_path_ini'] = config_file_h.get('Mapping', 'use_same_path')
            config_file_h.clear()
        except:
            self.status = error_Code.FILE_ERROR.value

            tkinter.messagebox.showerror("Error", "Read setting fail " + setting_name+" fail!\n"
                                         "Please check " + setting_name +
                                         " setting file is correct (UTF-16 format) or re-install AJSub",
                                         parent=self.top)
            self.close_ren_frame()

        self.show_rename_frame()

    def show_rename_frame(self):
        self.style = Style()

        self.style.configure('Trename_frame.TLabelframe', font=('iLiHei', 9))
        self.style.configure('Trename_frame.TLabelframe.Label', font=('iLiHei', 9))
        self.rename_frame = LabelFrame(self.top, text='更改檔名', style='Trename_frame.TLabelframe')
        self.rename_frame.place(relx=0.006, rely=0.605, relwidth=0.298, relheight=0.394)

        self.style.configure('Tmapping_frame.TLabelframe', font=('iLiHei', 9))
        self.style.configure('Tmapping_frame.TLabelframe.Label', font=('iLiHei', 9))
        self.mapping_frame = LabelFrame(self.top, text='比對更改檔名模式', style='Tmapping_frame.TLabelframe')
        self.mapping_frame.place(relx=0.31, rely=0.605, relwidth=0.580, relheight=0.394)

        self.style.configure('Tview_right_frame.TLabelframe', font=('iLiHei', 9))
        self.style.configure('Tview_right_frame.TLabelframe.Label', font=('iLiHei', 9))
        self.view_right_frame = LabelFrame(self.top, text='配對結果預覽', style='Tview_right_frame.TLabelframe')

        self.style.configure('Tview_center_frame.TLabelframe', font=('iLiHei', 9))
        self.style.configure('Tview_center_frame.TLabelframe.Label', font=('iLiHei', 9))
        self.view_center_frame = LabelFrame(self.top, style='Tview_center_frame.TLabelframe')
        self.view_center_frame.place(relx=0.500, rely=0., relwidth=0.500, relheight=0.595)

        self.style.configure('Tview_left_frame.TLabelframe', font=('iLiHei', 9))
        self.style.configure('Tview_left_frame.TLabelframe.Label', font=('iLiHei', 9))
        self.view_left_frame = LabelFrame(self.top, text='原始檔名', style='Tview_left_frame.TLabelframe')
        self.view_left_frame.place(relx=0.006, rely=0., relwidth=0.500, relheight=0.595)

        self.style.configure('Tvideo_path_label.TLabel', anchor='w', font=('iLiHei', 10))
        self.video_path_label = Label(self.mapping_frame, text='比對檔案路徑', style='Tvideo_path_label.TLabel')
        self.video_path_label.place(relx=0.032, rely=0.269, relwidth=0.250, relheight=0.084)

        self.video_path_entryVar = StringVar(value=self.setting_ini_dic['videopath_ini'])
        self.video_path_entry = Entry(self.mapping_frame, textvariable=self.video_path_entryVar, font=('iLiHei', 10))
        self.video_path_entry.place(relx=0.032, rely=0.360, relwidth=0.38, relheight=0.084)

        self.style.configure('Tvideo_type_label.TLabel', anchor='w', font=('iLiHei', 10))
        self.video_type_label = Label(self.mapping_frame, text='比對檔案類型', style='Tvideo_type_label.TLabel')
        self.video_type_label.place(relx=0.032, rely=0.458, relwidth=0.250, relheight=0.084)

        self.video_type_entryVar = StringVar(value=self.setting_ini_dic['videotype_ini'])
        self.video_type_entry = Entry(self.mapping_frame, textvariable=self.video_type_entryVar, font=('iLiHei', 10))
        self.video_type_entry.place(relx=0.032, rely=0.550, relwidth=0.38, relheight=0.084)

        self.style.configure('Tsub_path_label.TLabel', anchor='w', font=('iLiHei', 10))
        self.sub_path_label = Label(self.rename_frame, text='檔案路徑', style='Tsub_path_label.TLabel')
        self.sub_path_label.place(relx=0.042, rely=0.061, relwidth=0.194, relheight=0.084)

        self.sub_path_entryVar = StringVar(value=self.main_sub_path)
        self.sub_path_entry = Entry(self.rename_frame, textvariable=self.sub_path_entryVar, font=('iLiHei', 10))
        self.sub_path_entry.place(relx=0.042, rely=0.135, relwidth=0.915, relheight=0.084)

        self.style.configure('Tsub_type_label.TLabel', anchor='w', font=('iLiHei', 10))
        self.sub_type_label = Label(self.rename_frame, text='檔案類型', style='Tsub_type_label.TLabel')
        self.sub_type_label.place(relx=0.042, rely=0.255, relwidth=0.279, relheight=0.084)

        self.sub_type_entryVar = StringVar(value=self.main_sub_type)
        self.sub_type_entry = Entry(self.rename_frame, textvariable=self.sub_type_entryVar, font=('iLiHei', 10))
        self.sub_type_entry.place(relx=0.042, rely=0.340, relwidth=0.915, relheight=0.084)

        self.style.configure('Trename_button.TButton', font=('iLiHei', 10))
        self.rename_button = Button(self.rename_frame, text='更改檔名', command=self.start_rename, style='Trename_button.TButton')
        self.rename_button.place(relx=0.700, rely=0.835, relwidth=0.260, relheight=0.111)

        self.help_button = Button(self.rename_frame, text='Help', command=self.print_about, style='Trename_button.TButton')
        self.help_button.place(relx=0.350, rely=0.835, relwidth=0.260, relheight=0.111)

        self.style.configure('Tstart_button.TButton', font=('iLiHei', 10))
        self.start_button = Button(self.mapping_frame, text='比對改名', command=self.start_mapping_rename, style='Tstart_button.TButton')
        self.start_button.place(relx=0.021, rely=0.835, relwidth=0.127, relheight=0.111)

        self.turnon_mapping_chbuttonVar = IntVar(value=0)
        self.style.configure('Tturnon_mapping_chbutton.TCheckbutton', font=('iLiHei', 10))
        self.turnon_mapping_chbutton = Checkbutton(self.mapping_frame, text='啟用', variable=self.turnon_mapping_chbuttonVar, style='Tturnon_mapping_chbutton.TCheckbutton')
        self.turnon_mapping_chbutton.place(relx=0.021, rely=0.050, relwidth=0.159, relheight=0.084)

        self.uses_samepath_chbuttonVar = IntVar(value=self.setting_ini_dic['use_same_path_ini'])
        self.style.configure('Tuses_samepath_chbutton.TCheckbutton', font=('iLiHei', 10))
        self.uses_samepath_chbutton = Checkbutton(self.mapping_frame, text='使用相同路徑', variable=self.uses_samepath_chbuttonVar, style='Tuses_samepath_chbutton.TCheckbutton')
        self.uses_samepath_chbutton.place(relx=0.021, rely=0.160, relwidth=0.296, relheight=0.084)

        self.mapping_frameRadioVar = StringVar()
        self.style.configure('Tmanually_radio.TRadiobutton', font=('iLiHei', 10))
        self.manually_radio = Radiobutton(self.mapping_frame, text='手動模式', value=3, variable=self.radiobutton_select, style='Tmanually_radio.TRadiobutton')
        self.manually_radio.place(relx=0.463, rely=0.377, relwidth=0.254, relheight=0.084)

        self.style.configure('Tstrengthen_radio.TRadiobutton', font=('iLiHei', 10))
        self.strengthen_radio = Radiobutton(self.mapping_frame, text='檔案列表模式', value=2, variable=self.radiobutton_select, style='Tstrengthen_radio.TRadiobutton')
        self.strengthen_radio.place(relx=0.463, rely=0.242, relwidth=0.17, relheight=0.111)

        self.style.configure('Tdefault_radio.TRadiobutton', font=('iLiHei', 10))
        self.default_radio = Radiobutton(self.mapping_frame, text='預設模式', value=1, variable=self.radiobutton_select, style='Tdefault_radio.TRadiobutton')
        self.default_radio.place(relx=0.463, rely=0.135, relwidth=0.127, relheight=0.084)

        self.style.configure('Tmanually_keyword_frame.TLabelframe', font=('iLiHei', 9))
        self.style.configure('Tmanually_keyword_frame.TLabelframe.Label', font=('iLiHei', 9))
        self.manually_keyword_frame = LabelFrame(self.mapping_frame, text='關鍵字比對', style='Tmanually_keyword_frame.TLabelframe')
        self.manually_keyword_frame.place(relx=0.463, rely=0.485, relwidth=0.443, relheight=0.488)

        self.video_keyword_entryVar = StringVar(value=self.setting_ini_dic['videokeyword_ini'])
        self.video_keyword_entry = Entry(self.manually_keyword_frame, textvariable=self.video_keyword_entryVar, font=('iLiHei',10))
        self.video_keyword_entry.place(relx=0.047, rely=0.690, relwidth=0.834, relheight=0.172)

        self.sub_keyword_entryVar = StringVar(value=self.setting_ini_dic['subkeyword_ini'])
        self.sub_keyword_entry = Entry(self.manually_keyword_frame, textvariable=self.sub_keyword_entryVar, font=('iLiHei',10))
        self.sub_keyword_entry.place(relx=0.047, rely=0.276, relwidth=0.834, relheight=0.172)

        self.style.configure('Tvideo_keyword_label.TLabel', anchor='w', font=('iLiHei', 10))
        self.video_keyword_label = Label(self.manually_keyword_frame, text='比對檔名關鍵字', style='Tvideo_keyword_label.TLabel')
        self.video_keyword_label.place(relx=0.047, rely=0.500, relwidth=0.288, relheight=0.172)

        self.style.configure('Tsub_keyword_label.TLabel', anchor='w', font=('iLiHei', 10))
        self.sub_keyword_label = Label(self.manually_keyword_frame, text='原始檔名關鍵字', style='Tsub_keyword_label.TLabel')
        self.sub_keyword_label.place(relx=0.047, rely=0.100, relwidth=0.335, relheight=0.172)

        self.HScroll3 = Scrollbar(self.view_right_frame, orient='horizontal')
        self.HScroll3.place(relx=0.018, rely=0.944, relwidth=0.946, relheight=0.038)

        self.VScroll3 = Scrollbar(self.view_right_frame, orient='vertical')
        self.VScroll3.place(relx=0.961, rely=0.015, relwidth=0.039, relheight=0.935)

        self.view_text_rightFont = Font(font=('iLiHei',10))
        self.view_right_text = Text(self.view_right_frame, wrap='none', xscrollcommand=self.HScroll3.set, yscrollcommand=self.VScroll3.set, font=self.view_text_rightFont)
        self.view_right_text.place(relx=0.018, rely=0.015, relwidth=0.946, relheight=0.930)
        self.HScroll3['command'] = self.view_right_text.xview
        self.VScroll3['command'] = self.view_right_text.yview

        self.HScroll2 = Scrollbar(self.view_center_frame, orient='horizontal')
        self.HScroll2.place(relx=0.018, rely=0.944, relwidth=0.946, relheight=0.038)

        self.VScroll2 = Scrollbar(self.view_center_frame, orient='vertical')
        self.VScroll2.place(relx=0.961, rely=0.015, relwidth=0.039, relheight=0.935)

        self.view_center_textFont = Font(font=('iLiHei', 10))
        self.view_center_text = Text(self.view_center_frame, wrap='none', xscrollcommand=self.HScroll2.set, yscrollcommand=self.VScroll2.set, font=self.view_center_textFont)
        self.view_center_text.place(relx=0.018, rely=0.015, relwidth=0.946, relheight=0.930)
        self.HScroll2['command'] = self.view_center_text.xview
        self.VScroll2['command'] = self.view_center_text.yview

        self.style.configure('Trename_input_label.TLabel', anchor='w', font=('iLiHei', 10))
        self.rename_input_label = Label(self.rename_frame, text='取代為: (* 的位置將會代入編號)', style='Trename_input_label.TLabel')
        self.rename_input_label.place(relx=0.042, rely=0.450, relwidth=0.500, relheight=0.084)

        self.rename_input_enrtyVar = StringVar(value=self.setting_ini_dic['input_rename_ini'])
        self.rename_input_enrty = Entry(self.rename_frame, textvariable=self.rename_input_enrtyVar, font=('iLiHei', 10))
        self.rename_input_enrty.place(relx=0.042, rely=0.530, relwidth=0.915, relheight=0.084)

        # =======位數, 起始位數, 啟用反轉排序=====
        self.style.configure('Tdigit_number_label.TLabel', anchor='w', font=('iLiHei', 10))
        self.digit_number_label = Label(self.rename_frame, text='編號位數:', style='Tdigit_number_label.TLabel')
        self.digit_number_label.place(relx=0.042, rely=0.650, relwidth=0.279, relheight=0.084)

        self.digit_number_enrtyVar = StringVar(value=self.setting_ini_dic['digit_number_ini'])
        self.digit_number_enrty = Entry(self.rename_frame, textvariable=self.digit_number_enrtyVar, font=('iLiHei', 10))
        self.digit_number_enrty.place(relx=0.210, rely=0.650, relwidth=0.060, relheight=0.084)

        self.style.configure('Tstart_number_label.TLabel', anchor='w', font=('iLiHei', 10))
        self.start_number_label = Label(self.rename_frame, text='起始位數:', style='Tstart_number_label.TLabel')
        self.start_number_label.place(relx=0.280, rely=0.650, relwidth=0.279, relheight=0.084)

        self.start_number_enrtyVar = StringVar(value=self.setting_ini_dic['start_number_ini'])
        self.start_number_enrty = Entry(self.rename_frame, textvariable=self.start_number_enrtyVar, font=('iLiHei', 10))
        self.start_number_enrty.place(relx=0.450, rely=0.650, relwidth=0.060, relheight=0.084)
        #
        self.lucky_sort_chbuttonVar = IntVar(value=0)
        self.style.configure('Tlucky_sort_chbutton.TCheckbutton', font=('iLiHei', 10))
        self.lucky_sort_chbutton = Checkbutton(self.rename_frame, text='碰運氣排序', variable=self.lucky_sort_chbuttonVar, style='Tlucky_sort_chbutton.TCheckbutton')
        self.lucky_sort_chbutton.place(relx=0.042, rely=0.850, relwidth=0.250, relheight=0.084)
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
        self.uses_samepath_chbutton['command'] = self.use_thesame_path_selected
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

        # self.view_center_text.bind("<Control-Key-A>", self.view_select_all)
        # self.view_center_text.bind("<Control-Key-a>", self.view_select_all)
        # self.view_center_text.bind("<ButtonRelease-1>", self.view_select_get_and_mark_select)

        # -----Re-flash all GUI item-----
        self.turn_on_mapping_selected()

    def print_about(self):
        tkinter.messagebox.showinfo("About", self.help_text, parent=self.top)

    def view_select_get_and_mark_select(self, event=None):
        self.stop_count_timer()
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

            # print(user_mouse_left_select_list)
            self.show_preview_on_textview(user_mouse_left_select_list)
        except:
            # print("select error or empty")
            self.show_preview_on_textview()

    def view_select_all(self, event=None):
        self.view_left_text.tag_add(SEL, "1.0", END)
        self.view_left_text.mark_set(INSERT, "1.0")
        self.view_left_text.see(INSERT)
        self.view_select_get_and_mark_select()
        return

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
        # print("===start preview===")

        self.show_preview_on_textview()
        self.timer_running_fl = False

    def start_count_entry_input(self, event=None):
        if not self.timer_running_fl:
            self.timer_running_fl = True
            self.start_count_timer(0.6)
        else:
            self.stop_count_timer()
            self.start_count_timer(0.6)

    def use_thesame_path_selected(self, event=None):
        self.stop_count_timer()

        if self.uses_samepath_chbuttonVar.get() == 1:
            self.video_path_entry.config(state='normal')
            self.video_path_entryVar.set("")
            self.video_path_entry.config(state='disable')

            self.video_path_label.config(state='disable')
        else:
            self.video_path_entry.config(state='normal')
            self.video_path_entryVar.set(self.main_sub_path)

            self.video_path_label.config(state='normal')

        if not self.select_turn_on_mapping_fl:
            self.show_preview_on_textview()

    def turn_on_mapping_selected(self):
        # -----Rename function, disable mapping function input GUI-----
        if not self.turnon_mapping_chbuttonVar.get():
            self.select_turn_on_mapping_fl = False
            #
            self.view_right_frame.place_forget()
            self.view_center_frame.place(relx=0.500, rely=0., relwidth=0.500, relheight=0.595)
            self.view_left_frame.place(relx=0.006, rely=0., relwidth=0.500, relheight=0.595)
            self.view_center_frame.config(text='結果預覽')
            #
            self.rename_input_label.config(state='normal')
            self.rename_input_enrty.config(state='normal')
            self.digit_number_label.config(state='normal')
            self.digit_number_enrty.config(state='normal')
            self.start_number_label.config(state='normal')
            self.start_number_enrty.config(state='normal')
            # self.lucky_sort_chbutton.config(state='normal')
            self.rename_button.config(state='normal')
            #
            self.uses_samepath_chbutton.config(state='disabled')
            self.video_path_label.config(state='disabled')
            self.video_path_entry.config(state='disabled')
            self.video_type_label.config(state='disabled')
            self.video_type_entry.config(state='disabled')
            self.default_radio.config(state='disabled')
            self.strengthen_radio.config(state='disabled')
            self.manually_radio.config(state='disabled')
            self.sub_keyword_label.config(state='disabled')
            self.sub_keyword_entry.config(state='disabled')
            self.video_keyword_label.config(state='disabled')
            self.video_keyword_entry.config(state='disabled')
            self.start_button.config(state='disabled')
        # -----Mapping function, disable rename function input GUI-----
        else:
            self.select_turn_on_mapping_fl = True

            self.view_right_frame.place(relx=0.652, rely=0., relwidth=0.349, relheight=0.595)
            self.view_center_frame.place(relx=0.304, rely=0., relwidth=0.349, relheight=0.595)
            self.view_left_frame.place(relx=0.006, rely=0., relwidth=0.298, relheight=0.595)
            self.view_center_frame.config(text='比對檔案名稱')
            #
            self.rename_input_label.config(state='disabled')
            self.rename_input_enrty.config(state='disabled')
            self.digit_number_label.config(state='disabled')
            self.digit_number_enrty.config(state='disabled')
            self.start_number_label.config(state='disabled')
            self.start_number_enrty.config(state='disabled')
            # self.lucky_sort_chbutton.config(state='disabled')
            self.rename_button.config(state='disabled')
            #
            self.uses_samepath_chbutton.config(state='normal')
            self.video_path_label.config(state='normal')
            self.video_path_entry.config(state='normal')
            self.video_type_label.config(state='normal')
            self.video_type_entry.config(state='normal')
            self.default_radio.config(state='normal')
            self.strengthen_radio.config(state='normal')
            self.manually_radio.config(state='normal')
            self.radiokbutton_selected()
            self.use_thesame_path_selected()
            self.start_button.config(state='normal')

        self.select_turn_on_mapping_fl = False
        self.stop_count_timer()

        self.show_preview_on_textview()

    def lucky_store_selected(self):
        self.stop_count_timer()
        self.show_preview_on_textview()

    def radiokbutton_selected(self):
        self.stop_count_timer()

        if self.radiobutton_select.get() == 1 or self.radiobutton_select.get() == 2:
            self.sub_keyword_label.config(state='disabled')
            self.sub_keyword_entry.config(state='disabled')
            self.video_keyword_label.config(state='disabled')
            self.video_keyword_entry.config(state='disabled')
        else:
            self.sub_keyword_label.config(state='normal')
            self.sub_keyword_entry.config(state='normal')
            self.video_keyword_label.config(state='normal')
            self.video_keyword_entry.config(state='normal')

        if not self.select_turn_on_mapping_fl:
            self.show_preview_on_textview()

    def show_preview_on_textview(self, user_mouse_left_select_list=None, event=None):

        # turn on mapping function
        if self.turnon_mapping_chbuttonVar.get() == 1:
            all_sub_list_ll = []
            video_list_ll = []

            # print(user_mouse_left_select_list)
            if not user_mouse_left_select_list:
                mouse_select_flag = 0
                self.view_left_text.config(state="normal")
                self.view_left_text.delete('1.0', END)
                self.view_left_text.config(state="disable")
                self.view_center_text.config(state="normal")
                self.view_center_text.delete('1.0', END)
                self.view_center_text.config(state="disable")
            else:
                mouse_select_flag = 1

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
                    [status, sub_list_ll, video_list_ll] = self.match_sub_and_video_file_update_odic(
                                                sub_path_lv, sub_type_i, video_path_lv, video_type_lv, sub_keyword_lv,
                                                video_keywork_lv, user_mouse_left_select_list)

                    all_sub_list_ll.extend(sub_list_ll)
                # print("status:%s" % status)
                if status == error_Code.NORMAL.value:
                    self.show_list_on_view_text(1, mouse_select_flag)
                else:
                    self.show_list_on_view_text(0, mouse_select_flag, all_sub_list_ll, video_list_ll)

            self.status = status
        # Rename function
        else:
            self.view_center_text.config(state="normal")
            self.view_center_text.delete('1.0', END)
            self.view_center_text.config(state="disable")

            if not user_mouse_left_select_list:
                self.view_left_text.config(state="normal")
                self.view_left_text.delete('1.0', END)
                self.view_left_text.config(state="disable")

            self.rename_ori_and_rename_odic.clear()

            [status, sub_path_lv, sub_type_lv, rename_input_lv, user_input_star_number_lv, user_input_digit_number_lv] \
                = self.arrange_user_input_format()

            # print(status)
            if status == error_Code.NORMAL.value:
                self.ori_rename_store_odic(status, sub_path_lv, sub_type_lv, rename_input_lv, user_input_star_number_lv,
                                           user_input_digit_number_lv, user_mouse_left_select_list)

            self.status = status

    def arrange_user_input_format(self):
        status_lv = error_Code.NORMAL.value
        # -----Check user input sub path-----
        user_input_sub_path_lv = re.sub(r"/$", '', self.sub_path_entry.get())
        user_input_sub_path_lv = re.sub(r"\\$", "", user_input_sub_path_lv)
        if not os.path.exists(user_input_sub_path_lv):
            status_lv = error_Code.USER_SUB_INPUT_PATH_ERROR.value
            # return error_Code.USER_SUB_INPUT_PATH_ERROR.value

        # -----user input sub type-----
        re_lv = re.sub(r' ', '', self.sub_type_entry.get())
        user_input_sub_type_ls = re_lv.split(",")
        # -----remove duplicate item-----
        user_input_sub_type_ls = set(user_input_sub_type_ls)

        if not user_input_sub_type_ls:
            status_lv = error_Code.USER_SUB_INPUT_TYPE_ERROR.value
        # --------------------------------------

        # for rename function
        if self.turnon_mapping_chbuttonVar.get() == 0:

            user_input_rename_input_lv = self.rename_input_enrty.get()
            self.setting_ini_dic['input_rename_ini'] = user_input_rename_input_lv
            if not user_input_rename_input_lv.find('\*'):
                status_lv = error_Code.USER_RENAME_INPUT_ERROR.value

            user_input_star_number_lv = self.start_number_enrtyVar.get()
            self.setting_ini_dic['start_number_ini'] = user_input_star_number_lv
            # user_input_star_number_lv = re.math()
            # print(user_input_star_number_lv)
            if not user_input_star_number_lv.isdigit():
                user_input_star_number_lv = 1

            user_input_digit_number_lv = self.digit_number_enrtyVar.get()
            # user_input_star_number_lv = re.math()
            # print(user_input_star_number_lv)
            if not user_input_digit_number_lv.isdigit():
                user_input_digit_number_lv = 2
            self.setting_ini_dic['digit_number_ini'] = user_input_digit_number_lv

            return status_lv, user_input_sub_path_lv, user_input_sub_type_ls, user_input_rename_input_lv, \
                int(user_input_star_number_lv), int(user_input_digit_number_lv)

        # for mapping function
        else:
            # ----user input video path-----
            if self.uses_samepath_chbuttonVar.get() == 1:
                user_input_video_path_lv = user_input_sub_path_lv
                self.setting_ini_dic['use_same_path_ini'] = 1
            else:
                user_input_video_path_lv = re.sub(r"/$", '', self.video_path_entry.get())
                user_input_video_path_lv = re.sub(r"\\$", "", user_input_video_path_lv)
                self.setting_ini_dic['use_same_path_ini'] = 0

                if not os.path.exists(user_input_video_path_lv):
                    status_lv = error_Code.USER_VIDEO_INPUT_PATH_ERROR.value
                    # return error_Code.USER_VIDEO_INPUT_PATH_ERROR.value
            self.setting_ini_dic['videopath_ini'] = user_input_video_path_lv

            # -----Check user input video type-----
            re_lv = re.sub(r' ', '', self.video_type_entry.get())
            user_input_video_type_ls = re_lv.split(",")
            # remove duplicate item
            user_input_video_type_ls = set(user_input_video_type_ls)
            self.setting_ini_dic['videotype_ini'] = self.video_type_entry.get()
            if not user_input_video_type_ls:
                status_lv = error_Code.USER_VIDEO_INPUT_TYPE_ERROR.value

            user_input_sub_keyword_lv = self.sub_keyword_entry.get()
            self.setting_ini_dic['subkeyword_ini'] = user_input_sub_keyword_lv
            if not user_input_sub_keyword_lv.find('\*'):
                status_lv = error_Code.USER_SUB_INPUT_KEYWORD_ERROR.value

            user_input_video_keyword_lv = self.video_keyword_entry.get()
            self.setting_ini_dic['videokeyword_ini'] = user_input_video_keyword_lv
            if not user_input_video_keyword_lv.find('\*'):
                status_lv = error_Code.USER_VIDEO_INPUT_KEYWORD_ERROR.value

            return status_lv, user_input_sub_path_lv, user_input_sub_type_ls, user_input_video_path_lv, \
                user_input_video_type_ls, user_input_sub_keyword_lv, user_input_video_keyword_lv

    def ori_rename_store_odic(self, u_in_status, u_in_sub_path, u_in_sub_type, u_in_rename,
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
            os.chdir(u_in_sub_path)
            for i in u_in_sub_type:
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

        # -----User use mouse select list, no need to re-get file list, change to uses selected file list
        else:
            if self.lucky_sort_chbuttonVar.get():
                file_list_ll = sorted(user_mouse_select_list)
            else:
                file_list_ll = user_mouse_select_list
            # print(file_list_ll)

        # -----Store ori and rename file name to odic-----
        file_list_ll = tuple(file_list_ll)
        if u_in_status == error_Code.NORMAL.value:
            count = user_input_star_number_lv
            for i in file_list_ll:
                if i:  # remove empty file list
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
            if user_mouse_select_list:
                self.view_center_text.config(state="normal")
                for i, v in self.rename_ori_and_rename_odic.items():
                    self.view_center_text.insert(INSERT, '%s\n' % i)
                    self.view_center_text.insert(INSERT, '%s\n' % v, 'info')
                self.view_center_text.config(state="disable")
            else:
                self.view_left_text.config(state="normal")
                self.view_center_text.config(state="normal")
                for i, v in self.rename_ori_and_rename_odic.items():
                    self.view_left_text.insert(INSERT, '%s\n' % i)
                    self.view_center_text.insert(INSERT, '%s\n' % i)
                    self.view_center_text.insert(INSERT, '%s\n' % v, 'info')
                self.view_left_text.config(state="disable")
                self.view_center_text.config(state="disable")

    def match_sub_and_video_file_update_odic(self, u_in_sub_path, u_in_sub_type, u_in_video_path, u_in_video_type,
                                             u_in_sub_keyword, u_in_video_keywork, user_mouse_select_list=None):
        temp_file_list_ll = []
        videofile_list_ll = []
        sub_file_list_ll = []
        videofile_list_odic = OrderedDict()
        subfile_list_odic = OrderedDict()
        # -----user two orderedDice to store ori sub , video and rename sub file,
        # these two orderDice uses the same key: orisub-----
        mapping_orisub_and_video_odic = OrderedDict()
        mapping_orisub_and_sub_odic = OrderedDict()
        temp_list_ll = []
        videonum_re_h = ''
        subnum_re_h = ''
        status = error_Code.UNKNOW_ERROR.value
        # sub_type_fil_ext = ''


        # -----get video file list-----
        os.chdir(u_in_video_path)
        # glob.glob(sub_path + '\\' + i)
        for i in u_in_video_type:
            temp_list_ll = glob.glob(i)
            # temp_list_ll = glob.glob(u_in_video_path + '\\' + i)
            # temp_list_ll = glob.glob('%s\\%s' % (u_in_video_path, i))
            if temp_list_ll:
                videofile_list_ll.extend(temp_list_ll)
        # print(videofile_list_ll)

        # -----get sub file list-----
        os.chdir(u_in_sub_path)
        # -----clear temp list value-----
        temp_list_ll.clear()
        if not user_mouse_select_list:
            temp_list_ll = glob.glob(u_in_sub_type)

        else:
            # find all space type file list in mouse select list
            temp_u_in_sub_type = u_in_sub_type.replace("*", "")
            # print(temp_u_in_sub_type)
            user_mouse_select_list_ll = tuple(user_mouse_select_list)
            for i in user_mouse_select_list_ll:
                # print("i:%s" % i)
                temp_ext = os.path.splitext(i)[-1]
                if temp_u_in_sub_type == temp_ext:
                    temp_list_ll.append(i)
            # print(user_mouse_select_list_ll)
            # print(temp_list_ll)

        if self.lucky_sort_chbuttonVar.get():
            # revert sort list, try to split TC and SC file name
            temp_ll = []
            split_sub_file_list_ll = []
            # print(sub_file_list_ll)
            for i in temp_list_ll:
                temp_ll.append(i[::-1])
                temp_ll.sort()

            for i in temp_ll:
                split_sub_file_list_ll.append(i[::-1])

            temp_list_ll = split_sub_file_list_ll

        if user_mouse_select_list and self.lucky_sort_chbuttonVar.get():
            temp_list_ll = sorted(user_mouse_select_list)

        # temp_list_ll = glob.glob('%s\\%s' % (u_in_sub_path, u_in_sub_type))
        sub_type_fil_ext = u_in_sub_type.replace("*.", "")
        if temp_list_ll:
            sub_file_list_ll.extend(temp_list_ll)

        for i in sub_file_list_ll:
            # subfile_list_ls = tuple(subfile_list_ls)
            subfile_list_odic[i] = ""


        # -----Free memory-----
        del temp_file_list_ll
        del temp_list_ll

        # -----default matching method-----
        if self.radiobutton_select.get() == 1:
            # if user_input_digit_number_lv and user_mouse_left_select_list:
            #     sub_file_list_ll = user_input_digit_number_lv
            #     videofile_list_ll = user_mouse_left_select_list

            video_list_size = len(videofile_list_ll)
            # sub_list_size = len(sub_file_list_ll)

            # -----change to tuple type for speed up-----
            sub_file_list_ll = tuple(sub_file_list_ll)
            videofile_list_ll = tuple(videofile_list_ll)

            # print("video_size:%s" % video_list_size)
            if sub_file_list_ll and videofile_list_ll:
                # print("default mapping method, start mapping video and sub")

                count = 0
                for i in sub_file_list_ll:
                    c = os.path.splitext(videofile_list_ll[count])
                    mapping_orisub_and_video_odic[i] = videofile_list_ll[count]
                    mapping_orisub_and_sub_odic[i] = "%s.%s" % (c[0], sub_type_fil_ext)
                    # print("count:%s" % count)
                    # print("sub file: %s" % i)

                    count += 1
                    if count == video_list_size:
                        break

                # update mapping_orisub_and_video_odic, mapping_orisub_and_sub_odic
                self.mapping_orisub_and_video_odic.update(mapping_orisub_and_video_odic)
                self.mapping_orisub_and_sub_odic.update(mapping_orisub_and_sub_odic)

            if not self.mapping_orisub_and_video_odic or not self.mapping_orisub_and_sub_odic:
                status = error_Code.MAPPING_LIST_EMPTY.value
            else:
                status = error_Code.NORMAL.value

            return status, sub_file_list_ll, videofile_list_ll

        elif self.radiobutton_select.get() == 2:
            status = error_Code.MAPPING_LIST_EMPTY.value
            return status, sub_file_list_ll, videofile_list_ll
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
            # sub_file_list_ll = tuple(sub_file_list_ll)
            videofile_list_ll = tuple(videofile_list_ll)

            for i in videofile_list_ll:
                c = os.path.splitext(i)
                videofile_list_odic[i] = c[0]

            if subfile_list_odic and videofile_list_odic:
                # print("start mapping video and sub")
                # -----save mapping table to dic-----
                for s_name_j in subfile_list_odic:
                    mapping_state_lv = 0
                    # s_key_lv = list(map(int, (subnum_re_h.findall(s_name_j))))
                    try:
                        s_key_lv = subnum_re_h.findall(s_name_j)
                    except:
                        status = error_Code.MAPPING_LIST_EMPTY.value
                        return status, sub_file_list_ll, videofile_list_ll

                    if s_key_lv:
                        try:
                            s_key_lv = list(map(int, s_key_lv))
                        except:  # get key is not a number
                            continue
                    else:
                        continue

                    # s_key_lv = ''.join(subnum_re_h.findall)
                    for v_fullname_i, v_name_nonext_j in videofile_list_odic.items():
                        # print(v_name_nonext_j)
                        # v_key_lv = list(map(int, (videonum_re_h.findall(v_name_nonext_j))))
                        try:
                            v_key_lv = videonum_re_h.findall(v_name_nonext_j)
                        except:
                            status = error_Code.MAPPING_LIST_EMPTY.value
                            return status, sub_file_list_ll, videofile_list_ll

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
            if not self.mapping_orisub_and_video_odic or not self.mapping_orisub_and_sub_odic:
                status = error_Code.MAPPING_LIST_EMPTY.value
            else:
                status = error_Code.NORMAL.value

            return status, sub_file_list_ll, videofile_list_ll

    def show_list_on_view_text(self, mapping_ok, mouse_select_flag, sub_list=None, video_list=None):
        # print (mapping_orisub_and_sub_odic[])
        # Find mapping list, show origin file in left view, mapping file in center view, result in right view
        if mapping_ok:
            self.view_left_text.config(state="normal")
            self.view_center_text.config(state="normal")
            self.view_right_text.config(state="normal")
            for i, j in self.mapping_orisub_and_video_odic.items():
                # print(mapping_orisub_and_sub_odic[i])
                if not mouse_select_flag:
                    self.view_left_text.insert(INSERT, "%s\n" % i)
                    self.view_center_text.insert(INSERT, "%s\n" % j, 'info2')

                self.view_right_text.insert(INSERT, "%s\n" % i)
                self.view_right_text.insert(INSERT, "%s\n" % j, 'info2')
                self.view_right_text.insert(INSERT, "%s\n\n" % self.mapping_orisub_and_sub_odic[i], 'info')
                # print(i, mapping_orisub_and_sub_odic[i])
            self.view_left_text.config(state="disable")
            self.view_center_text.config(state="disable")
            self.view_right_text.config(state="disable")
        # not find mapping list, show origin file in left view, mapping file in center view,
        # don't show result in right view
        else:
            self.view_left_text.config(state="normal")
            self.view_center_text.config(state="normal")

            for i in sub_list:
                # print(mapping_orisub_and_sub_odic[i])
                # if not (user_mouse_left_select_list or user_mouse_center_select_list):
                self.view_left_text.insert(INSERT, "%s\n" % i)
            for j in video_list:
                self.view_center_text.insert(INSERT, "%s\n" % j, 'info2')

                # print(i, mapping_orisub_and_sub_odic[i])
            self.view_left_text.config(state="disable")
            self.view_center_text.config(state="disable")

    def start_rename(self):
        # -----Check preview is done, if not, wait preview done-----
        while self.timer_running_fl:
            sleep(0.3)

        c = tkinter.messagebox.askyesno("Start Rename", "確定要重新修改檔名?", parent=self.top)
        if c:
            # -----OK! start to rename
            if self.status == error_Code.NORMAL.value:
                for i, v in self.rename_ori_and_rename_odic.items():
                    os.rename(i, v)

                # -----Write config to setting-----
                self.write_config(1)

                self.show_preview_on_textview()
            else:
                tkinter.messagebox.showerror("Error", "Rename error! Error code is: %d" % self.status,
                                             parent=self.top)
        else:
            self.show_preview_on_textview()

    def start_mapping_rename(self):
        # -----Check preview is done, if not, wait preview done-----
        while self.timer_running_fl:
            sleep(0.3)

        c = tkinter.messagebox.askyesno("Start Rename", "確定要重新修改檔名?", parent=self.top)
        if c:
            # -----OK! start to rename
            if self.status == error_Code.NORMAL.value:
                for i, v in self.mapping_orisub_and_sub_odic.items():
                    os.rename(i, v)

                # -----Write config to setting-----
                self.write_config(0)

                self.show_preview_on_textview()
            else:
                tkinter.messagebox.showerror("Error", "Mapping rename error! Error code is: %d" % self.status,
                                             parent=self.top)
        else:
            self.show_preview_on_textview()

    def write_config(self, is_rename):
        try:
            config_lh = configparser.ConfigParser()
            file_ini_lh = open(self.setting_ini_file_name, 'r', encoding='utf16')
            config_lh.read_file(file_ini_lh)
            file_ini_lh.close()

            file_write_ini_lh = open(self.setting_ini_file_name, 'w', encoding='utf16')

            # if is_rename:
            #     if config_lh.get('Rename', 'input_rename') != self.setting_ini_dic['input_rename_ini']:
            #         config_lh.set('Rename', 'input_rename', self.setting_ini_dic['input_rename_ini'])
            #     if config_lh.get('Rename', 'digit_number') != self.setting_ini_dic['digit_number_ini']:
            #         config_lh.set('Rename', 'digit_number', self.setting_ini_dic['digit_number_ini'])
            #     if config_lh.get('Rename', 'start_number') != self.setting_ini_dic['start_number_ini']:
            #         config_lh.set('Rename', 'start_number', self.setting_ini_dic['start_number_ini'])
            # else:
            #     if config_lh.get('Mapping', 'mappingpath') != self.setting_ini_dic['videopath_ini']:
            #         config_lh.set('Mapping', 'mappingpath', self.setting_ini_dic['videopath_ini'])
            #     if config_lh.get('Mapping', 'mappingtype') != self.setting_ini_dic['videotype_ini']:
            #         config_lh.set('Mapping', 'mappingtype', self.setting_ini_dic['videotype_ini'])
            #     if config_lh.get('Mapping', 'videokeyword') != self.setting_ini_dic['videokeyword_ini']:
            #         config_lh.set('Mapping', 'videokeyword', str(self.setting_ini_dic['videokeyword_ini']))
            #     if config_lh.get('Mapping', 'subkeyword') != self.setting_ini_dic['subkeyword_ini']:
            #         config_lh.set('Mapping', 'subkeyword', str(self.setting_ini_dic['subkeyword_ini']))
            #     if int(config_lh.get('Mapping', 'use_same_path')) != self.setting_ini_dic['use_same_path_ini']:
            #         config_lh.set('Mapping', 'use_same_path', str(self.setting_ini_dic['use_same_path_ini']))

            if is_rename:
                config_lh.set('Rename', 'input_rename', self.setting_ini_dic['input_rename_ini'])
                config_lh.set('Rename', 'digit_number', self.setting_ini_dic['digit_number_ini'])
                config_lh.set('Rename', 'start_number', self.setting_ini_dic['start_number_ini'])
            else:
                config_lh.set('Mapping', 'mappingpath', self.setting_ini_dic['videopath_ini'])
                config_lh.set('Mapping', 'mappingtype', self.setting_ini_dic['videotype_ini'])
                config_lh.set('Mapping', 'videokeyword', str(self.setting_ini_dic['videokeyword_ini']))
                config_lh.set('Mapping', 'subkeyword', str(self.setting_ini_dic['subkeyword_ini']))
                config_lh.set('Mapping', 'use_same_path', str(self.setting_ini_dic['use_same_path_ini']))

            config_lh.write(file_write_ini_lh)
            file_write_ini_lh.close()

        except Exception:
            self.status = error_Code.FILE_ERROR.value

            tkinter.messagebox.showerror("Error!", "Error! Write setting to ini file fail, please create UTF-16 format "
                                         + self.setting_ini_file_name+" in tool path\n"
                                         "if file already exist, please check file format is correctly",
                                         parent=self.top)

    def close_ren_frame(self, event=None):
        self.stop_count_timer()
        # print("current path: %s" % os.getcwd())
        os.chdir(self.app_current_path)
        # print("change to path: %s" % os.getcwd())

        self.top.destroy()
