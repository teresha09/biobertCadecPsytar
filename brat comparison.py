import argparse
import csv
import os

parser = argparse.ArgumentParser()
parser.add_argument("--first", "-first", type=str, default="brat_output/00")
parser.add_argument("--second", "-second", type=str, default="data/cadec/original")
parser.add_argument("--text", "-text", type=str, default="data/cadec/text")
parser.add_argument("--result_dir", "-result_dir", type=str, default="data")
parser.add_argument("--entity", "-entity", type=str, default="ADR")
args = parser.parse_args()

first_folder = args.first
second_folder = args.second
result_dir = args.result_dir


def file_to_list(file1):
    l1 = []
    for line in file1:
        s = line.split(" ")
        if s[0].split("\t")[1] != 'ADR':
            continue
        start = s[1]
        for i in range(2, len(s)):
            if ';' in s[i].split("\t")[0]:
                end = s[i + 1].split("\t")[0]
            else:
                end = s[i].split("\t")[0]
                break
        line_list = [s[0].split('\t')[0], s[0].split('\t')[1], int(start), int(end), line.split("\t")[2]]
        l1.append(line_list)
    l1.sort(key = lambda x: x[1])
    return l1


def comparison(l1,l2):
    t1 = 0
    t2 = 0
    diff1 = []
    diff2 = []
    same = []
    while t1 < len(l1) and t2 < len(l2):
        if l1[t1][2] > l2[t2][2]:
            diff2.append(l2[t2])
            diff1.append('')
            same.append('')
            t2 +=1
        elif l1[t1][2] < l2[t2][2]:
            diff1.append(l1[t1])
            diff2.append('')
            same.append('')
            t1 += 1
        else:
            if (l1[t1][3] == l2[t2][3]) and l1[t1][-1] == l2[t2][-1]:
                same.append(l1[t1])
                diff1.append('')
                diff2.append('')
            else:
                diff1.append(l1[t1])
                diff2.append(l2[t2])
                same.append('')
            t1 += 1
            t2 += 1
    for i in range(t1,len(l1)):
        diff1.append(l1[i])
        diff2.append('')
        same.append('')
    for i in range(t2, len(l2)):
        diff2.append(l2[i])
        diff1.append('')
        same.append('')
    return diff1,same,diff2


def list_to_str(l):
    if len(l) == 0:
        return ','
    return '"{}\t{} {} {}\t{}",'.format(l[0], l[1], l[2], l[3], l[4].strip('\n'))


def make_csv(diff1, same, diff2,filename):
    f = open(os.path.join(args.result_dir, 'comparison.csv'), 'a+')
    i = 0
    t1 = 0
    t2 = 0
    f.write('{}\n'.format(filename))
    while t1 < len(diff1) and t2 < len(diff2):
        s1 = list_to_str(diff1[t1])
        s2 = list_to_str(diff2[t2])
        sim = list_to_str(same[t1])
        f.write('{}{}{}\n'.format(s1,sim,s2))
        t1 += 1
        t2 += 1


for filename in os.listdir(first_folder):
    f = open(os.path.join(first_folder, filename))
    f1 = open(os.path.join(second_folder, filename))
    print(filename)
    f_list = file_to_list(f)
    f1_list = file_to_list(f1)
    diff1,same,diff2 = comparison(f_list,f1_list)
    make_csv(diff1,same,diff2,filename[:-3] + 'txt')


