import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

load_dotenv()
PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")
if not PUBLIC_KEY:
    raise RuntimeError("DISCORD_PUBLIC_KEY is not set")

try:
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
except ValueError as e:
    raise RuntimeError("DISCORD_PUBLIC_KEY is not valid hex") from e

def verify_discord_signature(request: Request, body: bytes) -> None:
    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")
    print(signature)
    print(timestamp)

    if not signature or not timestamp:
        raise HTTPException(status_code=401, detail="Missing Discord signature headers")

    try:
        verify_key.verify(timestamp.encode() + body, bytes.fromhex(signature))
    except BadSignatureError:
        raise HTTPException(status_code=401, detail="Invalid request signature")