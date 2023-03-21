from flask import Flask;
from sqlalchemy import and_;

from configurationStore import Configuration;
from modelsStore import database, Product, Category, ProductCategory, OrderProduct, Order;
from redis import Redis;

application = Flask ( __name__ );
application.config.from_object ( Configuration );

database.init_app ( application );

while ( True ):
    with Redis( host = Configuration.REDIS_HOST ) as redis:
        #(b'products', b'kat2|kat5,pr2,15,150')
        row = str( redis.blpop( "products" ) ).split( "'" );
        with application.app_context( ) as context:
            info = ( row[3] ).split( "," );
            categoriesList = info[0].split( "|" );
            productName = info[1];
            quantity = int( info[2] );
            price = float( info[3] );
            product = Product.query.filter( Product.name == productName ).first( );

            if ( not product ): # product does not exist, it is being created and added to category connection table
                product = Product( name = productName, price = price, quantity = quantity );
                database.session.add( product );
                database.session.commit( );
                for categoryName in categoriesList:
                    category = Category.query.filter( Category.name == categoryName ).first( );
                    if ( not category ): # category does not exist, it is being created and added to product connection table
                        category = Category( name = categoryName );
                        database.session.add( category );
                        database.session.commit();
                        bond = ProductCategory( productId = product.id, categoryId = category.id );
                        database.session.add( bond );
                        database.session.commit( );
                    else: # category exists, it is being added to product connection table
                        bond = ProductCategory( productId = product.id, categoryId = category.id );
                        database.session.add( bond );
                        database.session.commit( );
            else: # product exists
                foundAll = True;
                for categoryName in categoriesList: # checking if product has all of the listed categories
                    if( not categoryName in str( product.categories ) ):
                        foundAll = False;
                        break;
                if( not foundAll ):
                    continue; # information about products are being rejected

                ### product updating
                newPrice = ( product.quantity * product.price + quantity * price ) / ( product.quantity + quantity );
                newQuantity = product.quantity + quantity;
                product.price = newPrice;
                product.quantity = newQuantity;
                database.session.commit( );
                ### order updating
                pendingOrders = OrderProduct.query.join( Order ).filter(
                    and_( Order.status == "PENDING", OrderProduct.productId == product.id ) ).order_by( Order.time.asc( ) ).all( );

                if( len( pendingOrders ) != 0 ): # if there are PENDING orders containing specified product
                    pendingOrderCounter = 0;
                    while( product.quantity > 0 and pendingOrderCounter < len( pendingOrders ) ):
                        if( product.quantity >= ( pendingOrders[pendingOrderCounter].requestedQuantity - pendingOrders[pendingOrderCounter].receivedQuantity ) ): # there is sufficient quantity for this order segment
                            product.quantity = product.quantity - ( pendingOrders[pendingOrderCounter].requestedQuantity - pendingOrders[pendingOrderCounter].receivedQuantity ); # product updating
                            pendingOrders[pendingOrderCounter].receivedQuantity = pendingOrders[pendingOrderCounter].requestedQuantity; # OrderProduct connection table updating
                            database.session.commit( );
                            orderSegments = Order.query.join( OrderProduct ).filter( and_( Order.id == pendingOrders[pendingOrderCounter].orderId, OrderProduct.receivedQuantity != OrderProduct.requestedQuantity  ) ).all( ); # order updating
                            if( len( orderSegments ) == 0 ): # all segments of order are fulfilled, status is COMPLETE
                                orderForUpdate = Order.query.filter( Order.id == pendingOrders[pendingOrderCounter].orderId ).first( );
                                orderForUpdate.status = "COMPLETE";
                        else:
                            pendingOrders[pendingOrderCounter].receivedQuantity = pendingOrders[pendingOrderCounter].receivedQuantity + product.quantity; # there is not sufficient quantity, adding what is left
                            product.quantity = 0;
                        pendingOrderCounter = pendingOrderCounter + 1;
                        database.session.commit( );






