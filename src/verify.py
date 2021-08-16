from hashlib import sha256
from os import path, listdir
from binascii import unhexlify

GREEN = '\u001b[32m'
RED = '\u001b[31m'
END = '\033[0m'

def verify(target_path, proof):
	root_tag = list(proof.keys())[0]
	try:
		if verify_proof(target_path, proof).hex() == root_tag:
			print(f'{GREEN}Filesystem integrity maintained.{END}')
		else:
			print(f'{RED}Filesystem integrity compromised.{END}')
	except ValueError as error:
		print(f'{RED}{error}{END}')

def verify_proof(target_path, proof):
	# grab the current node hash from the proof
	subproof = list(proof.keys())[0]
	# if we have a file, generate its hash along with a boolean for whether or not it matches
	if path.isfile(target_path):
		# return the sha256 hash of the file
		with open(target_path, 'rb') as new_file:
			digest = sha256(new_file.read()).digest()
			if subproof != digest.hex(): raise ValueError(f'Incorrect tag for {target_path}')
			return digest
	elif path.isdir(target_path):
		# call sign on every file in the directory
		return sha256(b''.join([verify_proof(path.join(target_path, file), subp) for file, subp in zip(listdir(target_path), proof[subproof])])).digest()