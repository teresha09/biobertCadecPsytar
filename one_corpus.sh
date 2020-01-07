#!/bin/bash

python3 folds_cadec.py -cadec data/cadec -cadec_text data/cadec/text -cadec_original data/cadec/original -cadec_folds data/cadec_folds -folds 5

python3 json2conll.py -cadec data/cadec_folds -psytar "None" -entity adr -tagger taggers/maxent_treebank_pos_tagger/english.pickle

python3 biobert_conll.py -cadec data/cadec_folds -psytar "None" -cadecIOB data/cadec_folds_biobert -psytarIOB "None"

cadecarr=()
SCRIPTPATH=$( cd "$(dirname "$0")" ; pwd -P )
IFS=$'\n'
for directory in ${SCRIPTPATH}/data/cadec_folds_biobert/*
do
for fold in $directory
do
echo $fold
cadecarr+=("$fold")
done
done
mkdir "/tmp/bioner/"
for (( i=0; i < "${#cadecarr[@]}"; i++ ))
do
mkdir "/tmp/bioner/"
mkdir "/tmp/bioner/cadec_fold_0${i}_cadec_test"
outputdir=/tmp/bioner/cadec_fold_0${i}_cadec_test
python3 run_ner.py --do_train=true --do_eval=true --vocab_file=${SCRIPTPATH}/BIOBERT_DIR/vocab.txt \
    --bert_config_file=${SCRIPTPATH}/BIOBERT_DIR/bert_config.json \
    --init_checkpoint=${SCRIPTPATH}/BIOBERT_DIR/biobert_model.ckpt \
    --num_train_epochs=10.0 \
    --data_dir="${cadecarr[$i]}" \
    --output_dir=$outputdir
cp /tmp/bioner/cadec_fold_0${i}_cadec_test -R /tmp/bioner/cadec_fold_0${i}_psytar_test
outputdir1=/tmp/bioner/cadec_fold_0${i}_psytar_test
python3 run_ner.py --do_train=false --do_predict=true --do_eval=true --vocab_file=${SCRIPTPATH}/BIOBERT_DIR/vocab.txt \
    --bert_config_file=${SCRIPTPATH}/BIOBERT_DIR/bert_config.json \
    --init_checkpoint=${SCRIPTPATH}/BIOBERT_DIR/biobert_model.ckpt \
    --num_train_epochs=10.0 \
    --data_dir="${cadecarr[$i]}" \
    --output_dir=$outputdir
python3 biocodes_detok.py \
--tokens=${outputdir}/token_test.txt \
--labels=${outputdir}/label_test.txt \
--save_to=${outputdir}/NER_result_conll.txt
perl ${SCRIPTPATH}/biocodes/conlleval.pl < ${outputdir}/NER_result_conll.txt
mkdir /tmp/bioner/cadec_fold_0${i}_cadec_test/brat_output
python3 output_working.py -data ${cadecarr[$i]}/test.json \
-output_data ${outputdir}/NER_result_conll.txt \
-conll ${cadecarr[$i]}/test.conll \
-entity "ADR" \
-brat_folder /tmp/bioner/cadec_fold_0${i}_cadec_test/brat_output
done



