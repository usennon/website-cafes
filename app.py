from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, current_user
from forms import LoginForm, RegisterForm, AddCafeForm, CafeSuggestForm
from flask_bootstrap import Bootstrap
from functools import wraps
from email_sender import send_email

app = Flask(__name__)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'fsdsfddfsfafaqwebgmjgd'
##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.id == 1:
            return func(*args, **kwargs)
        else:
            return 404

    return wrapper


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=True)


db.create_all()


@app.route('/', methods=['GET', 'POST'])
def main_page():
    cafes = Cafe.query.all()
    if request.method == 'POST':
        if request.form.get('wifi') == 'has_wifi':
            cafes = Cafe.query.filter_by(has_wifi=1)
            return render_template('index.html', cafes=cafes)
        elif request.form.get('toilet') == 'toilets':
            cafes = Cafe.query.filter_by(has_toilet=1)
            return render_template('index.html', cafes=cafes)
        elif request.form.get('sockets') == 'sockets':
            cafes = Cafe.query.filter_by(has_sockets=1)
            return render_template('index.html', cafes=cafes)
        elif request.form.get('calls') == 'calls':
            cafes = Cafe.query.filter_by(can_take_calls=1)
            return render_template('index.html', cafes=cafes)
        elif request.form.get('all') == 'all':
            return redirect(url_for('main_page'))

    return render_template('index.html', cafes=cafes, current_user=current_user)


@app.route('/cafe/<int:index>')
def cafe_page(index):
    cafe = Cafe.query.filter_by(id=index).first()
    print(cafe)
    return render_template('cafe.html', cafe=cafe)


@app.route('/suggest', methods=['GET', 'POST'])
def suggest_cafe():
    form = CafeSuggestForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = request.form.get('name')
        map_url = request.form.get('map_url')
        location = request.form.get('location')
        cafe_site = request.form.get('cafe_site')
        send_email(name, map_url, location, cafe_site=cafe_site)
    return render_template('suggest.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('This email does not exist. Please try again')
            return redirect(url_for('login'))
        else:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('main_page'))
            else:
                flash('Your password is incorrect. Please try again')
                return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if not user:
            hashed_pass = generate_password_hash(password)
            new_user = User(email=email,
                            password=hashed_pass)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('main_page'))
        else:
            flash('Such user already exists. Log in!')
            return redirect(url_for('login'))
    return render_template('register.html', form=form, current_user=current_user)


@app.route('/cafe-add', methods=['GET', 'POST'])
@admin_only
def add_cafe():
    form = AddCafeForm()
    if request.method == 'POST':
        name = request.form.get('name')
        map_url = request.form.get('map_url')
        img_url = request.form.get('img_url')
        location = request.form.get('location')
        seats = request.form.get('seats')
        price = request.form.get('coffee_price')
        wifi = request.form.get('has_wifi')
        sockets = request.form.get('has_sockets')
        toilet = request.form.get('has_toilet')
        calls = request.form.get('can_take_calls')
        new_cafe = Cafe(
            name=name,
            map_url=map_url,
            img_url=img_url,
            location=location,
            seats=seats,
            coffee_price=price,
            has_wifi=bool(wifi),
            has_sockets=bool(sockets),
            has_toilet=bool(toilet),
            can_take_calls=bool(calls)
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('main_page'))

    return render_template('add.html', form=form)


@app.route('/delete/<int:index>')
@admin_only
def delete_cafe(index):
    cafe = Cafe.query.filter_by(id=index).first()
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for('main_page'))


if __name__ == '__main__':
    app.run()
