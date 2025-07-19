
Secure Diary Web Application

Introduction

The Secure Diary Web App is a user-friendly, secure, and encrypted web application built using Flask for the backend, HTML, and CSS for the frontend. The app allows users to securely store their diary entries with encryption, providing a private and safe way to store sensitive thoughts. Users can create an account, log in, write and save encrypted entries, and even reset their passwords using a secure process.

Objective

The primary goal of this project is to create a secure, private, and easy-to-use online diary system using Flask as the backend, ensuring user privacy and security by encrypting the diary entries. Additionally, it will integrate user login, registration, and password reset functionality.

Features
- User registration and login with encrypted password storage
- Secure diary entries stored using encryption
- View saved diary entries
- Reset password functionality
- User-friendly interface with validation and messages
- Responsive and attractive UI design

Technologies Used

Frontend:
- HTML5
- CSS3
- Google Fonts (Poppins)

Backend:
- Python 3.x
- Flask micro web framework
- Cryptography (for encryption)
- Jinja2 templating engine

Project Structure

secure_diary_web/
├── app.py                  # Main Flask application with routes and logic
├── templates/
│   ├── index.html          # Home page for diary entry
│   ├── entries.html        # View saved diary entries
│   ├── login.html          # User login page
│   ├── register.html       # User registration page
│   ├── forgot_password.html  # Forgot password page
│   └── reset_password.html  # Reset password page
├── static/
│   └── style.css           # Custom CSS for styling the UI
├── diary_data/
│   ├── key.key             # Key for encryption
│   ├── diary.txt           # Encrypted diary entries
│   └── credentials.txt     # Store usernames and encrypted passwords

Implementation Details

Backend (Flask)
- Defines routes for user registration, login, diary entry management, and password reset.
- Uses the cryptography package to securely store diary entries and passwords.
- Handles both form submissions and dynamic content rendering with templates.

Frontend (HTML + CSS)
- Provides pages for user interactions including registration, login, diary entry creation, and viewing entries.
- Clean and attractive UI using gradient buttons, hover effects, and responsive layouts.

Styling Highlights
- Glassmorphism effect with subtle shadows and blurs
- Responsive design supporting mobile devices
- Gradient buttons for 'Add Entry' and 'Save Entry'
- Font: Poppins via Google Fonts
- Smooth animations and icon scaling

How to Run the Project

1. Ensure Python 3.x is installed.

2. Create and activate a virtual environment:

Linux/macOS:
python3 -m venv venv
source venv/bin/activate

Windows:
python -m venv venv
venv\Scripts ctivate

3. Install Flask and Cryptography:
pip install flask cryptography

4. Run the app:
python app.py

5. Open your browser and go to:
http://127.0.0.1:5000

Future Enhancements
- Implement a persistent database (e.g., SQLite) for user data and entries
- Add user authentication with Flask-Login
- Allow users to add tags or categories to their entries
- Enable search and filter functionality for diary entries
- Add email notifications for password resets

Conclusion

The Secure Diary Web App provides a simple, secure way to store personal notes while ensuring privacy and encryption. By using Flask and encryption libraries, it demonstrates important web development and security concepts. The app can serve as a foundation for more advanced features, including user authentication and data persistence.
