import configparser
from cryptography.fernet import Fernet

config = configparser.ConfigParser()
config.read("moodle.conf")
key = config.get("credentials", 'key')
encpassword = config.get("credentials", 'password')
fernet = Fernet(bytes(key,  encoding='utf8'))
password = fernet.decrypt(encpassword).decode()
print(password)
print(key)
