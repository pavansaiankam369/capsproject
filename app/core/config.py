import os

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:pavan%402003@localhost:3306/pavan_db")
SECRET_KEY = os.getenv("SECRET_KEY", "your_super_secret_key_here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
