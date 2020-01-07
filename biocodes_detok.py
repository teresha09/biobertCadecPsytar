from argparse import ArgumentParser


if __name__ == '__main__':
  parser = ArgumentParser()
  parser.add_argument('--tokens')
  parser.add_argument('--labels')
  parser.add_argument('--save_to')
  args = parser.parse_args()
  tokens = []
  labels = []
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
    for tkns, lbls in zip(tokens, labels):
      for token, label in zip(tkns, lbls):
        output_stream.write('{} {}-MISC {}-MISC\n'.format(token, label, label))
      output_stream.write('\n')
