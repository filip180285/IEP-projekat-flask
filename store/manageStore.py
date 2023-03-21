from flask import Flask;
from flask_migrate import Migrate, MigrateCommand, init, migrate, upgrade;
from flask_script import Manager;
from configurationStore import Configuration;
from modelsStore import database;
from sqlalchemy_utils import database_exists, create_database;

application = Flask ( __name__ );
application.config.from_object ( Configuration );

migrateObject = Migrate ( application, database );

#manager = Manager ( application );
#manager.add_command ( "db", MigrateCommand );

done = False;
while( done == False ):
    try:
        if ( not database_exists ( application.config["SQLALCHEMY_DATABASE_URI"] ) ):
            create_database ( application.config["SQLALCHEMY_DATABASE_URI"] );

        database.init_app ( application );

        with application.app_context ( ) as context:
            init ( );
            migrate ( message = "Production migration" );
            upgrade ( );

            done = True;

    except Exception as error:
        print(error);
