#!~/PycharmProjects/__VENV__/venv_nyxae/bin/python

from app.SamCrypto.Cipher import AES
from app.db_struct import db_insert
import random
import struct
import uuid
import os

__author__ = "salmansamie"


def store_logic(path_fname, timer):
    real_path = path_fname + '.zip'
    user_timer = timer
    rbitsize = [uuid.uuid4().hex, uuid.uuid4().hex[:-8], uuid.uuid4().hex[:-16]]
    _vault_key = random.choice(rbitsize)
    try:
        encrypt_file(_vault_key, real_path)
        real_path = real_path + '.enc'
    finally:
        db_insert(real_path, user_timer, _vault_key)

    '''
    TODO:
    Choose ENC logic arbitrarily and encrypt, set a flag for the ENC.
    Send to db new table > ENC flag, key)
    '''
    return _vault_key


def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):

    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                elif len(chunk) % 16 != 0:
                    chunk += bytes(16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))


def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):

    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)
