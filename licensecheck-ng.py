#!/usr/bin/python3
# Copyright (C) 2019 M. Zhou <lumin@debian.org>
from typing import *
import argparse, re, os, sys, json, glob, pickle, math
from collections import Counter


class BOWModel(object):
    '''
    Bag-of-Words Model
    '''
    def __init__(self):
        self.vocab_1gram = Counter()
        #self.vocab_2gram = Counter()  # to be implemented
        self.vectors_1gram = dict()

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
            self.vectors_1gram[k] = Counter(v)
            self.vocab_1gram.update(self.vectors_1gram[k])
        # training stat
        print('Vocab Size/Total of 1-Gram:', len(self.vocab_1gram), sum(self.vocab_1gram.values()))
        for k, v in self.vectors_1gram.items():
            print(f'Vocab Size/Total of {k}:', len(v), sum(v.values()))

    def predict(self, path: str):
        text = re.sub('\W', ' ', open(path).read()).lower()
        tokens = set(text.split())
        common_tokens = tokens.intersection(set(self.vocab_1gram.keys()))
        vector_raw = Counter(tokens)
        vector = {k: vector_raw[k] for k in common_tokens}
        print(vector)
        for k, v in self.vectors_1gram.items():
            print(k, self.cosSim(v, v))


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
    print(model.vocab_1gram.items())
    print(model.vectors_1gram.items())


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
./licensecheck-ng.py --train data --predict data/BSD-3-Clause
'''
