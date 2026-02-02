"""
MAIN FLASK APPLICATION - TRAVEL & TOURISM PORTAL
BIT233 - Web Technology Assignment

This is the main application file that:
1. Initializes Flask app and database
2. Configures session management
3. Defines all routes (URLs) and their functions
4. Handles user authentication and authorization

FLASK BASICS:
- Flask is a micro web framework for Python
- Routes map URLs to Python functions
- Functions return HTML templates or redirect to other routes
- @app.route decorator defines which URL triggers which function
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User, TourPackage, Booking
from forms import RegistrationForm, LoginForm, BookingForm, ProfileUpdateForm, PackageSearchForm, PackageForm
from datetime import datetime, date
from functools import wraps
import os

# ============================================================================
# FLASK APP INITIALIZATION
# ============================================================================

app = Flask(__name__)

# SECRET KEY - Used for session encryption and CSRF protection
# In production, use environment variable: os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production-12345'

# DATABASE CONFIGURATION
# SQLite database file will be created in the same directory
# For production, use PostgreSQL or MySQL instead
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_tourism.db'

# Disable modification tracking to save resources
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database with app
db.init_app(app)


# ============================================================================
# HELPER FUNCTIONS AND DECORATORS
# ============================================================================

def login_required(f):
    """
    DECORATOR - Protect routes that require authentication
    
    What is a decorator?
    - A function that wraps another function
    - Adds functionality without modifying the original function
    - In this case, checks if user is logged in
    
    Usage:
        @app.route('/dashboard')
        @login_required
        def dashboard():
            # This code only runs if user is logged in
    
    How it works:
    1. Check if 'user_id' exists in session
    2. If yes, allow access to the route
    3. If no, redirect to login page with error message
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user_id exists in session (meaning user is logged in)
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    DECORATOR - Protect routes that require admin access
    
    Similar to login_required but also checks if user has admin role
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        
        # Get current user and check role
        user = User.query.get(session['user_id'])
        if not user or user.role != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# PUBLIC ROUTES (No authentication required)
# ============================================================================

@app.route('/')
def index():
    """
    HOME PAGE ROUTE
    
    Displays:
    - Hero section with call-to-action
    - Featured tour packages (top 6)
    - Testimonials
    - Why choose us section
    
    Template: index.html
    """
    # Get featured packages (6 random packages for variety)
    featured_packages = TourPackage.query.order_by(db.func.random()).limit(6).all()
    
    return render_template('index.html', packages=featured_packages)


@app.route('/packages')
def packages():
    """
    BROWSE PACKAGES ROUTE
    
    Features:
    - Display all tour packages
    - Search by keyword (name/destination)
    - Filter by category
    - Filter by price range
    - Filter by duration
    
    Template: packages.html
    """
    # Create search form
    form = PackageSearchForm(request.args, meta={'csrf': False})
    
    # Start with base query
    query = TourPackage.query
    
    # Apply search filters if provided
    if form.keyword.data:
        # Search in name and destination using LIKE for partial matches
        keyword = f"%{form.keyword.data}%"
        query = query.filter(
            db.or_(
                TourPackage.name.like(keyword),
                TourPackage.destination.like(keyword)
            )
        )
    
    # Filter by category
    if form.category.data:
        query = query.filter(TourPackage.category == form.category.data)
    
    # Filter by price range
    if form.min_price.data is not None:
        query = query.filter(TourPackage.price >= form.min_price.data)
    
    if form.max_price.data is not None:
        query = query.filter(TourPackage.price <= form.max_price.data)
    
    # Filter by duration
    if form.duration.data:
        duration_filter = form.duration.data
        if duration_filter == '1-3':
            query = query.filter(TourPackage.duration.between(1, 3))
        elif duration_filter == '4-7':
            query = query.filter(TourPackage.duration.between(4, 7))
        elif duration_filter == '8-14':
            query = query.filter(TourPackage.duration.between(8, 14))
        elif duration_filter == '15+':
            query = query.filter(TourPackage.duration >= 15)
    
    # Execute query and get all matching packages
    all_packages = query.all()
    
    return render_template('packages.html', packages=all_packages, form=form)


