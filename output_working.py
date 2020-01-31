import argparse
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument("--data", "-data",type=str,default="data/psytar_folds/01/test.json")
parser.add_argument("--output_data", "-output_data", type=str, default="tmp/cadec_fold_01_psytar_test/NER_result_conll1.txt")
parser.add_argument("--conll", "-conll", type=str, default="data/psytar_folds/01/test.conll")
parser.add_argument("--entity", "-entity", type=str, default="ADR")
parser.add_argument("--brat_folder", "-brat_folder", type=str, default="brat_output/00")
args = parser.parse_args()
print(args)


def annotation_builder(output_string,out_file):
    words = output_string.split("\n")
    in_flag = False
    entity_counter = 0
    start = 0
    end = 0
    s1 = ""
    ann_file = open(out_file, "w+")
    for word in words:
        if word == '':
            continue
        if word.split(" ")[2] == "B-MISC":
            if in_flag:
                ann_file.write("{}{}\t{}\n".format(s, end, s1[:-1]))
                s = ""
                s1 = ""
            in_flag = True
            entity_counter += 1
            start = word.split(" ")[-2]
            s = "T{}\t{} {} ".format(entity_counter, args.entity, start)
        if word.split(" ")[2] == "O-MISC" and in_flag:
            ann_file.write("{}{}\t{}\n".format(s, end, s1[:-1]))
            in_flag = False
            s = ""
            s1 = ""
        if in_flag:
            end = word.split(" ")[-1]
            s1 += word.split(" ")[0] + " "




f = open(args.data)
js_data = json.load(f)
del js_data['schema']
js_data = js_data['data']
i = 0
token_counter = 0
output = open(args.output_data)
conll = open(args.conll)
review_string = ""
conll_list = conll.readlines()
output_list = output.readlines()
index = 0
index1 = 0
while index < len(output_list):
    if output_list[index] == '\n' and conll_list[index1] == '\n':
        index += 1
        index1 += 1
        continue
    if output_list[index] == '\n' and conll_list[index1] != '\n':
        index += 1
        continue
    if output_list[index] != '\n' and conll_list[index1] == '\n':
        index1 += 1
        continue
    if conll_list[index1] != '\n' and output_list[index] != '\n':
        token_counter += 1
        line1_list = conll_list[index1].split("\t")
        review_string += output_list[index][:-1] + " " + line1_list[4] + " " + line1_list[5] + "\n"
        index += 1
        index1 += 1
    if token_counter == js_data[i]['n_token']:
        token_counter = 0
        out_file = os.path.join(args.brat_folder, js_data[i]['filename'])
        annotation_builder(review_string,out_file)
        review_string = ""
        i += 1












