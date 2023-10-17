# -*- coding: utf-8 -*-
import time
import _thread as thr
import sys
import os
import re

from collections import defaultdict
try:
    from collections import Iterable
except:
    from collections.abc import Iterable

__all__ = [
    'str_time_day','print_var','str_time_year','str_time_Day','str_time_Month','str_time_hour','sleep',
    'print_sys','print_msg','print_error','lib_to_do_lib','len_var','print_dict','var_name',
    'readConfig','rename_file','copy_file','str_dict','input_lib','print_function','readTxt',
    'print_object','print_item','match_regex','print_module']

current_path = os.path.dirname(os.path.abspath(__file__))
min_sec = 60
hou_sec = min_sec * 60
day_sec = hou_sec * 24
tasks = {
    "1": "定时提醒",
    "2": "",
    "3": "",
    "4": "",
    "5": "",
    "q": "退出系统",
    "i": "查询现有任务",
    "r": "修改任务",
    "d": "del task",
    "reloading": "reloading task"
}
repeat_lib = {"1": "定时", "2": "每日", "3": "工作日", "4": "延迟N分钟", "5": "Now"}
group_lib = {
    "0": {
        "1": "项目组",
        "2": "贪吃蛇测试组",
        "3": "袁少华"
    },
    "袁少华":
    "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=cf6fe1e9-5bd9-42af-a518-4a7c3f609b79",
    "贪吃蛇测试组":
    "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2acaad96-591b-4176-9759-6cbba401855d",
    "项目组":
    "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=503a0e01-9dc6-4b98-8fc9-8980d76ac0a9"
}
models = {}
task_list = {}
task_replace = {}
debug = False
data_list = ["content", "mentioned_list", "mentioned_mobile_list"]

def match_regex(s1, a1):
    """判断字符串s1是否符合正则表达式a1"""
    pattern = re.compile(a1)
    match = pattern.match(s1)
    if match:
        return True
    else:
        return False
    
def readTxt(dir_file):
    """读入txt文件内容为list"""
    try:
        with open(dir_file,'r',encoding='UTF-8') as f:
            res = f.readlines()
            return [re.replace('\n','') for re in  res]
    except:
        print('UTF-8 encoding error,try gb2312 encoding file:', dir_file )
        with open(dir_file,'r',encoding='gb2312') as f:
        # with open(file,'r',encoding='ascii') as f:
            res = f.readlines()
            return [re.replace('\n','') for re in  res]
    finally:
        print('read end:%s' % dir_file)

def str_time_day(split='T', s_time='-'):
    return time.strftime(f'%Y-%m-%d{split}%H{s_time}%M{s_time}%S', time.localtime())

def str_time_year(split='T'):
    return time.strftime(f'%Y-%m-%d{split}%H-%M-%S', time.localtime())

def str_time_Day():
    return time.strftime('%Y-%m-%d', time.localtime())


def str_time_Month():
    return time.strftime('%Y-%m', time.localtime())


def str_time_hour(split=':'):
    return time.strftime(f'%H{split}%M{split}%S', time.localtime())


def sleep(times=2):
    for i in range(times):
        print("\r"+"wait for {}/{}s ".format(i, times),end='',flush=True)
        time.sleep(1)


def print_sys(tips=''):
    """
    :param tips:
    :return:
    """
    print_msg(f"{tips}\nUnexpected error: {sys.exc_info()[0]}, {sys.exc_info()[1]}")


def print_msg(tips=None):
    if not tips:
        print("task".center(100,'#'))
    else:
        print(f'{str_time_day()}'.center(100,'#'))
        print(tips)
        print(f'{str_time_day()}'.center(100,'#'))


def print_var(var,mark=None,dict_var=globals()):
    """
    dict_var:变量空间,建议使用local(),默认为全局变量globals()
    打印一个变量
    """
    print(f'{"**" * 10}{ mark}{"**" * 10}')
    print(f'变量【{var_name(var,dict_var)}】类型:{type(var)}')
    print(f'__str__:\n{var.__str__}')
    print(f'表达结果:\n{var}')
    print(f'{"**" * 10}{ mark}end{"**" * 10}')

