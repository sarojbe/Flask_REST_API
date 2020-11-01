from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
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

    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message':'item with name {} exists'.format(name)},400 #Bad request
        
        data = Item.parser.parse_args()
        
        item= ItemModel(name, **data)
        
        try:
            ItemModel.save_to_db()
        except:
            return {'message':'error occurred could not add item'}, 500
        return item, 201 # 202 accepted ..esp when delaying creation


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

    def delete(self, name):
        item= ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'item deleted'}



class ItemList(Resource):
    # @jwt_required
    def get(self):
        #return {'item': list(map(lambda x.json():x , ItemModel.find_all()  ))}
        return {'items': [x.json() for x in ItemModel.find_all()]}
        #return {'item': list(map(lambda x: x.json() ,ItemModel.query.all() )) }
        


