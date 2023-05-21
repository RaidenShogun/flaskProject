class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'  # 使用单独的数据库进行测试
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SECRET_KEY = 'your-secret-key'
    LOGIN_DISABLED = False