from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'some_secret_value'
socketio = SocketIO(app, cors_allowed_origins='*')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)

# make a global users dict
users = {}

class History(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    message = db.Column('message', db.String(500))



@socketio.on('message')
def handle_message(msg):
    print('Session ID ' + request.sid)
    print('Message ' + msg)
    # Add message to the db
    message = History(message=msg)
    db.session.add(message)
    db.session.commit()
    # send the message to clients
    send(msg, broadcast=True)

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

    emit('new_private_message', message, room=recipient_session_id)

@app.route('/')
def index():
    messages = History.query.all()
    return render_template('index.html', messages=messages)


if __name__ == '__main__':
    socketio.run(app, debug=True)
    print("started")