@app.route('/package/<int:package_id>')
def package_detail(package_id):
    """
    PACKAGE DETAIL ROUTE
    
    Shows detailed information about a specific tour package:
    - Full description
    - Pricing
    - Duration
    - Highlights
    - What's included/excluded
    - Booking button
    
    Args:
        package_id (int): ID of the package to display
    
    Template: package_detail.html
    """
    # Get package by ID or return 404 if not found
    package = TourPackage.query.get_or_404(package_id)
    
    return render_template('package_detail.html', package=package)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    USER REGISTRATION ROUTE
    
    GET: Display registration form
    POST: Process form submission and create new user
    
    Process:
    1. Display form
    2. Validate form data
    3. Check if username/email already exists
    4. Hash password
    5. Create new user in database
    6. Redirect to login page
    
    Template: register.html
    """
    # If user is already logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    
    # POST request - form submitted
    if form.validate_on_submit():
        # Create new user object
        user = User(
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data
        )
        
        # Hash and set password (NEVER store plain text passwords!)
        user.set_password(form.password.data)
        
        # Add to database
        try:
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
            print(f"Registration error: {e}")
    
    # GET request - display form
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    USER LOGIN ROUTE
    
    GET: Display login form
    POST: Authenticate user and create session
    
    Process:
    1. Display form
    2. Validate form data
    3. Check if user exists
    4. Verify password
    5. Create session
    6. Redirect to dashboard
    
    What is a session?
    - Temporary storage on the server for user data
    - Each user has a unique session
    - Session persists across page requests
    - Used to keep users logged in
    
    Template: login.html
    """
    # If user is already logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        # Find user by email
        user = User.query.filter_by(email=form.email.data).first()
        
        # Check if user exists and password is correct
        if user and user.check_password(form.password.data):
            # Create session - this keeps user logged in
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            
            flash(f'Welcome back, {user.username}!', 'success')
            
            # Redirect to the page user was trying to access, or dashboard
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        
        else:
            flash('Invalid email or password. Please try again.', 'danger')
    
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """
    LOGOUT ROUTE
    
    Process:
    1. Clear session data
    2. Display goodbye message
    3. Redirect to home page
    """
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))


# ============================================================================
# PROTECTED ROUTES (Authentication required)
# ============================================================================

@app.route('/dashboard')
@login_required
def dashboard():
    """
    USER DASHBOARD ROUTE
    
    Displays:
    - User information
    - Booking history (all bookings)
    - Booking statistics
    - Quick actions
    
    Template: dashboard.html
    """
    # Get current user
    user = User.query.get(session['user_id'])
    
    # Get all bookings for this user, ordered by booking date (newest first)
    bookings = Booking.query.filter_by(user_id=user.id).order_by(Booking.booking_date.desc()).all()
    
    # Calculate statistics
    total_bookings = len(bookings)
    pending_bookings = len([b for b in bookings if b.status == 'pending'])
    confirmed_bookings = len([b for b in bookings if b.status == 'confirmed'])
    
    return render_template('dashboard.html', 
                         user=user, 
                         bookings=bookings,
                         total_bookings=total_bookings,
                         pending_bookings=pending_bookings,
                         confirmed_bookings=confirmed_bookings)


@app.route('/book/<int:package_id>', methods=['GET', 'POST'])
@login_required
def book_package(package_id):
    """
    BOOK PACKAGE ROUTE
    
    GET: Display booking form for specific package
    POST: Process booking and create booking record
    
    Process:
    1. Display booking form
    2. Validate travel date and travelers
    3. Check available slots
    4. Calculate total amount
    5. Create booking record
    6. Update available slots
    7. Redirect to dashboard
    
    Args:
        package_id (int): ID of package to book
    
    Template: booking.html
    """
    # Get package or 404
    package = TourPackage.query.get_or_404(package_id)
    
    form = BookingForm()
    
    if form.validate_on_submit():
        # Check if enough slots are available
        if package.available_slots < form.number_of_travelers.data:
            flash(f'Sorry, only {package.available_slots} slots available.', 'danger')
            return redirect(url_for('book_package', package_id=package_id))
        
        # Calculate total amount
        total_amount = package.price * form.number_of_travelers.data
        
        # Create booking
        booking = Booking(
            user_id=session['user_id'],
            package_id=package_id,
            travel_date=form.travel_date.data,
            number_of_travelers=form.number_of_travelers.data,
            total_amount=total_amount,
            special_requests=form.special_requests.data,
            status='pending'
        )
        
        # Update available slots
        package.available_slots -= form.number_of_travelers.data
        
        try:
            db.session.add(booking)
            db.session.commit()
            
            flash('Booking successful! Your booking is pending confirmation.', 'success')
            return redirect(url_for('dashboard'))
        
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while processing your booking. Please try again.', 'danger')
            print(f"Booking error: {e}")
    
    return render_template('booking.html', package=package, form=form)


