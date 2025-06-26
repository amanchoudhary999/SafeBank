# 💰 SafeBank – A Secure Django-Based Banking System

SafeBank is a full-stack web application built with Django that simulates the core operations of a modern banking system — including registration, secure login, deposit, withdrawal, fund transfer, transaction history, and a custom admin dashboard.

---

## 🚀 Features

- 🧾 **User Registration with Aadhar & Photo Upload**
- 🔐 **Secure Login with Password Hashing**
- 💰 **Deposit, Withdraw & Transfer Money**
- 📜 **Transaction History with Timestamp & Direction**
- 🔍 **Password Confirmation Before Sensitive Operations**
- 🧑‍💻 **Session-Based Login Protection**
- 🧑‍⚖️ **Custom Admin Panel (not Django Admin!)**
- 📁 **Media File Handling**
- 🌐 **Basic UI with Dashboard and Secure Pages**

---

## 🧠 Tech Stack

| Layer        | Technology         |
|--------------|--------------------|
| Backend      | Python 3.10+, Django 5.2 |
| Database     | SQLite (default, file-based) |
| Frontend     | HTML, CSS, JavaScript |
| Auth & Forms | Django Forms, Session & CSRF |
| Styling      | Custom CSS (planned: Bootstrap) |
| Media        | Django's File/ImageField + Pillow |

---

## 🛠️ Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/amanchoudhary999/SafeBank.git
cd SafeBank
```
To Run the SafeBank Banking Website:

Step 1: Install VS Code and Python (version 3.10 or higher) from Google.
Step 2: Open Command Prompt and install required libraries by typing:
```bash
pip install django pillow
```
Step 3: Clone the GitHub repository in VS Code using this link:
https://github.com/amanchoudhary999/SafeBank.git
Step 4: In VS Code, open the folder SafeBank, then click on “Terminal → New Terminal” and run:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Step 5: Open your browser and go to:
http://127.0.0.1:8000
You will now see the SafeBank web application running locally.

✅ Custom Admin Dashboard
📍 URL: http://127.0.0.1:8000/admin-dashboard/

Features:

👥 View all registered users
→ /admin-users/

💳 View all account and balance details
→ /admin-users/ (combined with user info)

📜 View all transaction history
→ /admin-transactions/

🔒 Logout and session clear for admin
→ /admin-logout/

Note : for custom admin: username=admin and password =admin123
Some part of admin controls are still in progress due to lack of time and can be modified later.


