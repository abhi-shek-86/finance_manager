import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER','root')}:"
        f"{os.getenv('DB_PASSWORD','password')}@"
        f"{os.getenv('DB_HOST','localhost')}/"
        f"{os.getenv('DB_NAME','finance_db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
