#list1 = ["a|b|c","p1","10","15"]
#list2 =["p1"]
#for elem in list1:
#    if (not elem in list2):
#        print(True)
#    else:
#        print(False)
#print('aaasasas')
#print(1 == int('1'))

#@application.route ( "/categoryWaitingProducts", methods = ["GET"] ) # mod jun 2022
#@roleCheck ( role = "admin" )
#def categoryWaitingProducts( ):
#    countWaiting = coalesce( func.sum( OrderProduct.requestedQuantity - OrderProduct.receivedQuantity ), 0 ).label( "waiting" );
#
#    categoryStatisticsList = Category.query.outerjoin(ProductCategory).outerjoin(Product).outerjoin(OrderProduct) \
#        .group_by(Category.id) \
#        .with_entities(Category.name, countWaiting) \
#        .order_by(countWaiting.desc( ), Category.name.asc( )).all( );
#
#    statistics = [{
#        "name": element.name,
#        "waiting": int(element.waiting)
#    } for element in categoryStatisticsList];
#
#    return jsonify( statistics = statistics );
#
#@application.route ( "/productShare", methods = ["GET"] ) # mod jul 2022
#@roleCheck ( role = "admin" )
#def productShare( ):
#    result = database.session.query(
#        func.sum( OrderProduct.requestedQuantity )
#    ).scalar( );
#    #print(type(result))
#    countSoldByProduct = coalesce( func.sum( OrderProduct.requestedQuantity ), 0 ).label( "sold" );
#
#    products = Product.query.outerjoin( OrderProduct ).group_by(Product.id).with_entities(Product.name, countSoldByProduct).all( );
#
#    statistics = [{
#        "name": element.name,
#        "sold": int( element.sold ),
#        "total": int( result ),
#        "share": str( round( int( element.sold ) / int( result ) * 100, 2) ) + "%"
#    } for element in products];
#
#    #return Response ( json.dumps( statistics ), status=200 );
#    return jsonify( statistics = statistics );

#@application.route ( "/count", methods = ["GET"] )
#@roleCheck ( role = "admin" )
#def count( ):
#    count = Product.query.count(  );
#    return str(count)
#
#@application.route ( "/countDistinct", methods = ["GET"] )
#@roleCheck ( role = "admin" )
#def countDistinct ( ):
#    countDistinct = func.count( '*' ).label("cnt");
#    list = Product.query.join(
#    ProductCategory ).with_entities( countDistinct ).first( )
#    return str(list.cnt)

#@application.route ( "/maxPriceProduct", methods = ["GET"] )
#@roleCheck ( role = "admin" )
#def maxPriceProduct( ):
#    totalPrice = coalesce(func.sum( OrderProduct.priceWhenOrdered ) * func.sum ( OrderProduct.requestedQuantity ), 0).label("price");
#
#    maxPriceProducts = Product.query.outerjoin(OrderProduct) \
#        .group_by(Product.id) \
#        .with_entities(Product.id, Product.name, totalPrice) \
#        .order_by(totalPrice.desc(), Product.name.asc()).limit(3).all();
#
#    statistics = [{
#        "id": element.id,
#        "name": element.name,
#        "total": round(float(element.price),3),
#    } for element in maxPriceProducts];
#
#    return jsonify( statistics = statistics );

#@application.route ( "/productShareSA", methods = ["GET"] )
#@roleCheck ( role = "admin" )
#def productShareSA( ):
#    formula = func.sum(OrderProduct.priceWhenOrdered * OrderProduct.requestedQuantity ).label("total")
#    totalPrice = OrderProduct.query.with_entities(formula).first();
#
#
#    priceSoldByProduct = coalesce( func.sum( OrderProduct.priceWhenOrdered * OrderProduct.requestedQuantity ), 0 ).label( "sold" );
#
#    products = Product.query.outerjoin( OrderProduct ).group_by( Product.id ).with_entities(Product.name, priceSoldByProduct).all( );
#
#    statistics = [{
#          "name": element.name,
#          "sold": float( element.sold ),
#          "total": float( totalPrice.total ),
#          "share": str( round( float( element.sold ) / float( totalPrice.total ) * 100, 2) ) + "%"
#      } for element in products];
#
#    #return Response ( json.dumps( statistics ), status = 200 );
#    return jsonify( statistics = statistics );

#@application.route ( "/joinClause", methods = ["GET"] )
#@roleCheck ( role = "admin" )
#def joinClause( ):
#    return str( Category.query.join ( ProductCategory, Category.id == ProductCategory.categoryId).with_entities(Category.id,ProductCategory.categoryId).all())
#    return str(Order.query.filter(Order.time == '2022-09-27 15:40:37' ).all())
#   return str(Category.query.join(Order, Category.id == Order.id).with_entities(Category.name,Order.time).all())

