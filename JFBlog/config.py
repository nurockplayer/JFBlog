class Config(object):
    """Base config class."""
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'StiJumpDog'

    # RECAPTCHA_ENABLED = True
    RECAPTCHA_PUBLIC_KEY = '6LfZWncUAAAAAJwg2hdtLOorE83QuLVF4UJHHS6q'
    RECAPTCHA_PRIVATE_KEY = '6LfZWncUAAAAADsKdu2MhpGNMk31pi4c1V_shHzF'


class ProdConfig(Config):
    """Production config class."""
    pass


class DevConfig(Config):
    """Development config class."""
    # Open the DEBUG
    DEBUG = True
    # MySQL connection
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://tachikoma:PostgreSQL10isSoGood!@localhost:3306/jfblog?charset=utf8'
