#!/usr/bin/python3
# Copyright (C) 2019 M. Zhou <lumin@debian.org>
# License: MIT/Expat
from typing import *
import argparse, re, os, sys, json, glob, pickle, math
from collections import Counter, defaultdict
# NOTE: we don't use non-standard python libraries so pypy (JIT) can run


'''latex
\section{Informal Problem/Solution Formulation}

Given a sequence of tokens $t = [t_1, t_2, \ldots, t_M]$ whose license type
is unknown. We want to identify the license type $c$ from this sequence.
We solve this problem with k-NN ($k=1$) based on $n$-gram bag-of-words text
representations. Specifically, we use unigram, bigram and trigram.

Training: Given a set of $N$ known licenses $D=\{(C_i,T_i)\}_N, 1<=i<=N$
where $C_i$ is the unique name of the license, and $t$ is the token sequence
$ T_i = [t_1, t_2, \ldots, t_M] $. We train a k-NN (k=1) with the 1- and
2-gram bag-of-words representations from dataset $D$.

Predict: Given an unseen token sequence $T_x = [t_1, t_2, \ldots, t_M]$
where unseen tokens were already filtered out, we classify the sequence
$T_x$ by the similarity score $S$. Specifically, we denote the vector
representations of two sequences to be compared with $v_i$ and $v_j$,
then the similarity score $S$ is defined as:
$$ S = 0.5*cos(v_{i,1gram}, v_{j,1gram}) + 0.5*cos(v_{i,2gram}, v_{j,2gram}) $$
The score $S$ will fall in the range $[0,1]$. And the higher the score is,
the more similar the two sequences are.
'''


class Model(object):
    '''
    Model that leverages Bag-of-Words Representation
    '''
    def __init__(self):
        self.vocab_1gram = Counter()
        self.vocab_2gram = Counter()
        self.vocab_3gram = Counter()
        self.vectors_1gram = dict()
        self.vectors_2gram = dict()
        self.vectors_3gram = dict()

    def cosSim(self, vecA: Counter, vecB: Counter) -> float:
        '''
        cosine similarity
        '''
        keys = set(vecA.keys()).union(set(vecB.keys()))
        denomA = math.sqrt(sum(x**2 for x in vecA.values()))
        denomB = math.sqrt(sum(x**2 for x in vecB.values()))
        vA, vB = [], []
        for k in keys:
            vA.append(vecA.get(k, 0) / float(denomA))
            vB.append(vecB.get(k, 0) / float(denomB))
        dot = [vA[i]*vB[i] for i in range(len(vA))]
        return sum(dot)

    def train(self, data: Dict):
        '''
        train model from the given dataset
        dataset format:
        Dict(
            License name -> Tokens
        )
        '''
        # Collect vocabulary and Memorize vectors
        for k, v in data.items():
            # 1-gram
            self.vectors_1gram[k] = Counter(v)
            self.vocab_1gram.update(self.vectors_1gram[k])
            # 2-gram
            vec2g = Counter()
            for i in range(1, len(v)):
                vec2g.update([(v[i-1], v[i])])
            self.vectors_2gram[k] = vec2g
            self.vocab_2gram.update(vec2g)
            # 3-gram
            vec3g = Counter()
            for i in range(2, len(v)):
                vec3g.update([(v[i-2],v[i-1],v[i])])
            self.vectors_3gram[k] = vec3g
            self.vocab_3gram.update(vec3g)
        # training statistics
        print('1-Gram | Training Data:',
                f'{len(self.vocab_1gram)} vocabs',
                f'{sum(self.vocab_1gram.values())} tally',
                sep='\t')
        print('2-Gram | Training Data:',
                f'{len(self.vocab_2gram)} vocabs',
                f'{sum(self.vocab_2gram.values())} tally',
                sep='\t')
        print('3-Gram | Training Data:',
                f'{len(self.vocab_3gram)} vocabs',
                f'{sum(self.vocab_3gram.values())} tally',
                sep='\t')
        for k in data.keys():
            print(f'{k}:'.rjust(42),
                f'1-Gram[', '%6d'%len(self.vectors_1gram[k]), ']\t',
                f'2-Gram[', '%6d'%len(self.vectors_2gram[k]), ']\t',
                f'3-Gram[', '%6d'%len(self.vectors_3gram[k]), ']\t')


    def predict(self, path: str, topK: int = 1):
        # tokenization
        text = re.sub('\W', ' ', open(path).read()).lower()
        tokens = text.split()
        # 1-gram and score
        common_tokens = set(tokens).intersection(set(self.vocab_1gram.keys()))
        vector_raw = Counter(tokens)
        vector = {k: vector_raw[k] for k in common_tokens}
        scores = defaultdict(list)
        for k, v in self.vectors_1gram.items():
            scores[k].append(self.cosSim(v, vector))
        # 2-gram and score
        vec2g = Counter()
        for i in range(1, len(tokens)):
            token2g = (tokens[i-1], tokens[i])
            if token2g in self.vocab_2gram.keys():
                vec2g.update([token2g])
        for k, v in self.vectors_2gram.items():
            scores[k].append(self.cosSim(v, vec2g))
        # 3-gram and score
        vec3g = Counter()
        for i in range(2, len(tokens)):
            token3g = (tokens[i-2], tokens[i-1], tokens[i])
            if token3g in self.vocab_3gram.keys():
                vec3g.update([token3g])
        for k, v in self.vectors_3gram.items():
            scores[k].append(self.cosSim(v, vec3g))

        # aggregation
        score_aggregated = sorted(
                [(k, 0.33*scores[k][0] + 0.33*scores[k][1] + 0.34*scores[k][2])
                    for k in self.vectors_2gram.keys()],
                key=lambda x: x[1], reverse=True)
        for k, s in score_aggregated[:topK]:
            print(f'{k} similarity:'.rjust(42),
                '\t%.3f\t' % s,
                '1-Gram[', '%.3f' % scores[k][0], ']\t,',
                '2-Gram[', '%.3f' % scores[k][1], ']\t,',
                '3-Gram[', '%.3f' % scores[k][2], ']')


def train(datadir: str):
    '''
    Train the model from the given directory
    '''
    print('Collecting data from ./data ...')
    files = glob.glob('data/*')
    data = dict()
    for f in files:
        # tokenization
        text = re.sub('\W', ' ', open(f).read()).lower()
        tokens = text.split()
        print(f'{len(tokens)} ', end='')
        data[os.path.basename(f)] = tokens
    print()
    print('Training model ...')
    model = Model()
    model.train(data)
    pickle.dump(model, open('model.pkl', 'wb'))
    print('Model saved to model.pkg')


if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('--train', type=str, default='',
            help='Train the model from the given directory')
    ag.add_argument('--predict', type=str, default='',
            help='Try to classify the given file')
    ag.add_argument('--topk', type=int, default=1)
    ag = ag.parse_args()

    if ag.train:
        train(ag.train)
    elif ag.predict:
        model = pickle.load(open('model.pkl', 'rb'))
        model.predict(ag.predict, topK=ag.topk)