def print_error(tips=""):
    tips += "输入有误,请重新输入:"
    print("**" * 15 + tips + "**" * 15)


def lib_to_do_lib(dict_lib):
    libs = {}
    do_lib = {}
    if isinstance(dict_lib, (list, tuple)):
        print(dict_lib)
        for i in range(len(dict_lib)):
            libs[str(i + 1)] = dict_lib[i]
        do_lib = libs.copy()
    elif isinstance(dict_lib, dict):
        if '0' in dict_lib.keys():
            libs = dict_lib['0']
        else:
            keys_lib = list(dict_lib.keys())
            for i in range(len(keys_lib)):
                libs[str(i + 1)] = keys_lib.pop()
        do_lib = dict_lib.copy()
        for key in libs.keys():
            if libs[key] not in do_lib.keys():
                raise 'dict_lib error:%s' % str(dict_lib)
    return libs, do_lib


def len_var(ob):
        return len(f'{ob}')

def print_dict(dicts):
    """
    格式打印字典变量
    :param dicts:
    :return:
    """
    print(str_dict(dicts))

def var_name(var, dict_var=globals()):
    """
    :The function is tu return name of the variable:
    :param var:
    :param dict_var:变量空间,建议使用local().copy(),默认为全局变量globals().copy()
    :return var_name_str:
    """
    for key in dict_var:
        if dict_var[key] == var:
            return key
    dict_var = globals()
    for key in dict_var:
        if dict_var[key] == var:
            return key

def readConfig(path=''):
    """
    读取配置文件,转成字典
    """
    res = {}
    with open(os.path.join(path,'config.txt'),'r',encoding='utf8') as cf:
        for ls in cf.readlines():
            if ls[0] == '#' : continue
            key_val = ls.replace("\n",'').split(":")
            if len(key_val) == 2:
                res[key_val[0]] = key_val[1]
    return res

def rename_file(file_name, newName, path1='',path2=None):
    """
    重命名文件
    """
    print("rename", path1 + file_name, path2 + newName)

    os.rename(os.path.join(path1,file_name),os.path.join(path2 or path1,newName))

def copy_file(file_name, newName, path1='',path2=None):
    print("copy",  path1 + file_name, path2 or path1 + newName)
    import os
    import shutil
    shutil.copy(os.path.join(path1,file_name),os.path.join(path2 or path1,newName))

def str_dict(dicts, str1=''):
    """
    把字典格式的变量格式化为字符串
    :param dicts:
    :param str1:
    :param pre: 变量打印前缀,默认是None,统计item数量,
    :return:
    """
    if type(dicts) in [dict, defaultdict]:
        if len(dicts) <1: return '{}'
        pre = f'{len(dicts)} item in the {type(dicts)}:' 
        items = [pre]
        for key in dicts.keys():
            items.append(f'{key}:{str_dict(dicts[key], str1 + "  ")},')
        str_oneLine = ''.join(items)
        if len(str_oneLine) <= 120:
            return f'{{{str_oneLine}}}'
        str_item = f'\n  {str1}'.join(items)
        return f'{{{str_item}\n{str1}}}'

    # 判断是否是字符串
    elif isinstance(dicts, str):
        return dicts

    # 判断是否可以迭代
    elif isinstance(dicts, Iterable):
        if len(dicts) <1: return f'{dicts}'
        pre = f'{len(dicts)} item in the {type(dicts)}:'
        items = [pre]
        for item in dicts:
            items.append(f'{str_dict(item, str1 + "  ")},')        
        str_oneLine = ''.join(items)
        if len(str_oneLine) <= 120:
            return f'{{{str_oneLine}}}'
        str_item = f'\n  {str1}'.join(items)
        return f'[{str_item}\n{str1}]'
    else:
        return f'{dicts}'

