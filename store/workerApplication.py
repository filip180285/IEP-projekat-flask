from flask import Flask, request, Response;
from configurationStore import Configuration;
from modelsStore import database;
from redis import Redis;
from checkRoleDecorator import roleCheck;
from flask_jwt_extended import JWTManager;
import io;
import json, csv;

application = Flask ( __name__ );
application.config.from_object ( Configuration );
jwt = JWTManager ( application );

@application.route( "/", methods = ["GET"] )
def hello( ):
    return "<h1>Wellcome To Worker Page</h1>";


@application.route ( "/update", methods = ["POST"] )
@roleCheck ( role = "worker" )
def update( ):
    try:
        content = request.files["file"].stream.read( ).decode( "utf-8" );
    except Exception:
        return Response( json.dumps( {"message": "Field file is missing."} ), status = 400 );

    stream = io.StringIO( content );
    reader = csv.reader( stream );

    rowCounter = 0;
    NUMBER_OF_VALUES = 4;

    for row in reader:
        if ( len( row ) != NUMBER_OF_VALUES ):
            return Response( json.dumps( {"message": "Incorrect number of values on line "+ str( rowCounter ) + "."} ), status = 400 );

        try:
            quantityValue =  int( row[2] );
            if ( not quantityValue > 0 ):
                return Response( json.dumps( {"message": "Incorrect quantity on line " + str( rowCounter ) + "."} ), status = 400) ;
        except Exception:
            return Response( json.dumps( {"message": "Incorrect quantity on line " + str(rowCounter) + "."} ), status = 400 );

        try:
            priceValue =  float( row[3] );
            if ( not priceValue > 0 ):
                return Response( json.dumps( {"message": "Incorrect price on line " + str( rowCounter ) + "."} ), status = 400 );
        except Exception:
            return Response( json.dumps({"message": "Incorrect price on line " + str( rowCounter)  + "."} ), status = 400 );

        rowCounter = rowCounter + 1;

    stream = io.StringIO( content );
    reader = csv.reader( stream );

    with Redis( host = Configuration.REDIS_HOST ) as redis:
        for row in reader:
            redis.rpush( "products", str( row[0] + "," + row[1] + "," + row[2] + "," + row[3] ) );

    return Response( status = 200 );



if ( __name__ == "__main__" ):
    database.init_app ( application );
    #application.run ( debug = True, host = "0.0.0.0", port = 5002 );
    application.run(debug = True, port = 5002);