import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

load_dotenv()
PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")

verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

def verify_discord_signature(request: Request, body: bytes) -> None:
    signature = request.headers["X-Signature-Ed25519"]
    timestamp = request.headers["X-Signature-Timestamp"]
    print(signature)
    print(timestamp)

    if not signature or not timestamp:
        raise HTTPException(status_code=401, detail="Missing Discord signature headers")

    try:
        verify_key.verify(timestamp.encode() + body, bytes.fromhex(signature))
    except BadSignatureError:
        raise HTTPException(status_code=401, detail="Invalid request signature")