from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# Data contoh untuk bahan bangunan
bahan_bangunan = [
    {"id": 1, "name": "Semenn", "category": "Beton", "price": 50000, "available": True, "stock": 100},
    {"id": 2, "name": "Besi Beton", "category": "Logam", "price": 150000, "available": True, "stock": 50},
    {"id": 3, "name": "Bata", "category": "Masonry", "price": 1000, "available": True, "stock": 500},
    {"id": 4, "name": "Plywood", "category": "Kayu", "price": 200000, "available": True, "stock": 30},
    {"id": 5, "name": "Cat", "category": "Finishing", "price": 80000, "available": True, "stock": 80},
    {"id": 6, "name": "Seng Atap", "category": "Atap", "price": 120000, "available": False, "stock": 0},
    {"id": 7, "name": "Bahan Insulasi", "category": "Isolasi", "price": 60000, "available": True, "stock": 40},
    {"id": 8, "name": "Keramik", "category": "Lantai", "price": 25000, "available": True, "stock": 200},
    {"id": 9, "name": "Sekrup dan Pengikat", "category": "Perkakas", "price": 15000, "available": True, "stock": 300},
    {"id": 10, "name": "Bata Semen", "category": "Beton", "price": 1200, "available": True, "stock": 150}
]

# Fungsi bantu untuk mendapatkan ID baru
def get_new_id():
    if bahan_bangunan:
        return max(item["id"] for item in bahan_bangunan) + 1
    return 1

# Endpoint daftar bahan bangunan dengan opsi Create
class DaftarBahanBangunan(Resource):
    def get(self):
        return {"error": False, "message": "berhasil", "count": len(bahan_bangunan), "items": bahan_bangunan}

# Resource TambahBahanBangunan
class TambahBahanBangunan(Resource):
    def post(self):
        data = request.json
        new_id = get_new_id()
        
        new_item = {
            "id": new_id,
            "name": data.get("name"),
            "category": data.get("category"),
            "price": data.get("price"),
            "available": data.get("available", True),
            "stock": data.get("stock", 0)
        }
        bahan_bangunan.append(new_item)
        
        return {"error": False, "message": "Item berhasil dibuat", "item": new_item}, 201

# Endpoint detail bahan bangunan dengan opsi Read, Update, dan Delete
class DetailBahanBangunan(Resource):
    def get(self, item_id):
        item = next((item for item in bahan_bangunan if item["id"] == item_id), None)
        if not item:
            return {"error": True, "message": "Item tidak ditemukan"}, 404
        return {"error": False, "message": "berhasil", "item": item}

# Resource UpdateBahanBangunan
class UpdateBahanBangunan(Resource):
    def put(self, item_id):
        data = request.json
        item = next((item for item in bahan_bangunan if item["id"] == item_id), None)
        if not item:
            return {"error": True, "message": "Item tidak ditemukan"}, 404
        
        # Memperbarui data item
        item.update({
            "name": data.get("name", item["name"]),
            "category": data.get("category", item["category"]),
            "price": data.get("price", item["price"]),
            "available": data.get("available", item["available"]),
            "stock": data.get("stock", item["stock"])
        })
        
        return {"error": False, "message": "Item berhasil diperbarui", "item": item}

# Resource HapusBahanBangunan
class HapusBahanBangunan(Resource):
    def delete(self, item_id):
        global bahan_bangunan
        bahan_bangunan = [item for item in bahan_bangunan if item["id"] != item_id]
        
        return {"error": False, "message": "Item berhasil dihapus"}

# Mendaftarkan resource dengan endpoint
api.add_resource(DaftarBahanBangunan, "/materials")  # Untuk GET
api.add_resource(TambahBahanBangunan, '/materials/add')  # Untuk POST
api.add_resource(DetailBahanBangunan, "/materials/<int:item_id>")  # Untuk GET
api.add_resource(UpdateBahanBangunan, '/materials/update/<int:item_id>')  # Untuk PUT
api.add_resource(HapusBahanBangunan, '/materials/delete/<int:item_id>')  # Untuk DELETE

if __name__ == "__main__":
    app.run(debug=True)
