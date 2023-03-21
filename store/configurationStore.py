#import os;
#
#databaseUrl = os.environ["DATABASE_URL"];
#
#class Configuration ( ):
#    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@{databaseUrl}/store";
#    JWT_SECRET_KEY = "JWT_SECRET_KEY";
#    REDIS_HOST = "redis";

from datetime import timedelta;

class Configuration ( ):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3307/store";
    JWT_SECRET_KEY = "JWT_SECRET_KEY";
    REDIS_HOST = "localhost";