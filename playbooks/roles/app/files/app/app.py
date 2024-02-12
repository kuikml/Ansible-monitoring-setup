from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
socketio = SocketIO(app)

class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=0)

counter_instance = Counter.query.first()
if counter_instance is None:
    counter_instance = Counter(count=0)
    db.session.add(counter_instance)
    db.session.commit()

@socketio.on('connect', namespace='/test')
def test_connect():
    socketio.emit('count_update', {'count': counter_instance.count}, namespace='/test')

@app.route('/')
def index():
    return render_template('index.html', count=counter_instance.count)

@app.route('/increment')
def increment():
    counter_instance.count += 1
    db.session.commit()
    socketio.emit('count_update', {'count': counter_instance.count}, namespace='/test')
    return 'Incremented'

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80)

