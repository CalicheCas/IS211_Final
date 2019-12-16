from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, BookForm, RegistrationForm, SearchForm
from app.models import Book, User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import requests


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/home', methods=["GET", "POST"])
@login_required
def home():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data, author=form.author.data, page_count=form.page_count.data, maturity_rating=form.rating.data, thumbnail="N/A")
        db.session.add(book)
        db.session.commit()

    books = Book.query.all()

    return render_template("home.html", title="Home Page", form=form, books=books)


@app.route("/add", methods=["POST"])
def add():
    try:
        title = request.form.get("title")
        author = request.form.get("author")
        page_count = request.form.get("page_count")
        rating = request.form.get("maturity_rating")
        thum = request.form.get("thumbnail")
        book = Book(title=title, author=author, page_count=int(page_count), maturity_rating=rating, thumbnail=thum)
        db.session.add(book)
        db.session.commit()
    except Exception as e:
        print("Couldn't add book")
        print(e)
    return redirect("/home")


@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        book = Book.query.filter_by(title=oldtitle).first()
        book.title = newtitle
        db.session.commit()
    except Exception as e:
        print("Couldn't update book title")
        print(e)
    return redirect("/home")


@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/home")


@app.route("/search", methods=["GET", "POST"])
def search():

    api_key = app.config["API_KEY"]
    isbn = request.form.get("isbn")
    book = None

    try:
        url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn + "&key=" + api_key
        response = requests.get(url)
        json_obj = response.json()

        title = json_obj['items'][0]['volumeInfo']['title']
        authors = json_obj['items'][0]['volumeInfo']['authors'][0]
        page_count = json_obj['items'][0]['volumeInfo']['pageCount']
        rating = json_obj['items'][0]['volumeInfo']['maturityRating']
        thum = json_obj['items'][0]['volumeInfo']['imageLinks']['thumbnail']
        book = Book(title=title, author=authors, page_count=int(page_count), maturity_rating=rating, thumbnail=thum)
    except Exception as e:
        print("Could not find item")
        print(e)

    return render_template("search.html", title="Search Page", book=book)







