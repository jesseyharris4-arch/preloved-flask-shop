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
                <p style="font-size: 16px; color: #333;">Log in to your admin dashboard to manage this order.</p>
            </div>
        </body>
        </html>
        """
        mail.send(owner_msg)

        return redirect(url_for('home'))
