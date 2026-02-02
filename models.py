"""
DATABASE MODELS FOR TRAVEL & TOURISM PORTAL
BIT233 - Web Technology Assignment

This file contains all database models using SQLAlchemy ORM.
SQLAlchemy is a Python toolkit that makes it easy to work with databases.

What is ORM? 
- ORM = Object Relational Mapping
- It allows us to work with databases using Python classes instead of SQL
- Each class represents a table in the database
- Each object represents a row in that table
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy database object
# This will be imported and used in our main app.py file
db = SQLAlchemy()


class User(db.Model):
    """
    USER MODEL - Represents registered users in the system
    
    This table stores all user information including authentication details.
    Each user can have multiple bookings (one-to-many relationship).
    """
    
    # Define table name in database
    __tablename__ = 'users'
    
    # PRIMARY KEY - unique identifier for each user
    id = db.Column(db.Integer, primary_key=True)
    
    # User Information Fields
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    
    # Role field to differentiate between regular users and admins
    # Default value is 'user', admins have role='admin'
    role = db.Column(db.String(20), default='user')
    
    # Timestamp when user registered
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # RELATIONSHIP: One user can have many bookings
    # backref creates a reverse relationship (booking.user will give us the user)
    # lazy='dynamic' means bookings are loaded only when accessed
    bookings = db.relationship('Booking', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """
        Hash the password before storing in database
        
        Why hash passwords?
        - Security! Never store plain text passwords
        - If database is compromised, passwords remain safe
        - Werkzeug's generate_password_hash uses strong encryption
        
        Args:
            password (str): Plain text password from user
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Verify if provided password matches stored hash
        
        Args:
            password (str): Plain text password to check
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        """String representation of User object for debugging"""
        return f'<User {self.username}>'


class TourPackage(db.Model):
    """
    TOUR PACKAGE MODEL - Represents tour packages offered by the portal
    
    This table stores all information about tour packages including:
    - Basic info (name, destination, description)
    - Pricing and availability
    - Images and categories
    """
    
    __tablename__ = 'tour_packages'
    
    # PRIMARY KEY
    id = db.Column(db.Integer, primary_key=True)
    
    # Package Information
    name = db.Column(db.String(200), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # Tour duration in days
    duration = db.Column(db.Integer, nullable=False)
    
    # Price per person
    price = db.Column(db.Float, nullable=False)
    
    # URL to package image
    image_url = db.Column(db.String(500), nullable=True)
    
    # Number of slots available for booking
    available_slots = db.Column(db.Integer, default=50)
    
    # Category for filtering (e.g., 'Adventure', 'Beach', 'Cultural', 'Luxury')
    category = db.Column(db.String(50), nullable=True)
    
    # Additional package details
    highlights = db.Column(db.Text, nullable=True)
    includes = db.Column(db.Text, nullable=True)
    excludes = db.Column(db.Text, nullable=True)
    
    # Timestamp when package was added
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # RELATIONSHIP: One package can have many bookings
    bookings = db.relationship('Booking', backref='package', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        """String representation of TourPackage object"""
        return f'<TourPackage {self.name}>'


class Booking(db.Model):
    """
    BOOKING MODEL - Represents tour bookings made by users
    
    This is the junction table that connects Users and TourPackages.
    It demonstrates a many-to-many relationship through foreign keys.
    
    Relationships:
    - Many bookings can belong to one user (many-to-one)
    - Many bookings can belong to one package (many-to-one)
    """
    
    __tablename__ = 'bookings'
    
    # PRIMARY KEY
    id = db.Column(db.Integer, primary_key=True)
    
    # FOREIGN KEYS - Create relationships with other tables
    # Foreign Key to User table
    # ondelete='CASCADE' means if user is deleted, their bookings are also deleted
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    # Foreign Key to TourPackage table
    package_id = db.Column(db.Integer, db.ForeignKey('tour_packages.id', ondelete='CASCADE'), nullable=False)
    
    # Booking Information
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    travel_date = db.Column(db.Date, nullable=False)
    number_of_travelers = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    
    # Booking status: 'pending', 'confirmed', 'cancelled', 'completed'
    status = db.Column(db.String(20), default='pending')
    
    # Optional field for special requests from customers
    special_requests = db.Column(db.Text, nullable=True)
    
    # Payment status (for future enhancement)
    payment_status = db.Column(db.String(20), default='unpaid')
    
    def __repr__(self):
        """String representation of Booking object"""
        return f'<Booking {self.id} - User {self.user_id} - Package {self.package_id}>'


"""
DATABASE RELATIONSHIPS SUMMARY:

1. User ←→ Booking (One-to-Many)
   - One user can make many bookings
   - Each booking belongs to one user
   - Access: user.bookings or booking.user

2. TourPackage ←→ Booking (One-to-Many)
   - One package can have many bookings
   - Each booking is for one package
   - Access: package.bookings or booking.package

This design follows database normalization principles:
- Eliminates data redundancy
- Ensures data integrity
- Makes it easy to query related data
"""
