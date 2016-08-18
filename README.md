# AJSub - 強力轉換!!轉碼君

字幕檔自動簡繁轉換, Implement by [Llona](https://github.com/Llona/AJ-sub).

## Introduction 軟體簡介

- 本軟體會自動將指定目錄下的所有字幕檔內容簡體轉為繁體

例如:
> 
Style: Default,方正準圓_GBK,50,&H00FFFFFF,&HF0000000,&H00000000,&H0058281B,-1,0,0,0,100,100,0,0,1,2,0,2,30,30,15,1
S

會轉為

> Style: Default,方正准圆_GBK,50,&H00FFFFFF,&HF0000000,&H00000000,&H0058281B,-1,0,0,0,100,100,0,0,1,2,0,2,30,30,15,1

- 字型設定部份會轉為簡體, 這樣使用某些字型時系統才會認得 (例如方正系列的字型)

- UTF-8與UTF-16檔會照原格式儲存, 其餘會自動轉UTF-8格式

- 原始檔案備份在:backfile目錄下

## 使用說明

1. 執行AJSub.exe 

2. 將字幕檔路徑輸入SUB path欄位

3. 將字幕檔類型輸入SUB type欄位並用逗點隔開, 如*.ass, *.ssa

4. 按下Start之後, enjoy it!!!!

5. 字型設定檔若需新增或修改, 請直接修改SubList.sdb 

----------

- 繁簡轉換功能是採用OpenCC-python, develop by:[Yichen (Eugene)](https://github.com/yichen0831/opencc-python).