def input_lib(tips, dict_lib):
    """
    输入一个需要选择的字典
    """
    print_msg()
    times = 1
    libs, do_lib = lib_to_do_lib(dict_lib)

    while 1:
        print(tips)
        str_len = 100 // max([len_var(ob) for ob in libs.values()]) or 1
        line_num = str_len if str_len < 5 else 5
        index_en = 1
        for key in libs.keys():
            en = ";  " if index_en % line_num != 0 else ";\n"
            index_en += 1
            if libs[key]:
                print(key, libs[key], end=en)
        a_input = input("\ntips:如果没有需要的选项,输入“add”;退出输入“q“\n请选择:")
        if a_input in libs.keys():
            return libs[a_input]
        elif a_input == "q":
            return False
        elif a_input == "add":
            if isinstance(dict_lib, list):
                print(dict_lib)
                dict_lib.append(input("输入你需要的选项:"))
                libs, do_lib = lib_to_do_lib(dict_lib)
            elif isinstance(dict_lib, dict):
                key_name = input("输入你需要的选项:")
                if '0' in dict_lib.keys():
                    if key_name not in dict_lib.values():
                        dict_lib["0"][str(len(libs) + 1)] = key_name
                dict_lib[key_name] = input("输入对应参数:")
                key_name = input("输入你需要的选项:")
                if key_name not in libs.values():
                    libs["0"][str(len(libs) + 1)] = key_name
                libs[key_name] = input("输入对应参数:")
            else:
                print_error("该选择不能添加选项")
        else:
            times += 1
            print_error()
        if times >= 5:
            print("输入错误次数过多,退出")
            return False



# from itertools import *
def print_function(function):
    """
    打印一个模块的信息
    """
    print("++++"*10)
    functions = {}
    others = []
    for i in function.__dict__:
        # functions.append(str(i)+":"+str(function.__dict__[i].__doc__))
        # functions.append(function.__dict__[i].__doc__)
        if "_" != i[0]:
            if function.__dict__[i].__doc__:
                functions[i] = function.__dict__[i].__doc__
        else:
            others.append(i)
    print("functionName:", function.__name__)
    print("function is :", function.__class__)
    print("function doc :", function.__doc__)
    try:
        print("function in the module:", function.__module__)
    except Exception as es:
        print(es)
    print("function have :", "".join("\n" + key for key in functions.keys()),"\n" , "\n*************\n".join([""] + list(j+":\n    "+functions[j] for j in functions.keys())))
    print("function have others :\n", "\n".join(others))


def print_object(ob, dict_var=globals()):
    """
    打印一个变量的信息
    dict_var: 变量空间,建议使用local(),默认为全局变量globals()
    """
    print("++++"*10)
    print(ob.__dir__())
    print("object name:", var_name(ob, dict_var=dict_var))
    print("object is :", ob.__class__)
    print("object doc :", ob.__doc__)
    print("object have :\n", ob.__dir__())
    for i in ob.__dir__():
        print(i)
        try:
            print(i,eval("ob.%s()"%i))
        except Exception as es:
            print("error class:",es.__doc__, "\nerror str:", es.__str__())


def print_module(item):
    """
    打印一个库里的函数、类、字库
    item:modle,int,str,list,dict... ect
    """
    import pkgutil
    print("module".center(100, '#'))  
    print("type:", type(item))  
    functions = []
    classes = []
    for name in dir(item):  
        if callable(getattr(item, name)):  
            functions.append(name)
        if isinstance(getattr(item, name), type):  
            classes.append(name)
    
    print("functions:".center(100, '#'))  
    print(functions)
    
    print("classes:".center(100, '#'))  
    print(classes)

    sub_packages0 = []
    sub_packages1 = []
    for importer, modname, ispkg in pkgutil.walk_packages(item.__path__):  
        if ispkg:
            sub_packages1.append(modname)
        else:
            sub_packages0.append(modname)
    print("sub-packages0:".center(100, '#'))
    print(sub_packages0)  
    print("sub-packages1:".center(100, '#'))
    print(sub_packages1)  


def print_item(item):
    """
    打印一个目标的信息
    item:modle,int,str,list,dict... ect
    """
    try:
        print(item.__str__())
        print("begin:", item.__name__)
    except Exception as es:
        print("begin:", repr(item))
        print(es.__str__())

    print("type:", type(item))
    if type(item) in (int,str,list,dict):
        print_object(item)
    else:
        try:
            for i in item:
                if type(i) == str:
                    print(i)
                else:
                    try:
                        print_item(i)
                    except Exception as es:
                        print(es.__str__())
        except Exception as es:
            print(es.__str__())
            print_function(item)



