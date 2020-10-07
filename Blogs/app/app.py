from dataclasses import dataclass
from flask import Flask
from flask import render_template, flash, redirect, url_for, request, make_response, url_for, g, session, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, and_
import hashlib
from datetime import timedelta, datetime


app = Flask(__name__)
app.permanent_session_lifetime = timedelta(days=30)

app.config['SECRET_KEY'] = 'try try try but dont cry'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/loginfodb'
db = SQLAlchemy(app)


class userinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    about_me= db.Column(db.String(120), nullable=True)
    

    def __repr__(self):
        return '<User %r>' % self.username

@dataclass
class posts(db.Model):
    id:int
    username:str
    title:str
    description:str
    post_created:str
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(120),  nullable=False)
    description = db.Column(db.String(80),  nullable=False)
    post_created = db.Column(db.DateTime(), default=datetime.utcnow)


@app.before_request
def before_request():
    if 'user' in session:
        user = session['user']
        g.user = user


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():  
    if request.method == "POST": 
        Total_count = posts.query.count()
        count = request.get_json()
        offsetData = count['count']
        if(offsetData >= Total_count):   
            return jsonify({"data" : "end"})
        post = posts.query.order_by(posts.post_created.desc()).offset(offsetData).limit(10).all() 
        return jsonify(post)
    
    post = posts.query.order_by(posts.post_created.desc()).offset(0).limit(10).all()
    return render_template('index.html', title='home', post=post)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        details = request.form
        email = details['email']
        password = details['password']
        username = details['username']
        hash_password = hashlib.md5(password.encode()).hexdigest()
        new_user = userinfo(
            email=email, password=hash_password, username=username)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template('signup.html', title='Sign up')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        hash_password = hashlib.md5(password.encode()).hexdigest()
        for users in db.session.query(userinfo).order_by(userinfo.id):
            try:
                if users.password == hash_password and users.email == email:
                    session.permanent = True
                    session['user'] = users.username
                    return redirect(url_for("home", page_num=1))
            except :
                print('error')
                exit()
                error = 'Incorrect email or password'
                return render_template('login.html', error=error)
    return render_template('login.html', title='Log in')


@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == "POST":
        new_post = posts(title=request.form['title'],
                         description=request.form['description'], username=g.user)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home', page_num=1))
    return render_template('add_post.html', title='Add post')


@app.route('/post/delete/<int:id>', methods=['POST'])
def delete(id):
    post_to_delete = posts.query.get_or_404(id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return jsonify('{status:"success"}')


@app.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = posts.query.get_or_404(id)
    if request.method == "POST":
        post.title = request.form['title']
        post.description = request.form['description']
        db.session.commit()
        return redirect(url_for('home', page_num=1))
    return render_template('edit.html', post=post)

@app.route('/user')
def profile():
    users = userinfo.query.filter_by(username=g.user).first_or_404()
    return render_template('profile.html', users=users)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
    

