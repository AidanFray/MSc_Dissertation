default: green_onion


green_onion:
	g++ hash.cpp ./crypto/*.cpp ./util/*.cpp ./bloom/*.cpp -pthread -lOpenCL -lcrypto -lssl -Wall \
	-o GreenOnion.out

clean:
	rm GreenOnion.out