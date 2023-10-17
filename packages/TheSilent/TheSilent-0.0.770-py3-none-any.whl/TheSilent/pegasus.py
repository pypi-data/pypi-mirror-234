import hashlib
import os

def pegasus(init_hash,file):
    words = []
    if os.path.isfile(file):
        with open(file,"r") as f:
            for _ in f:
                words.append(_.replace("\n",""))

    if not os.path.isfile(file):
        files = os.listdir(file)
        for ff in files:
            with open(file + "/" + ff,"rb") as f:
                for _ in f:
                    words.append(_.decode(errors="ignore").replace("\n",""))

    for word in words:
        if hashlib.md5(word.encode()).hexdigest() == init_hash:
            return word

        if hashlib.sha1(word.encode()).hexdigest() == init_hash:
            return word

        if hashlib.sha224(word.encode()).hexdigest() == init_hash:
            return word

        if hashlib.sha256(word.encode()).hexdigest() == init_hash:
            return word

        if hashlib.sha384(word.encode()).hexdigest() == init_hash:
            return word

        if hashlib.sha512(word.encode()).hexdigest() == init_hash:
            return word

        if hashlib.sha3_224(word.encode()).hexdigest() == init_hash:
            return word

        if hashlib.sha3_256(word.encode()).hexdigest() == init_hash:
            return word

        if hashlib.sha3_384(word.encode()).hexdigest() == init_hash:
            return word

        if hashlib.sha3_512(word.encode()).hexdigest() == init_hash:
            return word
