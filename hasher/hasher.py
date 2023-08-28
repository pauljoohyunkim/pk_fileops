import hashlib
import sys

BUFSIZ = 65536

def sha256_hexdigest(filename : str, chunk=BUFSIZ):
    try:
        with open(filename, "rb") as file:
            sha256 = hashlib.sha256()
            while True:
                data = file.read(chunk)
                if not data:
                    break
                sha256.update(data)
            file.close()
        
        return sha256.hexdigest()
    except FileNotFoundError:
        sys.stderr.write(f"{filename} not found")
        sys.stderr.flush()
