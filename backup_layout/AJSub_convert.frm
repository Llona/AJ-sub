VERSION 5.00
Begin VB.Form Form1 
   Caption         =   "Form1"
   ClientHeight    =   9210
   ClientLeft      =   120
   ClientTop       =   450
   ClientWidth     =   11760
   LinkTopic       =   "Form1"
   ScaleHeight     =   9210
   ScaleWidth      =   11760
   StartUpPosition =   3  '系統預設值
   Begin VB.Frame log_frame 
      Caption         =   "log"
      BeginProperty Font 
         Name            =   "iLiHei"
         Size            =   9
         Charset         =   136
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   6495
      Left            =   120
      TabIndex        =   11
      Top             =   2640
      Width           =   11535
      Begin VB.HScrollBar HScroll1 
         Height          =   255
         Left            =   120
         TabIndex        =   14
         Top             =   6120
         Width           =   11055
      End
      Begin VB.VScrollBar VScroll1 
         Height          =   6015
         Left            =   11160
         TabIndex        =   13
         Top             =   120
         Width           =   255
      End
      Begin VB.TextBox log_txt 
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9.75
            Charset         =   136
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   6015
         Left            =   120
         MultiLine       =   -1  'True
         ScrollBars      =   3  '兩者皆有
         TabIndex        =   12
         Top             =   120
         Width           =   11055
      End
   End
   Begin VB.CheckBox shlog_chbutton 
      Caption         =   "Show log"
      BeginProperty Font 
         Name            =   "iLiHei"
         Size            =   9
         Charset         =   136
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   255
      Left            =   240
      TabIndex        =   9
      Top             =   2160
      Width           =   1215
   End
   Begin VB.Frame user_input_frame 
      Caption         =   "輸入"
      BeginProperty Font 
         Name            =   "iLiHei"
         Size            =   9
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   2415
      Left            =   120
      TabIndex        =   0
      Top             =   120
      Width           =   11535
      Begin VB.CommandButton clip_button 
         Caption         =   "Convert Clipboard"
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   495
         Left            =   9480
         TabIndex        =   8
         Top             =   1080
         Width           =   1575
      End
      Begin VB.CommandButton help_button 
         Caption         =   "Help"
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   495
         Left            =   6120
         TabIndex        =   7
         Top             =   1800
         Width           =   1215
      End
      Begin VB.CommandButton start_button 
         Caption         =   "Start"
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   495
         Left            =   3480
         TabIndex        =   6
         Top             =   1800
         Width           =   1215
      End
      Begin VB.CommandButton rename_button 
         Caption         =   "Sub Rename"
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   495
         Left            =   9480
         TabIndex        =   5
         Top             =   240
         Width           =   1575
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
         Left            =   1080
         TabIndex        =   4
         Text            =   "self.subpath_ini"
         Top             =   240
         Width           =   8055
      End
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
         Left            =   1080
         TabIndex        =   2
         Text            =   "self.subfiletype_list_ini"
         Top             =   960
         Width           =   8055
      End
      Begin VB.Label version_state 
         Alignment       =   1  '靠右對齊
         Caption         =   "idle"
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9
            Charset         =   136
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   9960
         TabIndex        =   10
         Top             =   2040
         Width           =   1335
      End
      Begin VB.Label sub_type_label 
         Caption         =   "SUB type:"
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
         Left            =   120
         TabIndex        =   3
         Top             =   960
         Width           =   855
      End
      Begin VB.Label sub_path_label 
         AutoSize        =   -1  'True
         Caption         =   "SUB Path:"
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9.75
            Charset         =   136
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   360
         Index           =   0
         Left            =   120
         TabIndex        =   1
         Top             =   240
         Width           =   825
      End
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub replace_all_sub_in_path()

End Sub

Private Sub print_about()

End Sub

Private Sub show_rename_frame()

End Sub

Private Sub convert_clipboard()

End Sub

Private Sub rename_button_Click()

End Sub
