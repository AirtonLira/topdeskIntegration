import os
from dotenv import load_dotenv
load_dotenv()

URL_TARGET = os.getenv("URL_TARGET")
URL_SLACK_BOT = os.getenv("URL_SLACK_BOT")