"""
Flask application with SQLite database integration.
Demonstrates Docker volumes and data persistence.
"""

from flask import Flask, jsonify, request
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Database configuration
DATABASE_PATH = '/app/data/app.db'
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)


def init_db():
    """Initialize the database with a simple users table."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def get_db_connection():
    """Get database connection."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def hello():
    return jsonify({
        "message": "Flask Advanced Example with Database",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "version": "1.0.0",
        "database": "SQLite"
    })


@app.route('/health')
def health():
    try:
        # Test database connection
        conn = get_db_connection()
        conn.execute('SELECT 1')
        conn.close()
        db_status = "healthy"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return jsonify({
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "service": "flask-advanced-app",
        "database": db_status,
        "timestamp": datetime.now().isoformat()
    })


@app.route('/users', methods=['GET'])
def get_users():
    """Get all users."""
    conn = get_db_connection()
    users = conn.execute(
        'SELECT * FROM users ORDER BY created_at DESC').fetchall()
    conn.close()

    return jsonify([dict(user) for user in users])


@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""
    data = request.get_json()

    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name and email are required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (name, email) VALUES (?, ?)',
            (data['name'], data['email'])
        )
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return jsonify({
            "id": user_id,
            "name": data['name'],
            "email": data['email'],
            "message": "User created successfully"
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user."""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?',
                        (user_id,)).fetchone()
    conn.close()

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(dict(user))


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
