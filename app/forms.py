from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

try:
    password = os.urandom(64)
    print("created default user")
    print("username: admin")
    print("password: " + password)
    
    users = {
        "admin": generate_password_hash(password)
    }

    file = open("auth.conf", "r")
    lines = file.readlines()

    for line in lines:
        new_user = line.split(",", 1)
        user[new_user[0]] = generate_password_hash(new_user[1])

except FileNotFoundError as e:
    print(e)

    password = os.urandom(64)
    print("auth.conf not found, created default user")
    print("username: admin")
    print("password: " + password)
    
    users = {
        "admin": generate_password_hash(password)
    }

finally:
    file.close()



@auth.verify_password
def verify_password(username, password, allowed):
    if username in users and username in allowed and \
            check_password_hash(users.get(username), password):
        return username