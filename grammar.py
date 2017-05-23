#!/usr/bin/python
# -*- coding:utf8 -*-
# TODO(GXY): Recrusive Descent Parser

'''
prog—> subprog
subprog—> begin exptable; exctable end
exptable—> exp exptable2
exptable2—> ; exp exptable2 | 空
exp—>  integer v | funcexp
v—> sym
sym—> alphabet sym2 | alphabet sym3
sym2—> alphabet sym2 | 空
sym3—> num sym3 | 空
alphabet—> …
num—> …
funcexp—> integer function sym (para); entity
para—> v
entity—> begin exptable; exctable end
exctable—> exc exctable2
exctable2—> ; exc exctable2 | 空
exc—> read(v) |  write(v) |  v:=arithexpress |  if cdexpress then exc else exc
arithexpress—> term arithexpress2
arithexpress2—> -term arithexpress2 | 空
term—> factor term2
term2—> *factor term2 | 空
factor—> v | const |  sym(func_x)
const—> unsigned
unsigned—> num unsigned2
unsigned2—> num unsigned2 | 空
cdexpress—> arithexpress relaexpress arithexpress
relaexpress—> …
funcall—> sym(arithexpress)
'''

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

# 读文件
file_path = "/Users/gxy/Desktop/Compile/Experiment/vocab_result.txt"
fp_read = open(file_path, 'r')
text = fp_read.read()

# 创建相关文件
variable_table = open('grammar_variable.txt', 'w')
variable_table.close()
process_table = open('grammar_process.txt', 'w')   # 创建文件
process_table.close()

# 对读取进来的文件相关参数设置
seq_num = 0   # 字符序号
l = 1   # line
line = 0
for letter in text:
    if letter == '\n' or letter == '\r':
        line += 1   # 计算行数
func_dic = {}


def advance(info):  # 将新字符相关信息读入info，info第五位为变量定义标志位，第六位
    l, i = info[0], info[1]
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
    info[0], info[1], info[2], info[3] = l+1, i+1, cha, numb    # 返回目前行数，当前字符序号，字符，对应类别[]=info。此处使用list方便函数对其进行修改


def prog(info):   # 输入是当前行数，当前字符序号,符号，类别(current_line, current_i, sym, n)的list
    subprog(info)


def subprog(info):
    if info[2] == 'begin':
        advance(info)  # 读入,分别等于list中对应值
        exptable(info)
        if info[2] == ';':
            advance(info)
            exctable(info)
            if info[2] == 'end':
                advance(info)
            else:
                error()
        else:
            error()
    else:
        error()


def error():
    print 'error'


def exptable(info):
    exp(info)
    exptable2(info)


def exp(info):  # 说明语句
    if info[2] == 'integer':    # 变量说明
        advance(info)
        exp_term(info)
    else:
        error()


def exp_term(info):
    if info[3] == 10:   # 是标识符，那么此时肯定是v
        v(info)
    elif info[2] == 'function':
        advance(info)
        sym(info)
        if info[2] == '(':
            advance(info)
            para(info)
            if info[2] == ')':
                advance(info)
                if info[2] == ';':
                    advance(info)
                    entity(info)
                else:
                    error()
            else:
                error()
        else:
            error()
    else:
        error()


def exptable2(info):
    if info[2] == ';':
        advance(info)
        exp(info)
        exptable2(info)


def v(info):
    sym(info)


def sym(info):
    if info[3] == 10:   # 属于标识符类别
        advance(info)
    else:
        error()


def para(info):
    v(info)


def entity(info):
    if info[2] == 'begin':
        advance(info)
        exptable(info)
        if info[2] == ';':
            advance(info)
            exctable(info)
            if info[2] == 'end':
                advance(info)
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
        advance(info)
        exc(info)
        exctable2(info)


def exc(info):
    if info[2] == 'read':
        advance(info)
        if info[2] =='(':
            advance(info)
            v(info)
            if info[2] == ')':
                advance(info)
            else:
                error()
        else:
            error()
    elif info[2] == 'write':
        advance(info)
        if info[2] == '(':
            advance(info)
            v(info)
            advance(info)
            if info[2] == ')':
                advance(info)
            else:
                error()
        else:
            error()
    elif info[3] == 10: # v()
        v(info)
        if info[2] == ':=':
            advance(info)
            arithexpress(info)
        else:
            error()
    elif info[2] == 'if':
        advance(info)
        cdexpress(info)
        if info[2] == 'then':
            advance(info)
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
        advance(info)
        term(info)
        arithexpress2(info)


def term(info):
    factor(info)
    term2(info)


def term2(info):
    if info[2] == '*':
        advance(info)
        factor(info)
        term2(info)


def factor(info):
    if info[3] == 10 and not func_dic.has_key(info[2]): # 此为变量
        v(info)
    elif info[3] == 11: # 此为数字
        advance(info)
    elif info[3] and func_dic.has_key(info[2]): # 此为函数名,且先前已定义(funccall)
        advance(info)
        if info[2] == '(':
            advance(info)
            arithexpress(info)
            if info[2] == ')':
                advance(info)
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
        advance(info)
    else:
        error()

prog([1, 0, 'initial', 'initial', 0, 0])