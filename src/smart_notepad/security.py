from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
from typing import Any


PREFIX = "sni1:"
KDF = "pbkdf2_sha256"
ITERATIONS = 390_000
SALT_BYTES = 16
NONCE_BYTES = 16


class SecurityError(ValueError):
    pass


def create_password_record(password: str) -> dict[str, Any]:
    salt = os.urandom(SALT_BYTES)
    digest = _derive(password, salt, ITERATIONS, 32)
    return {
        "kdf": KDF,
        "iterations": ITERATIONS,
        "salt": _b64(salt),
        "digest": _b64(digest),
    }


def verify_password(password: str, record: dict[str, Any] | None) -> bool:
    if not record:
        return False
    salt = _unb64(record["salt"])
    iterations = int(record.get("iterations", ITERATIONS))
    expected = _unb64(record["digest"])
    actual = _derive(password, salt, iterations, len(expected))
    return hmac.compare_digest(actual, expected)


def is_encrypted(value: str) -> bool:
    return value.startswith(PREFIX)


def encrypt_text(plaintext: str, password: str) -> str:
    salt = os.urandom(SALT_BYTES)
    nonce = os.urandom(NONCE_BYTES)
    key_material = _derive(password, salt, ITERATIONS, 64)
    enc_key = key_material[:32]
    mac_key = key_material[32:]
    data = plaintext.encode("utf-8")
    ciphertext = _xor(data, _keystream(enc_key, nonce, len(data)))
    payload: dict[str, Any] = {
        "v": 1,
        "kdf": KDF,
        "iterations": ITERATIONS,
        "salt": _b64(salt),
        "nonce": _b64(nonce),
        "ciphertext": _b64(ciphertext),
    }
    payload["mac"] = _b64(_mac(mac_key, payload))
    return PREFIX + _b64(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def decrypt_text(payload: str, password: str) -> str:
    if not is_encrypted(payload):
        return payload
    try:
        raw = json.loads(_unb64(payload[len(PREFIX) :]).decode("utf-8"))
        salt = _unb64(raw["salt"])
        nonce = _unb64(raw["nonce"])
        ciphertext = _unb64(raw["ciphertext"])
        iterations = int(raw.get("iterations", ITERATIONS))
        key_material = _derive(password, salt, iterations, 64)
        enc_key = key_material[:32]
        mac_key = key_material[32:]
        expected_mac = _unb64(raw["mac"])
    except (KeyError, ValueError, json.JSONDecodeError) as exc:
        raise SecurityError("Payload criptografado invalido.") from exc

    if not hmac.compare_digest(expected_mac, _mac(mac_key, raw)):
        raise SecurityError("Senha incorreta ou dados criptografados alterados.")

    plaintext = _xor(ciphertext, _keystream(enc_key, nonce, len(ciphertext)))
    return plaintext.decode("utf-8")


def _derive(password: str, salt: bytes, iterations: int, length: int) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations, dklen=length)


def _mac(mac_key: bytes, payload: dict[str, Any]) -> bytes:
    signed = {key: value for key, value in payload.items() if key != "mac"}
    message = json.dumps(signed, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hmac.new(mac_key, message, hashlib.sha256).digest()


def _keystream(key: bytes, nonce: bytes, length: int) -> bytes:
    blocks: list[bytes] = []
    counter = 0
    while sum(len(block) for block in blocks) < length:
        counter_bytes = counter.to_bytes(8, "big")
        blocks.append(hmac.new(key, nonce + counter_bytes, hashlib.sha256).digest())
        counter += 1
    return b"".join(blocks)[:length]


def _xor(left: bytes, right: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(left, right))


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii")


def _unb64(data: str) -> bytes:
    return base64.urlsafe_b64decode(data.encode("ascii"))

