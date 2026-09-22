
# 💬 TempChat — Temporary Chat & File Sharing

TempChat is a simple Flask-based temporary messaging application that allows users to create a temporary chat room, share the room link, exchange messages, and share files.

The application is designed for simple, short-lived communication without requiring user registration.

## 🚀 Features

* 🔒 Create temporary chat rooms
* 🔑 Automatically generated room code
* 💬 Real-time-style messaging using polling
* 👤 Username-based chatting without registration
* 🔗 Shareable room link
* 📎 File sharing
* 📄 Supports common document formats
* 📦 ZIP file sharing
* 💻 EXE file sharing
* ⏱️ Automatic room expiration
* 🗑️ Temporary messages and files
* 📱 Responsive interface
* 🗄️ SQLite database
* 🌐 Flask backend
* 🎨 Dark modern UI

## 🛠️ Technologies Used

| Technology     | Purpose                      |
| -------------- | ---------------------------- |
| Python         | Backend programming          |
| Flask          | Web framework                |
| SQLite         | Database                     |
| HTML5          | Page structure               |
| CSS3           | User interface               |
| JavaScript     | Chat interaction and polling |
| GitHub         | Source code management       |
| PythonAnywhere | Deployment                   |

## 📁 Project Structure

```text
chat_app/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── index.html
│   └── chat.html
│
├── static/
│   ├── style.css
│   └── script.js
│
└── uploads/
```

`chat.db` is created automatically by the Flask application when the application starts.

## ⚙️ Main Workflow

```text
User
  │
  ▼
Create Temporary Room
  │
  ▼
Unique Room Code
  │
  ▼
Share Room Link
  │
  ▼
Join Chat
  │
  ├── Send Messages
  │
  └── Upload Files
  │
  ▼
Temporary Storage
  │
  ▼
Room Expiration
  │
  ▼
Cleanup
```

## 💬 How to Use

### 1. Create a room

Open the application and enter your name.

Click:

```text
Create Temporary Room
```

The application generates a unique room code.

### 2. Share the room

Copy the generated room link and send it to another person.

### 3. Chat

Users inside the same room can exchange text messages.

### 4. Share files

Click the attachment button and select a supported file.

The application currently supports formats such as:

```text
PNG
JPG
JPEG
GIF
WEBP
PDF
TXT
DOC
DOCX
XLS
XLSX
PPT
PPTX
ZIP
EXE
```

### 5. Room expiration

Rooms are temporary and expire after the configured duration.

The application removes expired room data when cleanup runs.

## 💻 Run Locally

### Clone the repository

```bash
git clone https://github.com/noroomallow/chat_app.git
```

Move into the project:

```bash
cd chat_app
```

### Create a virtual environment

Windows:

```powershell
py -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\activate
```

### Install dependencies

```powershell
pip install -r requirements.txt
```

### Start the application

```powershell
py app.py
```

Open:

```text
http://127.0.0.1:5000
```

## 🌐 PythonAnywhere Deployment

The application can be deployed using PythonAnywhere's standard Flask WSGI deployment method.

### 1. Open a Bash console

Go to:

```text
PythonAnywhere → Consoles → Bash
```

### 2. Clone the repository

```bash
cd /home/tempchater
git clone https://github.com/noroomallow/chat_app.git
```

Your project should now be located at:

```text
/home/tempchater/chat_app
```

### 3. Create a virtual environment

Because the PythonAnywhere web application uses Python 3.13, create the virtual environment with Python 3.13:

```bash
mkvirtualenv tempchat --python=/usr/bin/python3.13
```

### 4. Activate the environment

```bash
workon tempchat
```

### 5. Install dependencies

```bash
cd /home/tempchater/chat_app
pip install -r requirements.txt
```

### 6. Configure the Web application

Go to:

```text
PythonAnywhere
→ Web
→ Your web application
```

Choose:

```text
Manual configuration
Python 3.13
```

Set the source code directory to:

```text
/home/tempchater/chat_app
```

### 7. Configure Virtualenv

Enter:

```text
/home/tempchater/.virtualenvs/tempchat
```

### 8. Configure WSGI

Open the WSGI configuration file and use:

```python
import sys

project_home = "/home/tempchater/chat_app"

if project_home not in sys.path:
    sys.path.insert(0, project_home)

from app import app as application
```

### 9. Configure static files

Under the Static files section add:

```text
URL:       /static/
Directory: /home/tempchater/chat_app/static
```

### 10. Create the uploads directory

Run:

```bash
mkdir -p /home/tempchater/chat_app/uploads
```

### 11. Reload the web application

Go to:

```text
Web → Reload
```

### 12. Open the website

```text
https://tempchater.pythonanywhere.com
```

## 🔧 Updating the Application

After pushing new changes to GitHub:

