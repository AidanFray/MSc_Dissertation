#include "sha1.c"

int main() {

    // Test message
    char* buff = "hello";

    // Needs to be 20 long 
    char* results[20]; 

    SHA1Hash(&results, buff);

    printHash(results);
}

void printHash(unsigned char *buffer)
{
   for (int n = 0; n < 20; n++)
   {
        printf("%02x", buffer[n]);
   }
    putchar('\n');
}