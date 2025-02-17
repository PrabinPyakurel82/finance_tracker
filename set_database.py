from dotenv import load_dotenv
import os

load_dotenv()

name = os.getenv('DATABASE_NAME')
user = os.getenv('USER')
host = os.getenv('HOST')
