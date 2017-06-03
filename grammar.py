#!/usr/bin/python
# -*- coding:utf8 -*-

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

info[line 0, i 1, cha 2, numb 3, vproc 4[], vkind 5(0 1 3), integer 6, vlev 7, vadr 8(除以2), pname 9[], ptype 10, plev 11, fadr 12, ladr 13, vflag(0 1变量) 14, padr 15 , exflag(0,1) 16]
'''


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
process_table = open('grammar_process.txt', 'w')
process_table.close()
err = open('grmmar_error.txt','w')
err.close()

def write_var(info):
    variable_table = open('grammar_variable.txt', 'a')
    mes = 'vname: '+info[2]+'\nvproc: '+info[4][-1]+'\nvkind: '+str(info[5]%2)+'\nvtype: '+info[6]\
    +'\nvlev:'+str(info[7])+'\nvadr: '+str(info[8]/2)+'\n\n'
    variable_table.write(mes)
    variable_table.close()


def write_proc(info):
    process_table = open('grammar_process.txt', 'a')
    mes = 'pname: '+info[9][-1]+'\nptype: '+info[10]+'\nplev: '+str(info[11])+'\nfadr: '+str(info[12][-1])\
    +'\nladr: '+str(info[13][-1])+'\n\n'
    process_table.write(mes)
    process_table.close()


def write_error(info, message):
    err = open('grmmar_error.txt','a')
    err.write(info[2]+': '+message)
    err.close()

err_case1 = '<miss symbol>.\n'
err_case2 = '<mismatch>.\n'
err_case3 = '<no define or repeat define>.\n'

# 对读取进来的文件相关参数设置
seq_num = 0   # 字符序号
l = 1   # line
line = 0
for letter in text:
    if letter == '\n' or letter == '\r':
        line += 1   # 计算行数
func_dic = {}
variable_dic = {}


def advance(info):  # 将新字符相关信息读入info，info第五位为变量定义标志位（奇数时为变量说明），第六位
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
    info[0], info[1], info[2], info[3] = l+1, i+1, cha, int(numb)    # 返回目前行数，当前字符序号，字符，对应类别[]=info。此处使用list方便函数对其进行修改


def prog(info):   # 输入是当前行数，当前字符序号,符号，类别(current_line, current_i, sym, n)的list
    subprog(info)


def subprog(info):
    if info[2] == 'begin':
        advance(info)  # 读入,分别等于list中对应值
        info[16] = 1    # expflag 置1
        info[7] += 1  # begin开始后深度加1
        info[11] += 1  # begin开始后深度加1
        exptable(info)  # 说明语句
        if info[2] == ';':
            advance(info)
            exctable(info)
            if info[2] == 'end':
                advance(info)
                write_proc(func_dic[info[4][-1]])
                info[16] = 0
                info[7] -= 1  # end后深度减1
                info[11] -= 1  # end后深度减1
                if info[2] == 'EOF':
                    print 'Success with EOF'
            else:
                error('without end '+err_case2)
        else:
            error('; '+err_case1)
    else:
        error('without begin '+err_case1)


def error(word):
    print word
    exit()


def exptable(info):
    exp(info)
    exptable2(info)


def exp(info):  # 说明语句
    if info[2] == 'integer':    # 变量说明
        advance(info)
        exp_term(info)
    else:
        error('without integer '+err_case1)


def exp_term(info):
    if info[3] == 10:   # 是标识符，那么此时肯定是v
        info[8] += 1  # 标志着定义变量,在完成定义后会+1
        v(info)     # 定义变量
    elif info[2] == 'function':
        advance(info)
        info[15] += 1   # padr 加1，函数定义状态
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
                    error('withou \';\' '+err_case1)
            else:
                error('withou \')\' '+err_case2)
        else:
            error('withou \'(\' '+err_case1)
    else:
        error(err_case1)


def exptable2(info):
    info_term = info[:]
    advance(info_term)
    info_ahead = info_term[:]
    if info[2] == ';' and info_ahead[2] == 'integer':
        advance(info)
        exp(info)
        exptable2(info)


def v(info):
    info[14] = 1    # vflag=1   用于确定这是一个变量
    sym(info)
    info[14] = 0    # 重置


def sym(info):
    if info[3] == 10:   # 属于标识符类别
        if info[14] == 1:   # vflag=1
            info[14] = 0    # 重置vflag=0
            if (not variable_dic.has_key(info[2])) and info[8] % 2 == 1:  # 表内没有该变量，且处于定义状态(奇数)
                info[8] += 1  # 完成定义
                if info[16] == 1:   # 第一个变量
                    info[12].append(info[8]/2)  # fadr
                    info[16] = 0
                info[13].append(info[8]/2)  # ladr
                write_var(info)
                variable_dic[info[2]]=info[5]   # dic vname-->vkind
            elif variable_dic.has_key(info[2]) and info[8] % 2 == 1 and info[5] == variable_dic[info[2]]:  # 字典中有该变量，处于
                # 定义状态，且vkind同，重复定义
                write_error(info, err_case3)
                # TODO(GXY): Regular error
                info[8] += 1  # 完成定义
            elif (not variable_dic.has_key(info[2])) and info[8] % 2 != 1 and info[5] != 3:  # 表内没有该变量，且没有定义状态,且不是声明内形参：未定义
                write_error(info,err_case3)
                # TODO(GXY): Regular error
            elif (not variable_dic.has_key(info[2])) and info[8] % 2 != 1 and info[5] == 3 and info[15] % 2 == 1:  # 表内没有该变量，且没有定义状态,但是是声明内形参,处于函数定义状态
                info[15] += 1  # 完成函数定义
            elif (not variable_dic.has_key(info[2])) and info[8] % 2 != 1 and info[5] == 3 and info[15] % 2 != 1:  # 表内没有该变量，且没有定义状态,但是是声明内形参,未处于函数定义状态
                write_error(info,err_case3)
                # TODO(GXY): Regular error
            elif variable_dic.has_key(info[2]) and info[8] % 2 == 1 and info[5] ==3:   # 字典中有该变量，未处于
                # 定义状态，但是是声明内形参
                pass
            elif variable_dic.has_key(info[2]) and info[8] % 2 == 1 and info[5] != variable_dic[info[2]] and info[5] !=3:   # 字典中有该变量，未处于
                # 定义状态，vkind不同，但是非声明内形参
                info[8] += 1  # 完成定义
                write_var(info)
                variable_dic[info[2]] = info[5]  # dic vname-->vkind
        else:  # 是函数名
            if info[15] % 2 == 1:   # 处于函数定义状态
                info[4].append(info[2])  # 当前函数入栈
                info[9].append(info[2])  # 当前函数入栈
                func_dic[info[2]] = info[:]
            elif info[15] % 2 == 0:  # 非函数定义状态
                pass

        advance(info)
    else:
        error(err_case1)


def para(info):
    info[5] = 3  # 设置该变量为形参
    v(info)


def entity(info):
    if info[2] == 'begin':
        advance(info)
        info[16] = 1
        info[7] += 1    # begin开始后深度加1 vlev
        info[11] += 1   # begin开始后深度加1 plev
        exptable(info)      # 说明语句表
        if info[2] == ';':
            advance(info)
            exctable(info)  # 执行语句表
            if info[2] == 'end':
                advance(info)
                info[16] = 0
                info[7] -= 1    # end后深度减1  vlev
                info[11] -= 1  # end后深度减1   plev
                write_proc(func_dic[info[4][-1]])
                info[12].pop()  # fadr
                info[13].pop()  # ladr
                info[4].pop()   # 函数出栈
                info[9].pop()
            else:
                error('without end'+err_case2)
        else:
            error('without ; '+err_case1)
    else:
        error('without begin '+err_case1)


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
        info[4].append(info[2])     # 将read加入过程
        advance(info)
        if info[2] =='(':
            advance(info)
            v(info)
            if info[2] == ')':
                info[4].pop()   # 退出read状态
                advance(info)
            else:
                error('withou \')\' '+err_case2)
        else:
            error('without \'(\''+err_case1)
    elif info[2] == 'write':
        info[4].append(info[2])  # 将write加入过程
        advance(info)
        if info[2] == '(':
            advance(info)
            v(info)
            if info[2] == ')':
                info[4].pop()  # 退出write状态
                advance(info)
            else:
                error('withou \')\' '+err_case2)
        else:
            error('without \'(\''+err_case1)
    elif info[3] == 10:
        v(info)
        if info[2] == ':=':
            advance(info)
            arithexpress(info)
        else:
            error('without \':=\''+err_case1)
    elif info[2] == 'if':
        advance(info)
        cdexpress(info)
        if info[2] == 'then':
            advance(info)
            exc(info)
            if info[2] == 'else':
                advance(info)
                exc(info)
            else:
                error('without else '+err_case2)
        else:
            error('without then '+err_case2)
    else:
        error(err_case1)


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
                error('withou \')\' '+err_case2)
        else:
            error('withou \'(\' '+err_case1)
    else:
        error(err_case1)


def cdexpress(info):
    arithexpress(info)
    relaexpress(info)
    arithexpress(info)

def relaexpress(info):
    if info[3] >= 12 and info[3] <= 17:
        advance(info)
    else:
        error(err_case1)

initial = [1, 0, 'initial', 'initial', ['main'], 0, 'integer', 0, 0, ['main'], 'integer', 1, [], [], 0, 0, 0]
advance(initial)
func_dic[initial[4][-1]]=initial[:]
prog(initial)
