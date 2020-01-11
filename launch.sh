#!/bin/bash
TMP_DIR=$1
python3 folds_cadec.py -cadec data/cadec -cadec_text data/cadec/text -cadec_original data/cadec/original -cadec_folds data/cadec_folds -folds 5

python3 folds_psytar.py -psytar data/psytar_folds -psytar_text data/Copy_of_PsyTAR_dataset.csv -psytar_adr data/Copy_of_PsyTAR_dataset_adr.csv -psytar_disease data/Copy_of_PsyTAR_dataset_disease.csv -psytar_symptoms data/Copy_of_PsyTAR_dataset_symptoms.csv -folds 5

python3 json2conll.py -cadec data/cadec_folds -psytar data/psytar_folds -entity adr -tagger taggers/maxent_treebank_pos_tagger/english.pickle

python3 statistic.py -cadec data/cadec_folds -psytar data/psytar_folds -stat data/stat.txt

python3 biobert_conll.py -cadec data/cadec_folds -psytar data/psytar_folds -cadecIOB data/cadec_folds_biobert -psytarIOB data/psytar_folds_biobert


cadecarr=()
psytararr=()
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
for directory1 in ${SCRIPTPATH}/data/psytar_folds_biobert/*
do
for fold1 in $directory1
do
echo $fold1
psytararr+=("$fold1")
done
done
mkdir $TMP_DIR
for (( i=0; i < "${#cadecarr[@]}"; i++ ))
do
mkdir "${TMP_DIR}/cadec_fold_0${i}_cadec_test"
outputdir=${TMP_DIR}/cadec_fold_0${i}_cadec_test
python3 run_ner.py --do_train=true --do_eval=true --vocab_file=${SCRIPTPATH}/BIOBERT_DIR/vocab.txt \
    --bert_config_file=${SCRIPTPATH}/BIOBERT_DIR/bert_config.json \
    --init_checkpoint=${SCRIPTPATH}/BIOBERT_DIR/biobert_model.ckpt \
    --num_train_epochs=50.0 \
    --data_dir="${cadecarr[$i]}" \
    --output_dir=$outputdir
cp ${TMP_DIR}/cadec_fold_0${i}_cadec_test -R /${TMP_DIR}/cadec_fold_0${i}_psytar_test
outputdir1=/${TMP_DIR}/cadec_fold_0${i}_psytar_test
python3 run_ner.py --do_train=false --do_predict=true --do_eval=true --vocab_file=${SCRIPTPATH}/BIOBERT_DIR/vocab.txt \
    --bert_config_file=${SCRIPTPATH}/BIOBERT_DIR/bert_config.json \
    --init_checkpoint=${SCRIPTPATH}/BIOBERT_DIR/biobert_model.ckpt \
    --num_train_epochs=50.0 \
    --data_dir="${cadecarr[$i]}" \
    --output_dir=$outputdir
python3 run_ner.py --do_train=false --do_predict=true --do_eval=true --vocab_file=${SCRIPTPATH}/BIOBERT_DIR/vocab.txt \
    --bert_config_file=${SCRIPTPATH}/BIOBERT_DIR/bert_config.json \
    --init_checkpoint=${SCRIPTPATH}/BIOBERT_DIR/biobert_model.ckpt \
    --num_train_epochs=50.0 \
    --data_dir="${psytararr[$i]}" \
    --output_dir=$outputdir1
python3 biocodes_detok.py \
--tokens=${outputdir}/token_test.txt \
--labels=${outputdir}/label_test.txt \
--save_to=${outputdir}/NER_result_conll.txt
perl ${SCRIPTPATH}/biocodes/conlleval.pl < ${outputdir}/NER_result_conll.txt
mkdir ${TMP_DIR}/cadec_fold_0${i}_cadec_test/brat_output
python3 output_working.py -data ${cadecarr[$i]}/test.json \
-output_data ${outputdir}/NER_result_conll.txt \
-conll ${cadecarr[$i]}/test.conll \
-entity "ADR" \
-brat_folder ${TMP_DIR}/cadec_fold_0${i}_cadec_test/brat_output
python3 biocodes_detok.py \
--tokens=${outputdir1}/token_test.txt \
--labels=${outputdir1}/label_test.txt \
--save_to=${outputdir1}/NER_result_conll.txt
perl ${SCRIPTPATH}/biocodes/conlleval.pl < ${outputdir1}/NER_result_conll.txt
mkdir ${TMP_DIR}/cadec_fold_0${i}_psytar_test/brat_output
python3 output_working.py -data ${psytararr[$i]}/test.json \
-output_data ${outputdir1}/NER_result_conll.txt \
-conll ${psytararr[$i]}/test.conll \
-entity "ADR" \
-brat_folder ${TMP_DIR}/cadec_fold_0${i}_psytar_test/brat_output
done
for (( i=0; i < "${#psytararr[@]}"; i++ ))
do
mkdir "${TMP_DIR}/psytar_fold_0${i}_cadec_test"
outputdir=${TMP_DIR}/psytar_fold_0${i}_cadec_test
python3 run_ner.py --do_train=true --do_eval=true --vocab_file=${SCRIPTPATH}/BIOBERT_DIR/vocab.txt \
    --bert_config_file=${SCRIPTPATH}/BIOBERT_DIR/bert_config.json \
    --init_checkpoint=${SCRIPTPATH}/BIOBERT_DIR/biobert_model.ckpt \
    --num_train_epochs=50.0 \
    --data_dir="${psytararr[$i]}" \
    --output_dir=$outputdir
cp ${TMP_DIR}/psytar_fold_0${i}_cadec_test -R ${TMP_DIR}/psytar_fold_0${i}_psytar_test
outputdir1=${TMP_DIR}/psytar_fold_0${i}_psytar_test
python3 run_ner.py --do_train=false --do_predict=true --do_eval=true --vocab_file=${SCRIPTPATH}/BIOBERT_DIR/vocab.txt \
    --bert_config_file=${SCRIPTPATH}/BIOBERT_DIR/bert_config.json \
    --init_checkpoint=${SCRIPTPATH}/BIOBERT_DIR/biobert_model.ckpt \
    --num_train_epochs=50.0 \
    --data_dir="${cadecarr[$i]}" \
    --output_dir=$outputdir
python3 run_ner.py --do_train=false --do_predict=true --do_eval=true --vocab_file=${SCRIPTPATH}/BIOBERT_DIR/vocab.txt \
    --bert_config_file=${SCRIPTPATH}/BIOBERT_DIR/bert_config.json \
    --init_checkpoint=${SCRIPTPATH}/BIOBERT_DIR/biobert_model.ckpt \
    --num_train_epochs=50.0 \
    --data_dir="${psytararr[$i]}" \
    --output_dir=$outputdir1
python3 biocodes_detok.py \
--tokens=${outputdir}/token_test.txt \
--labels=${outputdir}/label_test.txt \
--save_to=${outputdir}/NER_result_conll.txt
perl ${SCRIPTPATH}/biocodes/conlleval.pl < ${outputdir}/NER_result_conll.txt
mkdir ${TMP_DIR}/psytar_fold_0${i}_cadec_test/brat_output
python3 output_working.py -data ${cadecarr[$i]}/test.json \
-output_data ${outputdir}/NER_result_conll.txt \
-conll ${cadecarr[$i]}/test.conll \
-entity "ADR" \
-brat_folder ${TMP_DIR}/cadec_fold_0${i}_cadec_test/brat_output
python3 biocodes_detok.py \
--tokens=${outputdir1}/token_test.txt \
--labels=${outputdir1}/label_test.txt \
--save_to=${outputdir1}/NER_result_conll.txt
perl ${SCRIPTPATH}/biocodes/conlleval.pl < ${outputdir1}/NER_result_conll.txt
mkdir ${TMP_DIR}/psytar_fold_0${i}_psytar_test/brat_output
python3 output_working.py -data ${psytararr[$i]}/test.json \
-output_data ${outputdir1}/NER_result_conll.txt \
-conll ${psytararr[$i]}/test.conll \
-entity "ADR" \
-brat_folder ${TMP_DIR}/cadec_fold_0${i}_psytar_test/brat_output
done


