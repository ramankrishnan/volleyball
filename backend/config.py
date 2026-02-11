import os

class Config:
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_NAME = os.environ.get('DB_NAME', 'volleyball_db')
    DB_USER = os.environ.get('DB_USER', 'volleyball_user')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'volleyball_pass')
    
    @staticmethod
    def get_db_url():
        return f"host={Config.DB_HOST} port={Config.DB_PORT} dbname={Config.DB_NAME} user={Config.DB_USER} password={Config.DB_PASSWORD}"