from fastapi import Request, HTTPException
from jose import JWTError, jwt

from model.schemas import UserToken
from variables import SECRET_KEY, ALGORITHM



async def is_auth(request: Request):
    print(SECRET_KEY, ALGORITHM)
    token = request.headers.get('Authorization')
    if token is None:
        print(token)
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)

        
        user: str = payload.get("email")
        if user is None:
            raise HTTPException(status_code=401, detail="Not authenticated")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Not authenticated")

