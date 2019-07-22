# instance/config Application Configuration
    
SECRET_KEY = "Thisissupposedtobesecret!" #.from_object('config.DevelopmentConfig') # was (config.Config')
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:245353f10I@localhost/postgres"
SQLALCHEMY_TRACK_MODIFICATIONS = False