@app.route('/booking/<int:booking_id>/cancel', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    """
    CANCEL BOOKING ROUTE
    
    Allows users to cancel their pending bookings
    
    Process:
    1. Find booking
    2. Verify booking belongs to current user
    3. Check if booking is cancellable (only pending bookings)
    4. Update booking status
    5. Restore available slots
    6. Redirect to dashboard
    
    Args:
        booking_id (int): ID of booking to cancel
    """
    booking = Booking.query.get_or_404(booking_id)
    
    # Security check: ensure booking belongs to current user
    if booking.user_id != session['user_id']:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Can only cancel pending bookings
    if booking.status != 'pending':
        flash('Only pending bookings can be cancelled.', 'warning')
        return redirect(url_for('dashboard'))
    
    # Update booking status
    booking.status = 'cancelled'
    
    # Restore available slots
    package = TourPackage.query.get(booking.package_id)
    package.available_slots += booking.number_of_travelers
    
    try:
        db.session.commit()
        flash('Booking cancelled successfully.', 'info')
    except Exception as e:
        db.session.rollback()
        flash('Error cancelling booking.', 'danger')
        print(f"Cancel booking error: {e}")
    
    return redirect(url_for('dashboard'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    USER PROFILE ROUTE
    
    GET: Display profile information and edit form
    POST: Update user profile
    
    Template: profile.html
    """
    user = User.query.get(session['user_id'])
    form = ProfileUpdateForm(obj=user)
    
    if form.validate_on_submit():
        # Check if username is changed and not taken by another user
        if form.username.data != user.username:
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user:
                flash('Username already taken.', 'danger')
                return redirect(url_for('profile'))
        
        # Check if email is changed and not taken by another user
        if form.email.data != user.email:
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('Email already registered.', 'danger')
                return redirect(url_for('profile'))
        
        # Update user information
        user.username = form.username.data
        user.email = form.email.data
        user.phone = form.phone.data
        
        try:
            db.session.commit()
            session['username'] = user.username  # Update session
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating profile.', 'danger')
            print(f"Profile update error: {e}")
    
    return render_template('profile.html', user=user, form=form)


# ============================================================================
# ADMIN ROUTES
# ============================================================================

@app.route('/admin')
@admin_required
def admin_dashboard():
    """
    ADMIN DASHBOARD ROUTE
    
    Displays:
    - Total statistics
    - All bookings
    - User management
    - Package management
    
    Template: admin_dashboard.html
    """
    # Get statistics
    total_users = User.query.count()
    total_packages = TourPackage.query.count()
    total_bookings = Booking.query.count()
    total_revenue = db.session.query(db.func.sum(Booking.total_amount)).scalar() or 0
    
    # Get recent bookings
    recent_bookings = Booking.query.order_by(Booking.booking_date.desc()).limit(10).all()
    
    return render_template('admin_dashboard.html',
                         total_users=total_users,
                         total_packages=total_packages,
                         total_bookings=total_bookings,
                         total_revenue=total_revenue,
                         recent_bookings=recent_bookings)


@app.route('/admin/booking/<int:booking_id>/approve', methods=['POST'])
@admin_required
def approve_booking(booking_id):
    """
    APPROVE BOOKING ROUTE
    
    Allows admin to approve a pending booking
    
    Process:
    1. Find booking by ID
    2. Verify booking is in pending status
    3. Update status to confirmed
    4. Save changes to database
    5. Show success message
    6. Redirect back to admin dashboard
    
    Args:
        booking_id (int): ID of booking to approve
    """
    booking = Booking.query.get_or_404(booking_id)
    
    # Check if booking is pending
    if booking.status != 'pending':
        flash('Only pending bookings can be approved.', 'warning')
        return redirect(url_for('admin_dashboard'))
    
    # Update booking status to confirmed
    booking.status = 'confirmed'
    
    try:
        db.session.commit()
        flash(f'Booking #{booking.id} has been approved successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error approving booking. Please try again.', 'danger')
        print(f"Approve booking error: {e}")
    
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/booking/<int:booking_id>/reject', methods=['POST'])
@admin_required
def reject_booking(booking_id):
    """
    REJECT BOOKING ROUTE
    
    Allows admin to reject/disapprove a pending booking
    
    Process:
    1. Find booking by ID
    2. Verify booking is in pending status
    3. Update status to cancelled
    4. Restore available slots to the package
    5. Save changes to database
    6. Show success message
    7. Redirect back to admin dashboard
    
    Args:
        booking_id (int): ID of booking to reject
    """
    booking = Booking.query.get_or_404(booking_id)
    
    # Check if booking is pending
    if booking.status != 'pending':
        flash('Only pending bookings can be rejected.', 'warning')
        return redirect(url_for('admin_dashboard'))
    
    # Update booking status to cancelled
    booking.status = 'cancelled'
    
    # Restore available slots to the package
    package = TourPackage.query.get(booking.package_id)
    package.available_slots += booking.number_of_travelers
    
    try:
        db.session.commit()
        flash(f'Booking #{booking.id} has been rejected and slots restored.', 'info')
    except Exception as e:
        db.session.rollback()
        flash('Error rejecting booking. Please try again.', 'danger')
        print(f"Reject booking error: {e}")
    
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/packages')
@admin_required
def manage_packages():
    """
    MANAGE PACKAGES ROUTE
    
    Displays all tour packages with options to:
    - View all packages
    - Add new package
    - Edit existing package
    - Delete package
    
    Template: manage_packages.html
    """
    packages = TourPackage.query.order_by(TourPackage.created_at.desc()).all()
    return render_template('manage_packages.html', packages=packages)


@app.route('/admin/package/add', methods=['GET', 'POST'])
@admin_required
def add_package():
    """
    ADD PACKAGE ROUTE
    
    Allows admin to create a new tour package
    
    GET: Display the package creation form
    POST: Process form submission and create package
    
    Template: package_form.html
    """
    form = PackageForm()
    
    if form.validate_on_submit():
        # Create new package
        package = TourPackage(
            name=form.name.data,
            destination=form.destination.data,
            description=form.description.data,
            duration=form.duration.data,
            price=form.price.data,
            available_slots=form.available_slots.data,
            category=form.category.data,
            image_url=form.image_url.data,
            highlights=form.highlights.data,
            includes=form.includes.data,
            excludes=form.excludes.data
        )
        
        try:
            db.session.add(package)
            db.session.commit()
            flash('Package created successfully!', 'success')
            return redirect(url_for('manage_packages'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating package. Please try again.', 'danger')
            print(f"Add package error: {e}")
    
    return render_template('package_form.html', form=form, title='Add New Package')


@app.route('/admin/package/<int:package_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_package(package_id):
    """
    EDIT PACKAGE ROUTE
    
    Allows admin to edit an existing tour package
    
    GET: Display the package edit form with current values
    POST: Process form submission and update package
    
    Args:
        package_id (int): ID of package to edit
    
    Template: package_form.html
    """
    package = TourPackage.query.get_or_404(package_id)
    form = PackageForm(obj=package)
    
    if form.validate_on_submit():
        # Update package fields
        package.name = form.name.data
        package.destination = form.destination.data
        package.description = form.description.data
        package.duration = form.duration.data
        package.price = form.price.data
        package.available_slots = form.available_slots.data
        package.category = form.category.data
        package.image_url = form.image_url.data
        package.highlights = form.highlights.data
        package.includes = form.includes.data
        package.excludes = form.excludes.data
        
        try:
            db.session.commit()
            flash('Package updated successfully!', 'success')
            return redirect(url_for('manage_packages'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating package. Please try again.', 'danger')
            print(f"Edit package error: {e}")
    
    return render_template('package_form.html', form=form, title='Edit Package', package=package)


@app.route('/admin/package/<int:package_id>/delete', methods=['POST'])
@admin_required
def delete_package(package_id):
    """
    DELETE PACKAGE ROUTE
    
    Allows admin to delete a tour package
    
    Note: This will also delete all associated bookings (cascade delete)
    Admin should be warned before deletion
    
    Args:
        package_id (int): ID of package to delete
    """
    package = TourPackage.query.get_or_404(package_id)
    
    # Check if there are any confirmed bookings
    confirmed_bookings = Booking.query.filter_by(
        package_id=package_id, 
        status='confirmed'
    ).count()
    
    if confirmed_bookings > 0:
        flash(f'Cannot delete package with {confirmed_bookings} confirmed bookings. Please cancel them first.', 'danger')
        return redirect(url_for('manage_packages'))
    
    try:
        db.session.delete(package)
        db.session.commit()
        flash('Package deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting package. Please try again.', 'danger')
        print(f"Delete package error: {e}")
    
    return redirect(url_for('manage_packages'))


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors (page not found)"""
    flash('Page not found.', 'warning')
    return redirect(url_for('index'))


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors (server error)"""
    db.session.rollback()
    flash('An internal error occurred.', 'danger')
    return redirect(url_for('index'))


# ============================================================================
# DATABASE INITIALIZATION AND SAMPLE DATA
# ============================================================================

def init_db():
    """
    Initialize database and create sample data
    
    This function:
    1. Creates all database tables
    2. Adds sample tour packages
    3. Creates admin user
    
    Run this once when setting up the application
    """
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if data already exists
        if TourPackage.query.first() is not None:
            print("Database already initialized!")
            return
        
        print("Initializing database...")
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@travel.com',
            phone='1234567890',
            role='admin'
        )
        admin.set_password('Admin@123')
        db.session.add(admin)
        
        # Create sample tour packages
        packages = [
            TourPackage(
                name='Pokhara Adventure Trek',
                destination='Pokhara',
                description='Experience the breathtaking beauty of Pokhara with our adventure package. Trek through stunning mountain trails, visit serene lakes, and immerse yourself in the natural beauty of Nepal.',
                duration=5,
                price=15000.00,
                image_url='https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=800',
                available_slots=25,
                category='Adventure',
                highlights='Mountain trekking, Phewa Lake, Paragliding, Mountain views',
                includes='Accommodation, Meals, Guide, Transportation',
                excludes='Personal expenses, Travel insurance'
            ),
            TourPackage(
                name='Chitwan Wildlife Safari',
                destination='Chitwan',
                description='Explore the rich biodiversity of Chitwan National Park. Spot rare wildlife including rhinos, tigers, and exotic birds in their natural habitat.',
                duration=3,
                price=12000.00,
                image_url='https://images.unsplash.com/photo-1549366021-9f761d450615?w=800',
                available_slots=30,
                category='Wildlife',
                highlights='Jungle safari, Elephant ride, Bird watching, Tharu cultural show',
                includes='Park entry, Safari, Accommodation, Meals',
                excludes='Personal expenses, Camera fees'
            ),
            TourPackage(
                name='Lumbini Pilgrimage Tour',
                destination='Lumbini',
                description='Visit the birthplace of Lord Buddha. A spiritual journey through monasteries, temples, and the sacred Maya Devi Temple.',
                duration=2,
                price=8000.00,
                image_url='https://images.unsplash.com/photo-1548013146-72479768bada?w=800',
                available_slots=40,
                category='Pilgrimage',
                highlights='Maya Devi Temple, World Peace Pagoda, Monasteries, Sacred garden',
                includes='Accommodation, Meals, Guide, Transportation',
                excludes='Personal offerings, Donations'
            ),
            TourPackage(
                name='Kathmandu Cultural Heritage',
                destination='Kathmandu',
                description='Discover the rich cultural heritage of Kathmandu Valley. Visit UNESCO World Heritage Sites including Durbar Squares, ancient temples, and stupas.',
                duration=4,
                price=10000.00,
                image_url='https://images.unsplash.com/photo-1571678418934-4c99485db84a?w=800',
                available_slots=35,
                category='Cultural',
                highlights='Pashupatinath, Boudhanath, Swayambhunath, Durbar Squares',
                includes='Accommodation, Breakfast, Guide, Transportation',
                excludes='Lunch, Dinner, Site entry fees'
            ),
            TourPackage(
                name='Everest Base Camp Luxury Trek',
                destination='Everest Region',
                description='Luxury trekking experience to Everest Base Camp. Stay in premium lodges and enjoy gourmet meals while trekking to the base of the world\'s highest mountain.',
                duration=14,
                price=85000.00,
                image_url='https://images.unsplash.com/photo-1486870591958-9b9d0d1dda99?w=800',
                available_slots=15,
                category='Luxury',
                highlights='Everest Base Camp, Namche Bazaar, Tengboche Monastery, Sherpa culture',
                includes='Luxury accommodation, All meals, Guide, Permits, Helicopter return',
                excludes='International flight, Personal equipment, Travel insurance'
            ),
            TourPackage(
                name='Nagarkot Sunrise & Hill Station',
                destination='Nagarkot',
                description='Witness spectacular sunrise over the Himalayas from Nagarkot. Perfect weekend getaway with panoramic mountain views.',
                duration=2,
                price=6000.00,
                image_url='https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',
                available_slots=45,
                category='Hill Station',
                highlights='Himalayan sunrise, Mountain views, Hiking trails, Fresh mountain air',
                includes='Accommodation, Meals, Transportation',
                excludes='Personal expenses'
            ),
            TourPackage(
                name='Annapurna Circuit Trek',
                destination='Annapurna Region',
                description='Classic trek around the Annapurna massif. Experience diverse landscapes from subtropical forests to high mountain desert.',
                duration=18,
                price=45000.00,
                image_url='https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',
                available_slots=20,
                category='Adventure',
                highlights='Thorong La Pass, Diverse ecosystems, Local culture, Mountain views',
                includes='Accommodation, Meals, Guide, Permits',
                excludes='Personal equipment, Travel insurance, Tips'
            ),
            TourPackage(
                name='Bandipur Heritage Village',
                destination='Bandipur',
                description='Experience traditional Newari culture in this beautifully preserved hilltop village with stunning mountain views.',
                duration=2,
                price=7000.00,
                image_url='https://images.unsplash.com/photo-1504214208698-ea1916a2195a?w=800',
                available_slots=30,
                category='Cultural',
                highlights='Traditional architecture, Mountain views, Local culture, Village walks',
                includes='Accommodation, Meals, Guide',
                excludes='Transportation, Personal expenses'
            )
        ]
        
        # Add all packages to database
        for package in packages:
            db.session.add(package)
        
        # Commit all changes
        db.session.commit()
        
        print("Database initialized successfully!")
        print("Admin credentials: admin@travel.com / Admin@123")


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    # Initialize database if it doesn't exist
    if not os.path.exists('travel_tourism.db'):
        init_db()
    
    # Run Flask application
    # debug=True enables auto-reload and detailed error pages
    # Remove debug=True in production!
    app.run(debug=True, host='0.0.0.0', port=5000)


"""
UNDERSTANDING FLASK ROUTES:

Route Anatomy:
@app.route('/path', methods=['GET', 'POST'])
def function_name():
    # Function code
    return render_template('template.html')

Components:
- @app.route: Decorator that maps URL to function
- '/path': URL path (e.g., /login, /dashboard)
- methods: HTTP methods allowed (GET for viewing, POST for form submission)
- function_name: Python function that handles the request
- render_template: Returns HTML page
- redirect: Sends user to different page

HTTP Methods:
- GET: Retrieve data (viewing pages)
- POST: Submit data (form submissions)
- PUT: Update data
- DELETE: Delete data

Session Management:
- session['key'] = value: Store data in session
- session.get('key'): Retrieve data from session
- session.clear(): Delete all session data
- Sessions persist across requests
- Each user has unique session

Flash Messages:
- flash('message', 'category'): Display temporary message
- Categories: success, danger, warning, info
- Messages displayed once and then cleared
- Good for user feedback after actions

Security Best Practices:
1. Never store plain text passwords (use hashing)
2. Use CSRF tokens on forms (automatic with Flask-WTF)
3. Validate all user input (server-side)
4. Use @login_required for protected routes
5. Check user permissions before sensitive actions
6. Use environment variables for secret keys
"""
