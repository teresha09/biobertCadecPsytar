import codecs
import json
import os

from nltk.tokenize import wordpunct_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import wordnet
from nltk import pos_tag
import argparse

import tokenization

parser = argparse.ArgumentParser()
parser.add_argument('--cadec', '-cadec', type=str, default='data/cadec_folds')
parser.add_argument('--psytar', '-psytar', type=str, default=None)
parser.add_argument('--entity', '-entity', type=str, default='adr drug')
parser.add_argument('--tagger', '-tagger', type=str, default='averaged_perceptron_tagger')
parser.add_argument('--vocab_file', '-vocab_file', type=str, default='BIOBERT_DIR/vocab.txt')
parser.add_argument('--do_lower_case', '-do_lower_case', type=bool, default=True)

args = parser.parse_args()
nltk.download(args.tagger)
nltk.download('wordnet')
cadec_folds = args.cadec
psytar_folds = args.psytar
entity_type = args.entity


lemmatizer = WordNetLemmatizer()


def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def get_token_position_in_text(token, w_start, text):
    delimitter_start = None
    text = text.replace('й','и')
    text = text.replace("ё","е")
    while text[w_start:w_start+len(token)] != token or (delimitter_start == None and w_start != 0):
        w_start += 1
        delimitter_start = delimitter_start or w_start
    return w_start, w_start + len(token), text[delimitter_start:w_start]


def get_bio_tag(w_start, w_end, entities, entity_type):
    for key, entity in entities.items():
        try:
            start = int(entity['start'])
            end = int(entity['end'])
        except Exception:
            raise Exception("Entity start and end must be an integer")

        if entity['entity'] in entity_type:
            if w_start > start and w_end <= end:
                adding = entity['entity']
                return 'I-' + adding
            elif w_start == start and w_end <= end:
                adding = entity['entity']
                return 'B-' + adding
    return '0'





def json_to_conll(corpus_json_location, output_location, entity_type, by_sent = False):
    tokenizer = tokenization.FullTokenizer(
        vocab_file=args.vocab_file, do_lower_case=args.do_lower_case)
    with codecs.open(corpus_json_location, encoding='utf-8') as in_file:
        reviews = list(map(json.loads, in_file.readlines()))
        reviews = reviews[0]['data']
        f = open(corpus_json_location)
        js_data = json.load(f)
        i = 0
    with codecs.open(output_location, 'w', encoding='utf-8') as out_file:
        for review in reviews:
            documents = sent_tokenize(review['text']) if by_sent else [review['text']]
            w_start = 0
            w_end = 0
            tokens_counter = 0
            for document in documents:
                tokens = tokenization.make_token_list(document.split(' '),tokenizer)
                if args.tagger == "averaged_perceptron_tagger_ru":
                    pos_tags = pos_tag(tokens, lang='rus')
                else:
                    pos_tags = pos_tag(tokens)
                tokens_counter += len(tokens)
                for token, temp in zip(tokens, pos_tags):
                    token_corr = temp[0].lower()
                    pos = temp[1]
                    w_start, w_end, delimitter = get_token_position_in_text(token, w_start, review['text'].lower())
                    bio_tag = get_bio_tag(w_start, w_end, review['entities'], entity_type)
                    lemm = lemmatizer.lemmatize(token_corr, get_wordnet_pos(pos))
                    if '.' in lemm or '!' in lemm or '?' in lemm:
                        eol = "\n\n"
                    else:
                        eol = "\n"
                    out_file.write(u'{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}{}'.format(token, lemm, pos, bio_tag, w_start, w_end, delimitter, review['index'], eol))
                    w_start = w_end - 1
            js_data['data'][i]['n_token'] = tokens_counter
            i += 1
    os.remove(corpus_json_location)
    new_f = open(corpus_json_location, "w+")
    json.dump(js_data, new_f)


for directory in os.listdir(cadec_folds):
    fold_path_cadec = os.path.join(cadec_folds, directory)
    train_cadec = os.path.join(fold_path_cadec, "train.json")
    json_to_conll(train_cadec,os.path.join(fold_path_cadec, "train.conll"), entity_type)
    test_cadec = os.path.join(fold_path_cadec, "test.json")
    json_to_conll(test_cadec, os.path.join(fold_path_cadec, "test.conll"), entity_type)
    if args.psytar is not None:
        fold_path_psytar = os.path.join(psytar_folds, directory)
        train_psytar = os.path.join(fold_path_psytar, "train.json")
        json_to_conll(train_psytar, os.path.join(fold_path_psytar, "train.conll"), entity_type)
        test_psytar = os.path.join(fold_path_psytar, "test.json")
        json_to_conll(test_psytar, os.path.join(fold_path_psytar, "test.conll"), entity_type)

