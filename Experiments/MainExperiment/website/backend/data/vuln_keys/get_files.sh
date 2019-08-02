set -e

declare -a metricArr=("metaphone" "leven" "nysiis")
declare -a permsArr=("152" "1525" "15250") # 1 week

for i in "${metricArr[@]}"
do
    rm -fr $i
    mkdir $i

    cp ../../../../../../Code/TrustwordUtil/vuln_keys/$i/$i-152/$i-static-2.txt  ./$i
    cp ../../../../../../Code/TrustwordUtil/vuln_keys/$i/$i-1525/$i-static-1.txt  ./$i
    cp ../../../../../../Code/TrustwordUtil/vuln_keys/$i/$i-15250/$i-static-0.txt  ./$i

done