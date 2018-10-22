from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'dakey'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:**B1r2y3B$$@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#TODO:add a singleUser.html template that will be used to display only the blogs associated with a single given author.
    #It will be used when we dynamically generate a page using a GET request with a user query parameter on the /blog route
#TODO: We'll have a logout function that handles a POST request to /logout and redirects the user to /blog after deleting the username from the session

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))
    owner_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner_id = owner

    def title_exists(self):
        """
        Blank field check
        ```
        Return False if string is empty
        """
        if self.title or self.title.replace(' ','') != '':
            return True
        else:
            flash('The title field is empty','blog_title_error')

    def body_exists(self):
        """
        Blank field check
        ```
        Return False if string is empty
        """
        if self.body or self.body.replace(' ','') != '':
            return True
        else:
            flash('The body field is empty','blog_title_error')
            


class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(30))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def valid_username(self):
        """
        checks if a string has any spaces in it and if it is within 3-20 chars long
        returns False if none apply
        ```
        string, a string
        """
        if self.email and ' ' not in self.email and ((len(self.email) > 3 and len(self.email) < 20)):
            return True
        else:
            flash('Invalid username. Must be 3-20 characters long and contain no spaces.','invalid_username')

    def valid_password(self):
        """
        checks if a string has any spaces in it and if it is within 3-20 chars long
        returns False if none apply
        ```
        string, a string
        """
        if self.password and ' ' not in self.password and ((len(self.password) > 3 and len(self.password) < 20)):
            return True
        else:
            flash('Invalid password. Must be 3-20 characters long and contain no spaces.','invalid_password')
            

    def already_exists(self):
        """
        Check if username is unique and not already in database
        username, string that is between 3-20 characters with no spaces
        """
        if User.query.filter_by(email=self.email).first():
            flash('Username already exists.','user_exists')
            return True
        else:
            flash('User does not exist.','no_user')
            flash(self.email,'html_username')
            return False

    def matching_passwords(self, other_pass):
        """
        checks if password value matches verify password value
        ```
        pass_1, a string
        pass_2, a string
        """
        if self.password == other_pass:
            return True
        else:
            flash(self.email,'html_username')
            flash ('Incorrect password.','invalid_password')
            flash('Passwords do not match','different_passwords')
            return False

@app.before_request
def require_login():
    allowed_routes = ['login','signup','all_blog_home',]
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route("/signup", methods=["POST","GET"])
def signup():
    """
    checks if username, password and email are legit.
    ```
    username, must be 3-20 char long with no spaces
    password, must be 3-20 char long with no spaces
    """
    if request.method == "POST":
        submitted_user = User(request.form['typed_username'],request.form['pass1'])

        if  submitted_user.valid_password() and not submitted_user.already_exists() and submitted_user.valid_username() and submitted_user.matching_passwords(request.form['pass2']):
            db.session.add(submitted_user)
            db.session.commit()
            session['email'] = submitted_user.email
            return render_template("newpost.html")
        elif submitted_user.valid_username() and not submitted_user.already_exists():            
            submitted_user = None
            return render_template("signup.html")
        else:
            return render_template("signup.html")
    elif request.method == "GET":
        return render_template("signup.html")

@app.route('/login', methods =['POST','GET'])
def login():
    if request.method == 'POST':
        submitted_user = User(request.form['html_user'],request.form['html_pw'])
        if submitted_user.already_exists():
            user = User.query.filter_by(email=submitted_user.email).first()
            if user.matching_passwords(submitted_user.password):
                session['email'] = submitted_user.email
                flash('Logged in as {0}.'.format(submitted_user.email),'login_good')
                submitted_user=None
                return render_template('newpost.html')
    submitted_user = None
    return render_template('login.html')

@app.route('/log_out')
def logout():
    del session['email']
    #test the demo site to see where it is taking the user on logout
    return redirect('/')

@app.route('/')
def all_blog_home():
    all_users = User.query.order_by(User.email).all() 
    return render_template('blog.html',user_view=all_users)
    
@app.route('/blog', methods=['GET'])
def a_blog():

    #TODO - only display blog posts that are owned by the user
    if request.args.get('user'):
        #if id has user as arg we need to display all the post of that user
        user=User.query.filter_by(email=request.args.get('user')).one()
        #assign the id argument to a variable
        users_posts = Blog.query.join(User).add_columns(User.email,User.id,Blog.title,Blog.body,Blog.id,Blog.owner_id).filter_by(email=user.email).order_by(-Blog.id).all()
        #run a query filtering by the id
        return render_template('blog.html',users_post_view=users_posts,user=user.email)
    elif request.args.get('id'):
        #if id has an arg we need to display the single blog that the user selected
        blog_id=request.args.get('id')
        #assign the id argument to a variable
        blog_post = Blog.query.filter_by(id=blog_id).first()
        #run a query filtering by the id
        return render_template('blog.html',a_blog=blog_post)
        #render blog template with the blog object
    else:
        #if an id was not selected display all blogs in ascending order
        #blog_posts = Blog.query.order_by(-Blog.id).all()
        blog_posts = Blog.query.join(User).add_columns(User.email,Blog.title,Blog.body,Blog.id).order_by(-Blog.id).all()
        #run a query ordering by blog.id in reverse order (newest to oldest)
        return render_template('blog.html',all_blogs_view=blog_posts)
        #render blog template with all blog objects

@app.route('/newpost', methods=['GET','POST'])
def add_new_post():
    if request.method == 'POST':       
        #assign the user's blog title to a variable
        #assign the user's blog body to a variable
        current_user = User.query.filter_by(email=session['email']).first()
        submitted_blog = Blog(request.form['user_title'],request.form['user_body'],current_user.id)
        if submitted_blog.title_exists and submitted_blog.body_exists:
            #if either the submitted blog title or body are blank
            db.session.add(submitted_blog)
            db.session.commit()
            return render_template('blog.html',a_blog=submitted_blog)
            #render newpost template with error flags for jinja2 to evaluate
        return render_template('newpost.html',previous_title=submitted_blog.title,previous_body=submitted_blog.body)
        #assign new object with blog title, blog body and user 1
        

    return render_template('newpost.html') 

if __name__ == '__main__':
    app.run()