if __name__ == "__main__":
    a = {
                'theadList':['序号','月份','医院名称','阅片量','阳性量','阴性量','操作'],
                'arr':[{"hospital":"巧思医院","month":"2021-11","posicount":"19","negicount":"11","readcount":"32"},{"hospital":"远安演示","month":"2021-11","posicount":"3","negicount":"5","readcount":"10"},{"hospital":"银川麦克奥迪病理诊断中心","month":"2021-10","posicount":"629","negicount":"2824","readcount":"3648"},{"hospital":"海城市中心医院","month":"2021-10","posicount":"186","negicount":"523","readcount":"824"},{"hospital":"河南省人民医院","month":"2021-10","posicount":"140","negicount":"139","readcount":"319"},{"hospital":"张家口医疗小组","month":"2021-10","posicount":"157","negicount":"61","readcount":"224"},{"hospital":"首都医科大学附属北京友谊医院(膜式)","month":"2021-10","posicount":"65","negicount":"141","readcount":"221"},{"hospital":"深思考测试","month":"2021-10","posicount":"59","negicount":"56","readcount":"125"},{"hospital":"首都医科大学附属北京友谊医院(沉降)","month":"2021-10","posicount":"54","negicount":"25","readcount":"81"},{"hospital":"线上测试","month":"2021-10","posicount":"10","negicount":"0","readcount":"20"},{"hospital":"远安演示","month":"2021-10","posicount":"3","negicount":"11","readcount":"14"},{"hospital":"天津百利鑫","month":"2021-10","posicount":"2","negicount":"0","readcount":"7"},{"hospital":"天水市张家川县人民医院","month":"2021-10","posicount":"1","negicount":"1","readcount":"2"},{"hospital":"银川麦克奥迪病理诊断中心","month":"2021-09","posicount":"1210","negicount":"4129","readcount":"5672"},{"hospital":"海城市中心医院","month":"2021-09","posicount":"440","negicount":"766","readcount":"1298"},{"hospital":"天津百利鑫","month":"2021-09","posicount":"232","negicount":"223","readcount":"467"},{"hospital":"首都医科大学附属北京友谊医院(膜式)","month":"2021-09","posicount":"92","negicount":"274","readcount":"380"},{"hospital":"天水市张家川县人民医院","month":"2021-09","posicount":"21","negicount":"5","readcount":"26"},{"hospital":"河南省人民医院","month":"2021-09","posicount":"3","negicount":"3","readcount":"7"},{"hospital":"深思考测试","month":"2021-09","posicount":"1","negicount":"3","readcount":"4"},{"hospital":"远安演示","month":"2021-09","posicount":"2","negicount":"1","readcount":"3"},{"hospital":"线上测试","month":"2021-09","posicount":"0","negicount":"1","readcount":"2"},{"hospital":"银川麦克奥迪病理诊断中心","month":"2021-08","posicount":"796","negicount":"3699","readcount":"5029"},{"hospital":"海城市中心医院","month":"2021-08","posicount":"376","negicount":"1272","readcount":"1816"},{"hospital":"张家口医疗小组","month":"2021-08","posicount":"340","negicount":"461","readcount":"911"},{"hospital":"首都医科大学附属北京友谊医院(膜式)","month":"2021-08","posicount":"268","negicount":"302","readcount":"671"},{"hospital":"深思考测试","month":"2021-08","posicount":"179","negicount":"263","readcount":"490"},{"hospital":"友谊三类","month":"2021-08","posicount":"208","negicount":"37","readcount":"250"},{"hospital":"厦门大学附属第一医院","month":"2021-08","posicount":"18","negicount":"91","readcount":"132"},{"hospital":"远安演示","month":"2021-08","posicount":"33","negicount":"9","readcount":"44"},{"hospital":"天水市张家川县人民医院","month":"2021-08","posicount":"11","negicount":"16","readcount":"27"},{"hospital":"北京海德星","month":"2021-08","posicount":"9","negicount":"6","readcount":"23"},{"hospital":"北京海淀医院","month":"2021-08","posicount":"3","negicount":"0","readcount":"4"},{"hospital":"东北国际医院","month":"2021-08","posicount":"0","negicount":"0","readcount":"1"},{"hospital":"银川麦克奥迪病理诊断中心","month":"2021-07","posicount":"677","negicount":"3489","readcount":"4513"},{"hospital":"海城市中心医院","month":"2021-07","posicount":"243","negicount":"952","readcount":"1355"},{"hospital":"首都医科大学附属北京友谊医院(膜式)","month":"2021-07","posicount":"197","negicount":"468","readcount":"685"},{"hospital":"天津百利鑫","month":"2021-07","posicount":"429","negicount":"18","readcount":"451"},{"hospital":"张家口医疗小组","month":"2021-07","posicount":"154","negicount":"234","readcount":"439"},{"hospital":"厦门大学附属第一医院","month":"2021-07","posicount":"40","negicount":"133","readcount":"222"},{"hospital":"河南省人民医院","month":"2021-07","posicount":"67","negicount":"147","readcount":"217"},{"hospital":"海世嘉生强","month":"2021-07","posicount":"80","negicount":"131","readcount":"212"},{"hospital":"深思考测试","month":"2021-07","posicount":"108","negicount":"42","readcount":"156"},{"hospital":"长春市妇产医院","month":"2021-07","posicount":"95","negicount":"9","readcount":"109"},{"hospital":"浙二医院","month":"2021-07","posicount":"29","negicount":"17","readcount":"46"},{"hospital":"天水市张家川县人民医院","month":"2021-07","posicount":"23","negicount":"9","readcount":"33"},{"hospital":"远安演示","month":"2021-07","posicount":"19","negicount":"4","readcount":"24"},{"hospital":"湖北民族大学附属民大医院","month":"2021-07","posicount":"7","negicount":"4","readcount":"12"},{"hospital":"襄阳市中心医院","month":"2021-07","posicount":"5","negicount":"5","readcount":"10"},{"hospital":"东北国际医院","month":"2021-07","posicount":"6","negicount":"0","readcount":"9"}],
                'sourceData':[{"hospital":"巧思医院","month":"2021-11","posicount":"19","negicount":"11","readcount":"32"},{"hospital":"远安演示","month":"2021-11","posicount":"3","negicount":"5","readcount":"10"},{"hospital":"银川麦克奥迪病理诊断中心","month":"2021-10","posicount":"629","negicount":"2824","readcount":"3648"},{"hospital":"海城市中心医院","month":"2021-10","posicount":"186","negicount":"523","readcount":"824"},{"hospital":"河南省人民医院","month":"2021-10","posicount":"140","negicount":"139","readcount":"319"},{"hospital":"张家口医疗小组","month":"2021-10","posicount":"157","negicount":"61","readcount":"224"},{"hospital":"首都医科大学附属北京友谊医院(膜式)","month":"2021-10","posicount":"65","negicount":"141","readcount":"221"},{"hospital":"深思考测试","month":"2021-10","posicount":"59","negicount":"56","readcount":"125"},{"hospital":"首都医科大学附属北京友谊医院(沉降)","month":"2021-10","posicount":"54","negicount":"25","readcount":"81"},{"hospital":"线上测试","month":"2021-10","posicount":"10","negicount":"0","readcount":"20"},{"hospital":"远安演示","month":"2021-10","posicount":"3","negicount":"11","readcount":"14"},{"hospital":"天津百利鑫","month":"2021-10","posicount":"2","negicount":"0","readcount":"7"},{"hospital":"天水市张家川县人民医院","month":"2021-10","posicount":"1","negicount":"1","readcount":"2"},{"hospital":"银川麦克奥迪病理诊断中心","month":"2021-09","posicount":"1210","negicount":"4129","readcount":"5672"},{"hospital":"海城市中心医院","month":"2021-09","posicount":"440","negicount":"766","readcount":"1298"},{"hospital":"天津百利鑫","month":"2021-09","posicount":"232","negicount":"223","readcount":"467"},{"hospital":"首都医科大学附属北京友谊医院(膜式)","month":"2021-09","posicount":"92","negicount":"274","readcount":"380"},{"hospital":"天水市张家川县人民医院","month":"2021-09","posicount":"21","negicount":"5","readcount":"26"},{"hospital":"河南省人民医院","month":"2021-09","posicount":"3","negicount":"3","readcount":"7"},{"hospital":"深思考测试","month":"2021-09","posicount":"1","negicount":"3","readcount":"4"},{"hospital":"远安演示","month":"2021-09","posicount":"2","negicount":"1","readcount":"3"},{"hospital":"线上测试","month":"2021-09","posicount":"0","negicount":"1","readcount":"2"},{"hospital":"银川麦克奥迪病理诊断中心","month":"2021-08","posicount":"796","negicount":"3699","readcount":"5029"},{"hospital":"海城市中心医院","month":"2021-08","posicount":"376","negicount":"1272","readcount":"1816"},{"hospital":"张家口医疗小组","month":"2021-08","posicount":"340","negicount":"461","readcount":"911"},{"hospital":"首都医科大学附属北京友谊医院(膜式)","month":"2021-08","posicount":"268","negicount":"302","readcount":"671"},{"hospital":"深思考测试","month":"2021-08","posicount":"179","negicount":"263","readcount":"490"},{"hospital":"友谊三类","month":"2021-08","posicount":"208","negicount":"37","readcount":"250"},{"hospital":"厦门大学附属第一医院","month":"2021-08","posicount":"18","negicount":"91","readcount":"132"},{"hospital":"远安演示","month":"2021-08","posicount":"33","negicount":"9","readcount":"44"},{"hospital":"天水市张家川县人民医院","month":"2021-08","posicount":"11","negicount":"16","readcount":"27"},{"hospital":"北京海德星","month":"2021-08","posicount":"9","negicount":"6","readcount":"23"},{"hospital":"北京海淀医院","month":"2021-08","posicount":"3","negicount":"0","readcount":"4"},{"hospital":"东北国际医院","month":"2021-08","posicount":"0","negicount":"0","readcount":"1"},{"hospital":"银川麦克奥迪病理诊断中心","month":"2021-07","posicount":"677","negicount":"3489","readcount":"4513"},{"hospital":"海城市中心医院","month":"2021-07","posicount":"243","negicount":"952","readcount":"1355"},{"hospital":"首都医科大学附属北京友谊医院(膜式)","month":"2021-07","posicount":"197","negicount":"468","readcount":"685"},{"hospital":"天津百利鑫","month":"2021-07","posicount":"429","negicount":"18","readcount":"451"},{"hospital":"张家口医疗小组","month":"2021-07","posicount":"154","negicount":"234","readcount":"439"},{"hospital":"厦门大学附属第一医院","month":"2021-07","posicount":"40","negicount":"133","readcount":"222"},{"hospital":"河南省人民医院","month":"2021-07","posicount":"67","negicount":"147","readcount":"217"},{"hospital":"海世嘉生强","month":"2021-07","posicount":"80","negicount":"131","readcount":"212"},{"hospital":"深思考测试","month":"2021-07","posicount":"108","negicount":"42","readcount":"156"},{"hospital":"长春市妇产医院","month":"2021-07","posicount":"95","negicount":"9","readcount":"109"},{"hospital":"浙二医院","month":"2021-07","posicount":"29","negicount":"17","readcount":"46"},{"hospital":"天水市张家川县人民医院","month":"2021-07","posicount":"23","negicount":"9","readcount":"33"},{"hospital":"远安演示","month":"2021-07","posicount":"19","negicount":"4","readcount":"24"},{"hospital":"湖北民族大学附属民大医院","month":"2021-07","posicount":"7","negicount":"4","readcount":"12"},{"hospital":"襄阳市中心医院","month":"2021-07","posicount":"5","negicount":"5","readcount":"10"},{"hospital":"东北国际医院","month":"2021-07","posicount":"6","negicount":"0","readcount":"9"}],
                'filterList':[],
                'count':339,
                'searchVal':'',
                'searchMonth':'',
            }
    file = r"D:\BaiduNetdiskDownload\selenium_scmItools\scmItools2.txt"
    txt = open(file, 'r').readlines()
    print_dict(eval(txt[0]))
    print_dict(a)
