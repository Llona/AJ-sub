from tkinter import *
import tkinter.messagebox
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
import difflib
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


class rename_frame:
    def __init__(self, parent, main_sub_path, main_sub_type, setting_name):
        self.main_sub_path = main_sub_path
        self.main_sub_type = main_sub_type
        self.mapping_orisub_and_video_odic = OrderedDict()
        self.mapping_orisub_and_sub_odic = OrderedDict()
        self.app_current_path = os.getcwd()
        self.radiobutton_select = IntVar()
        # -----Timer-----
        self.timer_running_fl = False
        self.start_timer = 0
        # -----Create TopLevel frame-----
        self.top_window = Toplevel(parent)
        # self.top_window.overrideredirect(1)
        # msg = Label(top_window, text="轉換工作進行中...")
        # msg.pack(side=TOP, anchor=W, fill=X, expand=YES)
        self.top_window['takefocus'] = True
        self.top_window.grab_set()
        self.top_window.focus_force()
        # -----Create frame item-----
        self.sub_path_entry = Entry(self.top_window)
        self.sub_path_label = Label(self.top_window)
        self.sub_type_label = Label(self.top_window)
        self.sub_type_entry = Entry(self.top_window)
        self.video_path_label = Label(self.top_window)
        self.video_path_entry = Entry(self.top_window)
        self.video_type_label = Label(self.top_window)
        self.video_type_entry = Entry(self.top_window)
        self.video_keyword_label = Label(self.top_window)
        self.video_keyword_entry = Entry(self.top_window)
        self.sub_keyword_label = Label(self.top_window)
        self.sub_keyword_entry = Entry(self.top_window)

        self.start_button = Button(self.top_window)
        self.vert_scrollbar = Scrollbar(self.top_window, orient='vertical')
        self.hor_scrollbar = Scrollbar(self.top_window, orient=HORIZONTAL)
        self.view_txt = Text(self.top_window, wrap='none', state="disabled",
                             yscrollcommand=self.vert_scrollbar.set, xscrollcommand=self.hor_scrollbar.set)
        self.view_txt = Text(self.top_window, wrap='none', state="disabled",
                             yscrollcommand=self.vert_scrollbar.set, xscrollcommand=self.hor_scrollbar.set)

        self.default_radio = Radiobutton(self.top_window, text="預設模式", variable=self.radiobutton_select, value=1)
        self.strengthen_radio = Radiobutton(self.top_window, text="強力模式", variable=self.radiobutton_select, value=2)
        self.manually_radio = Radiobutton(self.top_window, text="手動模式", variable=self.radiobutton_select, value=3)
        # -----Register for handler and key event-----
        # make the top right close button minimize (iconify) the main window
        self.top_window.protocol("WM_DELETE_WINDOW", self.close_ren_frame)
        self.top_window.bind('<Escape>', self.close_ren_frame)
        self.sub_path_entry.bind('<Key>', self.start_count_entry_input)
        self.sub_type_entry.bind('<Key>', self.start_count_entry_input)
        self.video_path_entry.bind('<Key>', self.start_count_entry_input)
        self.video_type_entry.bind('<Key>', self.start_count_entry_input)
        self.video_keyword_entry.bind('<Key>', self.start_count_entry_input)
        self.sub_keyword_entry.bind('<Key>', self.start_count_entry_input)

        self.timer_h = None
        # self.error_code = error_Type()

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
        # -----Sub file input entry-----
        self.sub_path_label["text"] = "SUB Path:"
        self.sub_path_label.grid(row=3, column=0)
        self.sub_path_entry["width"] = 60
        self.sub_path_entry.insert(3, self.main_sub_path)
        self.sub_path_entry.grid(row=3, column=1, columnspan=6)
        # -----Sub file type entry-----
        self.sub_type_label["text"] = "SUB type:"
        self.sub_type_label.grid(row=4, column=0)
        self.sub_type_entry["width"] = 60
        self.sub_type_entry.insert(0, self.main_sub_type)
        self.sub_type_entry.grid(row=4, column=1, columnspan=6)
        # -----Video file path entry-----
        self.video_path_label["text"] = "Video Path:"
        self.video_path_label.grid(row=5, column=0)
        self.video_path_entry["width"] = 60
        self.video_path_entry.insert(0, self.videopath_ini)
        self.video_path_entry.grid(row=5, column=1, columnspan=6)
        # -----Video file type entry-----
        self.video_type_label["text"] = "Video Type:"
        self.video_type_label.grid(row=6, column=0)
        self.video_type_entry["width"] = 60
        self.video_type_entry.insert(0, self.videotype_ini)
        self.video_type_entry.grid(row=6, column=1, columnspan=6)
        # -----Video keyword entry-----
        self.video_keyword_label["text"] = "Video Keyword:"
        self.video_keyword_label.grid(row=7, column=0)
        self.video_keyword_entry["width"] = 60
        self.video_keyword_entry.insert(0, self.videokeyword_ini)
        self.video_keyword_entry.grid(row=7, column=1, columnspan=6)
        # -----Sub keyword entry-----
        self.sub_keyword_label["text"] = "Sub Keyword:"
        self.sub_keyword_label.grid(row=8, column=0)
        self.sub_keyword_entry["width"] = 60
        self.sub_keyword_entry.insert(0, self.subkeyword_ini)
        self.sub_keyword_entry.grid(row=8, column=1, columnspan=6)
        # -----Button Rename-----
        self.start_button["text"] = "Start"
        # self.rename_button["width"] = 5
        # self.start_button["command"] = self.start_rename
        self.start_button.grid(row=9, column=1, columnspan=1)
        # -----Default mapping Radiobutton-----
        self.default_radio.grid(row=10, column=0)
        self.strengthen_radio.grid(row=10, column=1)
        self.manually_radio.grid(row=10, column=2)
        self.strengthen_radio.select()  # default uses default mapping method

        # self.lb1 = tk.Listbox(master, yscrollcommand=scrollbar.set)
        # self.lb2 = tk.Listbox(master, yscrollcommand=scrollbar.set)
        # scrollbar.config(command=self.yview)
        # scrollbar.pack(side='right', fill='y')
        # self.lb1.pack(side='left', fill='both', expand=True)
        # self.lb2.pack(side='left', fill='both', expand=True)
        # -----View Text and Scrollbar-----
        self.vert_scrollbar.grid(row=0, column=2, sticky='NS')
        self.hor_scrollbar.grid(row=1, column=0, columnspan=3, sticky='EW')

        self.view_txt["width"] = 70
        self.view_txt["font"] = ("Purisa", 10)
        self.view_txt.grid(row=0, column=0, columnspan=2)
        # self.view_txt.grid_forget()

        # self.hor_scrollbar.config(command=self.ren_frame_renview_txt.xview and self.ren_frame_oriview_txt.xview)
        self.hor_scrollbar.config(command=self.view_txt.xview)
        self.vert_scrollbar.config(command=self.view_txt.yview)

        # self.view_txt.tag_config("error", foreground="#CC0000")
        self.view_txt.tag_config("info", foreground="#008800")
        # self.view_txt.tag_config("info2", foreground="#404040")

        # -----Show rename preview on text-----
        self.show_preview_on_textview()

    def start_count_timer(self, sec):
        if self.timer_h and self.timer_h.isAlive():
            self.timer_h.cancel()
        self.timer_h = Timer(sec, self.timer_count_expired)
        # print("start timer")
        self.timer_h.start()

    def stop_count_timer(self):
        if self.timer_h.isAlive():
            # Stop the timer instance
            self.timer_h.cancel()
            # print('Timer stopped')
        # If not active, do nothing
        # else:
        #     print('Timer inactive')
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

    def show_preview_on_textview(self):
        self.view_txt.config(state="normal")
        self.view_txt.delete('1.0', END)
        self.view_txt.config(state="disable")

        # -----Clear previous mapping result-----
        self.mapping_orisub_and_video_odic.clear()
        self.mapping_orisub_and_video_odic.clear()

        [status, sub_path_lv, sub_type_lv, video_path_lv, video_type_lv, sub_keyword_lv, video_keywork_lv] = \
            self.arrange_user_input_format()

        # print(status)
        if status == error_Code.NORMAL.value:
            for sub_type_i in sub_type_lv:
                self.match_sub_and_video_file_update_odic(sub_path_lv, sub_type_i, video_path_lv, video_type_lv,
                                                          sub_keyword_lv, video_keywork_lv)
            self.show_list_on_view_text(self.mapping_orisub_and_video_odic, self.mapping_orisub_and_sub_odic)

    # def set_txtview_text(self, string, level=None):
        # self.view_txt.config(state="normal")

        # if (level != 'error') and (level != 'info') and (level != 'info2'):
        #     level = ""

        # self.view_txt.insert(INSERT, string + "\n", level)
        # -----scroll to end of text widge-----
        # self.view_txt.see(END)
        # self.top_window.update_idletasks()

        # self.view_txt.config(state="disabled")

    def arrange_user_input_format(self):
        status_lv = error_Code.NORMAL.value
        # user_input_sub_path_lv = ""
        # user_input_sub_type_ls = ""
        # user_input_video_path_lv = ""
        # user_input_video_type_ls = ""
        # user_input_sub_keyword_lv = ""
        # user_input_video_keyword_lv = ""

        # ----user input sub path-----
        user_input_sub_path_lv = re.sub(r"/$", '', self.sub_path_entry.get())
        user_input_sub_path_lv = re.sub(r"\\$", "", user_input_sub_path_lv)

        user_input_video_path_lv = re.sub(r"/$", '', self.video_path_entry.get())
        user_input_video_path_lv = re.sub(r"\\$", "", user_input_video_path_lv)

        if not os.path.exists(user_input_sub_path_lv):
            status_lv = error_Code.USER_SUB_INPUT_PATH_ERROR.value
            # return error_Code.USER_SUB_INPUT_PATH_ERROR.value
        if not os.path.exists(user_input_video_path_lv):
            status_lv = error_Code.USER_VIDEO_INPUT_PATH_ERROR.value
            # return error_Code.USER_VIDEO_INPUT_PATH_ERROR.value

        re_lv = re.sub(r' ', '', self.sub_type_entry.get())
        user_input_sub_type_ls = re_lv.split(",")
        # -----remove duplicate item-----
        user_input_sub_type_ls = set(user_input_sub_type_ls)

        re_lv = re.sub(r' ', '', self.video_type_entry.get())
        user_input_video_type_ls = re_lv.split(",")
        # -----remove duplicate item-----
        user_input_video_type_ls = set(user_input_video_type_ls)

        if not user_input_video_type_ls:
            status_lv = error_Code.USER_VIDEO_INPUT_PATH_ERROR.value
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

    def match_sub_and_video_file_update_odic(self, u_in_sub_path, u_in_sub_type, u_in_video_path, u_in_video_type,
                                             u_in_sub_keyword, u_in_video_keywork):
        temp_file_list_ll = []
        videofile_list_ll = []
        sub_file_list_ll = []
        videofile_list_odic = OrderedDict()
        subfile_list_odic = OrderedDict()
        # -----user two orderedDice to store ori sub , video and rename sub file,
        # these two orderDice uses the same key: orisub-----
        mapping_orisub_and_video_odic = OrderedDict()
        mapping_orisub_and_sub_odic = OrderedDict()
        videonum_re_h = ''
        subnum_re_h = ''
        temp_list_lv = ''
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

        # -----change to tuple type for speed up-----
        sub_file_list_ll = tuple(sub_file_list_ll)
        videofile_list_ll = tuple(videofile_list_ll)

        # -----default matching method-----
        if self.radiobutton_select.get() == 1:
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

        # -----strengthen matching method-----
        elif self.radiobutton_select.get() == 2:
            # matcher = difflib.Differ()
            # aa = matcher.compare(videofile_list_ll[0], videofile_list_ll[1])
            # aa.
            # print(.join(aa))
            matcher = difflib.SequenceMatcher(None, videofile_list_ll[0], videofile_list_ll[1])
            print(matcher.get_opcodes())

            # print(matcher.get_matching_blocks())


        # -----Generate video keyword compile-----
        video_key_re_h = re.match(r'(.+)\*(.+)', u_in_video_keywork)
        if video_key_re_h:
            key_prv = video_key_re_h.group(1)
            key_aft = video_key_re_h.group(2)
            if not video_key_re_h.group(1):
                key_prv = '.*'
            if not video_key_re_h.group(2):
                key_aft = '.*'
            videonum_re_h = re.compile(r'%s(.*)%s'
                                       % (re.escape(key_prv), re.escape(key_aft)))
        # -----Generate video keyword compile-----
        sub_key_re_h = re.match(r'(.+)\*(.+)', u_in_sub_keyword)
        if sub_key_re_h:
            key_prv = sub_key_re_h.group(1)
            key_aft = sub_key_re_h.group(2)
            if not sub_key_re_h.group(1):
                key_prv = '.*'
            if not sub_key_re_h.group(2):
                key_aft = '.*'
            subnum_re_h = re.compile(r'%s(.*)%s'
                                     % (re.escape(key_prv), re.escape(key_aft)))


        # -----if uses manually mapping method, remove video filename extension and save list to ordered dict-----
        if self.manually_radio == 3:
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
                    s_key_lv = list(map(int, s_key_lv))
                else:
                    continue
                # print(s_key_lv)
                # s_key_lv = ''.join(subnum_re_h.findall)
                for v_fullname_i, v_name_nonext_j in videofile_list_odic.items():
                    # print(v_name_nonext_j)
                    # v_key_lv = list(map(int, (videonum_re_h.findall(v_name_nonext_j))))
                    v_key_lv = videonum_re_h.findall(v_name_nonext_j)
                    if v_key_lv:
                        v_key_lv = list(map(int, v_key_lv))
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

        self.view_txt.config(state="normal")
        for i, j in mapping_orisub_and_video_odic.items():
            # print(mapping_orisub_and_sub_odic[i])
            self.view_txt.insert(INSERT, i + "\n")
            self.view_txt.insert(INSERT, j + "\n")
            self.view_txt.insert(INSERT, mapping_orisub_and_sub_odic[i] + "\n", 'info')
            print(i, mapping_orisub_and_sub_odic[i])
        self.view_txt.config(state="disable")

    def start_rename(self):
        pass

    def close_ren_frame(self, event=None):
        print("current path: "+os.getcwd())
        os.chdir(self.app_current_path)
        print("change to path: " + os.getcwd())
        if self.timer_h:
            self.stop_count_timer()
        self.top_window.destroy()
        return
