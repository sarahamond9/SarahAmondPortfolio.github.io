#Sarah Amond
import string
import secrets

def generate_password(length=16):
    # Combine all characters: lowercase, uppercase, digits, and symbols
    alphabet = string.ascii_letters + string.digits + string.punctuation
    
    # Securely select characters randomly for the specified length
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

# Generate a 16-character secure password
print("Your secure password is:", generate_password(16))
