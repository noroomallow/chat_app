import os
import uuid
import sqlite3
from datetime import datetime, timedelta

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    send_from_directory,
    abort
)
from werkzeug.utils import secure_filename


app = Flask(__name__)

# -----------------------------
# Configuration
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(BASE_DIR, "chat.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB

# Temporary room duration
ROOM_EXPIRY_HOURS = 1

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "gif",
    "webp",
    "pdf",
    "txt",
    "doc",
    "docx",
    "xls",
    "xlsx",
    "ppt",
    "pptx",
    "zip",
    "exe"
}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -----------------------------
# Database
# -----------------------------

def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_code TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL,
            expires_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_code TEXT NOT NULL,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_code TEXT NOT NULL,
            username TEXT NOT NULL,
            original_name TEXT NOT NULL,
            stored_name TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# -----------------------------
# Cleanup expired rooms
# -----------------------------

def cleanup_expired_rooms():

    connection = get_db()
    cursor = connection.cursor()

    now = datetime.utcnow().isoformat()

    cursor.execute(
        "SELECT room_code FROM rooms WHERE expires_at <= ?",
        (now,)
    )

    expired_rooms = cursor.fetchall()

    for room in expired_rooms:

        room_code = room["room_code"]

        # Delete messages
        cursor.execute(
            "DELETE FROM messages WHERE room_code = ?",
            (room_code,)
        )

        # Find files
        cursor.execute(
            "SELECT stored_name FROM files WHERE room_code = ?",
            (room_code,)
        )

        files = cursor.fetchall()

        for file in files:

            file_path = os.path.join(
                UPLOAD_FOLDER,
                file["stored_name"]
            )

            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except OSError:
                    pass

        # Delete file records
        cursor.execute(
            "DELETE FROM files WHERE room_code = ?",
            (room_code,)
        )

        # Delete room
        cursor.execute(
            "DELETE FROM rooms WHERE room_code = ?",
            (room_code,)
        )

    connection.commit()
    connection.close()


# -----------------------------
# Helper functions
# -----------------------------

def room_exists(room_code):

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM rooms WHERE room_code = ?",
        (room_code,)
    )

    room = cursor.fetchone()

    connection.close()

    return room


def allowed_file(filename):

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_EXTENSIONS


# -----------------------------
# Home page
# -----------------------------

@app.route("/")
def index():

    cleanup_expired_rooms()

    return render_template("index.html")


# -----------------------------
# Create room
# -----------------------------

@app.route("/create-room", methods=["POST"])
def create_room():

    cleanup_expired_rooms()

    username = request.form.get("username", "").strip()

    if not username:
        username = "Guest"

    username = username[:30]

    # Generate unique room code
    room_code = uuid.uuid4().hex[:8].upper()

    created_at = datetime.utcnow()

    expires_at = created_at + timedelta(
        hours=ROOM_EXPIRY_HOURS
    )

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO rooms
        (room_code, created_at, expires_at)
        VALUES (?, ?, ?)
    """, (
        room_code,
        created_at.isoformat(),
        expires_at.isoformat()
    ))

    connection.commit()
    connection.close()

    return redirect(
        url_for(
            "chat",
            room_code=room_code,
            username=username
        )
    )


# -----------------------------
# Chat room
# -----------------------------

@app.route("/chat/<room_code>")
def chat(room_code):

    cleanup_expired_rooms()

    room_code = room_code.upper()

    room = room_exists(room_code)

    if not room:
        return render_template(
            "index.html",
            error="This chat room does not exist or has expired."
        )

    username = request.args.get(
        "username",
        "Guest"
    )

    username = username[:30]

    return render_template(
        "chat.html",
        room_code=room_code,
        username=username,
        expires_at=room["expires_at"]
    )


# -----------------------------
# Get messages
# -----------------------------

@app.route("/api/messages/<room_code>")
def get_messages(room_code):

    cleanup_expired_rooms()

    room_code = room_code.upper()

    room = room_exists(room_code)

    if not room:
        return jsonify({
            "success": False,
            "error": "Room expired."
        }), 404

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            username,
            message,
            created_at
        FROM messages
        WHERE room_code = ?
        ORDER BY id ASC
    """, (room_code,))

    messages = cursor.fetchall()

    connection.close()

    result = []

    for message in messages:

        result.append({
            "id": message["id"],
            "username": message["username"],
            "message": message["message"],
            "created_at": message["created_at"]
        })

    return jsonify({
        "success": True,
        "messages": result,
        "expires_at": room["expires_at"]
    })


