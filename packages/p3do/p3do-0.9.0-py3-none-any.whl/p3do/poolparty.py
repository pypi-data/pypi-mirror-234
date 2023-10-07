#!/usr/bin/env python3

from io import FileIO
import os

import json
from typing import TextIO
import requests
import textwrap
from pathlib import Path
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
import subprocess

from base64 import b64encode, b64decode

from cryptography.hazmat.primitives.hashes import SHA1
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives.ciphers.algorithms import AES

from loguru import logger

from flask import Flask, request
from rich import print


@logger.catch
def encrypt(clear: str, password, salt, strength) -> str:
    logger.info("Initializing encryption algorithm")
    kdf = PBKDF2HMAC(
        algorithm=SHA1(),
        # get bit need byte
        length=strength//8,
        # standard salt as used in `EncryptionService.java`
        salt=bytes(salt, "utf-8"),
        # always 1024, hardcoded in `EncryptionService.java`
        iterations=1024
    )

    logger.info("Deriving key and initializaiton vector")
    # errors on purpose if encryption.password does not exist
    key = kdf.derive(bytes(password, "utf-8"))
    iv = os.urandom(16) # always 16, hardcoded in `EncryptionService.java`

    logger.info("Padding clear text")
    padder = PKCS7(16*8).padder() # know bytes need bits, AES blocksize must be == iv length
    ct_padded = padder.update(bytes(clear, "utf-8")) + padder.finalize()

    logger.info("Encrypting clear text")
    encryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()
    ct = encryptor.update(ct_padded) + encryptor.finalize()

    logger.info("Encoding encrypted byte sequence")
    return str(b64encode(iv+ct), "utf-8")

@logger.catch
def decrypt(secret: str, password, salt, strength) -> str:
    logger.info("Initializing encryption algorithm")
    kdf = PBKDF2HMAC(
        algorithm=SHA1(),
        # get bit need byte
        length=strength//8,
        # standard salt as used in `EncryptionService.java`
        salt=bytes(salt, "utf-8"),
        # always 1024, hardcoded in `EncryptionService.java`
        iterations=1024
    )

    logger.info("Deriving key and initializaiton vector")
    # errors on purpose if encryption.password does not exist
    key = kdf.derive(bytes(password, "utf-8"))
    secret_bytes = b64decode(secret)
    iv, secret_bytes = (secret_bytes[:16], secret_bytes[16:])

    logger.info("Decrypting secret text")
    decryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    ct = decryptor.update(secret_bytes) + decryptor.finalize()

    logger.info("Un-padding clear text")
    unpadder = PKCS7(16*8).unpadder() # know bytes need bits, AES blocksize must be == iv length
    ct_unpadded = unpadder.update(ct) + unpadder.finalize()

    logger.info("Decode clear text bytes")
    return ct_unpadded.decode("utf-8")

def install_snapshot(path: Path):
    filename = 'PoolParty_integrator_9.0.0-SNAPSHOT-CD.run'
    url = f'https://sys-repo-prod.semantic-web.at/repo/poolparty/releases_rhel7/Integrator/8.2.0-SNAPSHOT/Linux/{filename}'

    response = requests.get(url, stream=True)

    block_size = 32768
    total_size_in_bytes= int(response.headers.get('content-length', 0))

    download_path = path.joinpath(filename)

    with Progress(TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
                           BarColumn(bar_width=None),
                           "[progress.percentage]{task.percentage:>3.1f}%",
                           "•",
                           DownloadColumn(),
                           "•",
                           TransferSpeedColumn(),
                           "•",
                           TimeRemainingColumn(),
                           ) as progress:

        task_id = progress.add_task("download", filename=download_path, total=total_size_in_bytes)

        with open(download_path, "wb") as out:
            for chunk in response.iter_content(block_size):
                if chunk:
                    out.write(chunk)
                    progress.update(task_id, advance=len(chunk), refresh=True)

    download_path.chmod(0o500)
    subprocess.call(["/bin/env", "sh", "-c", f"{download_path}"])


def run_mock_server(port):
    app = Flask(__name__)

    @app.post("/hook")
    def webhook():
        logger.info("Webhook triggered")
        print(request)
        print(request.headers)
        print(json.loads(request.data))
        return ""

    @app.get("/hook")
    def webhook_healthcheck():
        return ""

    app.run(debug=True, port=port)


def decrypt_license(license_file, key):
    logger.info("Reading license data and stripping slack")
    license_data = ""
    for line in license_file:
        if not "---" in line:
            license_data += line.strip()

    logger.info("Decoding license data")
    license_data = b64decode(license_data)

    logger.info("Setting up decryption algorithm")
    aes = algorithms.AES(b64decode(key))
    cipher = Cipher(aes, modes.ECB())
    decryptor = cipher.decryptor()

    logger.info("Decrypting license")
    license_data = decryptor.update(license_data) + decryptor.finalize()

    logger.info("Unpadding license")
    unpadder = PKCS7(16*8).unpadder()
    license_data = unpadder.update(license_data) + unpadder.finalize()

    return license_data.decode('utf-8')

def encrypt_license(license_file, key):
    logger.info("Reading license data")
    license_data = license_file.read()

    logger.info("Padding data")
    padder = PKCS7(16*8).padder()
    license_data = padder.update(bytes(license_data, 'utf8')) + padder.finalize()

    logger.info("Setting up encryption algorithm")
    aes = algorithms.AES(b64decode(key))
    cipher = Cipher(aes, modes.ECB())
    encryptor = cipher.encryptor()

    logger.info("Encrypting license data")
    license_data = encryptor.update(license_data) + encryptor.finalize()

    logger.info("Encoding license data")
    license_data = b64encode(license_data)

    logger.info("Finalizing license")
    license_data = textwrap.fill(license_data.decode('utf8'), 75)
    license_data = f"--- BEGIN LICENSE KEY ---\n{license_data}\n--- END LICENSE KEY ---"

    return license_data
