from sys import argv
from hashlib import sha256
from os import listdir, path
from json import dumps, loads
from binascii import hexlify, unhexlify
from argparse import ArgumentParser
from collections import defaultdict

def compute_proof(target_path, tag):
	if path.exists(target_path):
		return prove(target_path, tag)
	else:
		raise Exception(f"Path `{target_path}` doesn't exist.")

def prove(target_path, tag):
	if path.isfile(target_path):
		with open(target_path, 'rb') as new_file:
			digest = sha256(new_file.read()).hexdigest()
			return {digest: True} if (digest == tag) else {digest: False}
	elif path.isdir(target_path):
		# compute the tags of everything on this level
		digest_dict = [prove(path.join(target_path, file), tag) for file in listdir(target_path)]
		parent_tag = sha256(unhexlify(''.join([list(payload.keys())[0] for payload in digest_dict]))).hexdigest()
		# search for tag query in the list of digests
		if tag in digest_dict:
			return {parent_tag: digest_dict}
		# check for a dictionary among the values of the digest_dict
		if any(list(filter(lambda d: list(d.values())[0], digest_dict))):
			return {parent_tag: digest_dict}
		# branch does not contain the target file
		return {parent_tag: False}
	else:
		raise ValueError(f"Target path: <{target_path}> is not a file.")
		
def verify(proof):
	root_tag = list(proof.keys())[0]
	return verify_proof(proof).hex() == root_tag

def verify_proof(proof):
	subproof = list(proof.keys())[0]
	if not proof[subproof] or proof[subproof] == True: return unhexlify(subproof)
	return sha256(b''.join([verify_proof(child) for child in proof[subproof]])).digest()

def compute_checksum(target_path, full=False):
	if path.exists(target_path):
		signature = checksum(target_path, full)
		print(f'{hexlify(signature).decode()}\t{target_path}')
	else:
		raise Exception(f"Path `{target_path}` doesn't exist.")

def checksum(target_path, full=False):
	if path.isfile(target_path):
		# return the sha256 hash of the file
		with open(target_path, 'rb') as new_file:
			digest = sha256(new_file.read()).digest()
			if full: print(f'{digest.hex()}:	{target_path}')
			return digest
	elif path.isdir(target_path):
		# call sign on every file in the directory
		digest = sha256(b''.join([checksum(path.join(target_path, file), full) for file in listdir(target_path)])).digest()
		if full: print(f'{digest.hex()}:	{target_path}')
		return digest
	else:
		raise Exception(f'File type for `{target_path}` unknown.')

def parse_args(arg_length):
	if arg_length <= 3:
		parser = ArgumentParser()
		parser.add_argument('infile', action='store', type=str, help='Please enter a path')
		parser.add_argument('-f', '--full', action='store_true')
		return parser.parse_args()
	else:
		parser = ArgumentParser()
		mode_1 = parser.add_mutually_exclusive_group()
		mode_2 = parser.add_mutually_exclusive_group()
		parser.add_argument('infile', action='store', type=str, help='Please enter a path')
		parser.add_argument('-t', '--tag', type=str, required=True, help='Digest of the file you want a proof of')
		# add arguments for proof mode
		mode_1.add_argument('-p', '--proof', action='store_true')
		mode_1.add_argument('-i' '--input', type=str, help='Input file of the proof')
		# add arguments for verification mode
		mode_2.add_argument('-v', '--verify', action='store_true')
		mode_2.add_argument('-o' '--output', type=str, help='Output file for the proof')
		return parser.parse_args()


if __name__ == "__main__":
	arg_length = len(argv)
	args = parse_args(arg_length)
	if arg_length <= 3:
		compute_checksum(argv[1], True) if args.full else compute_checksum(argv[1], False)
	else:
		if args.proof:
			proof = compute_proof(argv[1], args.tag)
			if args.o__output:
				with open(args.o__output, 'w') as out_file:
					out_file.write(dumps(proof))
			else:
				print(f'Please input an output file for the proof')
				sys.exit(1)
		elif args.verify:
			if args.i__input and path.exists(args.i__input):
				with open(args.i__input, 'r') as in_file:
					proof = loads(in_file.read())
					verification = verify(proof)
					print(verification)
		else:
			print('Please enter valid arguments.\nRun `python fdig.py -h` for help')