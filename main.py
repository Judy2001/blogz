from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:launchcode@localhost:8889/blogz'
# Note:  The connection string after :// contains the following info:
#            user:password@server:portNumber/databaseName
app.config['SQLALCHEMY-ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'g3r0N1m0sc4D1ll4c'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(200))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner_id = owner


class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __repr__(self):
        return str(self.username)


@app.before_request
def require_login():
    allowed_routes = ['blogs', 'individual_blog', 'login', 'register', 'index']
    if request.endpoint not in allowed_routes:
        if 'user' not in session:
            return redirect("/login")


@app.route('/signup', methods=['POST', 'GET'])
def register():
    username = ''
    password = ''
    username_error=""
    password_error=""
    verify_error=""
    existing_user = User.query.filter_by(username=username).first()
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        verify=request.form['verify']

        if username == ' ' or len(username) <3 or len(username) >50:
            username_error = "Username should consist of 3-50 alphanumeric characters with no spaces."
        elif existing_user:
            username_error = "Username already exists."
    
        if password == ' ' or len(password) <3 or len(password) >50:
            password == ''
            password_error = "Password should consist of 3-50 characters with no spaces."

        if verify == ' ' or password != verify:
            verify == ''
            verify_error = "Passwords must match."

        if  not username_error and not password_error and not verify_error:
            new_user=User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['user']=new_user.id
            return redirect("/new_post?id=" + str(new_user.id))
        else:
            return render_template("signup.html", username_error=username_error, 
                password_error=password_error, verify_error=verify_error, username=username)

    return render_template("signup.html", username_error=username_error, 
                password_error=password_error, verify_error=verify_error)

@app.route('/login', methods=['POST', 'GET'])
def login():
    username = ""
    password = ""
    username_error=""
    password_error=""

    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        user=User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['user'] = user.id
            return redirect("/new_post?id=" + str(user.id))

        if not user or username == ' ':
            username_error = "Please enter a valid username."
            return render_template('/login.html', username_error=username_error)
        else:
            password_error = "Please enter a valid password."
            return render_template('/login.html', password_error=password_error, 
                username=username)
    return render_template("login.html", username_error=username_error, 
                password_error=password_error)


@app.route('/blog', methods=['POST', 'GET'])
def blogs():
    blog_id = request.args.get('blog.id')
    user_id = request.args.get('userid')
    if blog_id:
        posts = Blog.query.get(blog_id)
        return render_template('blog.html', all_blogs=posts)
    if user_id:
        blogs = Blog.query.filter_by(owner_id=user_id).all()
        return render_template("blog.html", all_blogs=blogs)

    return render_template("blog.html", all_blogs=Blog.query.all())


@app.route('/single_user')
def home():
    current_user = ''
    user_posts = ''
    if 'user' in session:
        blogs = Blog.query.filter_by(owner_id=session['user']).all()
        return render_template("single_user.html", blogs=blogs)


@app.route('/new_post', methods=['POST', 'GET'])
def new_post():
    title=''
    body=''
    title_error = ''
    body_error = ''
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if title == '':
            title_error = "Please enter a name for your blog."
        if body == '':
            body_error = "Please enter your blog."

        if not title_error and not body_error:
            owner_id = session['user']
            blog = Blog(title, body, owner_id)
            db.session.add(blog)
            db.session.commit()
            return redirect("/individual_blog?id=" + str(blog.id))
    else:
        return render_template("new_post.html", title=title, body=body, 
            title_error=title_error, body_error=body_error)


@app.route('/individual_blog', methods=['GET'])
def individual_blog():
    blog_id = request.args.get('id')
    blog = Blog.query.filter_by(id=blog_id).first()
    title = blog.title
    body = blog.body
    author = blog.owner
    return render_template("individual_blog.html", title=title, body=body, author=author)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    del session['user']
    return redirect("/blog")


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


if __name__ =='__main__':
    app.run()