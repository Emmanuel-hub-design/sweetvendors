# app/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

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
