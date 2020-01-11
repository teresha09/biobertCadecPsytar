import argparse
import os
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("--folder", "-folder", type=str, default="brat_files")
args = parser.parse_args()


if not os.path.exists("data/rus"):
    os.mkdir("data/rus")
if not os.path.exists("data/rus/original"):
    os.mkdir("data/rus/original")
if not os.path.exists("data/rus/text"):
    os.mkdir("data/rus/text")
for filename in os.listdir(args.folder):
    if filename[-3:] == 'txt':
        shutil.copyfile(os.path.join(args.folder, filename), os.path.join("data/rus/text", filename))
    if filename[-3:] == 'ann':
        shutil.copyfile(os.path.join(args.folder, filename), os.path.join("data/rus/original", filename))
