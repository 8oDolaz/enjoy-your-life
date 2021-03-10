from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
log_man = LoginManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://husfvgqkvdxrnl:03996089dc71428663700290dec1da75816ac9a893cfc2e3e3011d49842f9715@ec2-54-75-225-52.eu-west-1.compute.amazonaws.com/d4mf8o24stgs2j'
app.secret_key = 'your secrect key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, text):
        self.text = text


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    disc = db.Column(db.String(500), nullable=False)
    text = db.Column(db.Text, nullable=False)
    pre_im = db.Column(db.String(1000), nullable=False)
    arg1 = db.Column(db.String(50))
    arg2 = db.Column(db.String(50))
    arg3 = db.Column(db.String(50))

    def __init__(self, title, disc, text, pre_im, arg1, arg2, arg3):
        self.title = title
        self.disc = disc
        self.text = text
        self.pre_im = pre_im
        self.srg1 = arg1
        self.srg2 = arg2
        self.srg3 = arg3


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.Text, nullable=False)
    ar_tit = db.Column(db.String(100))
    alt = db.Column(db.String(100), nullable=False)

    def __init__(self, link, alt, ar_tit):
        self.link = link
        self.alt = alt
        self.ar_tit = ar_tit


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated


admin = Admin(app, index_view=MyAdminIndexView())


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(10), nullable=False)

    def __init__(self, name, password):
        self.name = name
        self.password = password


@log_man.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['name'] == '1' and request.form['password'] == '1':
            user = Users.query.first()
            login_user(user)
            return redirect(url_for('admin.index'))
        else:
            flash('Wrong login or password')
    return render_template('login.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        image1 = Images.query.get(len(Images.query.all()) + 1)
        images = Images.query.limit(len(Images.query.all())).all()
        if len(Articles.query.all()) > 2:
            ar1 = Articles.query.get(len(Articles.query.all()))
            ar2 = Articles.query.get(len(Articles.query.all()) - 1)
            ar3 = Articles.query.get(len(Articles.query.all()) - 2)
        else:
            ar1, ar2, ar3 = None, None, None
        return render_template('home.html',
                               images=images,
                               image1=image1,
                               about=About.query.first(),
                               ar1=ar1,
                               ar2=ar2,
                               ar3=ar3)


@app.route('/logout/')
def logout():
    logout_user()
    return 'Logged out!'


@app.route('/articles/')
def articles():
    article = Articles.query.all()
    return render_template('articles.html', articles=article)


@app.route('/articles/<string:title>')
def article(title):
    images = Images.query.filter_by(ar_tit=title).all()
    article = Articles.query.filter_by(title=title).first()
    return render_template('article.html', article=article, images=images)


@app.route('/images/')
def images():
    image = Images.query.all()
    return render_template('images.html', image=image)


#  admin.add_view(MyModelView(Users, db.session))
admin.add_view(MyModelView(Articles, db.session))
admin.add_view(MyModelView(Images, db.session))
admin.add_view(MyModelView(About, db.session))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=False)
