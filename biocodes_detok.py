from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--golden_path')
    parser.add_argument('--tokens')
    parser.add_argument('--labels')
    parser.add_argument('--save_to')
    args = parser.parse_args()
    tokens = []
    labels = []

    ans = dict()
    ans['toks'] = list()
    ans['labels'] = list()
    lineNoCount = 0
    with open(args.golden_path, 'r') as in_:
        for line in in_:
            line = line.strip()
            if line == '':
                ans['toks'].append('[SEP]')
                ans['labels'].append('O')
                lineNoCount += 1
                continue
            tmp = line.split()
            ans['toks'].append(tmp[0])
            ans['labels'].append(tmp[1])

    with open(args.tokens, encoding='utf-8') as tokens_input_stream, \
            open(args.labels, encoding='utf-8') as labels_input_stream:
        t_ = []
        l_ = []
        for token, label in zip(tokens_input_stream, labels_input_stream):
            token = token.strip()
            label = label.strip()
            if token == '[CLS]': continue
            if token == '[SEP]':
                tokens.append(t_)
                labels.append(l_)
                t_ = []
                l_ = []
                continue
            if token[:2] == '##':
                t_[-1] += token[2:]
                continue
            t_.append(token)
            l_.append(label)
    if len(t_) != 0:
        tokens.append(t_)
        labels.append(l_)
    with open(args.save_to, 'w', encoding='utf-8') as output_stream:
        c1 = 0
        for tkns, lbls in zip(tokens, labels):
            for token, label in zip(tkns, lbls):
                output_stream.write('{} {}-MISC {}-MISC\n'.format(token, ans['labels'][c1], label))
                c1 += 1
            if ans['toks'][c1] == '[SEP]':
                c1 += 1
            output_stream.write('\n')

