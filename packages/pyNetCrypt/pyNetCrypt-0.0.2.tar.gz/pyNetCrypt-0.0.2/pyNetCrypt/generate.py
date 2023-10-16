


import hashlib
# ------------------------------------------------------------------------------


def get_md5(file):
	"""create and return md5 hash for given file

	Args:
		file (str): input file

	Returns:
		str: MD5 hash value
	"""	
	chunk = 8192
	with open(file, 'rb') as f:
		_hash = hashlib.md5()
		c = f.read(chunk)
		while c:
			_hash.update(c)
			c = f.read(chunk)
	return _hash.hexdigest()

