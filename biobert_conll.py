import argparse
import os
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--cadec', '-cadec', type=str, default='data/rus_folds')
parser.add_argument('--psytar', '-psytar', type=str, default=None)
parser.add_argument('--cadecIOB', '-cadecIOB', type=str, default='data/rus_folds_biobert')
parser.add_argument('--psytarIOB', '-psytarIOB', type=str, default='data/psytar_folds_biobert')


args = parser.parse_args()

cadec_folds = args.cadec
psytar_folds = args.psytar
cadec_folds_IOB = args.cadecIOB
psytar_folds_IOB = args.psytarIOB


def to_IOB_format(filename, out_file):
    f = open(filename, 'r')
    f1 = open(out_file, 'a+')
    for line in f.readlines():
        tokens = line.split("\t")
        if line == '\n':
            f1.write('\n')
            continue
        if len(tokens) < 3:
            print(line)
            continue
        if tokens[3] == '0':
            tokens[3] = 'O'
        f1.write(u'{}\t{}\n'.format(tokens[0], tokens[3][0]))
    f.close()
    f1.close()


if not os.path.exists(cadec_folds_IOB):
    os.mkdir(cadec_folds_IOB)
if not os.path.exists(psytar_folds_IOB):
    os.mkdir(psytar_folds_IOB)
for directory in os.listdir(cadec_folds):
    fold_path_cadec = os.path.join(cadec_folds, directory)
    fold_path_cadec_IOB = os.path.join(cadec_folds_IOB,directory)
    if not os.path.exists(fold_path_cadec_IOB):
        os.mkdir(fold_path_cadec_IOB)
    train_cadec = os.path.join(fold_path_cadec, "train.conll")
    train_cadec_IOB = os.path.join(fold_path_cadec_IOB, "train.tsv")
    to_IOB_format(train_cadec, train_cadec_IOB)
    shutil.copyfile(train_cadec_IOB, os.path.join(fold_path_cadec_IOB, "train_dev.tsv"))
    test_cadec = os.path.join(fold_path_cadec, "test.conll")
    test_cadec_IOB = os.path.join(fold_path_cadec_IOB, "test.tsv")
    to_IOB_format(test_cadec,test_cadec_IOB)
    shutil.copyfile(test_cadec_IOB,os.path.join(fold_path_cadec_IOB, "devel.tsv"))
    if psytar_folds is not None:
        fold_path_psytar = os.path.join(psytar_folds, directory)
        fold_path_psytar_IOB = os.path.join(psytar_folds_IOB, directory)
        if not os.path.exists(fold_path_psytar_IOB):
            os.mkdir(fold_path_psytar_IOB)
        train_psytar = os.path.join(fold_path_psytar, "train.conll")
        train_psytar_IOB = os.path.join(fold_path_psytar_IOB, "train.tsv")
        to_IOB_format(train_psytar, train_psytar_IOB)
        shutil.copyfile(train_psytar_IOB,os.path.join(fold_path_psytar_IOB, "train_dev.tsv"))
        test_psytar = os.path.join(fold_path_psytar, "test.conll")
        test_psytar_IOB = os.path.join(fold_path_psytar_IOB, "test.tsv")
        to_IOB_format(test_psytar, test_psytar_IOB)
        shutil.copyfile(test_psytar_IOB, os.path.join(fold_path_psytar_IOB, "devel.tsv"))