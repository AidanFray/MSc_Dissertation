# Cryptanalysis of the Hash Functions MD4 and RIPEMD

## Paper findings

- Can find collisions in less than 2^8 operations
- 2nd pre-image attack on MD4 'weak messages'

Paper introduces new analytical techniques applicable to all the MD4 hash function family.

### Techniques

- Shows how to gain good conditions of chaining variables to ensure differential paths hold

- Message modification techniques (**Relevant to SHA1**)

∧ = AND
∨ = OR
⊕ = XOR