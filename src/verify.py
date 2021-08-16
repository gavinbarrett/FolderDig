from hashlib import sha256
from binascii import unhexlify

GREEN = '\u001b[32m'
RED = '\u001b[31m'
END = '\033[0m'

def verify(proof):
	root_tag = list(proof.keys())[0]
	if verify_proof(proof).hex() == root_tag:
		print(f'{GREEN}Filesystem integrity maintained.{END}')
	else:
		print(f'{RED}Filesystem integrity compromised.{END}')

def verify_proof(proof):
	subproof = list(proof.keys())[0]
	if not proof[subproof] or proof[subproof] == True: return unhexlify(subproof)
	return sha256(b''.join([verify_proof(child) for child in proof[subproof]])).digest()