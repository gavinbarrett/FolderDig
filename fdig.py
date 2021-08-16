from os import path
from sys import argv
from hashlib import sha256
from json import dumps, loads
from src.parser import arg_parser
from src.prove import prove, compute_proof
from src.verify import verify, verify_proof
from src.checksum import checksum, compute_checksum

if __name__ == "__main__":
	arg_length = len(argv)
	args = arg_parser(arg_length)
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
					verify(argv[1], proof)
		else:
			print('Please enter valid arguments.\nRun `python fdig.py -h` for help')