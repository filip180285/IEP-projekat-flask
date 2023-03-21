from flask import Flask;
from flask_migrate import Migrate, MigrateCommand, init, migrate, upgrade;
from flask_script import Manager;
from configuration import Configuration;
from models import database, User, Role, UserRole;
from sqlalchemy_utils import database_exists, create_database;

application = Flask ( __name__ );
application.config.from_object ( Configuration );

migrateObject = Migrate ( application, database );

#manager = Manager ( application );
#manager.add_command ( "db", MigrateCommand );

done = False;
while ( done == False ):
    try:
        if ( not database_exists ( application.config["SQLALCHEMY_DATABASE_URI"] ) ):
            create_database ( application.config["SQLALCHEMY_DATABASE_URI"] );

        database.init_app ( application );

        with application.app_context ( ) as context:
            init ( );
            migrate ( message = "Production migration" );
            upgrade ( );

            adminRole = Role ( name = "admin" );
            workerRole = Role ( name = "worker" );
            buyerRole = Role ( name = "buyer" );

            database.session.add ( adminRole );
            database.session.add( workerRole );
            database.session.add ( buyerRole );
            database.session.commit ( );

            admin = User (
                    forename = "admin",
                    surname = "admin",
                    email = "admin@admin.com",
                    password = "1",
                    isCustomer = 0
            );

            database.session.add ( admin );
            database.session.commit ( );

            role = Role.query.filter( Role.name == "admin" ).first( );
            userRole = UserRole( userId = admin.id, roleId = role.id );

            database.session.add( userRole );
            database.session.commit( );

            done = True;

    except Exception as error:
        print( error );
