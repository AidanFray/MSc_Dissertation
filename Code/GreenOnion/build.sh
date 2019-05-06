g++ hash.cpp ./Crypto/sha1.cpp -lOpenCL -lcrypto -lssl
rc=$?; 
if [[ $rc != 0 ]]; 
then 
    echo "[*] Error in complilation!"
    exit $rc;
fi
./a.out