# -----------------------------
# Send message
# -----------------------------

@app.route("/api/messages/<room_code>", methods=["POST"])
def send_message(room_code):

    cleanup_expired_rooms()

    room_code = room_code.upper()

    room = room_exists(room_code)

    if not room:
        return jsonify({
            "success": False,
            "error": "Room expired."
        }), 404

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "error": "Invalid request."
        }), 400

    username = str(
        data.get("username", "Guest")
    ).strip()

    message = str(
        data.get("message", "")
    ).strip()

    username = username[:30]
    message = message[:2000]

    if not username:
        username = "Guest"

    if not message:
        return jsonify({
            "success": False,
            "error": "Message cannot be empty."
        }), 400

    created_at = datetime.utcnow().isoformat()

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO messages
        (room_code, username, message, created_at)
        VALUES (?, ?, ?, ?)
    """, (
        room_code,
        username,
        message,
        created_at
    ))

    connection.commit()

    message_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "success": True,
        "id": message_id
    })


# -----------------------------
# Upload file
# -----------------------------

@app.route("/upload/<room_code>", methods=["POST"])
def upload_file(room_code):

    cleanup_expired_rooms()

    room_code = room_code.upper()

    room = room_exists(room_code)

    if not room:
        return jsonify({
            "success": False,
            "error": "Room expired."
        }), 404

    username = request.form.get(
        "username",
        "Guest"
    ).strip()

    username = username[:30]

    if not username:
        username = "Guest"

    if "file" not in request.files:
        return jsonify({
            "success": False,
            "error": "No file selected."
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "success": False,
            "error": "No file selected."
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "success": False,
            "error": "This file type is not allowed."
        }), 400

    original_name = secure_filename(
        file.filename
    )

    if not original_name:
        return jsonify({
            "success": False,
            "error": "Invalid filename."
        }), 400

    extension = ""

    if "." in original_name:
        extension = "." + original_name.rsplit(".", 1)[1]

    stored_name = (
        uuid.uuid4().hex
        + extension
    )

    file_path = os.path.join(
        UPLOAD_FOLDER,
        stored_name
    )

    file.save(file_path)

    created_at = datetime.utcnow().isoformat()

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO files
        (room_code, username, original_name, stored_name, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        room_code,
        username,
        original_name,
        stored_name,
        created_at
    ))

    connection.commit()

    file_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "success": True,
        "file_id": file_id,
        "filename": original_name
    })


# -----------------------------
# Get files
# -----------------------------

@app.route("/api/files/<room_code>")
def get_files(room_code):

    cleanup_expired_rooms()

    room_code = room_code.upper()

    room = room_exists(room_code)

    if not room:
        return jsonify({
            "success": False,
            "error": "Room expired."
        }), 404

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            username,
            original_name,
            created_at
        FROM files
        WHERE room_code = ?
        ORDER BY id ASC
    """, (room_code,))

    files = cursor.fetchall()

    connection.close()

    result = []

    for file in files:

        result.append({
            "id": file["id"],
            "username": file["username"],
            "filename": file["original_name"],
            "created_at": file["created_at"],
            "url": url_for(
                "download_file",
                room_code=room_code,
                file_id=file["id"]
            )
        })

    return jsonify({
        "success": True,
        "files": result
    })


# -----------------------------
# Download file
# -----------------------------

@app.route("/download/<room_code>/<int:file_id>")
def download_file(room_code, file_id):

    cleanup_expired_rooms()

    room_code = room_code.upper()

    room = room_exists(room_code)

    if not room:
        abort(404)

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT stored_name, original_name
        FROM files
        WHERE id = ?
        AND room_code = ?
    """, (
        file_id,
        room_code
    ))

    file = cursor.fetchone()

    connection.close()

    if not file:
        abort(404)

    return send_from_directory(
        UPLOAD_FOLDER,
        file["stored_name"],
        as_attachment=True,
        download_name=file["original_name"]
    )


# -----------------------------
# Run application
# -----------------------------

init_database()


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )