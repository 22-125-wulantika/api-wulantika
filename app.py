from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Contoh data produk
products = [
    {"id": "1", "name": "Semen", "description": "Semen berkualitas tinggi untuk konstruksi."},
    {"id": "2", "name": "Pasir", "description": "Pasir halus untuk bangunan."},
    {"id": "3", "name": "Batu Bata", "description": "Batu bata merah untuk dinding."},
    {"id": "4", "name": "Paku", "description": "Paku galvanis untuk sambungan."},
    {"id": "5", "name": "Cat", "description": "Cat tembok untuk interior dan eksterior."},
    {"id": "6", "name": "Papan Kayu", "description": "Papan kayu untuk konstruksi."},
    {"id": "7", "name": "Kawat Las", "description": "Kawat las untuk sambungan logam."},
    {"id": "8", "name": "Semen Instan", "description": "Semen instan untuk kemudahan penggunaan."},
    {"id": "9", "name": "Gergaji", "description": "Gergaji tangan untuk pemotongan kayu."},
    {"id": "10", "name": "Obeng", "description": "Obeng untuk berbagai jenis sekrup."}
]

details = {
    "1": {
        "name": "Semen",
        "description": "Semen berkualitas tinggi untuk konstruksi.",
        "customerReviews": []
    },
    "2": {
        "name": "Pasir",
        "description": "Pasir halus untuk bangunan.",
        "customerReviews": []
    },
    "3": {
        "name": "Batu Bata",
        "description": "Batu bata merah untuk dinding.",
        "customerReviews": []
    },
    "4": {
        "name": "Paku",
        "description": "Paku galvanis untuk sambungan.",
        "customerReviews": []
    },
    "5": {
        "name": "Cat",
        "description": "Cat tembok untuk interior dan eksterior.",
        "customerReviews": []
    },
    "6": {
        "name": "Papan Kayu",
        "description": "Papan kayu untuk konstruksi.",
        "customerReviews": []
    },
    "7": {
        "name": "Kawat Las",
        "description": "Kawat las untuk sambungan logam.",
        "customerReviews": []
    },
    "8": {
        "name": "Semen Instan",
        "description": "Semen instan untuk kemudahan penggunaan.",
        "customerReviews": []
    },
    "9": {
        "name": "Gergaji",
        "description": "Gergaji tangan untuk pemotongan kayu.",
        "customerReviews": []
    },
    "10": {
        "name": "Obeng",
        "description": "Obeng untuk berbagai jenis sekrup.",
        "customerReviews": []
    }
}

class ProductList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "success",
            "count": len(products),
            "products": products
        }

class ProductDetail(Resource):
    def get(self, product_id):
        if product_id in details:
            return {
                "error": False,
                "message": "success",
                "product": details[product_id]
            }
        return {"error": True, "message": "Product not found"}, 404

class ProductSearch(Resource):
    def get(self):
        query = request.args.get('q', '').lower()
        result = [p for p in products if query in p['name'].lower() or query in p['description'].lower()]
        return {
            "error": False,
            "found": len(result),
            "products": result
        }

class AddReview(Resource):
    def post(self):
        data = request.get_json()
        product_id = data.get('id')
        name = data.get('name')
        review = data.get('review')
        
        if product_id in details:
            new_review = {
                "name": name,
                "review": review,
                "date": datetime.now().strftime("%d %B %Y")
            }
            details[product_id]['customerReviews'].append(new_review)
            return {
                "error": False,
                "message": "success",
                "customerReviews": details[product_id]['customerReviews']
            }
        return {"error": True, "message": "Product not found"}, 404

class UpdateReview(Resource):
    def put(self):
        data = request.get_json()
        product_id = data.get('id')
        name = data.get('name')
        new_review_text = data.get('review')
        
        if product_id in details:
            reviews = details[product_id]['customerReviews']
            review_to_update = next((r for r in reviews if r['name'] == name), None)
            if review_to_update:
                review_to_update['review'] = new_review_text
                review_to_update['date'] = datetime.now().strftime("%d %B %Y")
                return {
                    "error": False,
                    "message": "success",
                    "customerReviews": reviews
                }
            return {"error": True, "message": "Review not found"}, 404
        return {"error": True, "message": "Product not found"}, 404

class DeleteReview(Resource):
    def delete(self):
        data = request.get_json()
        product_id = data.get('id')
        name = data.get('name')
        
        if product_id in details:
            reviews = details[product_id]['customerReviews']
            review_to_delete = next((r for r in reviews if r['name'] == name), None)
            if review_to_delete:
                reviews.remove(review_to_delete)
                return {
                    "error": False,
                    "message": "success",
                    "customerReviews": reviews
                }
            return {"error": True, "message": "Review not found"}, 404
        return {"error": True, "message": "Product not found"}, 404

# Register endpoints
api.add_resource(ProductList, '/products')
api.add_resource(ProductDetail, '/product/<string:product_id>')
api.add_resource(ProductSearch, '/products/search')
api.add_resource(AddReview, '/product/review')
api.add_resource(UpdateReview, '/product/review/update')
api.add_resource(DeleteReview, '/product/review/delete')

if __name__ == '__main__':
    app.run(debug=True)
