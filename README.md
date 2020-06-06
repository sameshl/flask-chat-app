# flask-chat-app
A chat app with private messaging feature(WIP), implemented using Flask-SocketIO.

## Setup
* Clone / Download this repository
* Setup a virtual environment (Optional, but recommended)
```bash
python3 -m venv venv
```
* Activate a virtual environment
```bash
source venv/bin/activate
```
* Install requirements
```bash
pip install -r requirements.txt
```
* Create the tables in database
  * Open a python interpreter in the root folder by typing ```python3``` in the terminal
  * Now in the interpreter, execute the following commands:
    * ```>>>from main import db```
    * ```>>>db.create_all()```
  * Exit the interpreter
* Start the server
```bash
python main.py
```
* Go to `http://localhost:5000` on your browser.
