from androlyze import *
from nltk.util import ngrams
from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
import os
import copy
import operator
import json
import pandas as pd
import csv
import matplotlib.pyplot as plt
import traceback

def extract_permission_info(directory, jsonfile):
    '''提取apk权限信息，参数是apk文件夹路径和官方权限txt文件名，
    返回值是统计权限列表和每个apk的权限字典'''

    #读取官方权限，保存在列表per_list中
    with open("permission_list.txt") as f:
        content = f.readlines()
    per_list = [x.strip() for x in content]


    permissions_list = []
    permissions_dict = {}
    apk_name_list = []
    number = 0

    #列出路径下的所有文件名
    for i in os.listdir(directory):
        i = directory + "/" + i
        apk_name_list.append(i)

    #对每个apk进行分析
    for i in apk_name_list:
        apk_name = i.split("/")[-1]
        #print("Analyzing apk:" + apk_name)
        try:
            a = apk.APK(i)
            number += 1
            permissions = a.get_permissions()
            permissions_copy = copy.deepcopy(permissions)
            #除去自定义的权限，即非官方权限
            for permission in permissions_copy:
                if permission not in per_list:
                    while permission in permissions:
                        permissions.remove(permission)
            #除去重复的权限，即每个apk中，相同权限只计算一次，结果保存在列表permissions中
            per = []
            for permission in permissions:
                if permission not in per:
                    per.append(permission)
            permissions = per

            #将每个apk得到的权限列表累加，保存在列表permissions_list中
            permissions_list += permissions
            #讲每个apk得到的权限保存在字典permissions_dict中
            permissions_dict[apk_name] = permissions
        except:
            print("ops! Something wrong with this apk file:" + i)
            traceback.print_exc()

    #提取权限名字，去掉前缀
    pure_permissions = []
    for i in permissions_list:
        pure_permissions.append(i.split(".")[-1])

    #统计权限出现的次数，和词频统计的处理方式一样
    pure_permissions_dict = {}
    for i in pure_permissions:
        if i in pure_permissions_dict:
            pure_permissions_dict[i] += 1
        else:
            pure_permissions_dict[i] = 1

    #将权限次数统计得到的字典排序，得到一个列表
    sorted_permissions_list = sorted(pure_permissions_dict.items(), key=operator.itemgetter(1))
    sorted_permissions_list = sorted_permissions_list[::-1]

    #将结果写成json文件
    json_dict = {}
    json_dict["total_perm"] = sorted_permissions_list
    json_dict["every_apk_perm"] = permissions_dict
    with open(jsonfile, 'w') as outfile:
        json.dump(json_dict, outfile)

    #函数的返回值为排序后的统计权限列表和每个apk的权限字典
    return sorted_permissions_list, permissions_dict

def extract_write_permission():

    sorted_permissions_list_benign, permissions_dict_benign = extract_permission_info("AMD_DATA/ben_data", "ben_perm.json")
    sorted_permissions_list_malicious, permissions_dict_malicious = extract_permission_info("AMD_DATA/mal_data", "mal_perm.json")
    a = copy.deepcopy(sorted_permissions_list_benign)
    b = copy.deepcopy(sorted_permissions_list_malicious)
    c = copy.deepcopy(permissions_dict_benign)
    d = copy.deepcopy(permissions_dict_malicious)

    a_keys = []
    for i in a:
        a_keys.append(i[0])
    for i in b:
        if i[0] not in a_keys:
            a.append((i[0],0))

    key_list = []
    for i in a:
        key_list.append(i[0])

    benign_dict = {}
    mal_dict = {}
    for i in c:
        benign_dict[i] = {}
        for j in c[i]:
            benign_dict[i][j.split(".")[-1]] = 1
        for k in key_list:
            if k not in benign_dict[i]:
                benign_dict[i][k] = 0

    for i in d:
        mal_dict[i] = {}
        for j in d[i]:
            mal_dict[i][j.split(".")[-1]] = 1
        for k in key_list:
            if k not in mal_dict[i]:
                mal_dict[i][k] = 0

    with open("mal_permission.csv", 'w', newline='') as csvfile:
        fieldnames = key_list
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in mal_dict:
            writer.writerow(mal_dict[i])

    with open("ben_permission.csv", 'w', newline='') as csvfile:
        fieldnames = key_list
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in benign_dict:
            writer.writerow(benign_dict[i])

    index = 1
    index_dict = {}
    for i in a:
        index_dict[i[0]] = index
        index += 1
    a_plot =[(index_dict[i[0]],i[1]) for i in a]
    b_plot =[(index_dict[i[0]],i[1]) for i in b]

    ben_length = len(os.listdir("AMD_DATA/ben_data"))
    mal_length = len(os.listdir("AMD_DATA/mal_data"))
    ay = []
    for i in a_plot:
        ay.append(i[1]/ben_length)
    by = []
    for i in b_plot:
        by.append(i[1]/mal_length)
    plt.plot(range(1,len(a)+1),ay[:len(a)],'r--',range(1,len(by)+1),by[:len(by)],'b--')
    plt.show()