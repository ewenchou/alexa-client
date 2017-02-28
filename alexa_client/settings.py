import os
import uuid

DEVICE_TYPE_ID = uuid.getnode()
CLIENT_ID = os.environ['ALEXA_CLIENT_ID']
CLIENT_SECRET = os.environ['ALEXA_CLIENT_SECRET']
REFRESH_TOKEN = os.environ['ALEXA_REFRESH_TOKEN']
