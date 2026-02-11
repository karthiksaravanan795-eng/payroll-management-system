# ?? Payroll Management System

A comprehensive **Payroll Management System** built with **Django** and **MySQL**. 
This system manages employees, attendance, salary calculations, and generates 
automated reports with role-based access control.

## ?? Features

### ?? User Roles
- **Admin**: Full system access (Add departments, employees, calculate salary, view reports)
- **Manager**: View employees, record attendance, calculate salary, view reports
- **HR**: Add/view employees, record attendance, view reports

### ?? Core Modules
- **Department Management**: Create and manage departments
- **Employee Management**: Add, view, and manage employee details
- **Attendance Tracking**: Record working days, present days, overtime hours
- **Salary Calculation**: Automated salary computation with overtime pay (?100/hour)
- **Report Generation**: Monthly salary reports with total payout analytics
- **Salary Slip**: Generate detailed salary slips with breakdown

## ??? Technology Stack

| **Layer** | **Technology** |
|-----------|---------------|
| **Backend** | Python 3.13, Django 4.2 |
| **Database** | MySQL 8.0 |
| **Frontend** | HTML5, CSS3, Bootstrap 5, JavaScript |
| **Version Control** | Git, GitHub |
| **IDE** | VS Code |

## ?? Prerequisites

- Python 3.13+
- MySQL 8.0+
- Git
- VS Code (recommended)

## ?? Installation & Setup

### 1. Clone the Repository
\\\ash
git clone https://github.com/YOUR_USERNAME/payroll-system.git
cd payroll-system
\\\

### 2. Create Virtual Environment
\\\ash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
\\\

### 3. Install Dependencies
\\\ash
pip install -r requirements.txt
\\\

### 4. Database Setup
\\\ash
# Create MySQL database
mysql -u root -p -e "CREATE DATABASE payroll_db;"

# Run migrations
python manage.py makemigrations payroll
python manage.py migrate

# Create superuser
python manage.py createsuperuser
# Username: admin
# Password: admin123
\\\

### 5. Run Application
\\\ash
python manage.py runserver
\\\

Visit \http://127.0.0.1:8000/\

## ?? Default Login Credentials

| **Role** | **Username** | **Password** |
|----------|------------|------------|
| Admin | admin | admin123 |
| Manager | manager | manager123 |
| HR | hr | hr123 |

## ?? Key Features Explained

### Salary Calculation Logic
\\\python
daily_salary = base_salary / working_days
earned_salary = daily_salary * present_days
overtime_pay = overtime_hours * 100
total_salary = earned_salary + overtime_pay
\\\

### Authentication & Authorization
- Secure password hashing with PBKDF2
- Session-based authentication
- Role-based access control using Django Groups
- Login attempt limiting

## ?? Screenshots

*[Add screenshots here after uploading]*

## ?? Project Structure

\\\
payroll-system/
+-- payroll_system/         # Django project configuration
+-- payroll/               # Main application
+-- templates/            # HTML templates
+-- static/              # CSS, JS, images
+-- manage.py            # Django management script
+-- requirements.txt     # Dependencies
+-- README.md           # Documentation
+-- .gitignore          # Git ignore rules
\\\

## ?? Contributing

1. Fork the repository
2. Create feature branch (\git checkout -b feature/AmazingFeature\)
3. Commit changes (\git commit -m 'Add AmazingFeature'\)
4. Push branch (\git push origin feature/AmazingFeature\)
5. Open Pull Request

## ?? Contact

Your Name - [your-email@example.com](mailto:your-email@example.com)

Project Link: [https://github.com/YOUR_USERNAME/payroll-system](https://github.com/YOUR_USERNAME/payroll-system)

## ?? License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**? Star this repository if you find it helpful!**
