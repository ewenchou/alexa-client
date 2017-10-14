import os

CLIENT_ID = os.environ['ALEXA_CLIENT_ID']
CLIENT_SECRET = os.environ['ALEXA_CLIENT_SECRET']
PRODUCT_ID = os.environ['ALEXA_PRODUCT_ID']
REFRESH_TOKEN = os.environ['ALEXA_REFRESH_TOKEN']
WEB_PORT = int(os.environ['ALEXA_PORT']) or 3000
