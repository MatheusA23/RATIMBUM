import os

class Config:
    SECRET_KEY = 'hotel-ratimbum-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
