import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-directory", "--directory", type=str, default="tmp")
args = parser.parse_args()

dirs = args.directory
temp_file = open(os.path.join("data", "temporary.csv"), "a+")
temp_file.write("corpus,file,entity,number tokens,number_entities,prediction psytar,prediction cadec\n")
for dir in os.listdir(dirs):
    brat_folder = os.path.join(os.path.join(dirs,dir), "brat_output")
    if not os.path.isdir(dir):
        continue
    corpus = dir.split("_")[3]
    flag_pred = True if dir.split("_")[0] == "cadec" else False
    for file in os.listdir(brat_folder):
        review = open(os.path.join(brat_folder,file), "r")
        for line in review:
            entity = line[line.find("\t")+1:line.find(" ")]
            n_toks = len(line.split("\t")[-1].split(" "))
            temp_file.write("{},{},{},{},n_ent,{},{}\n".format(corpus, file, entity, n_toks, not flag_pred, flag_pred))

temp_file.close()
ent_dict = {}
temp_file = open(os.path.join("data", "temporary.csv"), "r")
temp_file.readline()
for line in temp_file:
    ent = line.split(",")[2]
    if ent in ent_dict:
        ent_dict[ent] +=1
    else:
        ent_dict[ent] = 1
temp_file.seek(0)
out_file = open(os.path.join(dirs, "agg.csv"), "a+")
out_file.write(temp_file.readline())
for line in temp_file:
    s = line.replace("n_ent", str(ent_dict[line.split(",")[2]]))
    out_file.write(s)


