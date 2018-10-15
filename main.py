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

def blank(string):
    """
    Blank field check
    ```
    Return True if string is empty
    """
    if not string:
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

    #TODO - only display blog posts that are owned by the user
    if request.args.get('id'):
        #if id has an arg we need to display the single blog that the user selected
        blog_id=request.args.get('id')
        #assign the id argument to a variable
        blog_post = Blog.query.filter_by(id=blog_id).first()
        #run a query filtering by the id
        return render_template('blog.html',a_blog=blog_post)
        #render blog template with the blog object
    else:
        #if an id was not selected display all blogs in ascending order
        blog_posts = Blog.query.order_by(-Blog.id).all()
        #run a query ordering by blog.id in reverse order (newest to oldest)
        return render_template('blog.html',blog_view=blog_posts)
        #render blog template with all blog objects

@app.route('/newpost', methods=['GET','POST'])
def add_new_post():
    if request.method == 'POST':
        blog_title = request.form['user_title']
        #assign the user's blog title to a variable
        blog_body = request.form['user_body']
        #assign the user's blog body to a variable
        if blank(blog_title) or blank(blog_body):
            #if either the submitted blog title or body are blank
            return render_template('newpost.html',blank_title=blank(blog_title),blank_body=blank(blog_body),previous_title=blog_title,previous_body=blog_body)
            #render newpost template with error flags for jinja2 to evaluate
        new_blog = Blog(blog_title,blog_body,1)
        #assign new object with blog title, blog body and user 1
        db.session.add(new_blog)
        db.session.commit()
        blog_post = Blog.query.filter_by(title=blog_title).first()
        return render_template('blog.html',a_blog=blog_post)

    return render_template('newpost.html') 



if __name__ == '__main__':
    app.run()