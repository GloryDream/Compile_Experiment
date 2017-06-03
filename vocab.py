#!/usr/bin/python
# -*- coding:utf8 -*-

dic = {}
dic['begin'] =1
dic['end'] =2
dic['integer'] =3
dic['if'] = 4
dic['then']=5
dic['else'] =6
dic['function'] = 7
dic['read'] =8
dic['write'] =9
dic['='] = 12
dic['<>'] = 13
dic['<='] = 14
dic['<'] =15
dic['>='] =16
dic['>'] =17
dic['-'] = 18
dic['*'] = 19
dic[':='] =20
dic['('] = 21
dic[')'] = 22
dic[';'] = 23

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

def getnum(ind, num):
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

def reserve(character): # 返回单词种别，标识符除外
    if dic.has_key(character):
        return dic[character]
    elif str.isalnum(character):
        return 11
    else:
        assert 'Invalid syntax'

def write_info(word,kind):
    out = open('vocab_result.txt', 'a')   # 打开文件不清零
    k = str(kind)
    info = (16-len(word))*' ' + word + ' ' + (2-len(k)) * ' ' + k + '\n'
    out.write(info)
    out.close()

def write_err(word, line, error_type):
    err = open('vocab_error.txt', 'a')
    error = '***LINE:' + str(line) + 2 * ' ' + error_type + ' \'' + word + '\'\n'
    err.write(error)
    err.close()

file_path = "/Users/gxy/Desktop/Compile/Experiment/input.txt"
fp_read = open(file_path, 'r')
text = fp_read.read()
out = open('vocab_result.txt', 'w')   # 创建文件
out.close()
err = open('vocab_error.txt', 'w')
err.close()
i = 0   # 字符序号
l = 1   # line
while(i< len(text)-1):
    char = text[i]  # token()
    if char == ' ':  # getnbc()
        i += 1
        continue
    if char == '\n' or char == '\r':
        i += 1
        l += 1  #记行
        continue
    if str.isalpha(char):   # 以字母开头的标识符
        i += 1
        var, i = getvar(i, char)    # 返回变量与当前索引
        if len(var) > 16:
            err_type = 'Name is too long'
            write_err(var, l, err_type)
        else:
            if dic.has_key(var):
                write_info(var, reserve(var))
            else:
                write_info(var, 10)
        continue
    if str.isalnum(char):   # 数字
        i += 1
        num, i = getnum(i, char)
        if len(num)>16:
            err_type = 'Value is too large'
            write_err(num, l, err_type)
        else:
            write_info(num, reserve(num))
        continue
    if char == '=' or char == '-' or char == '*' or char == '(' or char == ')' or char == ';':
        i += 1
        write_info(char, reserve(char))
        continue
    if char == '<':
        i += 1
        if text[i] == '=' or text[i] == '>':
            char += text[i]
            i += 1
        write_info(char, reserve(char))
        continue
    if char == '>':
        i += 1
        if text[i] == '=':
            char += text[i]
            i += 1
        write_info(char, reserve(char))
        continue
    if char == ':':
        i += 1
        if text[i] == '=':
            char += text[i]
            i += 1
            write_info(char, reserve(char))
        else:
            err_type = 'Expected \'=\' after \':\''
            char += text[i]
            write_err(char, l, err_type)
            i += 1
        continue
    err_type = 'Invalid character'
    write_err(char, l, err_type)
    i += 1
write_info('EOF', 25)