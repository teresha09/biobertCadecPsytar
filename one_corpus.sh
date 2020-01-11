#!/bin/bash
TMP_DIR=$1
python3 folder_spliter.py -folder data/brat_files

python3 folds_rus.py -cadec data/rus -cadec_text data/rus/text -cadec_original data/rus/original -cadec_folds data/rus_folds -folds 5

python3 json2conll.py -cadec data/rus_folds -entity adr

python3 biobert_conll.py -cadec data/rus_folds -cadecIOB data/rus_folds_biobert

cadecarr=()
SCRIPTPATH=$( cd "$(dirname "$0")" ; pwd -P )
IFS=$'\n'
for directory in ${SCRIPTPATH}/data/rus_folds_biobert/*
do
for fold in $directory
do
echo $fold
cadecarr+=("$fold")
done
done
mkdir "${TMP_DIR}"
for (( i=0; i < "${#cadecarr[@]}"; i++ ))
do
mkdir "${TMP_DIR}/rus_fold_0${i}_rus_test"
outputdir=${TMP_DIR}/rus_fold_0${i}_rus_test
python3 run_ner.py --do_train=true --do_eval=true --vocab_file=${SCRIPTPATH}/BIOBERT_DIR/vocab.txt \
    --bert_config_file=${SCRIPTPATH}/BIOBERT_DIR/bert_config.json \
    --init_checkpoint=${SCRIPTPATH}/BIOBERT_DIR/biobert_model.ckpt \
    --num_train_epochs=10.0 \
    --data_dir="${cadecarr[$i]}" \
    --output_dir=$outputdir
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
mkdir ${TMP_DIR}/rus_fold_0${i}_rus_test/brat_output
python3 output_working.py -data ${cadecarr[$i]}/test.json \
-output_data ${outputdir}/NER_result_conll.txt \
-conll ${cadecarr[$i]}/test.conll \
-entity "ADR" \
-brat_folder ${TMP_DIR}/rus_fold_0${i}_rus_test/brat_output
done



