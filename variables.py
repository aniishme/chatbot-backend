import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")