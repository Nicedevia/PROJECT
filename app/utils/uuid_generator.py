import uuid
from hashlib import sha256

def generate_deterministic_uuid(latitude, longitude):
    """
    Génère un UUID déterministe basé sur les valeurs de latitude et longitude.
    """
    # Combine latitude et longitude pour créer un hash unique
    hash_input = f"{latitude},{longitude}".encode('utf-8')
    # Crée un UUID à partir du hash SHA256
    return uuid.UUID(sha256(hash_input).hexdigest()[:32])
