;Ver 2.0 - First version
;Read Sublist.ini for match Sub string

; Create the array, initially empty
Setting_Count := 0
PsPadPath := ""
SubPath := ""
SubType := ""
String_Array := Object()
String_ArrayCount := 0
;TempClipboard := ""
;-------------------Read file and store to Array--------------------------
FileRead, SubList, Sublist.ini
if ErrorLevel
{
	SubList = ;Free the memory
	MsgBox, read Sublist.ini error
	ExitApp
}

Loop, read, Setting.txt
{
	Setting_Count += 1
	if (Setting_Count <= 3)
	{
		if (Setting_Count = 1)
		{
			PsPadPath := A_LoopReadLine
		}
		else if (Setting_Count = 2)
		{
			SubPath := A_LoopReadLine
		}
		else
		{
			SubType := A_LoopReadLine
		}
	}
	else
	{
		String_ArrayCount += 1
		IfInString, SubList, %A_LoopReadLine%
		{
			;RegExMatch(A_LoopReadLine, "(.*);(.*)", SubPat)
			;String_Array[String_ArrayCount,1] := SubPat1
			;String_Array[String_ArrayCount,2] := SubPat2
			
			String_Array[String_ArrayCount,1] := A_LoopReadLine
			RegExMatch(SubList, A_LoopReadLine ";(.*)", SubPat)
			String_Array[String_ArrayCount,2] := SubPat1
			
			MsgBox % A_LoopReadLine "`n" SubPat1 "`n"
			
		}
		else
		{
			SubList = ;Free the memory
			MsgBox, Error! Sub %A_LoopReadLine% is not in SubList.ini
			ExitApp
		}

	}

}
SubList = ;Free the memory

MsgBox % SubPath "`n" SubType "`n" String_Array[1,1] "`n" String_Array[1,2] "`n" String_Array[2,1] "`n" String_Array[2,2] "`n" 
;MsgBox % SubPat1 "`n" SubPat2

;^p::
MsgBox, 4, ReplaceSub, Start to replace all SUB file in "%SubPath%"?
IfMsgBox No
{
	ExitApp
}

;-------------------Open PsPad for replace all sub file-----------------------------------------
Run, %PsPadPath%
winwait, ahk_class TfPSPad.UnicodeClass,
winactivate, ahk_class TfPSPad.UnicodeClass,
Sleep, 500

;---------------Replace sub text by PsPad from Setting.txt----------------------------------
String_ArrayCount := 1
While String_Array[String_ArrayCount, 1] != ""
{
	Send, !s+w
	Sleep, 300
	
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
	
	Send, !y
	Sleep, 1000
	
	winwait, ahk_class TMessageForm, , 5
	winactivate, ahk_class TMessageForm, , 5
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
MsgBox, , ReplaceSub, Replace all SUB file in "%SubPath%" done
ExitApp
Return
;---------------------------------------------------
^r::
	reload
	return
^q::
	ExitApp