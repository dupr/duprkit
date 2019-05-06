Licensecheck-NG
===============

Currently a (toy) license classifier based on k-NN. k-NN is a very simple
machine learning algorithm. In this implementation, we use n-gram bag-of-words
vectors to represent text, and measure text similarity by cosine distance.
The implimentation is pure python and doesn't use anything outside the python
standard library.

Many details could be further improved.
Open an issue on the salsa repo for anything you want to say.

Key words: k-NN, Bag-of-Words, n-Gram, Machine Learning, Computational Linguistics

## Known problems

1. this toy is still not properly assessed. people on IRC suggested me test
it against chromium, fpc, lazarus, boost

2. currently it works not quite well with very short license declarations,
such as the one on the python script itself `:-(`.

3. we need choose a threshold under which the program rejects to classify.

## Dependency

Just `pypy3`. The software is written in pure python and does not use anything
outside the standard library. At this stage we just try to let it work
correctly. Speed optimization? Not today.

## Automatic Training and Assessment on the training set

```
make train
make validate  # testing on training dataset generates a confusion matrix
```

It takes about 1 seconds to train. Very fast.

## Manual training and prediction

Training:

```
./licensecheck-ng.py --train data
```

It will write the trained model to `model.pkl`.

Predict:

```
./licensecheck-ng.py --predict <MY_FILE>
```

It requires `./model.pkl` to be present.

## Comparison to related works

https://wiki.debian.org/CopyrightReviewTools

Well, can I beat all of them? I have no answer currently.

* licensecheck
* scan-copyrights
* cme
* licensecheck2dep5
* license-reconcile
* debmake

Many thanks to Osamu Aoki who provided many training data in debmake's source.

* decopy
* license
* check-all-the-things
* cargo-lichking
* python-debian
* license finder
* licensed
* ninka
* scancode
* dlt
* deb-pkg-tools
* jninka
* apache-rat
* fossology
* OSLCv3
* https://github.com/nexB/scancode-toolkit

The core algorithm is similar to what scancode-toolkit called "match set":
https://github.com/nexB/scancode-toolkit/blob/develop/src/licensedcode/match_set.py

## FAQ

1. it doesn't recognize XXX license.

Training data is simply a bunch of plaintext licenses. Copy the license
content to data/XXX and train the model. Then the model will recognize
the XXX license.

2. it's accuracy is low on some special cases.

Currently the result is produced by the pure algorithm, and there is
no any engineering tweaks. Accuracy in special cases could be further
improved with those tweaks.

3. I want to compare xxx text files (or code) instead of license texts.

Train with your custom text and predict any plain text with the model.

4. why do you try writing such a tool?

Firstly just for fun.
Secondly as a part of the DUPR toolkit (https://github.com/dupr/duprkit)
