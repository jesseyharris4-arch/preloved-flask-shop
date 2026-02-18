from app import app, db, Product

with app.app_context():
    db.create_all()

    demo = Product(name="Navy Blue T-Shirt", price=29.99, category="Summer Wear", image="tshirt.jpg")
    db.session.add(demo)
    db.session.commit()

print("Database seeded with demo product!")
