inline uint andnot(uint a,uint b) { return a & ~b; }
inline uint rotate1(uint a) { return (a << 1) | (a >> 31); }
inline uint rotate5(uint a) { return (a << 5) | (a >> 27); }
inline uint rotate30(uint a) { return (a << 30) | (a >> 2); }

uint MurmurHash3_x86_32 (uint key, uint seed)
{
		uint len = sizeof(key);

		uint c1 = 0xcc9e2d51;
		uint c2 = 0x1b873593;
		uint m = 5;
		uint n = 0xe6546b64;

		uint h = seed;

		// 4 byte chunks are supposed to loop here
		// but we're only dealing with 32-bit ints here
		// so we don't need to loop
		uint k;
		k  = key;
		k *= c1;
		k = (k << 15) | (k >> 17);
		k *= c2;

		h ^= k;
		h = (h << 13) | (h >> 19);
		h  = (h * m) + n;

		h ^= len;
		h ^= (h >> 16);
		h *= 0x85ebca6b;
		h ^= (h >> 13);
		h *= 0xc2b2ae35;
		h ^= (h >> 16);

		return h;		
} 

void sha1_block(uint *W, uint *H)
{
	uint a = H[0];
	uint b = H[1];
	uint c = H[2];
	uint d = H[3];
	uint e = H[4];
	uint f;
	uint x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15;

	x0 = W[0];
	f = (c & b) | andnot(d,b);
	e = rotate5(a) + f + e + 0x5a827999 + x0;
	b = rotate30(b);
	x1 = W[1];
	f = (b & a) | andnot(c,a);
	d = rotate5(e) + f + d + 0x5a827999 + x1;
	a = rotate30(a);
	x2 = W[2];
	f = (a & e) | andnot(b,e);
	c = rotate5(d) + f + c + 0x5a827999 + x2;
	e = rotate30(e);
	x3 = W[3];
	f = (e & d) | andnot(a,d);
	b = rotate5(c) + f + b + 0x5a827999 + x3;
	d = rotate30(d);
	x4 = W[4];
	f = (d & c) | andnot(e,c);
	a = rotate5(b) + f + a + 0x5a827999 + x4;
	c = rotate30(c);
	x5 = W[5];
	f = (c & b) | andnot(d,b);
	e = rotate5(a) + f + e + 0x5a827999 + x5;
	b = rotate30(b);
	x6 = W[6];
	f = (b & a) | andnot(c,a);
	d = rotate5(e) + f + d + 0x5a827999 + x6;
	a = rotate30(a);
	x7 = W[7];
	f = (a & e) | andnot(b,e);
	c = rotate5(d) + f + c + 0x5a827999 + x7;
	e = rotate30(e);
	x8 = W[8];
	f = (e & d) | andnot(a,d);
	b = rotate5(c) + f + b + 0x5a827999 + x8;
	d = rotate30(d);
	x9 = W[9];
	f = (d & c) | andnot(e,c);
	a = rotate5(b) + f + a + 0x5a827999 + x9;
	c = rotate30(c);
	x10 = W[10];
	f = (c & b) | andnot(d,b);
	e = rotate5(a) + f + e + 0x5a827999 + x10;
	b = rotate30(b);
	x11 = W[11];
	f = (b & a) | andnot(c,a);
	d = rotate5(e) + f + d + 0x5a827999 + x11;
	a = rotate30(a);
	x12 = W[12];
	f = (a & e) | andnot(b,e);
	c = rotate5(d) + f + c + 0x5a827999 + x12;
	e = rotate30(e);
	x13 = W[13];
	f = (e & d) | andnot(a,d);
	b = rotate5(c) + f + b + 0x5a827999 + x13;
	d = rotate30(d);
	x14 = W[14];
	f = (d & c) | andnot(e,c);
	a = rotate5(b) + f + a + 0x5a827999 + x14;
	c = rotate30(c);
	x15 = W[15];
	f = (c & b) | andnot(d,b);
	e = rotate5(a) + f + e + 0x5a827999 + x15;
	b = rotate30(b);
	x0 = rotate1(x13 ^ x8 ^ x2 ^ x0);
	f = (b & a) | andnot(c,a);
	d = rotate5(e) + f + d + 0x5a827999 + x0;
	a = rotate30(a);
	x1 = rotate1(x14 ^ x9 ^ x3 ^ x1);
	f = (a & e) | andnot(b,e);
	c = rotate5(d) + f + c + 0x5a827999 + x1;
	e = rotate30(e);
	x2 = rotate1(x15 ^ x10 ^ x4 ^ x2);
	f = (e & d) | andnot(a,d);
	b = rotate5(c) + f + b + 0x5a827999 + x2;
	d = rotate30(d);
	x3 = rotate1(x0 ^ x11 ^ x5 ^ x3);
	f = (d & c) | andnot(e,c);
	a = rotate5(b) + f + a + 0x5a827999 + x3;
	c = rotate30(c);
	x4 = rotate1(x1 ^ x12 ^ x6 ^ x4);
	f = b ^ c ^ d;
	e = rotate5(a) + f + e + 0x6ed9eba1 + x4;
	b = rotate30(b);
	x5 = rotate1(x2 ^ x13 ^ x7 ^ x5);
	f = a ^ b ^ c;
	d = rotate5(e) + f + d + 0x6ed9eba1 + x5;
	a = rotate30(a);
	x6 = rotate1(x3 ^ x14 ^ x8 ^ x6);
	f = e ^ a ^ b;
	c = rotate5(d) + f + c + 0x6ed9eba1 + x6;
	e = rotate30(e);
	x7 = rotate1(x4 ^ x15 ^ x9 ^ x7);
	f = d ^ e ^ a;
	b = rotate5(c) + f + b + 0x6ed9eba1 + x7;
	d = rotate30(d);
	x8 = rotate1(x5 ^ x0 ^ x10 ^ x8);
	f = c ^ d ^ e;
	a = rotate5(b) + f + a + 0x6ed9eba1 + x8;
	c = rotate30(c);
	x9 = rotate1(x6 ^ x1 ^ x11 ^ x9);
	f = b ^ c ^ d;
	e = rotate5(a) + f + e + 0x6ed9eba1 + x9;
	b = rotate30(b);
	x10 = rotate1(x7 ^ x2 ^ x12 ^ x10);
	f = a ^ b ^ c;
	d = rotate5(e) + f + d + 0x6ed9eba1 + x10;
	a = rotate30(a);
	x11 = rotate1(x8 ^ x3 ^ x13 ^ x11);
	f = e ^ a ^ b;
	c = rotate5(d) + f + c + 0x6ed9eba1 + x11;
	e = rotate30(e);
	x12 = rotate1(x9 ^ x4 ^ x14 ^ x12);
	f = d ^ e ^ a;
	b = rotate5(c) + f + b + 0x6ed9eba1 + x12;
	d = rotate30(d);
	x13 = rotate1(x10 ^ x5 ^ x15 ^ x13);
	f = c ^ d ^ e;
	a = rotate5(b) + f + a + 0x6ed9eba1 + x13;
	c = rotate30(c);
	x14 = rotate1(x11 ^ x6 ^ x0 ^ x14);
	f = b ^ c ^ d;
	e = rotate5(a) + f + e + 0x6ed9eba1 + x14;
	b = rotate30(b);
	x15 = rotate1(x12 ^ x7 ^ x1 ^ x15);
	f = a ^ b ^ c;
	d = rotate5(e) + f + d + 0x6ed9eba1 + x15;
	a = rotate30(a);
	x0 = rotate1(x13 ^ x8 ^ x2 ^ x0);
	f = e ^ a ^ b;
	c = rotate5(d) + f + c + 0x6ed9eba1 + x0;
	e = rotate30(e);
	x1 = rotate1(x14 ^ x9 ^ x3 ^ x1);
	f = d ^ e ^ a;
	b = rotate5(c) + f + b + 0x6ed9eba1 + x1;
	d = rotate30(d);
	x2 = rotate1(x15 ^ x10 ^ x4 ^ x2);
	f = c ^ d ^ e;
	a = rotate5(b) + f + a + 0x6ed9eba1 + x2;
	c = rotate30(c);
	x3 = rotate1(x0 ^ x11 ^ x5 ^ x3);
	f = b ^ c ^ d;
	e = rotate5(a) + f + e + 0x6ed9eba1 + x3;
	b = rotate30(b);
	x4 = rotate1(x1 ^ x12 ^ x6 ^ x4);
	f = a ^ b ^ c;
	d = rotate5(e) + f + d + 0x6ed9eba1 + x4;
	a = rotate30(a);
	x5 = rotate1(x2 ^ x13 ^ x7 ^ x5);
	f = e ^ a ^ b;
	c = rotate5(d) + f + c + 0x6ed9eba1 + x5;
	e = rotate30(e);
	x6 = rotate1(x3 ^ x14 ^ x8 ^ x6);
	f = d ^ e ^ a;
	b = rotate5(c) + f + b + 0x6ed9eba1 + x6;
	d = rotate30(d);
	x7 = rotate1(x4 ^ x15 ^ x9 ^ x7);
	f = c ^ d ^ e;
	a = rotate5(b) + f + a + 0x6ed9eba1 + x7;
	c = rotate30(c);
	x8 = rotate1(x5 ^ x0 ^ x10 ^ x8);
	f = (b & c) | (b & d) | (c & d);
	e = rotate5(a) + f + e + 0x8f1bbcdc + x8;
	b = rotate30(b);
	x9 = rotate1(x6 ^ x1 ^ x11 ^ x9);
	f = (a & b) | (a & c) | (b & c);
	d = rotate5(e) + f + d + 0x8f1bbcdc + x9;
	a = rotate30(a);
	x10 = rotate1(x7 ^ x2 ^ x12 ^ x10);
	f = (e & a) | (e & b) | (a & b);
	c = rotate5(d) + f + c + 0x8f1bbcdc + x10;
	e = rotate30(e);
	x11 = rotate1(x8 ^ x3 ^ x13 ^ x11);
	f = (d & e) | (d & a) | (e & a);
	b = rotate5(c) + f + b + 0x8f1bbcdc + x11;
	d = rotate30(d);
	x12 = rotate1(x9 ^ x4 ^ x14 ^ x12);
	f = (c & d) | (c & e) | (d & e);
	a = rotate5(b) + f + a + 0x8f1bbcdc + x12;
	c = rotate30(c);
	x13 = rotate1(x10 ^ x5 ^ x15 ^ x13);
	f = (b & c) | (b & d) | (c & d);
	e = rotate5(a) + f + e + 0x8f1bbcdc + x13;
	b = rotate30(b);
	x14 = rotate1(x11 ^ x6 ^ x0 ^ x14);
	f = (a & b) | (a & c) | (b & c);
	d = rotate5(e) + f + d + 0x8f1bbcdc + x14;
	a = rotate30(a);
	x15 = rotate1(x12 ^ x7 ^ x1 ^ x15);
	f = (e & a) | (e & b) | (a & b);
	c = rotate5(d) + f + c + 0x8f1bbcdc + x15;
	e = rotate30(e);
	x0 = rotate1(x13 ^ x8 ^ x2 ^ x0);
	f = (d & e) | (d & a) | (e & a);
	b = rotate5(c) + f + b + 0x8f1bbcdc + x0;
	d = rotate30(d);
	x1 = rotate1(x14 ^ x9 ^ x3 ^ x1);
	f = (c & d) | (c & e) | (d & e);
	a = rotate5(b) + f + a + 0x8f1bbcdc + x1;
	c = rotate30(c);
	x2 = rotate1(x15 ^ x10 ^ x4 ^ x2);
	f = (b & c) | (b & d) | (c & d);
	e = rotate5(a) + f + e + 0x8f1bbcdc + x2;
	b = rotate30(b);
	x3 = rotate1(x0 ^ x11 ^ x5 ^ x3);
	f = (a & b) | (a & c) | (b & c);
	d = rotate5(e) + f + d + 0x8f1bbcdc + x3;
	a = rotate30(a);
	x4 = rotate1(x1 ^ x12 ^ x6 ^ x4);
	f = (e & a) | (e & b) | (a & b);
	c = rotate5(d) + f + c + 0x8f1bbcdc + x4;
	e = rotate30(e);
	x5 = rotate1(x2 ^ x13 ^ x7 ^ x5);
	f = (d & e) | (d & a) | (e & a);
	b = rotate5(c) + f + b + 0x8f1bbcdc + x5;
	d = rotate30(d);
	x6 = rotate1(x3 ^ x14 ^ x8 ^ x6);
	f = (c & d) | (c & e) | (d & e);
	a = rotate5(b) + f + a + 0x8f1bbcdc + x6;
	c = rotate30(c);
	x7 = rotate1(x4 ^ x15 ^ x9 ^ x7);
	f = (b & c) | (b & d) | (c & d);
	e = rotate5(a) + f + e + 0x8f1bbcdc + x7;
	b = rotate30(b);
	x8 = rotate1(x5 ^ x0 ^ x10 ^ x8);
	f = (a & b) | (a & c) | (b & c);
	d = rotate5(e) + f + d + 0x8f1bbcdc + x8;
	a = rotate30(a);
	x9 = rotate1(x6 ^ x1 ^ x11 ^ x9);
	f = (e & a) | (e & b) | (a & b);
	c = rotate5(d) + f + c + 0x8f1bbcdc + x9;
	e = rotate30(e);
	x10 = rotate1(x7 ^ x2 ^ x12 ^ x10);
	f = (d & e) | (d & a) | (e & a);
	b = rotate5(c) + f + b + 0x8f1bbcdc + x10;
	d = rotate30(d);
	x11 = rotate1(x8 ^ x3 ^ x13 ^ x11);
	f = (c & d) | (c & e) | (d & e);
	a = rotate5(b) + f + a + 0x8f1bbcdc + x11;
	c = rotate30(c);
	x12 = rotate1(x9 ^ x4 ^ x14 ^ x12);
	f = b ^ c ^ d;
	e = rotate5(a) + f + e + 0xca62c1d6 + x12;
	b = rotate30(b);
	x13 = rotate1(x10 ^ x5 ^ x15 ^ x13);
	f = a ^ b ^ c;
	d = rotate5(e) + f + d + 0xca62c1d6 + x13;
	a = rotate30(a);
	x14 = rotate1(x11 ^ x6 ^ x0 ^ x14);
	f = e ^ a ^ b;
	c = rotate5(d) + f + c + 0xca62c1d6 + x14;
	e = rotate30(e);
	x15 = rotate1(x12 ^ x7 ^ x1 ^ x15);
	f = d ^ e ^ a;
	b = rotate5(c) + f + b + 0xca62c1d6 + x15;
	d = rotate30(d);
	x0 = rotate1(x13 ^ x8 ^ x2 ^ x0);
	f = c ^ d ^ e;
	a = rotate5(b) + f + a + 0xca62c1d6 + x0;
	c = rotate30(c);
	x1 = rotate1(x14 ^ x9 ^ x3 ^ x1);
	f = b ^ c ^ d;
	e = rotate5(a) + f + e + 0xca62c1d6 + x1;
	b = rotate30(b);
	x2 = rotate1(x15 ^ x10 ^ x4 ^ x2);
	f = a ^ b ^ c;
	d = rotate5(e) + f + d + 0xca62c1d6 + x2;
	a = rotate30(a);
	x3 = rotate1(x0 ^ x11 ^ x5 ^ x3);
	f = e ^ a ^ b;
	c = rotate5(d) + f + c + 0xca62c1d6 + x3;
	e = rotate30(e);
	x4 = rotate1(x1 ^ x12 ^ x6 ^ x4);
	f = d ^ e ^ a;
	b = rotate5(c) + f + b + 0xca62c1d6 + x4;
	d = rotate30(d);
	x5 = rotate1(x2 ^ x13 ^ x7 ^ x5);
	f = c ^ d ^ e;
	a = rotate5(b) + f + a + 0xca62c1d6 + x5;
	c = rotate30(c);
	x6 = rotate1(x3 ^ x14 ^ x8 ^ x6);
	f = b ^ c ^ d;
	e = rotate5(a) + f + e + 0xca62c1d6 + x6;
	b = rotate30(b);
	x7 = rotate1(x4 ^ x15 ^ x9 ^ x7);
	f = a ^ b ^ c;
	d = rotate5(e) + f + d + 0xca62c1d6 + x7;
	a = rotate30(a);
	x8 = rotate1(x5 ^ x0 ^ x10 ^ x8);
	f = e ^ a ^ b;
	c = rotate5(d) + f + c + 0xca62c1d6 + x8;
	e = rotate30(e);
	x9 = rotate1(x6 ^ x1 ^ x11 ^ x9);
	f = d ^ e ^ a;
	b = rotate5(c) + f + b + 0xca62c1d6 + x9;
	d = rotate30(d);
	x10 = rotate1(x7 ^ x2 ^ x12 ^ x10);
	f = c ^ d ^ e;
	a = rotate5(b) + f + a + 0xca62c1d6 + x10;
	c = rotate30(c);
	x11 = rotate1(x8 ^ x3 ^ x13 ^ x11);
	f = b ^ c ^ d;
	e = rotate5(a) + f + e + 0xca62c1d6 + x11;
	b = rotate30(b);
	x12 = rotate1(x9 ^ x4 ^ x14 ^ x12);
	f = a ^ b ^ c;
	d = rotate5(e) + f + d + 0xca62c1d6 + x12;
	a = rotate30(a);
	x13 = rotate1(x10 ^ x5 ^ x15 ^ x13);
	f = e ^ a ^ b;
	c = rotate5(d) + f + c + 0xca62c1d6 + x13;
	e = rotate30(e);
	x14 = rotate1(x11 ^ x6 ^ x0 ^ x14);
	f = d ^ e ^ a;
	b = rotate5(c) + f + b + 0xca62c1d6 + x14;
	d = rotate30(d);
	x15 = rotate1(x12 ^ x7 ^ x1 ^ x15);
	f = c ^ d ^ e;
	a = rotate5(b) + f + a + 0xca62c1d6 + x15;
	c = rotate30(c);

	a = a + H[0];
	b = b + H[1];
	c = c + H[2];
	d = d + H[3];
	e = e + H[4];
	H[0] = a;
	H[1] = b;
	H[2] = c;
	H[3] = d;
	H[4] = e;
}

