from werkzeug.security import generate_password_hash
import sys

password = generate_password_hash(sys.argv[1])
print(password)