from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import logging

app = Flask(__name__)

# Database configuration
database_url = os.getenv(
    'DATABASE_URL', 'postgresql://postgres:password123@localhost:5432/pythonguide')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# User model


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

# Create tables


@app.before_first_request
def create_tables():
    try:
        db.create_all()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")

# Health check endpoint


@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

# Routes


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Flask Kubernetes App',
        'version': '1.0.0',
        'endpoints': ['/users', '/users/<id>', '/health']
    })


@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        if not data or not data.get('name') or not data.get('email'):
            return jsonify({'error': 'Name and email are required'}), 400

        # Check if user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 409

        user = User(name=data['name'], email=data['email'])
        db.session.add(user)
        db.session.commit()

        logger.info(f"User created: {user.name} ({user.email})")
        return jsonify(user.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating user: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict())
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {e}")
        return jsonify({'error': 'User not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
