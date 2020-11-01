from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_claims, 
    jwt_optional, 
    get_jwt_identity,
    fresh_jwt_required)
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="price field cannot be left blank"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Store id field cannot be left blank"
                        )
    @jwt_required
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found'}, 404

    @fresh_jwt_required # you can use claims as well
    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message':'item with name {} exists'.format(name)},400 #Bad request
        
        data = Item.parser.parse_args()
        
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message':'error occurred could not add item'}, 500
        
        return item.json(), 201 # 202 accepted ..esp when delaying creation


    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        #updated_item = ItemModel(name,data['price'])
        if item is None:
            item=  ItemModel(name, **data)
        else:
            item.price=data['price']
        item.save_to_db()
        return item.json()

    @jwt_required
    def delete(self, name):
        claims =get_jwt_claims()
        if not claims['is_admin']:
            return {'message':'Admin privilege required'}, 401

        item= ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'item deleted'}



class ItemList(Resource):
    @jwt_optional #check if logged in
    def get(self):
        user_id= get_jwt_identity()
        items= [x.json() for x in ItemModel.find_all()]
        if user_id:
            return {'items':items}, 200
        return {'items':[item['name'] for item in items],
                'message':'More data available if you log in '}


        #return {'item': list(map(lambda x.json():x , ItemModel.find_all()  ))}
        #return {'item': list(map(lambda x: x.json() ,ItemModel.query.all() )) }
        


