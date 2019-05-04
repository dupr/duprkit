#!/usr/bin/pypy3
# Copyright (C) 2019 M. Zhou <lumin@debian.org>
from typing import *
import argparse, re, os, sys, json, glob, pickle, math
from collections import Counter, defaultdict


class BOWModel(object):
    '''
    Model that leverages Bag-of-Words Representation
    '''
    def __init__(self):
        self.vocab_1gram = Counter()
        self.vocab_2gram = Counter()
        self.vocab_3gram = Counter() # not implemented
        self.vectors_1gram = dict()
        self.vectors_2gram = dict()
        self.vectors_3gram = dict() # not implemented

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
            self.vectors_2gram[k] = Counter(vec2g)
            self.vocab_2gram.update(self.vectors_2gram[k])
        # training stat
        print('1-Gram Vocab Size/Total of Training Data:', len(self.vocab_1gram), sum(self.vocab_1gram.values()))
        for k, v in self.vectors_1gram.items():
            print(f'1-Gram Vocab Size/Total of {k}:', len(v), sum(v.values()))
        print('2-Gram Vocab Size/Total of Training Data:', len(self.vocab_2gram), sum(self.vocab_2gram.values()))
        for k, v in self.vectors_2gram.items():
            print(f'2-Gram Vocab Size/Total of {k}:', len(v), sum(v.values()))


    def predict(self, path: str):
        text = re.sub('\W', ' ', open(path).read()).lower()
        tokens = text.split()
        common_tokens = set(tokens).intersection(set(self.vocab_1gram.keys()))
        vector_raw = Counter(tokens)
        vector = {k: vector_raw[k] for k in common_tokens}
        scores = defaultdict(list)
        print('1-Gram tokens:', len(vector.keys()))
        for k, v in self.vectors_1gram.items():
            scores[k].append(self.cosSim(v, vector))
        vec2g = Counter()
        for i in range(1, len(tokens)):
            token2g = (tokens[i-1], tokens[i])
            if token2g in self.vocab_2gram.keys():
                vec2g.update([token2g])
        print('2-Gram tokens:', len(vec2g.keys()))
        for k, v in self.vectors_2gram.items():
            scores[k].append(self.cosSim(v, vec2g))
        for k, v in scores.items():
            print(f'{k} similarity:',
                0.5 * v[0] + 0.5 * v[1],
                '1-gram', v[0], '2-gram', v[1])


def train(datadir: str):
    '''
    Train the model from the given directory
    '''
    files = glob.glob('data/*')
    data = dict()
    for f in files:
        text = re.sub('\W', ' ', open(f).read()).lower()
        tokens = text.split()
        print(f'Found {len(tokens)} tokens in file {f}')
        data[os.path.basename(f)] = tokens
    print('Training model ...')
    model = BOWModel()
    model.train(data)
    pickle.dump(model, open('model.pkl', 'wb'))
    print('Model saved to model.pkg')


if __name__ == '__main__':
    ag = argparse.ArgumentParser()
    ag.add_argument('--train', type=str, default='',
            help='Train the model from the given directory')
    ag.add_argument('--predict', type=str, default='',
            help='Try to classify the given file')
    ag = ag.parse_args()

    if ag.train:
        train(ag.train)
    if ag.predict:
        model = pickle.load(open('model.pkl', 'rb'))
        model.predict(ag.predict)

'''
./licensecheck-ng.py --train data
./licensecheck-ng.py --predict data/BSD-3-Clause
'''