```bash
cd /home/tempchater/chat_app
git pull
```

If dependencies changed:

```bash
workon tempchat
pip install -r requirements.txt
```

Then go to:

```text
Web → Reload
```

## 🗄️ Database

TempChat uses SQLite.

The database file is:

```text
chat.db
```

The application automatically creates the required tables:

```text
rooms
messages
files
```

## 📎 File Upload Limit

The Flask application currently has a maximum upload size of:

```text
10 MB
```

This is configured using:

```python
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
```

## 🔐 Security Notes

This project is intended as a simple educational/demo application.

For production use, consider adding:

* User authentication
* Secure room tokens
* Rate limiting
* File type/MIME validation
* Malware scanning
* File size quotas
* HTTPS-only access
* CSRF protection
* Stronger access control
* Secure file storage
* Scheduled cleanup
* Database backup

### Executable files

The application supports `.exe` uploads, but uploaded executable files should **never be executed by the server**.

Users should only download files from trusted sources.

## 📜 License

This project is provided for educational and development purposes.

## 👨‍💻 Author

**noroomallow**

GitHub:

[https://github.com/noroomallow](https://github.com/noroomallow)

Repository:

[https://github.com/noroomallow/chat_app](https://github.com/noroomallow/chat_app)

## 🚀 Now deploy your GitHub project to PythonAnywhere

Since your PythonAnywhere username is **`tempchater`**, you can use these commands exactly.

### Step 1 — Open Bash

Go to:

**PythonAnywhere → Consoles → Bash**

Run:

```bash
cd /home/tempchater
```

If you already have the old `chat_app` folder, first check it:

```bash
ls
```

If `chat_app` is already there, **don't clone again**. Instead:

```bash
cd /home/tempchater/chat_app
git pull
```

If it doesn't exist:

```bash
git clone https://github.com/noroomallow/chat_app.git
cd /home/tempchater/chat_app
```

Your GitHub repository's main files are indeed `app.py`, `requirements.txt`, `templates/`, and `static/`. ([GitHub][1])

### Step 2 — Create virtual environment

Because your Web app is configured for **Python 3.13**, use the same version for the virtualenv. PythonAnywhere specifically recommends matching the virtualenv Python version to the Web app's Python version. ([PythonAnywhere Help][2])

```bash
mkvirtualenv tempchat --python=/usr/bin/python3.13
```

Then:

```bash
workon tempchat
```

You should see:

```text
(tempchat)
```

at the beginning of your terminal prompt.

### Step 3 — Install Flask

```bash
cd /home/tempchater/chat_app
pip install -r requirements.txt
```

Then check:

```bash
python -c "import flask; print(flask.__version__)"
```

### Step 4 — Check the actual application

Run:

```bash
grep -n "Hello from Flask" app.py
```

If **nothing is returned**, that's good.

Then:

```bash
python -c "from app import app; print(app.url_map)"
```

You should see routes from your TempChat application.

### Step 5 — Your WSGI file

Your existing WSGI configuration is already essentially correct. Use:

```python
import sys

project_home = "/home/tempchater/chat_app"

if project_home not in sys.path:
    sys.path.insert(0, project_home)

from app import app as application
```

PythonAnywhere's official Flask deployment documentation uses this WSGI pattern for an existing Flask application. ([PythonAnywhere Help][2])

### Step 6 — Web settings

Your Web page should be:

```text
Source code:
/home/tempchater/chat_app

Working directory:
/home/tempchater/

Python version:
3.13

Virtualenv:
/home/tempchater/.virtualenvs/tempchat
```

Static files:

```text
URL:       /static/
Directory: /home/tempchater/chat_app/static
```

### Step 7 — Upload folder

Run:

```bash
mkdir -p /home/tempchater/chat_app/uploads
```

### Step 8 — Reload

Go to:

**Web → Reload**

Then visit:

[https://tempchater.pythonanywhere.com](https://tempchater.pythonanywhere.com?utm_source=chatgpt.com)

You should see the **TempChat homepage**, not `Hello from Flask`.

### Important

Do **not** remove the:

```python
if __name__ == "__main__":
    app.run(...)
```

block if you want to run the project locally. PythonAnywhere imports the Flask app through WSGI, so a correctly guarded `app.run()` won't execute during the WSGI import. PythonAnywhere explicitly recommends keeping `app.run()` inside that guard. ([PythonAnywhere Help][2])

Also, because you're allowing `.exe` uploads, keep the server configured to **store/download them, never execute them**.

[1]: https://github.com/noroomallow/chat_app "GitHub - noroomallow/chat_app · GitHub"
[2]: https://help.pythonanywhere.com/pages/Flask?utm_source=chatgpt.com "Setting up Flask applications on PythonAnywhere | PythonAnywhere Help"
