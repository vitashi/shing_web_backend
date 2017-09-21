import os
import hashlib
from string import upper

def to_upper(text):
	return upper(text)


def getSHA(pw, salt=None):
    if not salt:
        salt= os.urandom(32).encode('hex')
    sha = hashlib.sha256()
    sha.update((pw + salt).encode('utf-8'))
    pw_sha=sha.hexdigest()
    return salt, pw_sha