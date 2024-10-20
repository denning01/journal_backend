import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:your_password@localhost/test')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
