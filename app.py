# app.py

from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import validates

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define models
class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    vendor_sweets = db.relationship('VendorSweet', backref='vendor', lazy=True)

class Sweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    vendor_sweets = db.relationship('VendorSweet', backref='sweet', lazy=True)

class VendorSweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    sweet_id = db.Column(db.Integer, db.ForeignKey('sweet.id'), nullable=False)

    @validates('price')
    def validate_price(self, key, price):
        if price is None:
            raise ValueError("Price cannot be blank.")
        if price < 0:
            raise ValueError("Price cannot be a negative number.")
        return price

# Define routes
@app.route('/')
def home():
    return jsonify(message='Welcome to the Sweets Vendors API')

@app.route('/vendors', methods=['GET'])
def get_vendors():
    vendors = Vendor.query.all()
    vendors_data = [{'id': vendor.id, 'name': vendor.name} for vendor in vendors]
    return jsonify(vendors_data)

# ... (other routes remain the same)

# Sample data initialization
def initialize_data():
    vendor1 = Vendor(name='Vendor A')
    vendor2 = Vendor(name='Vendor B')

    sweet1 = Sweet(name='Sweet X')
    sweet2 = Sweet(name='Sweet Y')

    db.session.add_all([vendor1, vendor2, sweet1, sweet2])
    db.session.commit()

    vendor_sweet1 = VendorSweet(price=10, vendor=vendor1, sweet=sweet1)
    vendor_sweet2 = VendorSweet(price=15, vendor=vendor2, sweet=sweet2)

    db.session.add_all([vendor_sweet1, vendor_sweet2])
    db.session.commit()

# Ensure that the data is initialized when the application is run
with app.app_context():
    db.create_all()  # Create database tables before running the app
    initialize_data()  # Initialize sample data

if __name__ == '__main__':
    app.run(port=5555)
