#!/usr/bin/bash


# TRAINING
###################################

mkdir smalld
mkdir smalld/model
mkdir bigd
mkdir bigd/model

cp /home/wechsler/test_phrases/random.* ./
cp /home/wechsler/data_sets/complete/fren/training.en.gz corpus.en.gz
cp /home/wechsler/data_sets/complete/fren/training.fr.gz corpus.fr.gz
cp ${1}all.aligned aligned.grow-diag-final

gunzip corpus.*.gz


awk 'NR == FNR{a[$0]; next};FNR in a' random.small corpus.en > small.en
awk 'NR == FNR{a[$0]; next};FNR in a' random.small corpus.fr > small.fr
awk 'NR == FNR{a[$0]; next};FNR in a' random.small aligned.grow-diag-final > small.grow-diag-final

awk 'NR == FNR{a[$0]; next};FNR in a' random.big corpus.en > big.en
awk 'NR == FNR{a[$0]; next};FNR in a' random.big corpus.fr > big.fr
awk 'NR == FNR{a[$0]; next};FNR in a' random.big aligned.grow-diag-final > big.grow-diag-final


>&2 echo "Starting training script. ";
/home/wechsler/mosesdecoder/scripts/training/train-model.perl -root-dir $PWD/smalld -corpus $PWD/small -f fr -e en -external-bin-dir /home/wechsler/mosesdecoder/tools --first-step 5 --last-step 5 --alignment-file $PWD/small -cores 16

/home/wechsler/mosesdecoder/scripts/training/train-model.perl -root-dir $PWD/bigd -corpus $PWD/big -f fr -e en -external-bin-dir /home/wechsler/mosesdecoder/tools --first-step 5 --last-step 5 --alignment-file $PWD/big -cores 16

cd smalld/model
LC_ALL=C gunzip -c extract.sorted.gz | sort | uniq | gzip > extract.small.gz &

cd ../../bigd/model
LC_ALL=C gunzip -c extract.sorted.gz | sort | uniq | split -l 500000 --additional-suffix .sub ; gzip *.sub
cd ../../
wait

touch joblist.txt
for f in bigd/model/*.sub.gz
 do
 echo "python /home/wechsler/moses_experiments/coverage.py $f smalld/model/extract.small.gz" >> joblist.txt
 done

parallel --jobs 16 < joblist.txt


python /home/wechsler/moses_experiments/summing.py bigd/model/
