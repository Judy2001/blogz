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
    name = db.Column(db.String(120))
    body = db.Column(db.String(200))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, (50))
    password = db.Column(db.String, (50))
    blogs = db.relationship('Blog', backref='owner')


@app.routeJ('/signup')



@app.route('/login')



@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    title_error = ''
    body_error = ''
    if request.method == 'GET':
        return render_template('new_post.html')
    
    if request.method == 'POST':
        title = request.form['name']
        body = request.form['body']

        if title == '':
            title_error = "Please enter a name for your blog"
        if body == '':
            body_error = "Please enter your blog"

        if title_error and body_error:
            return render_template('new_post.html', title_error=title_error, body_error=body_error)
        elif title_error:
            return render_template('new_post.html', title_error=title_error, body=body)
        elif body_error:
            return render_template('new_post.html', title=title, body_error=body_error)
        else:
            blog = Blog(title, body)
            db.session.add(blog)
            db.session.commit()
            blog_query = "/blog?id=" + str(blog.id)
            return redirect('/individual_blog?title=' + title + '&body' + body)


@app.route('/individual_blog', methods=['GET'])
def individual_blog():
    title = request.args.get('blog.title')
    body = request.args.get('blog.body')
    return render_template('individual_blog.html', title=title, body=body)


@app.route('/index')



@app.route('/logout', methods=['POST'])


@app.route('/', methods=['POST', 'GET'])
def index():
    all_blogs = Blog.query.all()
    return render_template('blogs.html', title="Build A Blog", all_blogs=all_blogs)


if __name__ =='__main__':
    app.run()