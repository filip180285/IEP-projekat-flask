import json;

from flask import Flask, request, Response, jsonify;
from configuration import Configuration;
from models import database, User, UserRole;
import re;
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, create_refresh_token, get_jwt, get_jwt_identity;
from sqlalchemy import and_;
from checkRoleDecorator import roleCheck;

application = Flask ( __name__ );
application.config.from_object ( Configuration );

@application.route( "/", methods = ["GET"] )
def hello( ):
    return "<h1>Wellcome To Authentication Page</h1>";


@application.route( "/register", methods = ["POST"] )
def register( ):
    forename = request.json.get( "forename", "" );
    surname = request.json.get( "surname", "" );
    email = request.json.get( "email", "" );
    password = request.json.get( "password", "" );
    isCustomer = request.json.get( "isCustomer", None );

    if( len( forename ) == 0 ):
        return Response( json.dumps( {"message": "Field forename is missing."} ), status = 400 );

    if ( len( surname ) == 0 ):
        return Response( json.dumps( {"message": "Field surname is missing."} ), status = 400 );

    if ( len( email ) == 0 ):
        return Response( json.dumps( {"message": "Field email is missing."} ), status = 400 );

    if ( len( password ) == 0 ):
        return Response( json.dumps( {"message": "Field password is missing."} ), status = 400 );

    if ( isCustomer == None ):
        return Response( json.dumps( {"message": "Field isCustomer is missing."} ), status = 400 );

    regexEmail = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$';
    if ( not re.search( regexEmail, email ) or len( email ) > 256 ):
        return Response( json.dumps( {"message": "Invalid email."} ), status = 400 );

    regexPassword = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}'
    if (not re.search( regexPassword, password ) or len( password ) > 256 ):
        return Response( json.dumps( {"message": "Invalid password."} ), status = 400 );

    emailExists = User.query.filter( User.email == email ).first( );
    if( emailExists ):
        return Response( json.dumps( {"message": "Email already exists."} ), status = 400 );

    ### aditional checking of fields length, was not asked
    if( len( forename ) > 256 ):
        return Response( json.dumps( {"message": "Too long forename."} ), status = 400 );

    if ( len( surname ) > 256 ):
        return Response( json.dumps( {"message": "Too long surname."} ), status = 400 );

    user = User( forename = forename, surname = surname, email = email, password = password, isCustomer = isCustomer );
    database.session.add( user );
    database.session.commit( );

    roleIdValue = -1;
    if( isCustomer == True ):
        roleIdValue = 3; # 1-admin, 2-worker, 3-buyer
    else:
        roleIdValue = 2;

    userRole = UserRole( userId = user.id, roleId = roleIdValue );
    database.session.add( userRole );
    database.session.commit( );

    return Response( status = 200 );


jwt = JWTManager ( application );
@application.route ( "/login", methods = ["POST"] )
def login ( ):
    email = request.json.get( "email", "" );
    password = request.json.get( "password", "" );

    if ( len( email ) == 0 ):
        return Response( json.dumps( {"message": "Field email is missing."} ), status = 400 );

    if ( len( password ) == 0 ):
        return Response( json.dumps( {"message": "Field password is missing."} ), status = 400 );

    regexEmail = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$';
    if ( not re.search( regexEmail, email ) or len( email ) > 256 ):
        return Response( json.dumps( {"message": "Invalid email."} ), status = 400 );

    user = User.query.filter( and_( User.email == email, User.password == password ) ).first( );

    if ( not user ):
        return Response( json.dumps( {"message": "Invalid credentials."} ), status = 400 );

    additionalClaims = {
        "forename": user.forename,
        "surname": user.surname,
        "password": user.password,
        "roles": [str(role) for role in user.roles]
    };

    accessToken = create_access_token( identity = user.email, additional_claims = additionalClaims);
    refreshToken = create_refresh_token( identity = user.email, additional_claims = additionalClaims);

    return jsonify( accessToken = accessToken, refreshToken = refreshToken );


@application.route ( "/refresh", methods = ["POST"] )
@jwt_required ( refresh = True )
def refresh ( ):
    identity = get_jwt_identity ( );
    refreshClaims = get_jwt ( );

    additionalClaims = {
            "forename": refreshClaims["forename"],
            "surname": refreshClaims["surname"],
            "password": refreshClaims["password"],
            "roles": refreshClaims["roles"]
    };

    accessToken = create_access_token ( identity = identity, additional_claims = additionalClaims );
    return jsonify( accessToken = accessToken );


@application.route ( "/delete", methods = ["POST"] )
@roleCheck ( role = "admin" )
def delete( ):
   email = request.json.get("email", "" );

   if ( len( email ) == 0 ):
       return Response( json.dumps( {"message": "Field email is missing."} ), status = 400 );

   regexEmail = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$';
   if ( not re.search( regexEmail, email ) or len( email ) > 256 ):
       return Response( json.dumps( {"message": "Invalid email."} ), status = 400 );

   user = User.query.filter( and_( User.email == email )).first( );

   if ( not user ):
       return Response(json.dumps( {"message": "Unknown user."} ), status = 400 );

   database.session.delete( user );
   database.session.commit( );
   return Response( status = 200 );



if ( __name__ == "__main__" ):
    database.init_app ( application );
    #application.run ( debug = True, host="0.0.0.0", port = 5001 );
    application.run( debug = True, port = 5001 );