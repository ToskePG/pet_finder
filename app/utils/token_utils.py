import jwt
from datetime import datetime, timedelta
from ..security.auth import SECRET_KEY, ALGORITHM

def create_confirmation_token(email: str):
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode = {"exp": expire, "sub": email}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)