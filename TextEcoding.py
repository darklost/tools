#coding:utf-8
#
#Create on: 2015-1-21
#Create by:	D.K.
#use   for: 文件文本编码转换
import os
import codecs

def ReadFile(filePath, encoding):
    with codecs.open(filePath, "r", encoding=encoding) as f:
        return f.read()

def WriteFile(filePath, content, encoding):
    with codecs.open(filePath, "w", encoding=encoding) as f:
        f.write(content)

def UTF8_to_GBK(src, dst):
    content = ReadFile(src, encoding="utf-8")
    WriteFile(dst, content, "gbk")
	
def GBK_to_UTF8(src, dst):
    content = ReadFile(src, encoding="gbk")
    WriteFile(dst, content, "utf-8")