# bis-hd-poc
Proof of concept deterministic RSA address generation for Bismuth (https://github.com/hclivess/Bismuth)

Please test. Outputs working keys but should still be considered as proof-of-concept (PoC).

Outputs privkey, pubkey, and address to stdout.

Requirements:
- pycryptodome (DO NOT INSTALL pycrypto)
- numpy==1.11.3+mkl
- pynput==1.3.10

TECHNICAL SPECIFICATIONS
------------------------

Input: 24-word mnemonic seed in BIP39 format (reference implementation here: https://bip32jp.github.io/english/)

Output: Any number of RSA private/public key pairs

Algorithm:
* m = Mnemonic seed of choice; optionally generate using /dev/urandom
* p = User defined passphrase, prefixed by the string "mnemonic"

The master key is derived by 20000 rounds of PBKDF2(m,p) with dkLen of 48 bytes. All strings are utf-8 encoded.

A hierarchial path is constructed according to BIP44 spec (https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki), briefly:

h = m/purpose'/coin_type'/account'/change/address_index

 * purpose = 44
 * coin_type = 209 (officially Bismuth per BIP44)
 * account = user-defined non-negative integer
 * change = 0 or 1
 * address_index = user-defined non-negative integer
 
(NB1: single quotes are suffixed to the purpose, coin_type, and account fields, and not the change or address_index fields, per official BIP44 standard. The BIP44 path does not contain spaces, tabs, or other whitespace.)

(NB2: single Bismuth, like Ethereum, has no concept of change addresses, the change field is typically hardcoded to 0 in most implementations, including the reference.)

The account key is derived by 1 round of PBKDF2(master_key,h) with dkLen of 48 bytes. All strings are utf-8 encoded.

The account key is used in full to seed 48 bytes (first 32 bytes of key, last 16 bytes of IV) of a standard AES-256 (CTR mode) CSPRNG implementation. The first 1536 bytes of the CSPRNG are discarded, for legacy reasons, and the remainder is used to implement a Rabin-Miller primality search with 1000 pre-computed smallest primes. The output tuple is sent to RSA.Construct in the pycryptodome library to create the RSA private and pubkey keypair. The privkey, pubkey, and address along with intermediate master and account keys are output to stdout.
