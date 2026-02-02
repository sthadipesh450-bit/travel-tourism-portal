# 🌍 Travel & Tourism Portal

**BIT233 - Web Technology Assignment**

A comprehensive full-stack web application for booking tour packages, built with Flask, Bootstrap 5, and SQLAlchemy.

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Features](#-features)
- [Technologies Used](#-technologies-used)
- [Project Structure](#-project-structure)
- [Installation Guide](#-installation-guide)
- [Running the Application](#-running-the-application)
- [Database Schema](#-database-schema)
- [User Credentials](#-user-credentials)
- [Screenshots](#-screenshots)
- [CRUD Operations](#-crud-operations)
- [Validation Features](#-validation-features)
- [Future Enhancements](#-future-enhancements)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## 🎯 Project Overview

The **Travel & Tourism Portal** is a modern web application that allows users to:
- Browse and search tour packages
- Register and manage their accounts
- Book tour packages with real-time availability checking
- View and manage their bookings
- Admin dashboard for managing the system

This project demonstrates full-stack web development skills including:
- Backend development with Flask
- Database design and ORM usage
- Frontend development with Bootstrap 5
- Form validation (both client and server-side)
- User authentication and session management
- RESTful API design principles

---

## ✨ Features

### User Features
- **User Registration & Authentication**
  - Secure password hashing with Werkzeug
  - Session-based authentication
  - Profile management

- **Tour Package Browsing**
  - View all available packages
  - Search by keyword (name/destination)
  - Filter by category, price range, and duration
  - Detailed package information with images

- **Booking System**
  - Book packages with date selection
  - Specify number of travelers
  - Real-time price calculation
  - Add special requests
  - View booking history

- **User Dashboard**
  - View all bookings
  - Check booking status
  - Cancel pending bookings
  - Statistics overview

### Admin Features
- **Admin Dashboard**
  - View total users, packages, bookings
  - Monitor revenue
  - View recent bookings
  - User and package management

### Technical Features
- **Responsive Design**
  - Mobile-first approach
  - Bootstrap 5 grid system
  - Works on all devices

- **Security**
  - Password hashing (never stores plain text)
  - CSRF protection on all forms
  - SQL injection prevention (ORM)
  - Session management

- **Validation**
  - Client-side validation (JavaScript)
  - Server-side validation (WTForms)
  - Custom validators for business logic

---

## 🛠️ Technologies Used

### Backend
- **Flask 3.0.0** - Python web framework
- **Flask-SQLAlchemy 3.1.1** - ORM for database operations
- **Flask-WTF 1.2.1** - Form handling and CSRF protection
- **WTForms 3.1.1** - Form validation
- **Werkzeug 3.0.1** - Password hashing and utilities
- **SQLite** - Database (development)

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Custom styles with modern features
- **Bootstrap 5.3.0** - Responsive CSS framework
- **Bootstrap Icons 1.11.0** - Icon library
- **JavaScript (ES6+)** - Client-side interactivity
- **jQuery 3.7.0** - DOM manipulation

### Design Patterns
- MVC (Model-View-Controller)
- Template inheritance (Jinja2)
- RESTful routing
- ORM pattern

---

## 📁 Project Structure

```
travel-tourism-portal/
│
├── app.py                      # Main Flask application with routes
├── models.py                   # Database models (User, TourPackage, Booking)
├── forms.py                    # WTForms form definitions
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── travel_tourism.db          # SQLite database (auto-generated)
│
├── static/                    # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css          # Custom styles (TripAdvisor-inspired)
│   ├── js/
│   │   └── script.js          # Client-side JavaScript
│   └── images/                # Package images
│
└── templates/                 # HTML templates (Jinja2)
    ├── base.html              # Base template (parent)
    ├── index.html             # Home page
    ├── packages.html          # Browse packages
    ├── package_detail.html    # Package details
    ├── register.html          # User registration
    ├── login.html             # User login
    ├── dashboard.html         # User dashboard
    ├── booking.html           # Booking form
    ├── profile.html           # User profile
    └── admin_dashboard.html   # Admin dashboard
```

---

## 🚀 Installation Guide

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Step 1: Clone or Download Project
```bash
# Option 1: Clone with Git
git clone <repository-url>
cd travel-tourism-portal

# Option 2: Download ZIP and extract
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
pip list
# You should see Flask, Flask-SQLAlchemy, Flask-WTF, etc.
```

---

## 🎮 Running the Application

### First Time Setup
The database will be automatically created with sample data on first run.

### Start the Server
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Access the Application
Open your web browser and go to:
```
http://localhost:5000
```

### Stop the Server
Press `Ctrl + C` in the terminal

---

## 🗄️ Database Schema

### Users Table
| Field         | Type     | Description                    |
|---------------|----------|--------------------------------|
| id            | Integer  | Primary Key                    |
| username      | String   | Unique username                |
| email         | String   | Unique email address           |
| password_hash | String   | Hashed password (secure)       |
| phone         | String   | Phone number                   |
| role          | String   | 'user' or 'admin'              |
| created_at    | DateTime | Registration timestamp         |

### TourPackages Table
| Field           | Type    | Description                    |
|-----------------|---------|--------------------------------|
| id              | Integer | Primary Key                    |
| name            | String  | Package name                   |
| destination     | String  | Destination location           |
| description     | Text    | Detailed description           |
| duration        | Integer | Duration in days               |
| price           | Float   | Price per person               |
| image_url       | String  | Package image URL              |
| available_slots | Integer | Number of available slots      |
| category        | String  | Package category               |
| highlights      | Text    | Package highlights             |
| includes        | Text    | What's included                |
| excludes        | Text    | What's not included            |
| created_at      | DateTime| Creation timestamp             |

### Bookings Table
| Field              | Type     | Description                    |
|--------------------|----------|--------------------------------|
| id                 | Integer  | Primary Key                    |
| user_id            | Integer  | Foreign Key → Users            |
| package_id         | Integer  | Foreign Key → TourPackages     |
| booking_date       | DateTime | Booking timestamp              |
| travel_date        | Date     | Planned travel date            |
| number_of_travelers| Integer  | Number of travelers            |
| total_amount       | Float    | Total booking amount           |
| status             | String   | pending/confirmed/cancelled    |
| special_requests   | Text     | Customer special requests      |
| payment_status     | String   | unpaid/paid                    |

### Relationships
- **One-to-Many**: User → Bookings (One user can have many bookings)
- **One-to-Many**: TourPackage → Bookings (One package can have many bookings)
- **Many-to-One**: Booking → User (Each booking belongs to one user)
- **Many-to-One**: Booking → TourPackage (Each booking is for one package)

---

## 👤 User Credentials

### Admin Account
- **Email**: admin@travel.com
- **Password**: Admin@123
- **Role**: Administrator

### Sample Regular User
You can register a new account or use:
- **Email**: Create your own account
- **Password**: Must meet requirements (8+ chars, uppercase, lowercase, number)

---

## 📸 Screenshots

### Home Page
- Hero section with call-to-action
- Featured tour packages
- Why choose us section
- Customer testimonials

### Package Browsing
- Grid layout with cards
- Search and filter functionality
- Package details (price, duration, slots)

### Package Details
- Full package information
- Image gallery
- Booking button
- What's included/excluded

### Booking Page
- Package summary
- Date picker
- Traveler count selector
- Real-time price calculation
- Special requests field

### User Dashboard
- Booking statistics
- Booking history table
- Status indicators
- Cancel booking option

---

## 🔄 CRUD Operations

### Create (C)
- ✅ Register new user account
- ✅ Book new tour package
- ✅ Add special requests to booking

### Read (R)
- ✅ View all tour packages
- ✅ View package details
- ✅ View user bookings
- ✅ View user profile
- ✅ Search and filter packages

### Update (U)
- ✅ Update user profile information
- ✅ Update booking details
- ✅ Change booking status (admin)

### Delete (D)
- ✅ Cancel booking (user)
- ✅ Delete booking (admin)

---

## ✅ Validation Features

### Client-Side Validation (JavaScript)
- Real-time form field validation
- Password strength indicator
- Date validation (future dates only)
- Number range validation
- Instant error feedback

### Server-Side Validation (WTForms)
- Email format validation
- Password strength requirements:
  - Minimum 8 characters
  - At least one uppercase letter
  - At least one lowercase letter
  - At least one number
- Phone number format
- Unique username and email check
- Travel date must be future date
- Number of travelers: 1-50
- Available slots check before booking

### Security Validations
- CSRF token on all forms
- SQL injection prevention (ORM)
- XSS protection (template escaping)
- Password hashing (Werkzeug)
- Session management

---

## 🚀 Future Enhancements

### Planned Features
1. **Payment Integration**
   - Stripe/PayPal integration
   - Payment confirmation emails
   - Invoice generation

2. **Email Notifications**
   - Booking confirmations
   - Status updates
   - Password reset

3. **Advanced Features**
   - Review and rating system
   - Wishlist functionality
   - Booking reminders
   - Multi-language support

4. **Admin Features**
   - Add/Edit/Delete packages
   - Manage user accounts
   - Generate reports
   - Analytics dashboard

5. **Deployment**
   - Deploy to Heroku/Railway
   - Use PostgreSQL database
   - Set up CI/CD pipeline

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'flask'`
```bash
Solution: Install dependencies
pip install -r requirements.txt
```

**Issue**: Database not created
```bash
Solution: Delete existing DB and restart
rm travel_tourism.db
python app.py
```

**Issue**: Port already in use
```bash
Solution: Change port in app.py
app.run(debug=True, port=5001)
```

**Issue**: Static files not loading
```bash
Solution: Clear browser cache or hard refresh (Ctrl+F5)
```

**Issue**: Form validation not working
```bash
Solution: Ensure SECRET_KEY is set in app.py
```

---

## 📚 Learning Resources

### Flask Documentation
- Official Docs: https://flask.palletsprojects.com/
- Flask Mega-Tutorial: https://blog.miguelgrinberg.com/

### Bootstrap 5
- Official Docs: https://getbootstrap.com/docs/5.3/
- Examples: https://getbootstrap.com/docs/5.3/examples/

### SQLAlchemy
- Official Docs: https://docs.sqlalchemy.org/
- Flask-SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/

---

## 📝 Assignment Notes

### Project Requirements Met
✅ Flask framework with SQLAlchemy
✅ User authentication with password hashing
✅ Session management and protected routes
✅ RESTful routing structure
✅ Bootstrap 5 responsive design
✅ HTML5 semantic elements
✅ CSS3 with modern features
✅ JavaScript for interactivity
✅ 3+ related database tables
✅ 5+ pages (8 pages total)
✅ Complete CRUD operations
✅ Both client and server-side validation
✅ Flash messages for feedback
✅ Admin dashboard (bonus)

### Code Quality
- ✅ Detailed comments for beginners
- ✅ Clear variable and function names
- ✅ Organized project structure
- ✅ Follows Python PEP 8 style guide
- ✅ Responsive and accessible design

---

## 📄 License

This project is created for educational purposes as part of the BIT233 Web Technology course.

---

## 👨‍💻 Author

**BIT233 Student**
- Course: Web Technology
- Assignment: Travel & Tourism Portal
- Year: 2024

---

## 🙏 Acknowledgments

- Flask community for excellent documentation
- Bootstrap team for the amazing CSS framework
- TripAdvisor for design inspiration
- Course instructors for guidance

---

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the code comments (they're very detailed!)
3. Contact your course instructor

---

**Happy Coding! 🚀**

---

*Last Updated: February 2024*
#   t r a v e l - t o u r i s m - p o r t a l  
 