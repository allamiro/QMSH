import os 

class Config:
    SECRET_KEY = "your-secret-key"
    SQLALCHEMY_DATABASE_URI = "postgresql://admin:secret@db:5432/qmsh"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
