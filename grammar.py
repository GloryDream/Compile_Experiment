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
seq_num = 0   # 字符序号
l = 1   # line
line = 0
for letter in text:
    if letter == '\n' or letter == '\r':
        line += 1   # 计算行数


def advance(l, i):  # 返回当前读入的符号，以及其类别
    flag = 0  # 区分二项式前后，主要针对数字
    while text[i] != '\n' or text[i] != '\r':  # 当读到换行符时退出
        if text[i] == ' ':
            i += 1
            continue

        if str.isalpha(text[i]):  # 以字母开头的标识符
            i += 1
            cha, i = getvar(i, text[i - 1])  # 返回变量与当前索引
            flag += 1
            # print var
            continue

        if text[i] == '=' or text[i] == '-' or text[i] == '*' or text[i] == '(' or text[i] == ')' or text[i] == ';':
            i += 1
            cha = text[i - 1]
            flag += 1
            # print var
            continue

        if text[i] == '<':
            i += 1
            cha = text[i - 1]
            if text[i] == '=' or text[i] == '>':
                cha += text[i]
                i += 1
            flag += 1
            # print var
            continue

        if text[i] == '>':
            i += 1
            cha = text[i - 1]
            if text[i] == '=':
                cha += text[i]
                i += 1
            flag += 1
            # print var
            continue

        if text[i] == ':':
            i += 1
            cha = text[i - 1]
            if text[i] == '=':
                cha += text[i]
                i += 1
            flag += 1
            # print var
            continue

        if str.isalnum(text[i]):  # 数字
            i += 1
            if flag == 0:
                cha, i = getnum(i, text[i - 1])
                # print var
            else:
                numb, i = getnum(i, text[i - 1])
                # print num
            flag += 1
            continue
    return l+1, cha, numb   # 返回目前行数，字符，对应类别


