from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit

import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some_secret_value'
socketio = SocketIO(app, cors_allowed_origins='*')

# make a global users dict
users = {}

@socketio.on('username', namespace='/private')
def receive_username(username):
    # append to global list of all users
    # users.append({username: request.sid})
    users[username] = request.sid
    print("Username added")
    print(users)

@socketio.on('private_message', namespace='/private')
def private_message(payload):
    username_to_send = payload['username']
    message = payload['message']
    
    recipient_session_id = users[username_to_send]
    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
    
    data_to_send = {'message': message, 'time_stamp': time_stamp}
    emit('new_private_message', data_to_send, room=recipient_session_id)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, debug=True)
    print("started")