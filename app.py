from flask import Flask, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# Example laptop inventory data with realistic names
inventory = {
    "1": {"brand": "Apple", "model": "MacBook Pro 16", "price": 30000000, "stock": 5, "specs": {"ram": "16GB", "storage": "512GB SSD", "processor": "M1 Pro"}},
    "2": {"brand": "Dell", "model": "XPS 13", "price": 18000000, "stock": 10, "specs": {"ram": "16GB", "storage": "512GB SSD", "processor": "Intel i7"}},
    "3": {"brand": "HP", "model": "Spectre x360", "price": 20000000, "stock": 7, "specs": {"ram": "16GB", "storage": "1TB SSD", "processor": "Intel i7"}},
    "4": {"brand": "Lenovo", "model": "ThinkPad X1 Carbon", "price": 22000000, "stock": 4, "specs": {"ram": "16GB", "storage": "512GB SSD", "processor": "Intel i7"}},
    "5": {"brand": "Asus", "model": "ROG Zephyrus G14", "price": 25000000, "stock": 6, "specs": {"ram": "16GB", "storage": "1TB SSD", "processor": "AMD Ryzen 9"}},
}

class InventoryList(Resource):
    def get(self):
        return jsonify(inventory)

class InventoryDetail(Resource):
    def get(self, laptop_id):
        laptop = inventory.get(laptop_id)
        if laptop:
            return jsonify(laptop)
        return {"message": "Laptop not found"}, 404

class AddLaptop(Resource):
    def post(self):
        new_id = str(len(inventory) + 1)
        data = request.get_json()
        inventory[new_id] = {
            "brand": data["brand"],
            "model": data["model"],
            "price": data["price"],
            "stock": data["stock"],
            "specs": data.get("specs", {})
        }
        return {"message": "Laptop added", "laptop": inventory[new_id]}, 201

class UpdateLaptop(Resource):
    def put(self, laptop_id):
        if laptop_id in inventory:
            data = request.get_json()
            inventory[laptop_id].update(data)
            return {"message": "Laptop updated", "laptop": inventory[laptop_id]}
        return {"message": "Laptop not found"}, 404

class DeleteLaptop(Resource):
    def delete(self, laptop_id):
        if laptop_id in inventory:
            deleted_laptop = inventory.pop(laptop_id)
            return {"message": "Laptop deleted", "laptop": deleted_laptop}
        return {"message": "Laptop not found"}, 404

# Adding endpoints to the API
api.add_resource(InventoryList, '/inventory')
api.add_resource(InventoryDetail, '/inventory/<string:laptop_id>')
api.add_resource(AddLaptop, '/inventory/add')
api.add_resource(UpdateLaptop, '/inventory/update/<string:laptop_id>')
api.add_resource(DeleteLaptop, '/inventory/delete/<string:laptop_id>')

if __name__ == '__main__':
    app.run(debug=True)
