h=`hostname`

for i in "$@"
do
    nohup ./GreenOnion.out target_keys/nysiis_2s_real.txt $i > output/gpu-$h-$i.txt &
done