from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{os.getenv("username")}:{os.getenv("password")}@localhost/ecommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Customer(db.Model):
    __tablename__ = 'Customers'
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Product(db.Model):
    __tablename__ = 'Products'
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

class Order(db.Model):
    __tablename__ = 'Orders'
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.customer_id'))
    order_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.Enum('pending', 'shipped', 'delivered', 'canceled'), default='pending')
    customer = db.relationship("Customer", backref="orders")

class OrderItem(db.Model):
    __tablename__ = 'OrderItems'
    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.order_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('Products.product_id'))
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)

    order = db.relationship("Order", backref="order_items")
    product = db.relationship("Product")

# Decorator to validate product stock
def validate_stock(func):
    def wrapper(*args, **kwargs):
        product_id = request.json.get('product_id')
        quantity = request.json.get('quantity')
        product = Product.query.filter_by(product_id=product_id).first()
        
        if product and product.stock >= quantity:
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "Product not available in sufficient quantity"}), 400
    return wrapper

# Lambda for discount calculation
discount = lambda quantity: 0.10 if quantity > 10 else 0

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register_customer', methods=['POST'])
def register_customer():
    data = request.get_json()
    new_customer = Customer(name=data['name'], email=data['email'], phone_number=data.get('phone_number'))
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": f"Customer {data['name']} registered successfully!"}), 201

@app.route('/place_order', methods=['POST'])
@validate_stock
def place_order():
    data = request.get_json()
    customer_id = data['customer_id']
    items = data['items']

    # Create a new order
    new_order = Order(customer_id=customer_id)
    db.session.add(new_order)
    db.session.commit()

    # Add each item to the order
    total_amount = 0
    for item in items:
        product_id = item['product_id']
        quantity = item['quantity']

        product = Product.query.get(product_id)
        if product.stock < quantity:
            db.session.rollback()
            return jsonify({"error": f"Insufficient stock for {product.name}"}), 400
        
        unit_price = product.price
        total_price = unit_price * quantity
        discount_percentage = discount(quantity)
        final_price = total_price - (total_price * discount_percentage)
        total_amount += final_price

        # Deduct stock
        product.stock -= quantity
        db.session.add(OrderItem(order_id=new_order.order_id, product_id=product_id, quantity=quantity, unit_price=unit_price, total_price=final_price))

    new_order.total_amount = total_amount
    db.session.commit()
    return jsonify({"message": f"Order placed successfully for Customer {customer_id}", "total_amount": f"${total_amount:.2f}"}), 201

# Generator function to stream order history
@app.route('/order_history/<int:customer_id>')
def order_history(customer_id):
    def generate():
        orders = Order.query.filter_by(customer_id=customer_id).all()
        for order in orders:
            yield f"Order ID: {order.order_id}, Date: {order.order_date}, Status: {order.status}\n"
            for item in order.order_items:
                yield f"  - Product: {item.product.name}, Quantity: {item.quantity}, Total Price: ${item.total_price}\n"
    return app.response_class(generate(), mimetype='text/plain')

# Update Order Status
@app.route('/update_order_status', methods=['PATCH'])
def update_order_status():
    data = request.get_json()
    order_id = data['order_id']
    status = data['status']

    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    
    order.status = status
    db.session.commit()
    return jsonify({"message": f"Order {order_id} status updated to {status}"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
