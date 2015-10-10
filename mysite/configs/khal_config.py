

# configuration

class Config:
    """
        Class to handle my configuration needs
    """
    SECRET_KEY = '6AA0p[$f//LOLlpw'
    CSRF_ENABLED = True
    DATABASE = "/home/maria/Desktop/ciacicode/khaleesicode/mysite/microblog.db"
    USERNAME = "ciacicode"
    PASSWORD = "KLC!blogpass"
    PER_PAGE = 10
    CSS_FRAMEWORK = "bootstrap3"
    LINK_SIZE = "sm"
    SHOW_SINGLE_PAGE = False
    SERVER_NAME = "localhost.dev:5000"
    SQLALCHEMY_DATABASE_URI = 'sqlite:////home/maria/Desktop/ciacicode/khaleesicode/mysite/fci.db'
    FCICSVPATH = "/home/maria/Desktop/ciacicode/khaleesicode/mysite/static/fci.csv"