#@application.route ( "/updateID", methods = ["GET"] )
##@roleCheck ( role = "admin" )
#def updateID( ):
    #category1 = Category.query.filter(Category.id == 1).first();
    #category1.id = 111;
    #database.session.commit();
    #
    #categories1 = ProductCategory.query.filter(ProductCategory.categoryId == 1).all();
    #for element in categories1:
    #    element.categoryId=111;
    #database.session.commit();

    #categories1 = ProductCategory.query.join(Category).filter(ProductCategory.categoryId == 1).with_entities(Category.name).all();
    #for element in categories1:
        #element.name = 'catttt'
    #database.session.commit();

     #categories1 = Category.query.join(ProductCategory).filter(ProductCategory.categoryId == 1).all();
     #for element in categories1:
     #   element.name = 'Category0'
     #   print("a")
     #database.session.commit();
     #return str(categories1)

#@threadsBlueprint.route ( "/withWordsInTitle", methods = ["GET"] )
#def getThreadsWithWordsInTitle ( ):
#    words = [item.strip ( ) for item in request.args["words"].split ( "," )];
#
#    threads = Thread.query.filter (
#            and_ (
#                    *[Thread.title.like ( f"%{word}%" ) for word in words]
#            )
#    ).all ( );
#
#    return str ( threads );

#@tagsBlueprint.route ( "/frequency/<number>", methods = ["GET"] )
#def getFrequency ( number = None ):
#
#    count = func.count ( Tag.name );
#
#    query = Tag.query.join ( ThreadTag ).join ( Thread )\
#        .group_by ( Tag.name ).with_entities ( Tag.name, count );
#
#    if ( number != None ):
#        query = query.having ( count > int ( number ) );
#
#    result = query.all ( );
#
#    return str ( result );

#@application.route ( "/productsWithMultipleCategories", methods = ["GET"] )
##@roleCheck ( role = "admin" )
#def productsWithMultipleCategories( ):
#    cnt = func.count(ProductCategory.categoryId);
#    countCategories = coalesce(cnt, 0).label("countCategories");
#    query = Product.query.join(ProductCategory) \
#        .group_by(Product.id).with_entities(Product.id,Product.name, countCategories).having( cnt > 1);
#
#    return str(query.all())

#@application.route("/deleteProductsWithMultipleCategories", methods=["GET"])
## @roleCheck ( role = "admin" )
#def productsWithMultipleCategories():
#    cnt = func.count(ProductCategory.categoryId);
#    countCategories = coalesce(cnt, 0).label("countCategories");
#    query = Product.query.join(ProductCategory) \
#        .group_by(Product.id).having(cnt > 1);
#
#    products = query.all();
#    print(products)
#    for element in products:
#        database.session.delete(element)
#        database.session.commit()
#
#    return str(Product.query.all())

#@application.route ( "/productsDates", methods = ["GET"] )
##@roleCheck ( role = "admin" )
#def productsDates( ):
#    products = Product.query.join( OrderProduct ).join( Order ).with_entities(Product.name, Order.time).all();
#    list = [{
#        "name": product.name,
#        "date":product.time
#    } for product in products]
#
#    return jsonify(list=list)

#@application.route ( "/productsNewestDate", methods = ["GET"] )
#@roleCheck ( role = "admin" )
#def productsNewestDate( ):
#    maxDate = func.max( Order.time ).label("maxDate")
#    products = Product.query.join( OrderProduct ).join( Order ).group_by(Product.id).with_entities(Product.name, maxDate).all();
#    list = [{
#        "name": product.name,
#        "date":product.maxDate
#    } for product in products]
#
#    print(len(list))
#
#    return jsonify(list=list)

#@application.route ( "/productDatesList", methods = ["GET"] )
#@roleCheck ( role = "admin" )
#def productDatesList( ):
#    maxDate = func.max( Order.time ).label("maxDate")
#    products = Product.query.join( OrderProduct ).join( Order ).group_by(Product.id).with_entities(Product.id,Product.name, maxDate).all();
#    list = [{
#        "name": product.name,
#        "date": [ str(element.time) for element in Order.query.join(OrderProduct).filter(OrderProduct.productId == product.id).all() ]
#    } for product in products]
#
#    print(len(list))
#
#    return jsonify(list=list)

#@application.route ( "/productDatesList", methods = ["GET"] )
##@roleCheck ( role = "admin" )
#def productDatesList( ):
#    maxDate = func.max( Order.time ).label("maxDate")
#    products = Product.query.join( OrderProduct ).join( Order ).group_by(Product.id).with_entities(Product.id,Product.name, maxDate).all();
#    list = [{
#        "name": product.name,
#        "date": [ str(element.time) for element in Order.query.join(OrderProduct).filter(OrderProduct.productId == product.id).all() ]
#    } for product in products]
#
#    print(len(list))
#
#    return jsonify(list=list)