__kernel void key_hash(__global uint* finalBlock, 
					   __global uint* currentDigest, 
					   __global bool* bitVector,
					   __global long* bitVectorSize,
					//    __global uint* numberOfHashes,
					   __global uint* outResult)
{
	// We have 3 bytes to work with proving us with 16777215 (2^24)
	// increments per key

	// This means global work size must be set to
	// <= (0x01FFFFFF - 0x010001) / 2
	int ORIGINAL_EXPONENT_VALUE = 0x01000001;

	uint W[16];
	uint H[5];
	
	// Unrolled loops
	W[0] = finalBlock[0];
	W[1] = finalBlock[1];
	W[2] = finalBlock[2];
	W[3] = finalBlock[3];
	W[4] = finalBlock[4];
	W[5] = finalBlock[5];
	W[6] = finalBlock[6];
	W[7] = finalBlock[7];
	W[8] = finalBlock[8];
	W[9] = finalBlock[9];
	W[10] = finalBlock[10];
	W[11] = finalBlock[11];
	W[12] = finalBlock[12];
	W[13] = finalBlock[13];
	W[14] = finalBlock[14];
	W[15] = finalBlock[15];

	H[0] = currentDigest[0];
	H[1] = currentDigest[1];
	H[2] = currentDigest[2];
	H[3] = currentDigest[3];
	H[4] = currentDigest[4];

	//To exponent is split across two words
	// i.e
	//
	// W[3] = XX EE EE EE
	// W[4] = EE XX XX XX
	//
	// Therefore, we need to do some xoring bit magic to change these values
	// to match the value we want. The code below manipulates values into 
	// positions to xor. One characteritic here that is useful is the fact 
	// that the same value XORd == 0, anything XORd with 0 becauses itself.
	// This lets us replace bytes is certain positions.

	int newExponent = get_global_id(0) + ORIGINAL_EXPONENT_VALUE;
	
	//Moves the value to the right i.e. 0x01ffff -> 0x0001ff
	//This is required due to the bit length taking up the MSByte
	int exponentMaskLeft = ((int)(ORIGINAL_EXPONENT_VALUE / 0x100)) ^ ((int)(newExponent / 0x100));
	W[3] = W[3] ^ exponentMaskLeft;

	//Grabs the last byte of each exponent to apply to the next word
	int lastByte = (int)(ORIGINAL_EXPONENT_VALUE / 0x100) * 0x100 ^ ORIGINAL_EXPONENT_VALUE;
	int lastByteNew = (int)(newExponent / 0x100) * 0x100 ^ newExponent;

	//Moves it into position as the MSB of a 32-bit integer i.e 0xff -> 0xff000000
	int exponenetMaskRight = (lastByte * 0x1000000) ^ (lastByteNew * 0x1000000);
	W[4] = W[4] ^ exponenetMaskRight;

	uint a = H[0];
	uint b = H[1];
	uint c = H[2];
	uint d = H[3];
	uint e = H[4];
	uint f;
	uint x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15;

	x0 = W[0];
	f = (c & b) | andnot(d,b);
	e = rotate5(a) + f + e + 0x5a827999 + x0;
	b = rotate30(b);
	x1 = W[1];
	f = (b & a) | andnot(c,a);
	d = rotate5(e) + f + d + 0x5a827999 + x1;
	a = rotate30(a);
	x2 = W[2];
	f = (a & e) | andnot(b,e);
	c = rotate5(d) + f + c + 0x5a827999 + x2;
	e = rotate30(e);
	x3 = W[3];
	f = (e & d) | andnot(a,d);
	b = rotate5(c) + f + b + 0x5a827999 + x3;
	d = rotate30(d);
	x4 = W[4];
	f = (d & c) | andnot(e,c);
	a = rotate5(b) + f + a + 0x5a827999 + x4;
	c = rotate30(c);
	x5 = W[5];
	f = (c & b) | andnot(d,b);
	e = rotate5(a) + f + e + 0x5a827999 + x5;
	b = rotate30(b);
	x6 = W[6];
	f = (b & a) | andnot(c,a);
	d = rotate5(e) + f + d + 0x5a827999 + x6;
	a = rotate30(a);
	x7 = W[7];
	f = (a & e) | andnot(b,e);
	c = rotate5(d) + f + c + 0x5a827999 + x7;
	e = rotate30(e);
	x8 = W[8];
	f = (e & d) | andnot(a,d);
	b = rotate5(c) + f + b + 0x5a827999 + x8;
	d = rotate30(d);
	x9 = W[9];
	f = (d & c) | andnot(e,c);
	a = rotate5(b) + f + a + 0x5a827999 + x9;
	c = rotate30(c);
	x10 = W[10];
	f = (c & b) | andnot(d,b);
	e = rotate5(a) + f + e + 0x5a827999 + x10;
	b = rotate30(b);
	x11 = W[11];
	f = (b & a) | andnot(c,a);
	d = rotate5(e) + f + d + 0x5a827999 + x11;
	a = rotate30(a);
	x12 = W[12];
	f = (a & e) | andnot(b,e);
	c = rotate5(d) + f + c + 0x5a827999 + x12;
	e = rotate30(e);
	x13 = W[13];
	f = (e & d) | andnot(a,d);
	b = rotate5(c) + f + b + 0x5a827999 + x13;
	d = rotate30(d);
	x14 = W[14];
	f = (d & c) | andnot(e,c);
	a = rotate5(b) + f + a + 0x5a827999 + x14;
	c = rotate30(c);
	x15 = W[15];
	f = (c & b) | andnot(d,b);
	e = rotate5(a) + f + e + 0x5a827999 + x15;
	b = rotate30(b);
	x0 = rotate1(x13 ^ x8 ^ x2 ^ x0);
	f = (b & a) | andnot(c,a);
	d = rotate5(e) + f + d + 0x5a827999 + x0;
	a = rotate30(a);
	x1 = rotate1(x14 ^ x9 ^ x3 ^ x1);
	f = (a & e) | andnot(b,e);
	c = rotate5(d) + f + c + 0x5a827999 + x1;
	e = rotate30(e);
	x2 = rotate1(x15 ^ x10 ^ x4 ^ x2);
	f = (e & d) | andnot(a,d);
	b = rotate5(c) + f + b + 0x5a827999 + x2;
	d = rotate30(d);
	x3 = rotate1(x0 ^ x11 ^ x5 ^ x3);
	f = (d & c) | andnot(e,c);
	a = rotate5(b) + f + a + 0x5a827999 + x3;
	c = rotate30(c);
	x4 = rotate1(x1 ^ x12 ^ x6 ^ x4);
	f = b ^ c ^ d;
	e = rotate5(a) + f + e + 0x6ed9eba1 + x4;
	b = rotate30(b);
	x5 = rotate1(x2 ^ x13 ^ x7 ^ x5);
	f = a ^ b ^ c;
	d = rotate5(e) + f + d + 0x6ed9eba1 + x5;
	a = rotate30(a);
	x6 = rotate1(x3 ^ x14 ^ x8 ^ x6);
	f = e ^ a ^ b;
	c = rotate5(d) + f + c + 0x6ed9eba1 + x6;
	e = rotate30(e);
	x7 = rotate1(x4 ^ x15 ^ x9 ^ x7);
	f = d ^ e ^ a;
	b = rotate5(c) + f + b + 0x6ed9eba1 + x7;
	d = rotate30(d);
	x8 = rotate1(x5 ^ x0 ^ x10 ^ x8);
	f = c ^ d ^ e;
	a = rotate5(b) + f + a + 0x6ed9eba1 + x8;
	c = rotate30(c);
	x9 = rotate1(x6 ^ x1 ^ x11 ^ x9);
	f = b ^ c ^ d;
	e = rotate5(a) + f + e + 0x6ed9eba1 + x9;
	b = rotate30(b);
	x10 = rotate1(x7 ^ x2 ^ x12 ^ x10);
	f = a ^ b ^ c;
	d = rotate5(e) + f + d + 0x6ed9eba1 + x10;
	a = rotate30(a);
	x11 = rotate1(x8 ^ x3 ^ x13 ^ x11);
	f = e ^ a ^ b;
	c = rotate5(d) + f + c + 0x6ed9eba1 + x11;
	e = rotate30(e);
	x12 = rotate1(x9 ^ x4 ^ x14 ^ x12);
	f = d ^ e ^ a;
	b = rotate5(c) + f + b + 0x6ed9eba1 + x12;
	d = rotate30(d);
	x13 = rotate1(x10 ^ x5 ^ x15 ^ x13);
	f = c ^ d ^ e;
	a = rotate5(b) + f + a + 0x6ed9eba1 + x13;
	c = rotate30(c);
	x14 = rotate1(x11 ^ x6 ^ x0 ^ x14);
	f = b ^ c ^ d;
	e = rotate5(a) + f + e + 0x6ed9eba1 + x14;
	b = rotate30(b);
	x15 = rotate1(x12 ^ x7 ^ x1 ^ x15);
	f = a ^ b ^ c;
	d = rotate5(e) + f + d + 0x6ed9eba1 + x15;
	a = rotate30(a);
	x0 = rotate1(x13 ^ x8 ^ x2 ^ x0);
	f = e ^ a ^ b;
	c = rotate5(d) + f + c + 0x6ed9eba1 + x0;
	e = rotate30(e);
	x1 = rotate1(x14 ^ x9 ^ x3 ^ x1);
	f = d ^ e ^ a;
	b = rotate5(c) + f + b + 0x6ed9eba1 + x1;
	d = rotate30(d);
	x2 = rotate1(x15 ^ x10 ^ x4 ^ x2);
	f = c ^ d ^ e;
	a = rotate5(b) + f + a + 0x6ed9eba1 + x2;
	c = rotate30(c);
	x3 = rotate1(x0 ^ x11 ^ x5 ^ x3);
	f = b ^ c ^ d;
	e = rotate5(a) + f + e + 0x6ed9eba1 + x3;
	b = rotate30(b);
	x4 = rotate1(x1 ^ x12 ^ x6 ^ x4);
	f = a ^ b ^ c;
	d = rotate5(e) + f + d + 0x6ed9eba1 + x4;
	a = rotate30(a);
	x5 = rotate1(x2 ^ x13 ^ x7 ^ x5);
	f = e ^ a ^ b;
	c = rotate5(d) + f + c + 0x6ed9eba1 + x5;
	e = rotate30(e);
	x6 = rotate1(x3 ^ x14 ^ x8 ^ x6);
	f = d ^ e ^ a;
	b = rotate5(c) + f + b + 0x6ed9eba1 + x6;
	d = rotate30(d);
	x7 = rotate1(x4 ^ x15 ^ x9 ^ x7);
	f = c ^ d ^ e;
	a = rotate5(b) + f + a + 0x6ed9eba1 + x7;
	c = rotate30(c);
	x8 = rotate1(x5 ^ x0 ^ x10 ^ x8);
	f = (b & c) | (b & d) | (c & d);
	e = rotate5(a) + f + e + 0x8f1bbcdc + x8;
	b = rotate30(b);
	x9 = rotate1(x6 ^ x1 ^ x11 ^ x9);
	f = (a & b) | (a & c) | (b & c);
	d = rotate5(e) + f + d + 0x8f1bbcdc + x9;
	a = rotate30(a);
	x10 = rotate1(x7 ^ x2 ^ x12 ^ x10);
	f = (e & a) | (e & b) | (a & b);
	c = rotate5(d) + f + c + 0x8f1bbcdc + x10;
	e = rotate30(e);
	x11 = rotate1(x8 ^ x3 ^ x13 ^ x11);
	f = (d & e) | (d & a) | (e & a);
	b = rotate5(c) + f + b + 0x8f1bbcdc + x11;
	d = rotate30(d);
	x12 = rotate1(x9 ^ x4 ^ x14 ^ x12);
	f = (c & d) | (c & e) | (d & e);
	a = rotate5(b) + f + a + 0x8f1bbcdc + x12;
	c = rotate30(c);
	x13 = rotate1(x10 ^ x5 ^ x15 ^ x13);
	f = (b & c) | (b & d) | (c & d);
	e = rotate5(a) + f + e + 0x8f1bbcdc + x13;
	b = rotate30(b);
	x14 = rotate1(x11 ^ x6 ^ x0 ^ x14);
	f = (a & b) | (a & c) | (b & c);
	d = rotate5(e) + f + d + 0x8f1bbcdc + x14;
	a = rotate30(a);
	x15 = rotate1(x12 ^ x7 ^ x1 ^ x15);
	f = (e & a) | (e & b) | (a & b);
	c = rotate5(d) + f + c + 0x8f1bbcdc + x15;
	e = rotate30(e);
	x0 = rotate1(x13 ^ x8 ^ x2 ^ x0);
	f = (d & e) | (d & a) | (e & a);
	b = rotate5(c) + f + b + 0x8f1bbcdc + x0;
	d = rotate30(d);
	x1 = rotate1(x14 ^ x9 ^ x3 ^ x1);
	f = (c & d) | (c & e) | (d & e);
	a = rotate5(b) + f + a + 0x8f1bbcdc + x1;
	c = rotate30(c);
	x2 = rotate1(x15 ^ x10 ^ x4 ^ x2);
	f = (b & c) | (b & d) | (c & d);
	e = rotate5(a) + f + e + 0x8f1bbcdc + x2;
	b = rotate30(b);
	x3 = rotate1(x0 ^ x11 ^ x5 ^ x3);
	f = (a & b) | (a & c) | (b & c);
	d = rotate5(e) + f + d + 0x8f1bbcdc + x3;
	a = rotate30(a);
	x4 = rotate1(x1 ^ x12 ^ x6 ^ x4);
	f = (e & a) | (e & b) | (a & b);
	c = rotate5(d) + f + c + 0x8f1bbcdc + x4;
	e = rotate30(e);
	x5 = rotate1(x2 ^ x13 ^ x7 ^ x5);
	f = (d & e) | (d & a) | (e & a);
	b = rotate5(c) + f + b + 0x8f1bbcdc + x5;
	d = rotate30(d);
	x6 = rotate1(x3 ^ x14 ^ x8 ^ x6);
	f = (c & d) | (c & e) | (d & e);
	a = rotate5(b) + f + a + 0x8f1bbcdc + x6;
	c = rotate30(c);
	x7 = rotate1(x4 ^ x15 ^ x9 ^ x7);
	f = (b & c) | (b & d) | (c & d);
	e = rotate5(a) + f + e + 0x8f1bbcdc + x7;
	b = rotate30(b);
	x8 = rotate1(x5 ^ x0 ^ x10 ^ x8);
	f = (a & b) | (a & c) | (b & c);
	d = rotate5(e) + f + d + 0x8f1bbcdc + x8;
	a = rotate30(a);
	x9 = rotate1(x6 ^ x1 ^ x11 ^ x9);
	f = (e & a) | (e & b) | (a & b);
	c = rotate5(d) + f + c + 0x8f1bbcdc + x9;
	e = rotate30(e);
	x10 = rotate1(x7 ^ x2 ^ x12 ^ x10);
	f = (d & e) | (d & a) | (e & a);
	b = rotate5(c) + f + b + 0x8f1bbcdc + x10;
	d = rotate30(d);
	x11 = rotate1(x8 ^ x3 ^ x13 ^ x11);
	f = (c & d) | (c & e) | (d & e);
	a = rotate5(b) + f + a + 0x8f1bbcdc + x11;
	c = rotate30(c);
	x12 = rotate1(x9 ^ x4 ^ x14 ^ x12);
	f = b ^ c ^ d;
	e = rotate5(a) + f + e + 0xca62c1d6 + x12;
	b = rotate30(b);
	x13 = rotate1(x10 ^ x5 ^ x15 ^ x13);
	f = a ^ b ^ c;
	d = rotate5(e) + f + d + 0xca62c1d6 + x13;
	a = rotate30(a);
	x14 = rotate1(x11 ^ x6 ^ x0 ^ x14);
	f = e ^ a ^ b;
	c = rotate5(d) + f + c + 0xca62c1d6 + x14;
	e = rotate30(e);
	x15 = rotate1(x12 ^ x7 ^ x1 ^ x15);
	f = d ^ e ^ a;
	b = rotate5(c) + f + b + 0xca62c1d6 + x15;
	d = rotate30(d);
	x0 = rotate1(x13 ^ x8 ^ x2 ^ x0);
	f = c ^ d ^ e;
	a = rotate5(b) + f + a + 0xca62c1d6 + x0;
	c = rotate30(c);
	x1 = rotate1(x14 ^ x9 ^ x3 ^ x1);
	f = b ^ c ^ d;
	e = rotate5(a) + f + e + 0xca62c1d6 + x1;
	b = rotate30(b);
	x2 = rotate1(x15 ^ x10 ^ x4 ^ x2);
	f = a ^ b ^ c;
	d = rotate5(e) + f + d + 0xca62c1d6 + x2;
	a = rotate30(a);
	x3 = rotate1(x0 ^ x11 ^ x5 ^ x3);
	f = e ^ a ^ b;
	c = rotate5(d) + f + c + 0xca62c1d6 + x3;
	e = rotate30(e);
	x4 = rotate1(x1 ^ x12 ^ x6 ^ x4);
	f = d ^ e ^ a;
	b = rotate5(c) + f + b + 0xca62c1d6 + x4;
	d = rotate30(d);
	x5 = rotate1(x2 ^ x13 ^ x7 ^ x5);
	f = c ^ d ^ e;
	a = rotate5(b) + f + a + 0xca62c1d6 + x5;
	c = rotate30(c);
	x6 = rotate1(x3 ^ x14 ^ x8 ^ x6);
	f = b ^ c ^ d;
	e = rotate5(a) + f + e + 0xca62c1d6 + x6;
	b = rotate30(b);
	x7 = rotate1(x4 ^ x15 ^ x9 ^ x7);
	f = a ^ b ^ c;
	d = rotate5(e) + f + d + 0xca62c1d6 + x7;
	a = rotate30(a);
	x8 = rotate1(x5 ^ x0 ^ x10 ^ x8);
	f = e ^ a ^ b;
	c = rotate5(d) + f + c + 0xca62c1d6 + x8;
	e = rotate30(e);
	x9 = rotate1(x6 ^ x1 ^ x11 ^ x9);
	f = d ^ e ^ a;
	b = rotate5(c) + f + b + 0xca62c1d6 + x9;
	d = rotate30(d);
	x10 = rotate1(x7 ^ x2 ^ x12 ^ x10);
	f = c ^ d ^ e;
	a = rotate5(b) + f + a + 0xca62c1d6 + x10;
	c = rotate30(c);
	x11 = rotate1(x8 ^ x3 ^ x13 ^ x11);
	f = b ^ c ^ d;
	e = rotate5(a) + f + e + 0xca62c1d6 + x11;
	b = rotate30(b);
	x12 = rotate1(x9 ^ x4 ^ x14 ^ x12);
	f = a ^ b ^ c;
	d = rotate5(e) + f + d + 0xca62c1d6 + x12;
	a = rotate30(a);
	x13 = rotate1(x10 ^ x5 ^ x15 ^ x13);
	f = e ^ a ^ b;
	c = rotate5(d) + f + c + 0xca62c1d6 + x13;
	e = rotate30(e);
	x14 = rotate1(x11 ^ x6 ^ x0 ^ x14);
	f = d ^ e ^ a;
	b = rotate5(c) + f + b + 0xca62c1d6 + x14;
	d = rotate30(d);
	x15 = rotate1(x12 ^ x7 ^ x1 ^ x15);
	f = c ^ d ^ e;
	a = rotate5(b) + f + a + 0xca62c1d6 + x15;
	c = rotate30(c);

	a = a + H[0];
	b = b + H[1];
	c = c + H[2];
	d = d + H[3];
	e = e + H[4];
	H[0] = a;
	H[1] = b;
	H[2] = c;
	H[3] = d;
	H[4] = e;


	//Checks for a matach
	bool match = true;

	// for(int n = 0; n < numberOfHashes[0]; n++)
	for(int n = 0; n < 2; n++)
	{		
		uint l = MurmurHash3_x86_32(H[0], n) % bitVectorSize[0];
		uint r = MurmurHash3_x86_32(H[1], n) % bitVectorSize[0];

		if(!bitVector[l] || !bitVector[r])
		{
			match = false;
			break;
		}
	}

	if(match)
	{
		outResult[0] = 0x12345678;
		outResult[1] = newExponent;
	}
}

// Test the SHA hash code
__kernel void shaTest(__global uint* success)
{
    int i;
    uint W[16];
    uint H[5];

    // Zero out W
    for(i=0;i<16;i++) {
        W[i] = 0;
    }

    // Init the SHA state
    H[0] = 0x67452301;
    H[1] = 0xEFCDAB89;
    H[2] = 0x98BADCFE;
    H[3] = 0x10325476;
    H[4] = 0xC3D2E1F0;

    // Load our (pre-padded) test block: "Hello world!"
    W[0] = 0x48656c6cu;   // Hell
    W[1] = 0x6f20776fu;   // o wo
    W[2] = 0x726c6421u;   // rld!
    W[3] = 0x80000000u;   // (bit 1)
    W[15] = 0x00000060u;  // m-length in bits (not including bit '1')

    // Take the SHA
    sha1_block(W, H);

    success[0] = H[0];
    success[1] = H[1];
    success[2] = H[2];
    success[3] = H[3];
    success[4] = H[4];
}
