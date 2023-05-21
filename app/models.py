from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    chats = db.relationship('Chat', backref='author', lazy=True)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(10), nullable=True)  # New field for role

    def to_dict(self):
        return {
            "id": self.id,
            "date_posted": self.date_posted.strftime("%Y-%m-%d %H:%M:%S"),
            "content": self.content,
            "user_id": self.user_id,
            "role": self.role,
        }


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))