import pytest
from flask_testing import TestCase
from werkzeug.security import generate_password_hash

from app import app, db, login_manager
from app.models import User, Chat
from testConfig import TestConfig

class TestChatApp(TestCase):
    def create_app(self):
        app.config.from_object(TestConfig)
        return app

    def setUp(self):
        db.create_all()
        hashed_password = generate_password_hash('test_password', method='pbkdf2:sha256')
        test_user1 = User(username='test_user1', password=hashed_password)
        test_user2 = User(username='test_user2', password=hashed_password)
        db.session.add(test_user1)
        db.session.add(test_user2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_login_user1(self):
        with self.client:
            response = self.client.post('/index', json={'username': 'test_user1', 'password': 'test_password'})
            self.assertRedirects(response, '/chat')

    def test_login_user2(self):
        with self.client:
            response = self.client.post('/index', json={'username': 'test_user2', 'password': 'test_password'})
            self.assertRedirects(response, '/chat')

    def test_login_invalid_user(self):
        with self.client:
            response = self.client.post('/index', json={'username': 'invalid_user', 'password': 'invalid_password'})
            self.assert400(response)


    def test_register_new_user(self):
        with self.client:
            response = self.client.post('/register', json={'username': 'new_user', 'password': 'new_password'})
            self.assertRedirects(response, '/login')

    def test_register_existing_user1(self):
        with self.client:
            response = self.client.post('/register', json={'username': 'test_user1', 'password': 'new_password'})
            self.assert400(response)

    def test_register_existing_user2(self):
        with self.client:
            response = self.client.post('/register', json={'username': 'test_user2', 'password': 'new_password'})
            self.assert400(response)


    def test_chat_history_user1(self):
        with self.client:
            self.client.post('/index', json={'username': 'test_user1', 'password': 'test_password'})
            new_chat = Chat(content='Hello, World!', user_id=1)
            db.session.add(new_chat)
            db.session.commit()
            response = self.client.get('/chat')
            self.assert200(response)
            self.assertTrue(b'Hello, World!' in response.data)

    def test_chat_history_user2(self):
        with self.client:
            self.client.post('/index', json={'username': 'test_user2', 'password': 'test_password'})
            new_chat = Chat(content='Hello again, World!', user_id=2)
            db.session.add(new_chat)
            db.session.commit()
            response = self.client.get('/chat')
            self.assert200(response)
            self.assertTrue(b'Hello again, World!' in response.data)

    def test_chat_history_no_chats(self):
        with self.client:
            self.client.post('/index', json={'username': 'test_user1', 'password': 'test_password'})
            response = self.client.get('/chat')
            self.assert200(response)
            self.assertTrue(b'No chats yet.' in response.data)

if __name__ == "__main__":
    pytest.main(["-v", "tests.py"])
