import random
import string
import secrets

def generate_confirmation_code(length=8):
    """Generate a random confirmation code."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Generate token
def generate_token():
    return secrets.token_urlsafe(16)