from hashlib import sha256

class SHA256HashService:
    def hash(self, value: str) -> str:
        return sha256(value.encode()).hexdigest()

    def verify(self, plain: str, hashed: str) -> bool:
        return self.hash(plain) == hashed