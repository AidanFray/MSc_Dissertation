g++ hash.cpp ./crypto/*.cpp \
    ./util/*.cpp \
    ./bloom/*.cpp \
    -pthread \
    -lOpenCL \
    -lcrypto \
    -lssl \
    -o \
    GreenOnion.out \

rc=$?; 
if [[ $rc != 0 ]]; 
then 
    echo "[*] Error in complilation!"
    exit $rc;
fi
./GreenOnion.out