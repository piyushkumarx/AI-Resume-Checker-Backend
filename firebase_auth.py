import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Header

# initialize firebase once
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)


def verify_firebase_token(authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.split(" ")[1]

    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")