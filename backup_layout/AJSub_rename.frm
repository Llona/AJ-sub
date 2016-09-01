VERSION 5.00
Begin VB.Form Form1 
   Caption         =   "Form1"
   ClientHeight    =   11310
   ClientLeft      =   120
   ClientTop       =   450
   ClientWidth     =   22095
   LinkTopic       =   "Form1"
   ScaleHeight     =   11310
   ScaleWidth      =   22095
   StartUpPosition =   3  '系統預設值
   Begin VB.Frame rename_frame 
      Caption         =   "Rename"
      BeginProperty Font 
         Name            =   "iLiHei"
         Size            =   9.75
         Charset         =   136
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   4335
      Left            =   1560
      TabIndex        =   20
      Top             =   6840
      Width           =   6255
      Begin VB.CommandButton Command1 
         Caption         =   "Command1"
         Height          =   495
         Left            =   4800
         TabIndex        =   25
         Top             =   3600
         Width           =   1215
      End
      Begin VB.TextBox Text6 
         Height          =   375
         Left            =   240
         TabIndex        =   24
         Text            =   "Text6"
         Top             =   1920
         Width           =   4815
      End
      Begin VB.TextBox Text5 
         Height          =   375
         Left            =   240
         TabIndex        =   22
         Text            =   "Text5"
         Top             =   840
         Width           =   4815
      End
      Begin VB.Label Label2 
         Caption         =   "Label2"
         Height          =   375
         Left            =   240
         TabIndex        =   23
         Top             =   1560
         Width           =   855
      End
      Begin VB.Label Label1 
         Caption         =   "Label1"
         Height          =   375
         Left            =   240
         TabIndex        =   21
         Top             =   600
         Width           =   1095
      End
   End
   Begin VB.Frame mapping_frame 
      Caption         =   "Mapping Sub and Video"
      BeginProperty Font 
         Name            =   "iLiHei"
         Size            =   9.75
         Charset         =   136
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   4455
      Left            =   9480
      TabIndex        =   12
      Top             =   6840
      Width           =   11415
      Begin VB.TextBox Text7 
         Height          =   375
         Left            =   1080
         TabIndex        =   29
         Text            =   "Text7"
         Top             =   1680
         Width           =   3855
      End
      Begin VB.CommandButton Command2 
         Caption         =   "Command2"
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
         Top             =   240
         Width           =   1815
      End
      Begin VB.CheckBox uses_samepath_chbutton 
         Caption         =   "使用相同路徑"
         Height          =   255
         Left            =   240
         TabIndex        =   18
         Top             =   840
         Width           =   3375
      End
      Begin VB.TextBox sub_type_entry 
         Height          =   375
         Left            =   1080
         TabIndex        =   17
         Text            =   "Text4"
         Top             =   1080
         Width           =   3855
      End
      Begin VB.OptionButton Option3 
         Caption         =   "Option3"
         Height          =   375
         Left            =   5280
         TabIndex        =   15
         Top             =   1560
         Width           =   2895
      End
      Begin VB.OptionButton Option2 
         Caption         =   "Option2"
         Height          =   495
         Left            =   5280
         TabIndex        =   14
         Top             =   840
         Width           =   1935
      End
      Begin VB.OptionButton Option1 
         Caption         =   "Option1"
         Height          =   375
         Left            =   5280
         TabIndex        =   13
         Top             =   240
         Width           =   1455
      End
      Begin VB.Frame Frame5 
         Caption         =   "Frame5"
         Height          =   2415
         Left            =   5280
         TabIndex        =   16
         Top             =   1920
         Width           =   6015
         Begin VB.TextBox Text9 
            Height          =   375
            Left            =   240
            TabIndex        =   33
            Text            =   "Text9"
            Top             =   1560
            Width           =   4215
         End
         Begin VB.TextBox Text8 
            Height          =   375
            Left            =   240
            TabIndex        =   31
            Text            =   "Text8"
            Top             =   720
            Width           =   4095
         End
         Begin VB.Label Label6 
            Caption         =   "Label6"
            Height          =   375
            Left            =   240
            TabIndex        =   32
            Top             =   1200
            Width           =   1095
         End
         Begin VB.Label Label5 
            Caption         =   "Label5"
            Height          =   375
            Left            =   240
            TabIndex        =   30
            Top             =   360
            Width           =   1695
         End
      End
      Begin VB.Label sub_type_label 
         Caption         =   "SUB Type"
         Height          =   375
         Left            =   240
         TabIndex        =   28
         Top             =   1800
         Width           =   855
      End
      Begin VB.Label sub_path_label 
         Caption         =   "SUB Path"
         Height          =   375
         Left            =   240
         TabIndex        =   27
         Top             =   1200
         Width           =   975
      End
   End
   Begin VB.Frame view_right_frame 
      Caption         =   "配對結果預覽"
      BeginProperty Font 
         Name            =   "iLiHei"
         Size            =   9.75
         Charset         =   136
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   6735
      Left            =   14760
      TabIndex        =   2
      Top             =   0
      Width           =   7335
      Begin VB.HScrollBar HScroll3 
         Height          =   255
         Left            =   120
         TabIndex        =   11
         Top             =   6360
         Width           =   6855
      End
      Begin VB.VScrollBar VScroll3 
         Height          =   6135
         Left            =   6960
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
         Width           =   6855
      End
   End
   Begin VB.Frame view_center_frame 
      Caption         =   "結果預覽"
      BeginProperty Font 
         Name            =   "iLiHei"
         Size            =   9.75
         Charset         =   136
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   6735
      Left            =   7440
      TabIndex        =   1
      Top             =   0
      Width           =   7335
      Begin VB.HScrollBar HScroll2 
         Height          =   255
         Left            =   120
         TabIndex        =   9
         Top             =   6360
         Width           =   6855
      End
      Begin VB.VScrollBar VScroll2 
         Height          =   6135
         Left            =   6960
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
         Width           =   6855
      End
   End
   Begin VB.Frame view_left_frame 
      Caption         =   "原始檔名"
      BeginProperty Font 
         Name            =   "iLiHei"
         Size            =   9.75
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
      Width           =   7335
      Begin VB.HScrollBar HScroll1 
         Height          =   255
         Left            =   120
         TabIndex        =   7
         Top             =   6360
         Width           =   6855
      End
      Begin VB.VScrollBar VScroll1 
         Height          =   6135
         Left            =   6960
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
         Width           =   6855
      End
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub Frame5_DragDrop(Source As Control, X As Single, Y As Single)

End Sub
