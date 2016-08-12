# AJSub by sdb file, 字幕檔自動繁簡轉換

## implement by python

## Introduction 軟體簡介

本軟體會自動將目錄下的所有字幕檔簡體轉為繁體

繁簡轉換是採用OpenCC-python, develop by:[Yichen (Eugene)]:(https://github.com/yichen0831/opencc-python).

但字型設定會是簡體, 這樣使用某些字型時系統才會認得(例如方正系列的字型)

UTF-8與UTF-16檔會照原格式儲存, 其餘會自動轉UTF-8格式

原始檔案備份在:"+backup_folder_name+"目錄下

## 使用說明

1. 將字幕檔路徑輸入SUB type欄位

2. 輸入字幕檔類型並用逗點隔開, 如*.ass, *.ssa

3. 按下Start之後, enjoy it!!!!
