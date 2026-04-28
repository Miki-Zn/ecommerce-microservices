from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt


SECRET_KEY = "my-super-secret-jwt-key-for-microservices"
ALGORITHM = "HS256"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8001/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    """Расшифровывает токен и возвращает ID пользователя"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token format")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")