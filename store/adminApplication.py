import json

from flask import Flask, jsonify;
from flask import Response

from configurationStore import Configuration;
from modelsStore import database;
from checkRoleDecorator import roleCheck;
from flask_jwt_extended import JWTManager;
from modelsStore import Product, OrderProduct, Category, ProductCategory;
from sqlalchemy import func;
from sqlalchemy.sql.functions import coalesce;

application = Flask ( __name__ );
application.config.from_object ( Configuration );
jwt = JWTManager ( application );

@application.route( "/", methods = ["GET"] )
def hello( ):
    return "<h1>Wellcome To Admin Page</h1>";

@application.route ( "/productStatistics", methods = ["GET"] )
@roleCheck ( role = "admin" )
def productStatistics( ):
    countSold = func.sum( OrderProduct.requestedQuantity ).label( "sold" );
    countWaiting = func.sum( OrderProduct.requestedQuantity - OrderProduct.receivedQuantity ).label( "waiting" );

    productStatisticsList = OrderProduct.query.join(Product)\
        .group_by( OrderProduct.productId )\
        .with_entities( Product.name, OrderProduct.productId, countSold, countWaiting ).all( );

    statistics = [{
        "name": productStatistics.name,
        "sold": int( productStatistics.sold ),
        "waiting": int( productStatistics.waiting ),
    } for productStatistics in productStatisticsList];

    return jsonify( statistics = statistics );

@application.route ( "/categoryStatistics", methods = ["GET"] )
@roleCheck ( role = "admin" )
def categoryStatistics( ):
    countSold = coalesce( func.sum( OrderProduct.requestedQuantity ), 0 ).label( "sold" );

    categoryStatisticsList = Category.query.join(ProductCategory).join(Product).outerjoin(OrderProduct)  \
        .group_by( Category.id ) \
        .with_entities(Category.name, countSold) \
        .order_by( countSold.desc( ) , Category.name.asc( ) ).all( );

    statistics = [ categoryStatistics.name for categoryStatistics in categoryStatisticsList ];

    return jsonify( statistics = statistics );


if ( __name__ == "__main__" ):
    database.init_app ( application );
    #application.run ( debug = True, host = "0.0.0.0", port = 5004 );
    application.run(debug = True, port = 5004);