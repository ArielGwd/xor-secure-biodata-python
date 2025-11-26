from dotenv import load_dotenv
import os

load_dotenv()  

SECRET_KEY = os.getenv("APP_SECRET_XOR_KEY", 'lah')
DB_USER = os.getenv("DATABASE_USER", "root")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_PORT = os.getenv("DATABASE_PORT", "3306")
DB_NAME = os.getenv("DATABASE_NAME", "db_secure_xor")

# PERBAIKAN: Menggunakan mysqlconnector
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"