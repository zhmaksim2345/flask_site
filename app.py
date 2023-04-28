from flask import Flask, render_template, request, flash, get_flashed_messages, session, redirect, url_for, abort, g
import datetime
from os import environ
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

class Config(object):
    SECRET_KEY = environ.get("SECRET_KEY") or 'adasdasdasd'

app.permanent_session_lifetime = datetime.timedelta(seconds=10000)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.bd'
db = SQLAlchemy(app)

users = [{'user': 'user', 'psw': 'pswrd'}]

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable = False)

    def __repr__(self):
        return f'Пользователь: {self.username} оставил отзыв: {self.text}'

@app.route('/')
@app.route('/index')
def index():  # put application's code here
    return render_template('index.html')

@app.route('/feedback')
def feedback():  # put application's code here
    items = Feedback.query.all()
    return render_template('feedback.html', data=items)

@app.route('/login', methods=['POST', 'GET'])
def login():  # put application's code here
    if 'userlogin' in session:
        return redirect(url_for('profile', username=session['userlogin']))
    elif request.method == 'POST' and {'username': request.form['username'], 'psw': request.form['psw']} in users:
        session['userlogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userlogged']))
    elif request.method == 'POST' and {'username': request.form['username'], 'psw': request.form['psw']} not in users:
        session['userlogged'] = request.form['username']
        users.append({'user': request.form['username'], 'psw': request.form['psw']})
        return redirect(url_for('profile', username=session['userlogged']))
    return render_template('login.html')

@app.route('/profile', methods=['POST', 'GET'])
@app.route('/make_feedback', methods=['POST', 'GET'])
@app.route('/profile/<username>', methods=['POST', 'GET'])
def profile(username=None):
    if 'userlogged' not in session or session['userlogged'] != username or username == None:
        abort(401)
    if request.method == "POST":
        usern = request.form['username']
        message = request.form['message']
        item = Feedback(username=usern, text=message)
        try:
            db.session.add(item)
            db.session.commit()
        except:
            flash('Ошибка добавления в БД', category='success')
        flash('Сообщение отправлено', category='success')
    return render_template("make_feedback.html", username=username)

@app.errorhandler(401)
def unauthorized(error):
    return render_template('page401.html'), 401


if __name__ == '__main__':
    app.run(debug=True)
