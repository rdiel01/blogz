from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:**B1r2y3B$$@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))
    owner_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner_id = owner

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(30))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

def blank_title(title):
    if not title:
        return True
    else:
        return False

def blank_body(body):
    if not body:
        return True
    else:
        return False

'''
# require users to login if not currently in a session.
# uncomment once sessions are added
@app.before_request
def require_login():
    allowed_routes = ['login','register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')
'''

@app.route('/')
def to_blog():
    return redirect ('/blog', code=302)

@app.route('/blog', methods=['GET'])
def a_blog():
    #TODO - display all blog posts from newest to oldest
    #TODO - only display blog posts that are owned by the user
    if request.args.get('id'):
        blog_id=request.args.get('id')
        blog_post = Blog.query.filter_by(id=blog_id).first()   
        return render_template('blog.html',a_blog=blog_post)
    else:
        blog_posts = Blog.query.order_by(-Blog.id).all()
        return render_template('blog.html',blog_view=blog_posts)
    #else:
    #blog_entries = Blog.query.all()
    #return render_template('blog.html',blog_view=blog_entries)


@app.route('/newpost', methods=['GET','POST'])
def add_new_post():
    #TODO - submit new blog post
    #TODO - After submitted the app displays(redirect) the main blog page /blog to view the new post
    #TODO - Blog must have title and body, if false return newpost.html with helpful error message and any previously entered content
    if request.method == 'POST':
        blog_title = request.form['user_title']
        blog_body = request.form['user_body']
        if blank_title(blog_title) or blank_body(blog_body):
            return render_template('newpost.html',blank_title=blank_title(blog_title),blank_body=blank_body(blog_body))
        new_blog = Blog(blog_title,blog_body,1)
        db.session.add(new_blog)
        db.session.commit()
        blog_post = Blog.query.filter_by(title=blog_title).first()
        return render_template('blog.html',a_blog=blog_post)

    return render_template('newpost.html') 



if __name__ == '__main__':
    app.run()