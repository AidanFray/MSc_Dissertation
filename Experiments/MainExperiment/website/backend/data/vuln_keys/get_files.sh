set -e

declare -a metricArr=("metaphone" "soundex" "nysiis")

for i in "${metricArr[@]}"
do
    rm -fr $i
    mkdir $i

    cp ../../trustwords_util/vuln_keys/$i/$i-1000/$i-static-2.txt  ./$i
    cp ../../trustwords_util/vuln_keys/$i/$i-10000/$i-static-1.txt  ./$i
    cp ../../trustwords_util/vuln_keys/$i/$i-100000/$i-static-0.txt  ./$i

done