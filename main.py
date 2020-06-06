from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some_secret_value'
socketio = SocketIO(app, cors_allowed_origins='*')

# make a global users dict of user_profile_id vs users_session_id (from flask)
users_and_session_id = {}

@socketio.on('user_profile_id', namespace='/private')
def receive_user_profile_id(user_profile_id):
    """
    This function adds the user's profile id to
    the global user_and_session_id dict. This is the first
    event to be triggered in the chat app.

    Args:
        user_profile_id (str): The profile id of the person in the database
    """
    users_and_session_id[user_profile_id] = request.sid
    print("User profile id added")
    print(users_and_session_id)

@socketio.on('private_message', namespace='/private')
def private_message(payload):
    """
    Sends a private message

    Args:
        payload (dict): dict of recipient_profile_id, message, jwt_token of user
    """
    # the profile id of the user to whom the message should be sent
    recipient_profile_id = payload['recipient_profile_id']
    # message to be sent
    message = payload['message']
    # jwt token of sender
    jwt_token_of_sender = payload['jwt_token']
    recipient_session_id = users_and_session_id.get(recipient_profile_id)

    if recipient_session_id:
        data_to_send = {'message': message}
        emit('new_private_message', data_to_send, room=recipient_session_id)
    else:
        print("User is offline")

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, debug=True)
    print("started")