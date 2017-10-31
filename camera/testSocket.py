from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('connect')
def test_connect():
    print('Client connected!')
    emit('ques', {'ques': 'Connected'})
    emit('ans', {'ans': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected!')

if __name__ == '__main__':
    socketio.run(app, host='192.168.20.140', port=3001)