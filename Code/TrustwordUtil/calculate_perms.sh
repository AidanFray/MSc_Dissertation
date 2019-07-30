## Script used to create lists of `vulnerable` keys

set -e

# declare -a metricArr=("soundex" "leven" "metaphone" "nysiis" "wordvec_4_5")
declare -a metricArr=("wordvec_4")


# declare -a permsArr=("1000" "10000" "100000") # 1 day
# declare -a permsArr=("500" "5000" "50000") # 2 days
# declare -a permsArr=("250" "2500" "25000") # 3 days
declare -a permsArr=("152" "1525" "15250") # 1 week

declare -a staticArr=("0" "1" "2")

for perm in "${permsArr[@]}"
do
    rm -f report-perms-$perm.md
    touch report-perms-$perm.md
    echo $perm 
    echo 

    for simMetric in "${metricArr[@]}"
    do
        for staticWords in "${staticArr[@]}" 
        do
            echo $simMetric-$staticWords
    
            mkdir -p ./vuln_keys/$simMetric
            mkdir -p ./vuln_keys/$simMetric/$simMetric-$perm

            python trustwords_util.py --vuln-keys avergae_perms/realWorldAverage/100000_pairs.txt $perm $staticWords -s ../../SimilarLists/$simMetric.csv > ./vuln_keys/$simMetric/$simMetric-$perm/$simMetric-static-$staticWords.txt

            KEY_NUM=`cat ./vuln_keys/$simMetric/$simMetric-$perm/$simMetric-static-$staticWords.txt | wc -l`

            echo $simMetric-$staticWords $KEY_NUM/100000 >> report-perms-$perm.md
        done
    done
done
