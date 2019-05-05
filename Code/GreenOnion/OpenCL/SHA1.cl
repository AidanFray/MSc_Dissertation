inline uint andnot(uint a,uint b) { return a & ~b; }
inline uint rotate1(uint a) { return (a << 1) | (a >> 31); }
inline uint rotate5(uint a) { return (a << 5) | (a >> 27); }
inline uint rotate30(uint a) { return (a << 30) | (a >> 2); }

//int MAX_EXPONENT = 16777215;  

void sha1_block(uint *in, uint *H)
{
	uint a = H[0];
	uint b = H[1];
	uint c = H[2];
	uint d = H[3];
	uint e = H[4];
	uint f;
	uint x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15;

	x0 = in[0];
	f = (c & b) | andnot(d,b);
	e = rotate5(a) + f + e + 0x5a827999 + x0;
	b = rotate30(b);
	x1 = in[1];
	f = (b & a) | andnot(c,a);
	d = rotate5(e) + f + d + 0x5a827999 + x1;
	a = rotate30(a);
	x2 = in[2];
	f = (a & e) | andnot(b,e);
	c = rotate5(d) + f + c + 0x5a827999 + x2;
	e = rotate30(e);
	x3 = in[3];
	f = (e & d) | andnot(a,d);
	b = rotate5(c) + f + b + 0x5a827999 + x3;
	d = rotate30(d);
	x4 = in[4];
	f = (d & c) | andnot(e,c);
	a = rotate5(b) + f + a + 0x5a827999 + x4;
	c = rotate30(c);
	x5 = in[5];
	f = (c & b) | andnot(d,b);
	e = rotate5(a) + f + e + 0x5a827999 + x5;
	b = rotate30(b);
	x6 = in[6];
	f = (b & a) | andnot(c,a);
	d = rotate5(e) + f + d + 0x5a827999 + x6;
	a = rotate30(a);
	x7 = in[7];
	f = (a & e) | andnot(b,e);
	c = rotate5(d) + f + c + 0x5a827999 + x7;
	e = rotate30(e);
	x8 = in[8];
	f = (e & d) | andnot(a,d);
	b = rotate5(c) + f + b + 0x5a827999 + x8;
	d = rotate30(d);
	x9 = in[9];
	f = (d & c) | andnot(e,c);
	a = rotate5(b) + f + a + 0x5a827999 + x9;
	c = rotate30(c);
	x10 = in[10];
	f = (c & b) | andnot(d,b);
	e = rotate5(a) + f + e + 0x5a827999 + x10;
	b = rotate30(b);
	x11 = in[11];
	f = (b & a) | andnot(c,a);
	d = rotate5(e) + f + d + 0x5a827999 + x11;
	a = rotate30(a);
	x12 = in[12];
	f = (a & e) | andnot(b,e);
	c = rotate5(d) + f + c + 0x5a827999 + x12;
	e = rotate30(e);
	x13 = in[13];
	f = (e & d) | andnot(a,d);
	b = rotate5(c) + f + b + 0x5a827999 + x13;
	d = rotate30(d);
	x14 = in[14];
	f = (d & c) | andnot(e,c);
	a = rotate5(b) + f + a + 0x5a827999 + x14;
	c = rotate30(c);
	x15 = in[15];
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

__kernel void key_hash(__global uint* finalBlock, __global uint* currentDigest, __global uint* outResult)
{
	int i;

	uint W[16];
	uint H[5];
	
	for(i = 0; i < 16; i++) W[i] = finalBlock[i];
	for(i = 0; i < 5; i++) H[i] = currentDigest[i];

	// The exponenet is embedded in the 4th block
	// beacuse the original value is 3 we can use some bit
	// magic to change it to a certain value
	int newExponent = (get_global_id(0) + 2);

	W[4] = W[4] ^ 3 ^ newExponent;

    // Take the last part of the hash
	sha1_block(W,H);

	// ############################# //
	// TODO: This isn't working, need
	// to find a way to dynamically
	// provide all the results to an
	// array back at base??
	// ############################# //

	for(i = 0; i < 5; i++) outResult[(5 * get_global_id(0) + 1) + i] = H[i];
}

// Test the SHA hash code
__kernel void shaTest(__global uint* success)
{
    int i;
    uint W[80];
    uint H[5];

    // Zero out W
    for(i=0;i<80;i++) {
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
