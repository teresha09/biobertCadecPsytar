import csv
import os
import argparse
from brat_comparison_v2 import comparison
import json

parser = argparse.ArgumentParser()
parser.add_argument("-directory", "--directory", type=str, default="tmp")
parser.add_argument("-data", "--data", type=str, default="data")
parser.add_argument("-entity", "--entity", type=str, default="adr")
args = parser.parse_args()

dirs = args.directory
temp_file = open(os.path.join("data", "temporary.csv"), "w")
writer = csv.writer(temp_file)
l = [["corpus","file","entity","number tokens","number_entities","prediction psytar","prediction cadec","correct psytar","correct cadec"]]
n_ent = "n_ent"
for dir in os.listdir(dirs):
    if dir.split("_")[0] == "psytar" or not os.path.isdir(os.path.join(dirs, dir)):
        continue
    brat_folder = os.path.join(os.path.join(dirs, dir), "brat_output")
    l_dir = dir.split("_")
    l_dir[0] = "psytar"
    new_dir = '_'.join(l_dir)
    brat_folder1 = os.path.join(os.path.join(dirs, new_dir), "brat_output")
    corpus = dir.split("_")[3]
    json_file = open(
        os.path.join(os.path.join(os.path.join(args.data, "{}_folds".format(corpus)), dir.split("_")[2]), "test.json"),
        "r")
    original = json.load(json_file)
    del original['schema']
    for i in original['data']:
        filename = i['filename']
        for j in i['entities']:
            if i['entities'][j]['entity'] != args.entity:
                continue
            entity_text = i['entities'][j]['text']
            n_toks = len(entity_text)
            pred_psytar = comparison(i['entities'][j]['start'], i['entities'][j]['start'],
                                     os.path.join(brat_folder1, filename)).replace("\n", '')
            pred_cadec = comparison(i['entities'][j]['start'], i['entities'][j]['start'],
                                    os.path.join(brat_folder1, filename)).replace("\n", '')
            flag_psytar = True if pred_psytar == entity_text else False
            flag_cadec = True if pred_cadec == entity_text else False
            l.append([corpus, filename, entity_text, n_toks, n_ent, pred_psytar, pred_cadec,flag_psytar, flag_cadec])
writer.writerows(l)
temp_file.close()
ent_dict = {}
temp_file = open(os.path.join("data", "temporary.csv"), "r")
temp_file.readline()
reader = csv.reader(temp_file)
for line in reader:
    ent = line[2]
    if ent in ent_dict:
        ent_dict[ent] +=1
    else:
        ent_dict[ent] = 1
temp_file.close()
temp_file = open(os.path.join("data", "temporary.csv"), "r")
out_file = open(os.path.join(dirs, "agg.csv"), "a+")
writer = csv.writer(out_file)
reader = csv.reader(temp_file)
writer.writerow(next(reader))
for line in reader:
    line[4] = str(ent_dict[line[2]])
    writer.writerow(line)

