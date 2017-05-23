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
func_dic = {}


def advance(l, i):  # 返回目前行数，当前字符序号，字符，对应类别
    flag = 0  # 区分二项式前后，主要针对数字
    while text[i] != '\n' and text[i] != '\r':  # 当读到换行符时退出
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
    return [l+1, i+1, cha, numb]   # 返回目前行数，当前字符序号，字符，对应类别[]=info。此处使用list方便函数对其进行修改


def prog(info):   # 输入是当前行数，当前字符序号,符号，类别(current_line, current_i, sym, n)的list
    subprog(info)


def subprog(info):
    if info[2] == 'begin':
        info = advance(info[0], info[1])  # 读入,分别等于list中对应值
        exptable(info)
        if info[2] == ';':
            info = advance(info[0], info[1])
            exctable(info)
            if info[2] == 'end':
                info = advance(info[0], info[1])
            else:
                error()
        else:
            error()
    else:
        error()


def error():
    pass


def exptable(info):
    exp(info)
    exptable2(info)


def exp(info):
    if info[2] == 'integer':
        info = advance(info[0], info[1])
        v(info)
    else:
        funcexp(info)


def exptable2(info):
    if info[2] == ';':
        info = advance(info[0], info[1])
        exp(info)
        exptable2(info)


def v(info):
    sym(info)


def sym(info):
    if info[3] == 10:   # 属于标识符类别
        info = advance(info[0], info[1])
    else:
        error()


def funcexp(info):
    if info[2] == 'integer':
        info = advance(info[0], info[1])
        if info[2] == 'function':
            info = advance(info[0], info[1])
            sym(info)
            if info[2] == '(':
                info = advance(info[0], info[1])
                para(info)
                if info[2] == ')':
                    info = advance(info[0], info[1])
                    if info[2] == ';':
                        info = advance(info[0], info[1])
                        entity(info)
                    else:
                        error()
                else:
                    error()
            else:
                error()
        else:
            error()
    else:
        error()


def para(info):
    v(info)


def entity(info):
    if info[2] == 'begin':
        info = advance(info[0], info[1])
        exptable(info)
        if info[2] == ';':
            info = advance(info[0], info[1])
            exctable(info)
            if info[2] == 'end':
                info = advance(info[0], info[1])
            else:
                error()
        else:
            error()
    else:
        error()


def exctable(info):
    exc(info)
    exctable2(info)


def exctable2(info):
    if info[2] == ';':
        info = advance(info[0], info[1])
        exc(info)
        exctable2(info)


def exc(info):
    if info[2] == 'read':
        info = advance(info[0], info[1])
        if info[2] =='(':
            info = advance(info[0], info[1])
            if info[3] == '10':
                info = advance(info[0], info[1])
                if info[2] == ')':
                    info = advance(info[0], info[1])
                else:
                    error()
            else:
                error()
        else:
            error()
    elif info[2] == 'write':
        info = advance(info[0], info[1])
        if info[2] == '(':
            info = advance(info[0], info[1])
            if info[3] == '10':
                info = advance(info[0], info[1])
                if info[2] == ')':
                    info = advance(info[0], info[1])
                else:
                    error()
            else:
                error()
        else:
            error()
    elif info[3] == 10:
        info = advance(info[0], info[1])
        if info[2] == ':=':
            info = advance(info[0], info[1])
            arithexpress(info)
        else:
            error()
    elif info[2] == 'if':
        info = advance(info[0], info[1])
        cdexpress(info)
        if info[2] == 'then':
            info = advance(info[0], info[1])
            exc(info)
            if info[2] == 'else':
                exc(info)
            else:
                error()
        else:
            error()
    else:
        error()


def arithexpress(info):
    term(info)
    arithexpress2(info)


def arithexpress2(info):
    if info[2] == '-':
        info = advance(info[0], info[1])
        term(info)
        arithexpress2(info)


def term(info):
    factor(info)
    term2(info)


def term2(info):
    if info[2] == '*':
        info = advance(info[0], info[1])
        factor(info)
        term2(info)


def factor(info):
    if info[3] == 10 and not func_dic.has_key(info[2]): # 此为变量
        info = advance(info[0], info[1])
    elif info[3] == 11: # 此为数字
        info = advance(info[0], info[1])
    elif info[3] and func_dic.has_key(info[2]): # 此为函数名,且先前已定义(funccall)
        info = advance(info[0], info[1])
        if info[2] == '(':
            info = advance(info[0], info[1])
            arithexpress(info)
            if info[2] == ')':
                info = advance(info[0], info[1])
            else:
                error()
        else:
            error()
    else:
        error()


def cdexpress(info):
    arithexpress(info)
    relaexpress(info)
    arithexpress(info)

def relaexpress(info):
    if info[3] >= 12 and info[3] <= 17:
        info = advance(info[0], info[1])

prog(advance(l, 0))