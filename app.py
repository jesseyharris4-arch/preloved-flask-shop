from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Message
import requests

from email_config import init_mail   # ✅ import helper

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ✅ Initialize Mail using Afrihost helper
mail = init_mail(app)

# Paystack secret key (replace with your own from dashboard)
PAYSTACK_SECRET_KEY = "sk_test_yourpaystackkey"
PAYSTACK_INIT_URL = "https://api.paystack.co/transaction/initialize"

# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(120), nullable=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(120), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="Pending")
    buyer_email = db.Column(db.String(120), nullable=False)

# Routes
@app.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

# ✅ New route for category pages
@app.route('/category/<name>')
def category(name):
    products = Product.query.filter(Product.category.ilike(name)).all()
    return render_template('category.html', category=name, products=products)

# ✅ Test email route
@app.route('/test-email')
def test_email():
    msg = Message("Test Email", recipients=["hello@prelovedlittlesandbigs.co.za"])
    msg.html = """
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background: #ffffff; border-radius: 8px; padding: 20px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
            <div style="text-align: center;">
                <img src="https://cdn-icons-png.flaticon.com/512/891/891462.png" alt="Shopping Bag" width="80" style="margin-bottom: 20px;">
                <h2 style="color: #ff6f61;">Test Email Sent Successfully!</h2>
            </div>
            <p style="font-size: 16px; color: #333;">This is a styled test email from Preloved Littles & Bigs.</p>
        </div>
    </body>
    </html>
    """
    mail.send(msg)
    return "Test email sent!"

# Regular add route (if you want customers to suggest products)
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        category = request.form['category']
        image = request.form['image']

        new_product = Product(name=name, price=price, category=category, image=image)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_product.html')

# ✅ Admin add route with Toastify integration
@app.route('/admin/add', methods=['GET', 'POST'])
def admin_add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        category = request.form['category']
        image = request.form['image']

        new_product = Product(name=name, price=price, category=category, image=image)
        db.session.add(new_product)
        db.session.commit()

        flash("product_added")  # triggers Toastify notification
        return redirect(url_for('home'))

    return render_template('admin_add_product.html')

@app.route('/cart')
def cart():
    orders = Order.query.all()
    return render_template('cart.html', orders=orders)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        buyer_email = request.form['email']
        product_name = request.form['product_name']
        total_price = float(request.form['total_price'])

        # Save order
        new_order = Order(product_name=product_name, total_price=total_price, buyer_email=buyer_email)
        db.session.add(new_order)
        db.session.commit()

        # ✅ Styled HTML email to buyer
        msg = Message("Order Confirmation - Preloved Littles & Bigs", recipients=[buyer_email])
        msg.html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background: #ffffff; border-radius: 8px; padding: 20px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                <div style="text-align: center;">
                    <img src="https://cdn-icons-png.flaticon.com/512/891/891462.png" alt="Shopping Bag" width="80" style="margin-bottom: 20px;">
                    <h2 style="color: #ff6f61;">Thank You for Your Order!</h2>
                </div>
                <p style="font-size: 16px; color: #333;">Hi {buyer_email},</p>
                <p style="font-size: 16px; color: #333;">We’re excited to let you know your order has been received.</p>
                <div style="background: #f1f1f1; padding: 15px; border-radius: 6px; margin: 20px 0;">
                    <p style="margin: 0; font-size: 16px; color: #333;">
                        <strong>Order Number:</strong> #{new_order.id}<br>
                        <strong>Product:</strong> {product_name}<br>
                        <strong>Total:</strong> R{total_price}<br>
                        <strong>Email:</strong> {buyer_email}
                    </p>
                </div>
                <p style="font-size: 16px; color: #333;">We’ll notify you once your order is on its way.</p>
                <div style="text-align: center; margin-top: 30px;">
                    <a href="https://prelovedlittlesandbigs.co.za" style="background: #ff6f61; color: #fff; text-decoration: none; padding: 12px 20px; border-radius: 6px; font-size: 16px;">Visit Our Store</a>
                </div>
                <p style="font-size: 14px; color: #777; margin-top: 30px; text-align: center;">
                    Preloved Littles & Bigs © 2026<br>
                    hello@prelovedlittlesandbigs.co.za
                </p>
            </div>
        </body>
        </html>
        """
        mail.send(msg)

        # ✅ Styled HTML email to store owner
        owner_msg = Message("New Order Received - Preloved Littles & Bigs", recipients=["hello@prelovedlittlesandbigs.co.za"])
        owner_msg.html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background: #ffffff; border-radius: 8px; padding: 20px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                <div style="text-align: center;">
                    <img src="https://cdn-icons-png.flaticon.com/512/891/891463.png" alt="Order Icon" width="80" style="margin-bottom: 20px;">
                    <h2 style="color: #4CAF50;">New Order Alert!</h2>
                </div>
                <p style="font-size: 16px; color: #333;">A new order has been placed:</p>
                <div style="background: #f1f1f1; padding: 15px; border-radius: 6px; margin: 20px 0;">
                    <p style="margin: 0; font-size: 16px; color: #333;">
                        <strong>Order Number:</strong> #{new_order.id}<br>
                        <strong>Product:</strong> {product_name}<br>
                        <strong>Total:</strong> R{total_price}<br>
                        <strong>Customer Email:</strong> {buyer_email}
                    </p>
                </div>
                <p style="font-size: 16px; color: #333;">Log