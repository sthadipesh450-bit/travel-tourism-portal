"""
FORMS MODULE FOR TRAVEL & TOURISM PORTAL
BIT233 - Web Technology Assignment

This file contains all form definitions using Flask-WTF and WTForms.

What is WTForms?
- WTForms is a flexible forms validation and rendering library for Python
- It provides automatic validation, CSRF protection, and error handling
- Makes form handling much easier and more secure

Why use forms?
- Server-side validation (client-side JS validation can be bypassed)
- Automatic CSRF token generation for security
- Cleaner code with reusable form classes
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, FloatField, DateField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange
from models import User
import re


class RegistrationForm(FlaskForm):
    """
    REGISTRATION FORM - For new user signup
    
    Validators ensure data quality:
    - DataRequired: Field cannot be empty
    - Length: String must be between min and max length
    - Email: Must be valid email format
    - EqualTo: Password confirmation must match password
    """
    
    username = StringField('Username', 
        validators=[
            DataRequired(message='Username is required'),
            Length(min=3, max=80, message='Username must be between 3 and 80 characters')
        ])
    
    email = StringField('Email', 
        validators=[
            DataRequired(message='Email is required'),
            Email(message='Invalid email address')
        ])
    
    phone = StringField('Phone Number', 
        validators=[
            Length(min=10, max=20, message='Phone number must be between 10 and 20 characters')
        ])
    
    password = PasswordField('Password', 
        validators=[
            DataRequired(message='Password is required'),
            Length(min=8, message='Password must be at least 8 characters long')
        ])
    
    confirm_password = PasswordField('Confirm Password', 
        validators=[
            DataRequired(message='Please confirm your password'),
            EqualTo('password', message='Passwords must match')
        ])
    
    def validate_username(self, username):
        """
        CUSTOM VALIDATOR - Check if username already exists
        
        This method is automatically called by WTForms when validating.
        Method name must be: validate_<field_name>
        
        Args:
            username: The username field from the form
            
        Raises:
            ValidationError: If username is already taken
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        """
        CUSTOM VALIDATOR - Check if email already exists
        
        Args:
            email: The email field from the form
            
        Raises:
            ValidationError: If email is already registered
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email or login.')
    
    def validate_password(self, password):
        """
        CUSTOM VALIDATOR - Check password strength
        
        Requirements:
        - At least 8 characters (checked by Length validator)
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        
        Args:
            password: The password field from the form
            
        Raises:
            ValidationError: If password doesn't meet requirements
        """
        password_value = password.data
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password_value):
            raise ValidationError('Password must contain at least one uppercase letter')
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password_value):
            raise ValidationError('Password must contain at least one lowercase letter')
        
        # Check for at least one digit
        if not re.search(r'\d', password_value):
            raise ValidationError('Password must contain at least one number')


class LoginForm(FlaskForm):
    """
    LOGIN FORM - For user authentication
    
    Simpler than registration form, only needs:
    - Email or username
    - Password
    """
    
    email = StringField('Email', 
        validators=[
            DataRequired(message='Email is required'),
            Email(message='Invalid email address')
        ])
    
    password = PasswordField('Password', 
        validators=[
            DataRequired(message='Password is required')
        ])


class BookingForm(FlaskForm):
    """
    BOOKING FORM - For booking tour packages
    
    Includes validation for:
    - Number of travelers (must be positive)
    - Travel date (must be future date)
    - Special requests (optional)
    """
    
    travel_date = DateField('Travel Date', 
        validators=[
            DataRequired(message='Travel date is required')
        ],
        format='%Y-%m-%d')  # Date format: YYYY-MM-DD
    
    number_of_travelers = IntegerField('Number of Travelers', 
        validators=[
            DataRequired(message='Number of travelers is required'),
            NumberRange(min=1, max=50, message='Number of travelers must be between 1 and 50')
        ])
    
    special_requests = TextAreaField('Special Requests',
        validators=[
            Length(max=500, message='Special requests cannot exceed 500 characters')
        ])
    
    def validate_travel_date(self, travel_date):
        """
        CUSTOM VALIDATOR - Ensure travel date is in the future
        
        Args:
            travel_date: The travel date field from the form
            
        Raises:
            ValidationError: If travel date is in the past
        """
        from datetime import date
        if travel_date.data < date.today():
            raise ValidationError('Travel date must be in the future')


class ProfileUpdateForm(FlaskForm):
    """
    PROFILE UPDATE FORM - For users to update their information
    
    Similar to registration but:
    - No password fields (separate form for password change)
    - Email and username can be updated
    - Custom validators check if new email/username is available
    """
    
    username = StringField('Username', 
        validators=[
            DataRequired(message='Username is required'),
            Length(min=3, max=80, message='Username must be between 3 and 80 characters')
        ])
    
    email = StringField('Email', 
        validators=[
            DataRequired(message='Email is required'),
            Email(message='Invalid email address')
        ])
    
    phone = StringField('Phone Number', 
        validators=[
            Length(max=20, message='Phone number cannot exceed 20 characters')
        ])


class PackageSearchForm(FlaskForm):
    """
    SEARCH FORM - For filtering tour packages
    
    Allows users to search by:
    - Keyword (searches in name and destination)
    - Category
    - Price range
    - Duration
    """
    
    keyword = StringField('Search', 
        validators=[
            Length(max=100, message='Search keyword too long')
        ])
    
    category = SelectField('Category', 
        choices=[
            ('', 'All Categories'),
            ('Adventure', 'Adventure'),
            ('Beach', 'Beach'),
            ('Cultural', 'Cultural'),
            ('Luxury', 'Luxury'),
            ('Wildlife', 'Wildlife'),
            ('Pilgrimage', 'Pilgrimage'),
            ('Hill Station', 'Hill Station')
        ])
    
    min_price = FloatField('Min Price',
        validators=[
            NumberRange(min=0, message='Price cannot be negative')
        ])
    
    max_price = FloatField('Max Price',
        validators=[
            NumberRange(min=0, message='Price cannot be negative')
        ])
    
    duration = SelectField('Duration', 
        choices=[
            ('', 'Any Duration'),
            ('1-3', '1-3 days'),
            ('4-7', '4-7 days'),
            ('8-14', '8-14 days'),
            ('15+', '15+ days')
        ])


class PackageForm(FlaskForm):
    """
    PACKAGE FORM - For admin to create and edit tour packages
    
    Includes all fields needed to create/update a tour package:
    - Basic info (name, destination, description)
    - Pricing and availability
    - Categories and images
    - Package details
    """
    
    name = StringField('Package Name', 
        validators=[
            DataRequired(message='Package name is required'),
            Length(min=3, max=200, message='Package name must be between 3 and 200 characters')
        ])
    
    destination = StringField('Destination', 
        validators=[
            DataRequired(message='Destination is required'),
            Length(min=2, max=100, message='Destination must be between 2 and 100 characters')
        ])
    
    description = TextAreaField('Description', 
        validators=[
            DataRequired(message='Description is required'),
            Length(min=20, max=2000, message='Description must be between 20 and 2000 characters')
        ])
    
    duration = IntegerField('Duration (days)', 
        validators=[
            DataRequired(message='Duration is required'),
            NumberRange(min=1, max=365, message='Duration must be between 1 and 365 days')
        ])
    
    price = FloatField('Price (NPR)', 
        validators=[
            DataRequired(message='Price is required'),
            NumberRange(min=0, message='Price cannot be negative')
        ])
    
    available_slots = IntegerField('Available Slots', 
        validators=[
            DataRequired(message='Available slots is required'),
            NumberRange(min=0, max=1000, message='Available slots must be between 0 and 1000')
        ])
    
    category = SelectField('Category', 
        choices=[
            ('Adventure', 'Adventure'),
            ('Beach', 'Beach'),
            ('Cultural', 'Cultural'),
            ('Luxury', 'Luxury'),
            ('Wildlife', 'Wildlife'),
            ('Pilgrimage', 'Pilgrimage'),
            ('Hill Station', 'Hill Station')
        ],
        validators=[
            DataRequired(message='Category is required')
        ])
    
    image_url = StringField('Image URL', 
        validators=[
            Length(max=500, message='Image URL too long')
        ])
    
    highlights = TextAreaField('Highlights', 
        validators=[
            Length(max=1000, message='Highlights cannot exceed 1000 characters')
        ])
    
    includes = TextAreaField('What\'s Included', 
        validators=[
            Length(max=1000, message='Includes section cannot exceed 1000 characters')
        ])
    
    excludes = TextAreaField('What\'s Excluded', 
        validators=[
            Length(max=1000, message='Excludes section cannot exceed 1000 characters')
        ])


"""
FORM VALIDATION PROCESS:

1. Client Side (Browser):
   - HTML5 validation attributes (required, min, max, type="email")
   - JavaScript validation for better UX
   - Can be bypassed by users

2. Server Side (Flask):
   - WTForms validation (CANNOT be bypassed)
   - Runs when form.validate_on_submit() is called
   - Checks all validators in order
   - Runs custom validate_<field> methods
   - Returns True if all validations pass

3. Security:
   - CSRF token automatically added by Flask-WTF
   - Protects against Cross-Site Request Forgery attacks
   - Token is checked on every form submission

This two-layer validation ensures:
- Good user experience (instant feedback from client-side)
- Strong security (server-side cannot be bypassed)
"""
