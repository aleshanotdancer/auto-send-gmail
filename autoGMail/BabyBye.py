import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

def get_secret_baby():
    """
    Reads the key and encrypted string from .env 
    and returns the plain-text baby (p).
    """
    try:
        key = os.getenv("BABY_KEY").encode()
        encrypted_baby = os.getenv("ENCRYPTED_BABY").encode()
        
        cipher_suite = Fernet(key)
        decoded_baby = cipher_suite.decrypt(encrypted_baby).decode()
        
        return decoded_baby
    except Exception as e:
        # Keeping error messages vague to stay stealthy
        print(f"Baby Error: Check the nursery. {e}")
        return None
