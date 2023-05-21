class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SECRET_KEY = 'your-secret-key'
    LOGIN_DISABLED = False