import os
import re
from sklearn.model_selection import KFold
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--cadec', '-cadec', type=str, default="data/cadec")
parser.add_argument('--cadec_text', '-cadec_text', type=str, default="data/cadec/text")
parser.add_argument('--cadec_original', '-cadec_original;', type=str, default="data/cadec/original")
parser.add_argument('--cadec_folds', '-cadec_folds', type=str, default="data/cadec_folds")
parser.add_argument('--folds', '-folds', type=int, default=5)

args = parser.parse_args()


cadec_dir = args.cadec
text_path = args.cadec_text
original_path = args.cadec_original
folds_path = args.cadec_folds
n_folds = args.folds




def get_entity_and_slice(directory):
    result = []
    for filename in sorted(os.listdir(directory)):
        f = open(os.path.join(directory, filename))
        text = f.read().lower().split("\n")
        rev = []
        for elem in text[:-1]:
            sentence = elem.replace("\t", " ")
            words = sentence.split(" ")
            if words[0][0] == "#":
                continue
            ent = words[1:4]
            ent.append(elem.split("\t")[-1])
            rev.append(ent)
        result.append(rev)
    return result



def get_text(directory):
    result = []
    names = []
    n_s = []
    for filename in sorted(os.listdir(directory)):
        f = open(os.path.join(directory, filename))
        text = f.read()
        n_sen = text.count("\n")
        text = text.replace("\n", " ")
        text = text.lower()
        result.append(text)
        names.append(filename[:-4])
        n_s.append(n_sen)
        f.close()
    return result, names, n_s


def make_entity_dictionary(ent,len_dataset):
    result = {}
    for i in range(len_dataset):
        d = {}

        for j in range(len(ent[i])):
            if ';' in ent[i][j][1]:
                ent[i][j][1] = int(ent[i][j][1].split(";")[-1])
            if ';' in ent[i][j][2]:
                ent[i][j][2] = int(ent[i][j][2].split(";")[-1])
            d[j] = {'start': ent[i][j][1], 'end': ent[i][j][2],
                    'entity': ent[i][j][0],'text':ent[i][j][3]}
        result[i] = d
    return result


df = pd.DataFrame(columns=['filename', 'text', 'sentences', 'entities'])

text, names, n_s = get_text(text_path)
ent_slice = get_entity_and_slice(original_path)

len_dataset = len(list(os.listdir(text_path)))
entity_dict = make_entity_dictionary(ent_slice,len_dataset)
number = 0
for i in list(entity_dict):
    df = df.append({'filename':names[i], 'text': text[i], 'sentences': n_s[i], 'entities':entity_dict[i]}, ignore_index=True)

rkf = KFold(n_splits=n_folds)

n_fold = 0
if not os.path.exists(folds_path):
    os.mkdir(folds_path)
for i_train,i_test in rkf.split(df):
    os.mkdir(os.path.join(folds_path,str(n_fold // 10) + str(n_fold)))
    fold_path = os.path.join(folds_path,str(n_fold // 10) + str(n_fold))
    train = df.iloc[i_train]
    test = df.iloc[i_test]
    train.to_json(os.path.join(fold_path,"train.json"), orient='table')
    test.to_json(os.path.join(fold_path, "test.json"), orient='table')
    n_fold += 1

