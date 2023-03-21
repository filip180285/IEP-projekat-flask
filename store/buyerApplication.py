from flask import Flask, request, Response, jsonify;
from configurationStore import Configuration;
from modelsStore import database, Product, ProductCategory, Category, Order, OrderProduct;
from checkRoleDecorator import roleCheck;
from flask_jwt_extended import JWTManager, get_jwt_identity;
from sqlalchemy import and_;
import json;
from datetime import datetime;

application = Flask ( __name__ );
application.config.from_object ( Configuration );
jwt = JWTManager ( application );

@application.route( "/", methods = ["GET"] )
def hello( ):
    return "<h1>Wellcome To Buyer Page</h1>";


@application.route( "/search", methods = ["GET"] )
@roleCheck ( role = "buyer" )
def search( ):
    productName = request.args.get( "name", "" );
    categoryName = request.args.get( "category", "" );

    products = Product.query.join( ProductCategory ).join( Category ).filter(
        and_( Product.name.like( f"%{productName}%" ), Category.name.like( f"%{categoryName}%" ) ) ).all( );

    categories = Category.query.join( ProductCategory ).join( Product ).filter( and_(
        Category.name.like( f"%{categoryName}%" ), Product.name.like( f"%{productName}%" ) ) ).all( );

    categoriesList = [category.name for category in categories];

    productsList = [{
        "categories": [category.name for category in product.categories],
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    } for product in products];

    return jsonify( categories = categoriesList, products = productsList );

@application.route("/order", methods = ["POST"])
@roleCheck ( role = "buyer" )
def order( ):
    requests = request.json.get( "requests", "" )
    userEmail = get_jwt_identity();

    if ( len( requests ) == 0 ):
        return Response(json.dumps( {"message": "Field requests is missing."} ), status = 400);

    requestCounter = 0;
    for singleRequest in requests:
        if ( not "id" in singleRequest ):
            return Response( json.dumps( {"message": "Product id is missing for request number " + str( requestCounter ) + "."} ), status = 400 );

        if ( not "quantity" in singleRequest ):
            return Response( json.dumps( {"message": "Product quantity is missing for request number " + str( requestCounter ) + "."} ), status = 400 );

        if( not isinstance( singleRequest["id"], int ) or not singleRequest["id"] > 0 ):
            return Response( json.dumps( {"message": "Invalid product id for request number " + str( requestCounter ) + "."} ), status = 400 );

        if( not isinstance( singleRequest["quantity"], int ) or not singleRequest["quantity"] > 0 ):
            return Response( json.dumps( {"message": "Invalid product quantity for request number " + str( requestCounter ) + "."} ), status = 400 );

        product = Product.query.filter( ( Product.id == singleRequest["id"] ) ).first( );
        if( not product ):
            return Response( json.dumps( {"message": "Invalid product for request number " + str(requestCounter) + "."} ), status = 400 );
        requestCounter = requestCounter + 1;

    allRequestedProductsAvailable = True;
    overallPrice = 0;
    received = -1;

    order = Order( price = 0, status = "UNDEFINED", time = datetime.now( ).isoformat( ), userEmail = userEmail );
    database.session.add( order );
    database.session.commit( );

    for singleRequest in requests:
        product = Product.query.filter( ( Product.id == singleRequest["id"] ) ).first();
        overallPrice += singleRequest["quantity"] * product.price;

        if ( product.quantity >= singleRequest["quantity"] ): # there is sufficient quantity of product
            received = singleRequest["quantity"];
            product.quantity = product.quantity - singleRequest["quantity"];
        else: # insufficient quantity
            received = product.quantity;
            product.quantity = 0;
            allRequestedProductsAvailable = False;

        database.session.commit( );

        orderProduct = OrderProduct( orderId = order.id, productId = product.id, priceWhenOrdered = product.price, requestedQuantity = singleRequest["quantity"], receivedQuantity = received );
        database.session.add( orderProduct );
        database.session.commit( );

    order.price = overallPrice;
    if( allRequestedProductsAvailable ): # sufficient quantity of products for all segments of an order
        order.status = "COMPLETE";
    else:
        order.status = "PENDING";
    order.time = datetime.now( ).isoformat( );
    database.session.commit();

    return jsonify( id = order.id );

@application.route( "/status", methods = ["GET"] )
@roleCheck ( role = "buyer" )
def status( ):
    userEmail = get_jwt_identity();
    orders = Order.query.filter( Order.userEmail == userEmail ).all( );

    ordersList = [{
       "products": [{
           "categories": [category.name for category in product.categories],
           "name": product.name,
           "price": ( OrderProduct.query.filter( and_(
               OrderProduct.productId == product.id, OrderProduct.orderId == order.id) ).first( ) ).priceWhenOrdered,
           "received": ( OrderProduct.query.filter(and_(
               OrderProduct.productId == product.id, OrderProduct.orderId == order.id)).first( ) ).receivedQuantity,
           "requested": ( OrderProduct.query.filter(and_(
               OrderProduct.productId == product.id, OrderProduct.orderId == order.id)).first( ) ).requestedQuantity,
       } for product in order.products],
        "price": order.price,
       "status": order.status,
       "timestamp": order.time,
    } for order in orders];

    return jsonify( orders = ordersList );

if ( __name__ == "__main__" ):
    database.init_app ( application );
    #application.run ( debug = True, host = "0.0.0.0", port = 5003 );
    application.run(debug = True, port = 5003);