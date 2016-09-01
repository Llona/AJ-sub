VERSION 5.00
Begin VB.Form Form1 
   Caption         =   "Form1"
   ClientHeight    =   11040
   ClientLeft      =   120
   ClientTop       =   450
   ClientWidth     =   11850
   LinkTopic       =   "Form1"
   ScaleHeight     =   11040
   ScaleWidth      =   11850
   StartUpPosition =   3  '系統預設值
   Begin VB.Frame log_frame 
      Caption         =   "LOG"
      BeginProperty Font 
         Name            =   "iLiHei"
         Size            =   9.75
         Charset         =   136
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   7815
      Left            =   120
      TabIndex        =   10
      Top             =   3120
      Width           =   11535
      Begin VB.HScrollBar HScroll1 
         Height          =   255
         Left            =   120
         TabIndex        =   13
         Top             =   7320
         Width           =   11055
      End
      Begin VB.VScrollBar VScroll1 
         Height          =   6975
         Left            =   11160
         TabIndex        =   12
         Top             =   360
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
         Height          =   6975
         Left            =   120
         MultiLine       =   -1  'True
         ScrollBars      =   3  '兩者皆有
         TabIndex        =   11
         Top             =   360
         Width           =   11055
      End
   End
   Begin VB.Frame user_input_frame 
      Caption         =   "輸入"
      BeginProperty Font 
         Name            =   "iLiHei"
         Size            =   9.75
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   2895
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
         Left            =   9600
         TabIndex        =   8
         Top             =   1440
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
         Left            =   6480
         TabIndex        =   7
         Top             =   2280
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
         Left            =   3240
         TabIndex        =   6
         Top             =   2280
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
         Left            =   9600
         TabIndex        =   5
         Top             =   480
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
         Height          =   495
         Left            =   120
         TabIndex        =   4
         Text            =   "self.subpath_ini"
         Top             =   600
         Width           =   8535
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
         Height          =   495
         Left            =   120
         TabIndex        =   2
         Text            =   "self.subfiletype_list_ini"
         Top             =   1560
         Width           =   8535
      End
      Begin VB.Label version_label 
         Alignment       =   1  '靠右對齊
         Caption         =   "version"
         BeginProperty Font 
            Name            =   "iLiHei"
            Size            =   9
            Charset         =   136
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   375
         Left            =   9720
         TabIndex        =   14
         Top             =   2520
         Width           =   1695
      End
      Begin VB.Label version_state 
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
         Height          =   375
         Left            =   120
         TabIndex        =   9
         Top             =   2520
         Width           =   1335
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
         Left            =   120
         TabIndex        =   3
         Top             =   1200
         Width           =   1095
      End
      Begin VB.Label sub_path_label 
         AutoSize        =   -1  'True
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
         Height          =   480
         Index           =   0
         Left            =   120
         TabIndex        =   1
         Top             =   240
         Width           =   900
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

