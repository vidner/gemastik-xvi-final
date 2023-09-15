import hmac
import json
from base64 import urlsafe_b64encode, urlsafe_b64decode
from hashlib import sha224, sha256, sha384, sha512
from ecdsa import SigningKey, NIST256p, NIST224p, NIST384p, NIST521p

allowed_curve = [
    NIST224p,
    NIST256p,
    NIST384p,
    NIST521p
]

hashfunc = [
    sha224,
    sha256,
    sha384,
    sha512
]

key_size = [28, 32, 48, 66]
signature_size = [56, 64, 96, 132]


class PastaSigner:
    def __init__(self, secret: bytes, version: int):
        self.purpose = 'public'
        if version > 4 or version < 1:
            version = 1
        self.version = version
        self.hashfunc = hashfunc[self.version - 1]
        self.key_size = key_size[self.version - 1]
        self.priv = SigningKey.from_string(secret[:self.key_size], curve=allowed_curve[self.version - 1])

    def serialize(self, data: bytes, sig):
        token = 'v' + str(self.version) + '.'
        token += self.purpose + '.'
        token += urlsafe_b64encode(data + sig).decode().replace('=', '')
        return token

    def sign(self, data: str):
        data = data.encode()
        pub = self.priv.get_verifying_key().to_string()
        h = self.hashfunc(data + pub).digest()
        nonce = hmac.new(self.priv.to_string(), data, self.hashfunc).hexdigest()
        sig = self.priv.sign_digest(h, k=int(nonce, 16))

        return self.serialize(data + pub, sig)


class PastaVerifier:

    def __init__(self, secret):
        self.purpose = 'public'
        self.secret = secret

    def deserialize(self, data: bytes):
        try:
            version, purpose, payload = data.split(b'.')
            version = int(version.replace(b'v', b''))
            if version > 4 or version < 1:
                return False
            self.version = version
            self.hashfunc = hashfunc[self.version - 1]
            self.key_size = key_size[self.version - 1]
            self.priv = SigningKey.from_string(self.secret[:self.key_size], curve=allowed_curve[self.version - 1])

            raw_data = urlsafe_b64decode(payload + (b'==' * 2))
            size = signature_size[self.version - 1]
            signature = raw_data[-size:]
            public_key = raw_data[-size * 2:-size]
            message = raw_data[:-size]

            return message, raw_data[:-size * 2], signature
        except Exception as e:
            return False

    def verify(self, token: str):
        deserialized = self.deserialize(token.encode())
        if deserialized:
            message, plain_data, signature = deserialized
            h = self.hashfunc(message).digest()
            verifier = self.priv.get_verifying_key()
            verifier.verify_digest(signature, h)

            return json.loads(plain_data)

        return False
