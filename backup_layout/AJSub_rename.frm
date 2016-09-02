VERSION 5.00
Begin VB.Form Form1 
   Caption         =   "Form1"
   ClientHeight    =   11310
   ClientLeft      =   225
   ClientTop       =   555
   ClientWidth     =   18960
   LinkTopic       =   "Form1"
   ScaleHeight     =   11310
   ScaleWidth      =   18960
   StartUpPosition =   3  '系統預設值
   Begin VB.Frame rename_frame 
      Caption         =   "Rename"
      BeginProperty Font 
         Name            =   "iLiHei"
         Size            =   9
         Charset         =   136
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   4455
      Left            =   120
      TabIndex        =   20
      Top             =   6840
      Width           =   5655
      Begin VB.CommandButton Command1 
         Caption         =   "Command1"
         Height          =   495
         Left            =   4080
         TabIndex        =   25
         Top             =   3720
         Width           =   1215
      End
      Begin VB.TextBox video_type_entry 
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9.75
            Charset         =   136
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   375
         Left            =   240
         TabIndex        =   24
         Text            =   "self.videotype_ini"
         Top             =   1440
         Width           =   5175
      End
      Begin VB.TextBox video_path_entry 
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9.75
            Charset         =   136
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   375
         Left            =   240
         TabIndex        =   22
         Text            =   "self.videopath_ini"
         Top             =   600
         Width           =   5175
      End
      Begin VB.Label video_type_label 
         Caption         =   "Video Type"
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9.75
            Charset         =   136
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   375
         Left            =   240
         TabIndex        =   23
         Top             =   1200
         Width           =   1575
      End
      Begin VB.Label video_path_label 
         Caption         =   "Video Path"
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9.75
            Charset         =   136
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   375
         Left            =   240
         TabIndex        =   21
         Top             =   360
         Width           =   1095
      End
   End
   Begin VB.Frame mapping_frame 
      Caption         =   "Mapping Sub and Video"
      BeginProperty Font 
         Name            =   "iLiHei"
         Size            =   9
         Charset         =   136
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   4455
      Left            =   5880
      TabIndex        =   12
      Top             =   6840
      Width           =   11415
      Begin VB.TextBox sub_type_entry 
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9.75
            Charset         =   136
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   375
         Left            =   360
         TabIndex        =   29
         Text            =   "self.main_sub_type"
         Top             =   2280
         Width           =   4335
      End
      Begin VB.CommandButton start_button 
         Caption         =   "Start"
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9.75
            Charset         =   136
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   495
         Left            =   240
         TabIndex        =   26
         Top             =   3720
         Width           =   1455
      End
      Begin VB.CheckBox turnon_mapping_chbutton 
         Caption         =   "啟用"
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9.75
            Charset         =   136
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   375
         Left            =   240
         TabIndex        =   19
         Top             =   360
         Width           =   1815
      End
      Begin VB.CheckBox uses_samepath_chbutton 
         Caption         =   "使用相同路徑"
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9.75
            Charset         =   136
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   240
         TabIndex        =   18
         Top             =   840
         Width           =   3375
      End
      Begin VB.TextBox sub_path_entry 
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9.75
            Charset         =   136
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   375
         Left            =   360
         TabIndex        =   17
         Text            =   "self.main_sub_path"
         Top             =   1440
         Width           =   4335
      End
      Begin VB.OptionButton manually_radio 
         Caption         =   "手動模式"
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9.75
            Charset         =   136
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   375
         Left            =   5280
         TabIndex        =   15
         Top             =   1680
         Width           =   2895
      End
      Begin VB.OptionButton strengthen_radio 
         Caption         =   "強力模式"
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9.75
            Charset         =   136
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   495
         Left            =   5280
         TabIndex        =   14
         Top             =   1080
         Width           =   1935
      End
      Begin VB.OptionButton default_radio 
         Caption         =   "預設模式"
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9.75
            Charset         =   136
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   375
         Left            =   5280
         TabIndex        =   13
         Top             =   600
         Width           =   1455
      End
      Begin VB.Frame manually_keyword_frame 
         Caption         =   "輸入關鍵字"
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9
            Charset         =   136
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   2175
         Left            =   5280
         TabIndex        =   16
         Top             =   2160
         Width           =   5055
         Begin VB.TextBox video_keyword_entry 
            BeginProperty Font 
               Name            =   "iLiHei"
               Size            =   9.75
               Charset         =   136
               Weight          =   400
               Underline       =   0   'False
               Italic          =   0   'False
               Strikethrough   =   0   'False
            EndProperty
            Height          =   375
            Left            =   240
            TabIndex        =   33
            Text            =   "self.videokeyword_ini"
            Top             =   1440
            Width           =   4215
         End
         Begin VB.TextBox sub_keyword_entry 
            BeginProperty Font 
               Name            =   "iLiHei"
               Size            =   9.75
               Charset         =   136
               Weight          =   400
               Underline       =   0   'False
               Italic          =   0   'False
               Strikethrough   =   0   'False
            EndProperty
            Height          =   375
            Left            =   240
            TabIndex        =   31
            Text            =   "self.subkeyword_ini"
            Top             =   600
            Width           =   4215
         End
         Begin VB.Label video_keyword_label 
            Caption         =   "Video Keyword"
            BeginProperty Font 
               Name            =   "iLiHei"
               Size            =   9.75
               Charset         =   136
               Weight          =   400
               Underline       =   0   'False
               Italic          =   0   'False
               Strikethrough   =   0   'False
            EndProperty
            Height          =   375
            Left            =   240
            TabIndex        =   32
            Top             =   1200
            Width           =   1455
         End
         Begin VB.Label sub_keyword_label 
            Caption         =   "Sub Keyword"
            BeginProperty Font 
               Name            =   "iLiHei"
               Size            =   9.75
               Charset         =   136
               Weight          =   400
               Underline       =   0   'False
               Italic          =   0   'False
               Strikethrough   =   0   'False
            EndProperty
            Height          =   375
            Left            =   240
            TabIndex        =   30
            Top             =   360
            Width           =   1695
         End
      End
      Begin VB.Label sub_type_label 
         Caption         =   "SUB Type"
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9.75
            Charset         =   136
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   375
         Left            =   360
         TabIndex        =   28
         Top             =   2040
         Width           =   855
      End
      Begin VB.Label sub_path_label 
         Caption         =   "SUB Path"
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9.75
            Charset         =   136
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   375
         Left            =   360
         TabIndex        =   27
         Top             =   1200
         Width           =   975
      End
   End
   Begin VB.Frame view_right_frame 
      Caption         =   "配對結果預覽"
      BeginProperty Font 
         Name            =   "iLiHei"
         Size            =   9
         Charset         =   136
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   6735
      Left            =   12360
      TabIndex        =   2
      Top             =   0
      Width           =   6615
      Begin VB.HScrollBar HScroll3 
         Height          =   255
         Left            =   120
         TabIndex        =   11
         Top             =   6360
         Width           =   6255
      End
      Begin VB.VScrollBar VScroll3 
         Height          =   6135
         Left            =   6360
         TabIndex        =   10
         Top             =   240
         Width           =   255
      End
      Begin VB.TextBox view_text_right 
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9.75
            Charset         =   136
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   6135
         Left            =   120
         MultiLine       =   -1  'True
         ScrollBars      =   3  '兩者皆有
         TabIndex        =   5
         Text            =   "AJSub_rename.frx":0000
         Top             =   240
         Width           =   6255
      End
   End
   Begin VB.Frame view_center_frame 
      Caption         =   "結果預覽"
      BeginProperty Font 
         Name            =   "iLiHei"
         Size            =   9
         Charset         =   136
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   6735
      Left            =   5760
      TabIndex        =   1
      Top             =   0
      Width           =   6615
      Begin VB.HScrollBar HScroll2 
         Height          =   255
         Left            =   120
         TabIndex        =   9
         Top             =   6360
         Width           =   6255
      End
      Begin VB.VScrollBar VScroll2 
         Height          =   6135
         Left            =   6360
         TabIndex        =   8
         Top             =   240
         Width           =   255
      End
      Begin VB.TextBox view_center_text 
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9.75
            Charset         =   136
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   6135
         Left            =   120
         MultiLine       =   -1  'True
         ScrollBars      =   3  '兩者皆有
         TabIndex        =   4
         Text            =   "AJSub_rename.frx":0006
         Top             =   240
         Width           =   6255
      End
   End
   Begin VB.Frame view_left_frame 
      Caption         =   "原始檔名"
      BeginProperty Font 
         Name            =   "iLiHei"
         Size            =   9
         Charset         =   136
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   6735
      Left            =   120
      TabIndex        =   0
      Top             =   0
      Width           =   5655
      Begin VB.HScrollBar HScroll1 
         Height          =   255
         Left            =   120
         TabIndex        =   7
         Top             =   6360
         Width           =   5295
      End
      Begin VB.VScrollBar VScroll1 
         Height          =   6135
         Left            =   5400
         TabIndex        =   6
         Top             =   240
         Width           =   255
      End
      Begin VB.TextBox view_left_text 
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9.75
            Charset         =   136
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   6135
         Left            =   120
         MultiLine       =   -1  'True
         ScrollBars      =   3  '兩者皆有
         TabIndex        =   3
         Text            =   "AJSub_rename.frx":000C
         Top             =   240
         Width           =   5295
      End
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
