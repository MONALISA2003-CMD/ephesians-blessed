# app.py - Main Application File
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

app = Flask(_name_)
app.secret_key = 'eph_blessed_2023'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ephesians.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Executive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    last_login = db.Column(db.DateTime)

class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    executive_id = db.Column(db.Integer, db.ForeignKey('executive.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    districts = db.Column(db.Text, nullable=False)
    id_photos = db.Column(db.String(255), nullable=False)  # JSON with front/back
    profile_photo = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    nok_details = db.Column(db.Text)  # JSON with next of kin info
    group_name = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    id_photos = db.Column(db.String(255), nullable=False)
    profile_photo = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    nok_details = db.Column(db.Text)  # JSON with next of kin(s) info
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PhoneModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(50), nullable=False)
    storage = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    loan_terms = db.Column(db.Text)

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('phone_model.id'), nullable=False)
    imei = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='available')  # available, allocated, sold
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_nok = db.Column(db.String(100), nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)
    receipt_number = db.Column(db.String(20), unique=True, nullable=False)
    payment_details = db.Column(db.Text)  # JSON with payment info

# Create tables
with app.app_context():
    db.create_all()