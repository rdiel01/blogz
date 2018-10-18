from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:**B1r2y3B$$@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#TODO: add the following route handler functions: signup, login, and index
#TODO:add a singleUser.html template that will be used to display only the blogs associated with a single given author.
    #It will be used when we dynamically generate a page using a GET request with a user query parameter on the /blog route
#TODO: We'll have a logout function that handles a POST request to /logout and redirects the user to /blog after deleting the username from the session
#TODO: 

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

def error(string):
    """
    checks is a string has any spaces in it and if it is within 3-20 chars long
    ```
    string, a string
    """
    if string and ' ' not in string and ((len(string) > 3 and len(string) < 20)):
        return False
    else:
        return True

def password_compare(pass_1,pass_2):
    """
    checks if password value matches verify password value
    ```
    pass_1, a string
    pass_2, a string
    """
    if pass_1 != pass_2:
        return False
    else:
        return True

@app.route("/signup", methods=["POST"])
def verification():
    """
    checks if username, password and email are legit.
    ```
    username, must be 3-20 char long with no spaces
    password, must be 3-20 char long with no spaces
     
     - User enters new, valid username, a valid password, and verifies
      password correctly and is redirected to the '/newpost' page with
      their username being stored in a session.
    - User leaves any of the username, password, or verify fields blank and gets
      an error message that one or more fields are invalid.
    - User enters a username that already exists and gets an error message that username already exists.
    - User enters different strings into the password and verify fields and
      gets an error message that the passwords do not match.
    - User enters a password or username less than 3 characters long and gets either
      an invalid username or an invalid password message.
    """
    username = ""
    password = ""
    username_error = error(request.form['typed_username'])
    password_error = error(request.form['typed_password'])
    
    matching_passwords = password_compare(request.form['typed_password'],request.form['verify_password'])
    #check username and assign username if pass
    if not username_error:
        username = request.form['typed_username']
    #check passwords and assign password if pass
    if not password_error and matching_passwords:
        password=request.form['typed_password']
    #check email and assign email if pass
    existing_user = User.query.filter_by(email=username).first()

    if not existing_user and not username_error and not password_error and matching_passwords:
        new_user = User(username,password)
        db.session.add(new_user)
        db.session.commit()
        session['email'] = username
        return render_template("newpost.html",html_username=username)
    else:
        return render_template("signup.html",html_username=username,html_email=email,html_username_error=username_error,html_password_error=password_error,html_password_verification_error=matching_passwords,html_email_error=email_error)
'''
# require users to login if not currently in a session.
# uncomment once sessions are added
@app.before_request
def require_login():
    allowed_routes = ['login','signup','blog','index']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')
'''
@app.route('/login')
def login():
    '''
    - User enters a username that is stored in the database with the correct password and is 
      redirected to the /newpost page with their username being stored in a session.
    - User enters a username that is stored in the database with an incorrect password and is
      redirected to the /login page with a message that their password is incorrect.
    - User tries to login with a username that is not stored in the database and is redirected
      to the /login page with a message that this username does not exist.
    - User does not have an account and clicks "Create Account" and is directed to the /signup page.
    '''
    pass

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