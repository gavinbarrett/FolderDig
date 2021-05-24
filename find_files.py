from os import path, walk
from hashlib import sha256


def get_signature(target_path):
	if path.isdir(target_path):
		# path is a directory; open directory and recur through files/directories
		return None
	elif path.isfile(target_path):
		# default to hashing single file
		f = open(target_path, 'rb')
		digest = sha256(f.read()).hexdigest()
		print(digest)
	return None

def sign_directory(target_path):
	try:
		if path.exists(target_path):
			signature = get_signature(target_path)
			print(signature)
		else:
			raise Exception(f"Path `{target_path}` doesn't exist.")
	except Exception as err:
		print(err)

if __name__ == "__main__":
	sign_directory("/home/gavin/Development/MerkleHashTree/target/hello.txt")
