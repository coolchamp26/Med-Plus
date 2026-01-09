# MedPlus – Hospital & Emergency Management System 🏥

**First Programming Project (Class 12)**

MedPlus is a **Python-based desktop application** developed using **Tkinter and MySQL**.
This project was created during **Class 12** as my **first complete end-to-end software project**, covering GUI design, user authentication, and database interaction.

The goal of MedPlus is to provide a simple system for:

* User & Admin login/register
* Managing hospital contacts
* Storing emergency contacts
* Basic admin control over records

---

## 🧠 Motivation

This project was built as part of my school curriculum to understand:

* How real applications are structured
* GUI programming with Tkinter
* Database connectivity using MySQL
* Role-based access (User vs Admin)
* Breaking a problem into multiple functions/modules

It represents my **first real hands-on experience** building a complete application from scratch.

---

## ✨ Features

### 👤 User Features

* User registration & login
* View hospital contact options
* Add and view emergency contacts
* Simple GUI-based navigation

### 🛠️ Admin Features

* Admin login & registration
* Add / delete / modify hospital details
* Add / delete / modify hospital contacts
* Delete users
* Full control over stored records

---

## 🖥️ Tech Stack

* **Language:** Python
* **GUI:** Tkinter
* **Database:** MySQL
* **Connector:** mysql-connector-python
* **Platform:** Windows (tested)

---

## 🗂️ Project Structure (Simplified)

```
MedPlus/
│
├── main.py               # Main application file
├── image0.png            # Background image
├── pills.png             # UI image
├── README.md             # Project documentation
```

---

## 🗄️ Database Details

* **Database Name:** MedPlus
* **Tables Used:**

  * Contact_List
  * Emergency_List
  * Admins
  * File-based user credential storage

> ⚠️ Note:
> User authentication is implemented using **file-based storage**, which is **not secure** and was done purely for learning purposes at school level.

---

## ▶️ How to Run

### 1️⃣ Install Requirements

```bash
pip install mysql-connector-python
```

### 2️⃣ Setup MySQL

* Create a database named `MedPlus`
* Update MySQL credentials in the code:

```python
host='localhost'
user='root'
passwd='1234'
database='MedPlus'
```

### 3️⃣ Run the Application

```bash
python main.py
```

---

## 🚧 Limitations

Since this was a **Class 12 project**, it has some known limitations:

* Passwords are not encrypted
* File-based authentication is insecure
* Minimal input validation
* Basic UI design
* Large single-file codebase
* The actual logic and functionality of the app is minimal

These limitations reflect my **learning stage at the time**.

---

## 📚 What I Learned

* GUI development using Tkinter
* Connecting Python applications with MySQL
* Writing modular functions
* Understanding real-world application flow
* Debugging and improving large scripts
* Importance of clean and structured code (learned later)

---

## 🌱 Possible Future Improvements

* Database-based authentication system
* Password hashing and security
* Improved UI/UX design
* Input validation and error handling
* Refactoring into modules and classes
* Make the app actually functioning

---

## 🧾 Disclaimer

This project is uploaded **as-is** to showcase my **learning journey**.
It is **not intended for production use**.

---

## 🙌 Acknowledgement

Built during **Class 12 Computer Science**, as my **first real project** combining:

* Programming logic
* GUI design
* Database interaction
* User management
