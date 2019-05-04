Licensecheck-NG
===============

Currently a (toy) license classifier based on k-NN. k-NN is a very simple
machine learning algorithm. In this implementation, we use n-gram bag-of-words
vectors to represent text, and measure text similarity by cosine distance.

Key words: k-NN, Bag-of-Words, n-Gram, Machine Learning, Computational Linguistics

## Dependency

Just pypy3. It is written in pure python and does not use anything outside
the standard library.

## Train and Predict

```
make train
make test  # testing on training dataset generates a confusion matrix
```

## FAQ

1. it doesn't recognize XXX license.

Training data is simply a bunch of plaintext licenses. Copy the license
content to data/XXX and train the model. Then the model will recognize
the XXX license.
