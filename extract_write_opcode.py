from nltk.util import ngrams
from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
import os
import csv
import traceback

def extract_opcode(apkfile):
    lis = []
    a = apk.APK(apkfile)
    d = dvm.DalvikVMFormat(a.get_dex())
    for current_class in d.get_classes():
        for method in current_class.get_methods():
            #print("[*]", method.get_name(),method.get_descriptor())
            byte_code = method.get_code()
            if byte_code != None:
                byte_code = byte_code.get_bc()
                idx = 0
                for i in byte_code.get_instructions():
                    #print("\t, %x" % (idx), i.get_name(), i.get_output())
                    #print(i.get_name(), i.get_output())
                    #print(i.get_name())
                    lis.append(i.get_name())
                    idx += i.get_length()

    seq_list = []
    for i in lis:
        if i.startswith("cmp"):
            seq_list.append("C")
        elif i.startswith("const"):
            seq_list.append("D")
        elif i.startswith("move"):
            seq_list.append("M")
        elif i.startswith("return"):
            seq_list.append("R")
        elif i.startswith("monitor"):
            seq_list.append("L")
        elif i.startswith("goto"):
            seq_list.append("G")
        elif i.startswith("if"):
            seq_list.append("I")
        elif i.startswith("get",1):
            seq_list.append("T")
        elif i.startswith("put",1):
            seq_list.append("P")
        elif i.startswith("invoke"):
            seq_list.append("V")
        else:
            pass

    ng = list(ngrams(seq_list,3))
    length = len(ng)

    ngrams_statistics = {}
    for ngram in ng:
        if ngram not in ngrams_statistics:
            ngrams_statistics[ngram] = 1
        else:
            ngrams_statistics[ngram] += 1
    for i in ngrams_statistics:
        ngrams_statistics[i] /= length

    ngrams_statistics_sorted = sorted(ngrams_statistics.items())

    oc_inside = ["C","D","M","R","L","G","I","T","P","V"]
    key_list_inside = [(i,j,k) for i in oc_inside for j in oc_inside for k in oc_inside]

    cmp_list = []
    for i in ngrams_statistics_sorted:
        cmp_list.append(i[0])
    for i in key_list_inside:
        if i not in cmp_list:
            ngrams_statistics_sorted.append((i,0))
    ngrams_statistics_sorted = sorted(ngrams_statistics_sorted)

    return ngrams_statistics_sorted

def write_csv(ngrams_statistics_sorted,csv_file):

    oc = ["C","D","M","R","L","G","I","T","P","V"]
    key_list = [i+j+k for i in oc for j in oc for k in oc]

    dict_a = {}
    for i in ngrams_statistics_sorted:
        dict_a[i[0][0]+i[0][1]+i[0][2]] = i[1]

    with open(csv_file, 'a', newline='') as csvfile:
        fieldnames = key_list
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(dict_a)

def extract_write_opcode():
    oc = ["C","D","M","R","L","G","I","T","P","V"]
    key_list = [i+j+k for i in oc for j in oc for k in oc]

    #建立csv文件，写入header
    with open('mal_opcode.csv', 'w', newline='') as csvfile:
        fieldnames = key_list
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    with open('ben_opcode.csv', 'w', newline='') as csvfile:
        fieldnames = key_list
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    for i in os.listdir("AMD_DATA/ben_data"):
        i = "AMD_DATA/ben_data/" + i
        try:
            a = extract_opcode(i)
            write_csv(a,"ben_opcode.csv")
        except:
            print("Oops! Something wrong with this apk file:" + i)
            traceback.print_exc()

    for i in os.listdir("AMD_DATA/mal_data"):
        i = "AMD_DATA/mal_data/" + i
        try:
            a = extract_opcode(i)
            write_csv(a,"mal_opcode.csv")
        except:
            print("Oops! Something wrong with this apk file:" + i)
            traceback.print_exc()