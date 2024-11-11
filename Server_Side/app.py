from flask import *
from flask_pymongo import PyMongo
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import bcrypt
import os
import datetime

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config["MONGO_URI"] = "mongodb://localhost:27017/Weapon_Detection_Alert_Info"
db = PyMongo(app).db.users
# db_dash = PyMongo(app).db.dashboard



# Configure Flask Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'vp35233523@gmail.com'
app.config['MAIL_PASSWORD'] = 'cewb vhqq crnu pbpd'
mail = Mail(app)



# Serializer for generating and verifying tokens
s = URLSafeTimedSerializer('secret_key')


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))




@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'email' in session:
        user = db.find_one({'email':session['email']})
        email = user['email']
        detection = user['detections']
        listdire = os.listdir(f'Server_Side/static/Images/{email}')
        return render_template('dashboard.html', username=user['username'],items=detection, email=user['email'],listdir=listdire)
    
    return redirect('/')



@app.route('/',methods=['GET','POST'])
def login(): 
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = db.find_one({'email':email})
        
        if user and check_password(user['password'],password):
            session['username'] = user['username']
            session['email'] = user['email']
            return redirect('/dashboard')
        else:   
            flash('Invalid credentials', 'error')   
            return redirect('/')
        
    return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('email',None)
    session.pop('username',None)
    return redirect('/')



@app.route('/email_check', methods=['POST'])
def email_check():
    try:
        email = request.form['email']
        
        if email and request.method == 'POST':
            if db.find_one({'email': email}):
                # Email already exists
                return '<span style="color:red;">Email already exists.</span>'
            else:
                # Email is available
                return '<span style="color:green;">Email is available</span>'
        else:
            # Email field is empty
            return '<span style="color:red;">Email is a required field.</span>'

    except Exception as e:
        print(e)
        return '<span style="color:red;">An error occurred. Please try again later.</span>'
    


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = hash_password(password)
        
        if db.find_one({'email':email}):
            flash('Email already exit.','error')
            return redirect(url_for('register'))
        else:
            new_user = {'username': username,
                    'email': email, 'password': hashed_password}
            db.insert_one(new_user)
            return redirect('/')

    return render_template('register.html')



@app.route('/password_reset_done', methods=['GET', 'POST'])
def password_reset_done():
    if request.method == 'POST':
        return render_template('login.html')
    return render_template('password_reset_done.html')



@app.route('/password_reset_form/<token>', methods=['GET', 'POST'])
def password_reset_form(token):
    
    try:
        print(f"Received token: {token}")  # Debugging statement
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
        print(f"Loaded email: {email}")  # Debugging statement
    except Exception as e:
        print(f"Error loading token: {str(e)}")  # Debugging statement
        flash('The password reset link is invalid or has expired.', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        
        new_password = request.form['new_password']
        confirm_password = request.form['repeat_password']
        
        if confirm_password == new_password:
            hashed_password = hash_password(new_password)
            db.update_one({'email':email},{'$set':{'password':hashed_password}})
            return redirect('/password_reset_done')
        else:
            flash('Password does not match.')
            return render_template('password_reset_form.html',token = token)
    
    return render_template('password_reset_form.html',token=token)


@app.route('/password_reset_sent', methods=['GET', 'POST'])
def password_reset_sent():
    return render_template('password_reset_sent.html')


@app.route('/password_reset', methods=['GET', 'POST'])
def password_reset():
    if request.method == 'POST':
        email = request.form['email']
        
        if db.find_one({'email':email}):            
            token = s.dumps(email,salt='password-reset-salt')
            # password link
            reset_url = url_for('password_reset_form', token=token, _external=True)
            # send email
            msg = Message('Password Reset Request',
                        sender='vp35233523@gmail.com',
                        recipients=[email])
            msg.body = f'To reset your password, viits the following link: {reset_url}'
            mail.send(msg)
            return redirect('/password_reset_sent')        
        else:
            flash('Email does not exit.')
            return redirect('/password_reset')
        
    return render_template('password_reset.html')


if __name__ == '__main__':
    app.run(debug=True)
