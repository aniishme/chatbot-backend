from fastapi import Request, HTTPException
from jose import JWTError, jwt

from variables import SECRET_KEY, ALGORITHM

async def is_auth(request: Request):
    print(SECRET_KEY, ALGORITHM)
    token = request.headers.get('Authorization')
    if token is None:
        print(token)
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        print("payload")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Not authenticated")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Not authenticated")

