PERMS=1000

PAIR_SIZE=100000

# declare -a metricArr=("soundex" "leven" "metaphone" "nysiis" "wordvec")
declare -a metricArr=("soundex" "metaphone" "nysiis")

declare -a staticArr=("0" "1" "2")

rm report-perms-$PERMS.md
touch report-perms-$PERMS.md

for i in "${metricArr[@]}"
do
    for s in "${staticArr[@]}" 
    do
        echo $i-$s
  
        mkdir ./vuln_keys/$i
        mkdir ./vuln_keys/$i/$i-$PERMS
        mkdir ./vuln_keys/$i/$i-$PERMS/$PERM

        python trustwords_util.py --vuln-keys ../avergae_perms/realWorldAverage/100000_pairs.txt $PERMS $s -s ../../../SimilarLists/$i.csv > ./vuln_keys/$i/$i-$PERMS/$i-static-$s.txt

        KEY_NUM=`cat ./vuln_keys/$i/$i-$PERMS/static-$s.txt | wc -l`

        echo $i-$s $KEY_NUM/100000 >> report-perms-$PERMS.md
    done
done


