#!/usr/bin/python
# -*- coding:utf8 -*-
# TODO(GXY): Recrusive Descent Parser
import sys
import string

def getvar(ind, character): # 抓取标识符
    if str.isalpha(text[ind]) or str.isalnum(text[ind]):
        character += text[ind]
        if ind == len(text)-1:
            return character, ind
        else:
            ind += 1
            a, b = getvar(ind, character)   # 此处需要接变量
    else:
        return character, ind
    return a, b

def getnum(ind, num):   # 抓取数字
    if str.isalnum(text[ind]):
        num += text[ind]
        if ind == len(text)-1:
            return num, ind
        else:
            ind += 1
            a, b = getnum(ind, num)
    else:
        return num, ind
    return a, b

file_path = "/Users/gxy/Desktop/Compile/Experiment/vocab_result.txt"
fp_read = open(file_path, 'r')
text = fp_read.read()
out = open('grammar_result.txt', 'w')   # 创建文件
out.close()
i = 0   # 字符序号
l = 1   # line
line = 0
flag = 0 # 区分二项式前后，主要针对数字
for letter in text:
    if letter == '\n' or letter == '\r':
        line += 1   # 计算行数

while(l < line):
    if text[i] == ' ':
        i += 1
        continue

    if str.isalpha(text[i]):   # 以字母开头的标识符
        i += 1
        var, i = getvar(i, text[i-1])    # 返回变量与当前索引
        flag += 1
        # print var
        continue

    if text[i] == '=' or text[i] == '-' or text[i] == '*' or text[i] == '(' or text[i] == ')' or text[i] == ';':
        i += 1
        var = text[i-1]
        flag += 1
        continue

    if text[i] == '<':
        i += 1
        var = text[i-1]
        if text[i] == '=' or text[i] == '>':
            var += text[i]
            i += 1
        flag += 1
        continue

    if text[i] == '>':
        i += 1
        var = text[i-1]
        if text[i] == '=':
            var += text[i]
            i += 1
        flag += 1
        continue

    if text[i] == ':':
        i += 1
        var = text[i-1]
        if text[i] == '=':
            var += text[i]
            i += 1
        flag += 1
        continue

    if str.isalnum(text[i]):    # 数字
        i += 1
        if flag == 0:
            var, i = getnum(i, text[i - 1])
        else:
            num, i = getnum(i, text[i-1])
        # print num
        flag += 1
        continue

    if text[i] == '\n' or text[i] == '\r':  # 换行符
        i += 1
        l += 1  # 循环内唯一控制换行
        flag = 0 # 换行时初始化flag
        continue
