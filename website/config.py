import os

# Secret key (environment variable takes precedence)
SECRET_KEY = os.getenv("SECRET_KEY", "aabbccddeeffgghhiijjkkllmmnnoopp112233445566778899")

# Database URI
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///quizme.db")

# MongoDB URI
MONGO_URI = os.getenv("MONGO_URL", "mongodb://root:password@localhost:27017/quizme")

# Disable SQLAlchemy event system to improve performance
SQLALCHEMY_TRACK_MODIFICATIONS = False