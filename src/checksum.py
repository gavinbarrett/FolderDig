from hashlib import sha256
from os import path, listdir
from binascii import hexlify

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