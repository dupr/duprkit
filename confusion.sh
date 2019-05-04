#!/bin/sh
set -e
if ! test -r confusion.txt; then
	make test > confusion.txt
fi
awk '/similarity:/{print $3}' confusion.txt > confusion.mat
N=22
echo $N

cat > confusion.m << EOF
x = load('confusion.mat');
x = reshape(x, 22, 22);
pcolor(x);
print -dpdf confusion.pdf;
EOF
octave -q confusion.m
rm confusion.mat confusion.m
