from hashlib import sha256
from os import path, listdir
from binascii import unhexlify

RED = '\u001b[31m'
END = '\033[0m'

def compute_proof(target_path, tag):
	if path.exists(target_path):
		return prove(target_path, tag)
	else:
		raise Exception(f"{RED}Path `{target_path}` doesn't exist.{END}")

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