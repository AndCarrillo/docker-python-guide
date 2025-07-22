from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://user:password@localhost:5432/devdb'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }

# Routes


@app.route('/')
def home():
    return jsonify({
        "message": "Flask + PostgreSQL Development Example",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "database": "Connected" if db.engine.url.database else "Not connected"
    })


@app.route('/health')
def health():
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return jsonify({
        "status": "healthy",
        "service": "flask-postgres-app",
        "database": db_status
    })


@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])


@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400

    task = Task(
        title=data['title'],
        description=data.get('description', '')
    )

    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()

    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'completed' in data:
        task.completed = data['completed']

    db.session.commit()
    return jsonify(task.to_dict())


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

# Create tables


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
