import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
MODEL_PATH = os.getenv('MODEL_PATH')
CONFIG_PATH = os.getenv('CONFIG_PATH')
STYLE_PATH = os.getenv('STYLE_PATH')
EXCEPT_BOTS = os.getenv('EXCEPT_BOTS')
LOGGING = os.getenv('LOGGING') == 'True' or os.getenv('LOGGING') == 'true'
