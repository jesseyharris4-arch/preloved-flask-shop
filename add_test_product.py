from app import app, db
from models import Product

# Demo product based on your uploaded t-shirt
demo_product = {
    "name": "Children's T-Shirt - Hentiesbaai Namibia",
    "price": 120.00,   # adjust to your preferred value
    "category": "Clothing",
    "image": "henties_tshirt.jpg"  # optional filename or URL
}

with app.app_context():
    item = Product(
        name=demo_product["name"],
        price=demo_product["price"],
        category=demo_product["category"],
        image=demo_product["image"]
    )
    db.session.add(item)
    db.session.commit()

print("Demo product added successfully!")
