from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, socketio
from app.models import User, Chat
from flask_socketio import send, emit
from flask_login import logout_user
import openai

openai.api_key = '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'

@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
        new_user = User(username=data['username'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))  # 重定向到登录页面
    return render_template('register.html')

@app.route("/index", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if not user or not check_password_hash(user.password, data['password']):
            flash('Login Unsuccessful. Please check username and password', 'danger')
            return redirect(url_for('index'))  # 登录失败，重新定向到登录页面
        login_user(user)
        return redirect(url_for('chat_page'))  # 登录成功，重定向到聊天页面
    return render_template('index.html')

@app.route("/chat", methods=['GET'])
@login_required
def chat_page():
    print(f"Entering chat_page for user {current_user.username}")
    chats = Chat.query.filter_by(user_id=current_user.id).all()  # 获取聊天记录
    chats_dict = [chat.to_dict() for chat in chats]  # 将每个chat对象转化为字典
    return render_template('chat.html', chats=chats_dict, username=current_user.username)  # 渲染聊天页面，并传入聊天记录


@socketio.on('message')
# @login_required
def chat(data):
    print("发送了")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": data['message']}
        ]
    )
    user_chat = Chat(content=data['message'], user_id=current_user.id, role='user')
    db.session.add(user_chat)

    bot_chat = Chat(content=response['choices'][0]['message']['content'], user_id=current_user.id,
                    role='assistant')  # GPT生成的消息
    db.session.add(bot_chat)

    db.session.commit()
    socketio.emit('bot response', response['choices'][0]['message']['content'])
    print(response['choices'][0]['message']['content'])

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


