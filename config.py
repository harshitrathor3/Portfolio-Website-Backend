import os

from dotenv import load_dotenv

try:
    ENV = os.environ["ENV"]
except Exception:
    print("Using local env")
    load_dotenv("config_local.env")


############### MYSQL #################
MYSQL_USERNAME = os.environ["MYSQL_USERNAME"]
MYSQL_HOSTNAME = os.environ["MYSQL_HOSTNAME"]
MYSQL_DATABASE = os.environ["MYSQL_DATABASE"]
MYSQL_PASSWORD = os.environ["MYSQL_PASSWORD"]
MYSQL_PORT = os.environ["MYSQL_PORT"]
MYSQL_URL = f"mysql+asyncmy://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}/{MYSQL_DATABASE}"


############### CLOUDINARY #################
CLOUDINARY_CLOUD_NAME = os.environ["CLOUDINARY_CLOUD_NAME"]
CLOUDINARY_API_KEY = os.environ["CLOUDINARY_API_KEY"]
CLOUDINARY_API_SECRET = os.environ["CLOUDINARY_API_SECRET"]

