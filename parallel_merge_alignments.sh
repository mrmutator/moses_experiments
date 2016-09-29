#!/usr/bin/env bash

# file1 file2 num_cores

BASEDIR=$(dirname "$0")



size="$(wc -l $1| cut --delimiter=" " -f1)"
nmt=`expr $size / $3`
nm=`expr $nmt + 1`

split -l $nm $1 file1.
split -l $nm $2 file2.

for f in file1.*; do
    r="${f/file1/file2}"
    sfx="${f/file1./}"
    python $BASEDIR/merge_alignments.py --filename merged.$sfx --grow-diag-final $f $r  2> /dev/null &
done
wait
cat merged.* > aligned.grow-diag-final
rm file1.*
rm file2.*
rm merged.*