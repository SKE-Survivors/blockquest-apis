from decouple import config

SECRET_KEY = config('SECRET_KEY').encode('utf-8')

GOOGLE_CLIENT_ID = config("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = config("GOOGLE_CLIENT_SECRET")