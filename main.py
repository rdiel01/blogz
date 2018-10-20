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

    def not_blank(string):
        """
        Blank field check
        ```
        Return False if string is empty
        """
        if string or string.replace(' ','') != '':
            return True
        else:
            return flash('The {0} field is empty','blog_error')


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
        print('username check!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!')
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
        print('password check!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!')
        if self.password and ' ' not in self.password and ((len(self.password) > 3 and len(self.password) < 20)):
            return True
        else:
            flash('Invalid password. Must be 3-20 characters long and contain no spaces.','invalid_password')
            

    def is_unique(self):
        """
        Check if username is unique and not already in database
        username, string that is between 3-20 characters with no spaces
        """
        print('unique check!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@')
        if not User.query.filter_by(email=self.email).first():
            return True
        else:
            flash('Username already exists.','user_exists')

    def matching_passwords(self, other_pass):
        """
        checks if password value matches verify password value
        ```
        pass_1, a string
        pass_2, a string
        """
        print('match check!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!')
        if self.password == other_pass:
            return True
        else:
            return flash('Passwords do not match','different_passwords')



@app.route("/signup", methods=["POST","GET"])
def verification():
    """
    checks if username, password and email are legit.
    ```
    username, must be 3-20 char long with no spaces
    password, must be 3-20 char long with no spaces
    """
    if request.method == "POST":
        submitted_user = User(request.form['typed_username'],request.form['pass1'])

        if  submitted_user.valid_password() and submitted_user.is_unique() and submitted_user.valid_username() and submitted_user.matching_passwords(request.form['pass2']):
            db.session.add(submitted_user)
            db.session.commit()
            session['email'] = submitted_user.email
            print(session['email'])
            return render_template("newpost.html")
        elif submitted_user.valid_username() and submitted_user.is_unique():
            flash(submitted_user.email,'html_username')
            submitted_user = None
            return render_template("signup.html")
        else:
            return render_template("signup.html")
    elif request.method == "GET":
        return render_template("signup.html")
'''
# require users to login if not currently in a session.
# uncomment once sessions are added
@app.before_request
def require_login():
    allowed_routes = ['login','signup','blog','index']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')
'''
@app.route('/login', methods =['POST','GET'])
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
    if request.method == 'POST':
        submitted_user = User(request.form['html_user'],request.form['html_pw'])
        print(not submitted_user.is_unique())
        if not submitted_user.is_unique():
            print('USER!!!11!!!!!!!!!!!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@@!@!@!@!@!@!@!@!@!@!@!@!')
            user = User.query.filter_by(email=submitted_user.email).first()
            if submitted_user.password == user.password:
                print('PASS!!!11!!!!!!!!!!!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@@!@!@!@!@!@!@!@!@!@!@!@!')
                session['email'] = submitted_user.email
                flash('Logged in')
                #add user welcome
                return render_template('newpost.html')
    print('firstFAIL!!!11!!!!!!!!!!!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@@!@!@!@!@!@!@!@!@!@!@!@!')
    submitted_user = None
    print('secondFAIL!!!11!!!!!!!!!!!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@!@@!@!@!@!@!@!@!@!@!@!@!@!')
    return render_template('login.html')

@app.route('/index')
def index():
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

@app.route('/test')
def tests():
    test_user = User
    return render_template('test.html')


if __name__ == '__main__':
    app.run()