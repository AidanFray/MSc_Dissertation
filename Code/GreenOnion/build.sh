g++ hash.cpp ./Crypto/sha1.cpp -pthread -lOpenCL -lcrypto -lssl -o GreenOnion.out
rc=$?; 
if [[ $rc != 0 ]]; 
then 
    echo "[*] Error in complilation!"
    exit $rc;
fi
./GreenOnion.out