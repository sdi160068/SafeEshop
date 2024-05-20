import base64
import hmac
import json
import hashlib
import datetime

from auth.models import Token
from secureProject import settings

def encode_jwt(payload):
    # Add expiration time to the payload
    exp = datetime.datetime.now() + datetime.timedelta(minutes=120)
    payload['exp'] = exp.isoformat()    
    # Encode the payload as JSON
    encoded_payload = json.dumps(payload)

    # Encode the header and payload as base64
    header_payload = base64.urlsafe_b64encode(encoded_payload.encode()).decode()

    # Create a signature using HMAC and the secret key
    signature = hmac.new(settings.SECRET_KEY.encode(), header_payload.encode(), hashlib.sha256).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).decode()

    # Concatenate the header, payload, and signature with dots
    jwt_token = f"{header_payload}.{encoded_signature}"

    return jwt_token

def decode_jwt(token):
    try:
        # Split the token into header, payload, and signature
        header_payload, signature = token.split('.')
        
        # Verify the signature using the secret key
        expected_signature = base64.urlsafe_b64encode(hmac.new(settings.SECRET_KEY.encode(), header_payload.encode(), hashlib.sha256).digest()).decode()

        # Check if the signature matches
        if expected_signature == signature:
            # Decode the payload
            decoded_payload = base64.urlsafe_b64decode(header_payload.encode()).decode()
            payload = json.loads(decoded_payload)

            # Check if the token is expired
            if datetime.datetime.now() < datetime.datetime.fromisoformat(payload['exp']):
               return payload
    except:
        pass

    # If any error occurs or token is invalid, return None
    return None

def validate_token(token):
    token_obj = Token.objects.filter(token=token).first()

    if token_obj == None :
        return None

    paylaod = decode_jwt(token)

    if paylaod == None :
        token_obj.delete()
    
    return paylaod