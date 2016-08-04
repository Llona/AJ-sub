;Ver 1.0 - First version
;Ver 2.0 - Uses database for match SUB file name and read Sublist.ini for match Sub string
;Ver 3.0 - Uses GUI for parameter input


; Init the var and array
TitleVersion := "Replace Sub v3.0"
Setting_Count := 0
PsPadPath := ""
SubPath := ""
SubType := ""
String_Array := Object()
String_ArrayCount := 0
TempStr := "" ;Only uses for append ";" for match sub filename
IsReplaceSubChangeInGUI := false

;-------------------Read Setting.ini for get parameter--------------------
IniRead, IniOutput, Settings.ini, Global, PsPadPath
PsPadPath := IniOutput
IniRead, IniOutput, Settings.ini, Global, SubPath
SubPath := IniOutput
IniRead, IniOutput, Settings.ini, Global, SubType
SubType := IniOutput
;MsgBox, The value is `n%PsPadPath%`n%SubPath%`n%SubType%

;---------------------------------------------------------------------------
IfNotExist, ReplaceList.tmp
{
	MsgBox,,%TitleVersion%,ReplaceList.tmp is not exist, please uses unicode format creat it
	ExitApp
}

FileRead, ReplaceListTmp, ReplaceList.tmp
if ErrorLevel
{
	ReplaceListTmp = ;Free the memory
	MsgBox,,%TitleVersion%,read ReplaceList.tmp error
	ExitApp
}

;^p::
;--------------------Run GUI for user edit------------------------------------------------
Gui, Add, Edit, vEditPsPadPath x22 y30 w470 h30 , %PsPadPath%
Gui, Add, Edit, vEditSUBPath x22 y100 w470 h30 , %SubPath%
Gui, Add, Text, x22 y10 w100 h20 , 請輸入PsPad路徑
Gui, Add, Text, x22 y70 w100 h20 , 請輸入SUB目錄
Gui, Add, Button, x112 y540 w80 h30 , OK
Gui, Add, Button, x312 y540 w80 h30 , Cancle
Gui, Add, Edit, vEditReplaceSub x22 y170 w470 h320 , %ReplaceListTmp%
Gui, Add, Text, x22 y140 w200 h20 , 請輸入要替換的字型
; Generated using SmartGUI Creator 4.0
Gui, Show, x210 y260 h590 w510, %TitleVersion%
Return

GuiClose:
ExitApp

ButtonCancle:
ExitApp

ButtonOK:
Gui, Submit  ; Save the input from the user to each control's associated variable.
;MsgBox, %EditPsPadPath%`n%EditSUBPath%

IfNotExist, %EditPsPadPath%
{
	MsgBox,,%TitleVersion%, Can't find PsPad in %EditPsPadPath%, please check PsPAd path
	Reload
	return
}
IfNotExist, %EditSUBPath%
{
	MsgBox,,%TitleVersion%, Can't find Sub path in %EditSUBPath%, please check sub path
	Reload
	return
}



;--------------------------store user GUI setting to ini and ReplaceList.tmp file-----------------------------------
IfNotEqual, EditPsPadPath, %PsPadPath%
{
	IniWrite, %EditPsPadPath%, Settings.ini, Global, PsPadPath
}
IfNotEqual, EditSUBPath, %SubPath%
{
	IniWrite, %EditSUBPath%, Settings.ini, Global, SubPath
}
IfNotEqual, EditReplaceSub, %ReplaceListTmp%
{
	;Msgbox, EditReplaceSub is true
	file := FileOpen("ReplaceList.tmp", "w", "UTF-16")
	if !IsObject(file)
	{
		MsgBox Can't open "ReplaceList.tmp" for writing.
		ExitApp
	}
	file.Write(EditReplaceSub)
	file.Close()
}

;Get user setting in GUI
PsPadPath := EditPsPadPath
SubPath := EditSUBPath
ReplaceListTmp := EditReplaceSub
;MsgBox, %EditReplaceSub%

;-------------------Read Sub database file and store sub file name that in GUI setting to Array--------------------------
FileRead, SubList, Sublist.sdb
if ErrorLevel
{
	SubList = ;Free the memory
	MsgBox, read Sublist.sdb error
	ExitApp
}

Loop, Parse, ReplaceListTmp, `n	
{
	String_ArrayCount += 1
	TempStr := A_LoopField ";"
	
	IfInString, SubList , %TempStr%
	{
		String_Array[String_ArrayCount,1] := A_LoopField
		RegExMatch(SubList, A_LoopField ";(.*)" , SubPat)
		String_Array[String_ArrayCount,2] := SubPat1
		;MsgBox % A_LoopField "`n" SubPat1 "`n"
	}
	else
	{
		SubList = ;Free the memory
		ReplaceListTmp =
		MsgBox,,%TitleVersion%,Error! Sub %A_LoopField% is not in SubList.sdb
		Reload
		return
	}

}
SubList = ;Free the memory
ReplaceListTmp = ;Free the memory

;MsgBox % SubPath "`n" SubType "`n" String_Array[1,1] "`n" String_Array[1,2] "`n" String_Array[2,1] "`n" String_Array[2,2] "`n" 
;MsgBox % SubPat1 "`n" SubPat2

;-------------------Open PsPad for replace all sub file-----------------------------------------
IfWinNotExist,ahk_class TfPSPad.UnicodeClass
{
	Run, %PsPadPath%
	Sleep, 500
	winwait, ahk_class TfPSPad.UnicodeClass,
	winactivate, ahk_class TfPSPad.UnicodeClass,
}
else
{
	;PsPad already exist, set win focuse to PsPad
	WinActivate, ahk_class TfPSPad.UnicodeClass
	Sleep, 300
}

;---------------Replace sub text by PsPad from Setting.txt----------------------------------
String_ArrayCount := 1
While String_Array[String_ArrayCount, 1] != ""
{
	Send, !s+w
	Sleep, 300
	winwait, ahk_class TfFileSearch, , 10
	winactivate, ahk_class TfFileSearch, , 10
	
	
	Send, !t
	SendStringByClipboard(String_Array[String_ArrayCount,1])

	Send, !r
	SendStringByClipboard(String_Array[String_ArrayCount,2])

	Send, !d
	Sleep, 300
	Send, {Right}
	SendStringByClipboard(SubPath)

	Send, !f
	SendStringByClipboard(SubType)

	Send, !o
	Sleep, 300
	winwait, ahk_class #32770, , 10
	winactivate, ahk_class #32770, , 10

	
	Send, !y
	Sleep, 1000
	
	winwait, ahk_class TMessageForm, , 10
	winactivate, ahk_class TMessageForm, , 10
	IfWinActive,ahk_class TMessageForm
	{
		Send, {Enter}
	}

	String_ArrayCount += 1
}

;----------------Send text by clipboard-----------------------------------
SendStringByClipboard(String)
{
	;TempClipboard := clipboard
	Sleep, 200
	clipboard := String
	Send, ^v
	Sleep, 300
}

;MsgBox Replace SUB file in "%SubPath%" done
MsgBox,,%TitleVersion%,ReplaceSub, Replace all SUB file in "%SubPath%" done

Reload
return

;---------------------------------------------------
^r::
	reload
	return
^q::
	ExitApp